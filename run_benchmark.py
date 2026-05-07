"""
run_benchmark.py
Full benchmark: 50 scenarios x 3 pipelines = 150 pipeline runs.
Saves raw outputs to results/raw/, computes metrics, saves summary to results/metrics.json.

Usage:
    python run_benchmark.py                    # run everything
    python run_benchmark.py --limit 5          # smoke test on first 5 scenarios
    python run_benchmark.py --pipeline monolithic   # only run one pipeline
    python run_benchmark.py --skip-existing    # skip scenarios already done (for resumability)

Owner: Yug Marwaha (deadline cleanup)
"""

import argparse
import glob
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

# Make repo root importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipelines.monolithic import run_monolithic
from pipelines.cooperative import run_cooperative_pipeline
from pipelines.adversarial import run_adversarial_pipeline
from evaluation.metrics import (
    score_accuracy,
    score_informativeness,
    score_robustness,
    brier_from_outputs,
    compute_disagreement,
)

PIPELINES = {
    "monolithic": run_monolithic,
    "cooperative": run_cooperative_pipeline,
    "adversarial": run_adversarial_pipeline,
}

RESULTS_DIR = "results"
RAW_DIR = os.path.join(RESULTS_DIR, "raw")


def load_all_scenarios() -> List[dict]:
    """Load all scenarios from data/scenarios/{real,modified}/, skip TEMPLATEs."""
    scenarios = []
    for subdir in ("real", "modified"):
        pattern = os.path.join("data", "scenarios", subdir, "*.json")
        for path in sorted(glob.glob(pattern)):
            fname = os.path.basename(path)
            if "TEMPLATE" in fname:
                continue
            with open(path, "r") as f:
                s = json.load(f)
            s["_source_subdir"] = subdir  # tag for robustness scoring
            scenarios.append(s)
    return scenarios


def collapse_pipeline_output(pipeline_name: str, raw_output: dict) -> dict:
    """Reduce a pipeline's raw output to the standard agent schema for metrics."""
    if pipeline_name == "adversarial":
        # Adversarial returns {"agent_outputs": {...}, "arbiter": {...}}
        arb = raw_output["arbiter"]
        return {
            "directional_view": arb.get("final_directional_view", "neutral"),
            "confidence_score": arb.get("final_confidence_score", 50),
            "key_factors": arb.get("key_disagreements", []) + [arb.get("synthesis", "")],
            "reasoning": arb.get("synthesis", ""),
        }
    # monolithic and cooperative already return the agent schema
    return raw_output


def run_one(pipeline_name: str, scenario: dict, use_prod: bool = False) -> dict:
    """Run one pipeline on one scenario. Returns raw output dict."""
    fn = PIPELINES[pipeline_name]
    return fn(scenario, use_prod=use_prod)


def _run_and_save(pname: str, scenario: dict, use_prod: bool, out_path: str):
    """Worker function for parallel execution. Returns (pname, sid, ok, dt, err)."""
    sid = scenario["scenario_id"]
    t0 = time.time()
    try:
        raw = run_one(pname, scenario, use_prod=use_prod)
        with open(out_path, "w") as f:
            json.dump(raw, f, indent=2)
        return (pname, sid, True, time.time() - t0, None)
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        with open(out_path, "w") as f:
            json.dump({"_error": err, "_traceback": traceback.format_exc()}, f, indent=2)
        return (pname, sid, False, time.time() - t0, err)


def benchmark(limit: int, only_pipeline: str, skip_existing: bool, use_prod: bool, parallel: int):
    os.makedirs(RAW_DIR, exist_ok=True)

    scenarios = load_all_scenarios()
    if limit:
        scenarios = scenarios[:limit]

    pipelines_to_run = [only_pipeline] if only_pipeline else list(PIPELINES.keys())

    print(f"Running {len(pipelines_to_run)} pipeline(s) on {len(scenarios)} scenario(s)")
    print(f"Pipelines: {', '.join(pipelines_to_run)}")
    print(f"Model:    {'sonnet (PROD)' if use_prod else 'haiku (DEV)'}")
    print(f"Parallel: {parallel} workers")
    print("=" * 78)

    failures = []

    # Build the full job list (skip existing if requested)
    jobs = []
    for pname in pipelines_to_run:
        for scenario in scenarios:
            sid = scenario["scenario_id"]
            out_path = os.path.join(RAW_DIR, f"{pname}__{sid}.json")
            if skip_existing and os.path.exists(out_path):
                print(f"[{pname}] {sid}: SKIP (exists)")
                continue
            jobs.append((pname, scenario, out_path))

    if not jobs:
        print("No jobs to run.")
        return scenarios, pipelines_to_run, failures

    print(f"Total jobs: {len(jobs)}\n")

    if parallel <= 1:
        # Sequential mode (back-compat)
        for i, (pname, scenario, out_path) in enumerate(jobs, 1):
            pname2, sid, ok, dt, err = _run_and_save(pname, scenario, use_prod, out_path)
            tag = "OK" if ok else f"FAIL {err}"
            print(f"[{pname}] [{i}/{len(jobs)}] {sid}: {tag} ({dt:.1f}s)")
            if not ok:
                failures.append((pname, sid, err))
    else:
        # Parallel mode — scenarios are independent, safe to run concurrently
        with ThreadPoolExecutor(max_workers=parallel) as ex:
            futures = {
                ex.submit(_run_and_save, pname, scenario, use_prod, out_path): (pname, scenario["scenario_id"])
                for pname, scenario, out_path in jobs
            }
            for i, fut in enumerate(as_completed(futures), 1):
                pname, sid, ok, dt, err = fut.result()
                tag = "OK" if ok else f"FAIL {err}"
                print(f"[{pname}] [{i}/{len(jobs)}] {sid}: {tag} ({dt:.1f}s)")
                if not ok:
                    failures.append((pname, sid, err))

    print("\n" + "=" * 78)
    print(f"Done. {len(failures)} failure(s).")
    for pname, sid, err in failures:
        print(f"  {pname} :: {sid} :: {err}")

    return scenarios, pipelines_to_run, failures


def compute_metrics(scenarios: List[dict], pipelines_to_run: List[str]) -> Dict:
    """Load raw outputs, compute all metrics per pipeline, return summary dict."""
    # Group scenarios by modification type
    real_scenarios = [s for s in scenarios if s["modification_type"] == "none"]
    modified_scenarios = [s for s in scenarios if s["modification_type"] != "none"]

    summary = {"per_pipeline": {}, "per_pipeline_per_subset": {}}

    for pname in pipelines_to_run:
        outputs_all, gts_all = [], []
        outputs_real, gts_real = [], []
        outputs_modified, gts_modified = [], []
        disagreements = []

        for s in scenarios:
            sid = s["scenario_id"]
            out_path = os.path.join(RAW_DIR, f"{pname}__{sid}.json")
            if not os.path.exists(out_path):
                continue
            with open(out_path) as f:
                raw = json.load(f)
            if "_error" in raw:
                continue
            collapsed = collapse_pipeline_output(pname, raw)
            outputs_all.append(collapsed)
            gts_all.append(s["ground_truth"])

            if s["modification_type"] == "none":
                outputs_real.append(collapsed)
                gts_real.append(s["ground_truth"])
            else:
                outputs_modified.append(collapsed)
                gts_modified.append(s["ground_truth"])

            # Disagreement only meaningful for adversarial (has all 5 agents)
            if pname == "adversarial":
                ao = raw.get("agent_outputs", {})
                if "bull" in ao and "base" in ao and "bear" in ao:
                    disagreements.append(compute_disagreement(ao["bull"], ao["base"], ao["bear"]))

        if not outputs_all:
            continue

        metrics = {
            "n_scenarios": len(outputs_all),
            "accuracy_overall_pct": round(score_accuracy(outputs_all, gts_all), 2),
            "brier_overall": round(brier_from_outputs(outputs_all, gts_all), 4),
            "informativeness_pct": round(score_informativeness(outputs_all, gts_all), 2),
        }

        if outputs_real and outputs_modified:
            rob = score_robustness(outputs_real, gts_real, outputs_modified, gts_modified)
            metrics["robustness"] = {k: round(v, 2) for k, v in rob.items()}

        if disagreements:
            metrics["mean_inter_agent_disagreement"] = round(sum(disagreements) / len(disagreements), 4)

        summary["per_pipeline"][pname] = metrics

        # Subset breakdown
        summary["per_pipeline_per_subset"].setdefault(pname, {})
        if outputs_real:
            summary["per_pipeline_per_subset"][pname]["real"] = {
                "n": len(outputs_real),
                "accuracy_pct": round(score_accuracy(outputs_real, gts_real), 2),
                "brier": round(brier_from_outputs(outputs_real, gts_real), 4),
                "informativeness_pct": round(score_informativeness(outputs_real, gts_real), 2),
            }
        if outputs_modified:
            summary["per_pipeline_per_subset"][pname]["modified"] = {
                "n": len(outputs_modified),
                "accuracy_pct": round(score_accuracy(outputs_modified, gts_modified), 2),
                "brier": round(brier_from_outputs(outputs_modified, gts_modified), 4),
                "informativeness_pct": round(score_informativeness(outputs_modified, gts_modified), 2),
            }

    metrics_path = os.path.join(RESULTS_DIR, "metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(summary, f, indent=2)

    print("\n" + "=" * 78)
    print("METRICS SUMMARY")
    print("=" * 78)
    print(json.dumps(summary, indent=2))
    print(f"\nSaved to {metrics_path}")
    return summary


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--limit", type=int, default=0, help="Run on first N scenarios only (for testing)")
    p.add_argument("--pipeline", choices=list(PIPELINES.keys()), default=None,
                   help="Run only one specific pipeline")
    p.add_argument("--skip-existing", action="store_true", help="Resume — skip already-done scenarios")
    p.add_argument("--prod", action="store_true", help="Use Sonnet (production model). Default is Haiku.")
    p.add_argument("--metrics-only", action="store_true", help="Skip pipeline runs, just (re)compute metrics from existing results/raw/")
    p.add_argument("--parallel", type=int, default=8, help="Number of concurrent workers (default 8). Set 1 for sequential.")
    args = p.parse_args()

    if args.metrics_only:
        scenarios = load_all_scenarios()
        pipelines = [args.pipeline] if args.pipeline else list(PIPELINES.keys())
        compute_metrics(scenarios, pipelines)
        return

    scenarios, pipelines_to_run, failures = benchmark(
        limit=args.limit,
        only_pipeline=args.pipeline,
        skip_existing=args.skip_existing,
        use_prod=args.prod,
        parallel=args.parallel,
    )
    compute_metrics(scenarios, pipelines_to_run)


if __name__ == "__main__":
    main()
