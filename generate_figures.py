"""
generate_figures.py
Loads results/raw/ and results/metrics.json, reshapes into the format
evaluation/visualization.py expects, and renders every report figure.

Outputs to report/figures/:
- pipeline_comparison.png         — bar+line comparison across all 3 pipelines
- disagreement_<scenario_id>.png  — one disagreement map per adversarial scenario
- disagreement_vs_uncertainty.png — scatter testing H2

Usage:
    python generate_figures.py

Owner: Yug Marwaha
"""

import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from evaluation.metrics import compute_disagreement
from evaluation.visualization import generate_all_report_figures

RESULTS_DIR = "results"
RAW_DIR = os.path.join(RESULTS_DIR, "raw")
FIG_DIR = os.path.join("report", "figures")


def load_metrics_json() -> dict:
    with open(os.path.join(RESULTS_DIR, "metrics.json")) as f:
        return json.load(f)


def load_scenarios_by_id() -> dict:
    """Load every scenario JSON keyed by scenario_id."""
    out = {}
    for subdir in ("real", "modified"):
        for path in sorted(glob.glob(os.path.join("data", "scenarios", subdir, "*.json"))):
            if "TEMPLATE" in os.path.basename(path):
                continue
            with open(path) as f:
                s = json.load(f)
            out[s["scenario_id"]] = s
    return out


def load_adversarial_outputs() -> dict:
    """Load every saved adversarial pipeline output keyed by scenario_id."""
    out = {}
    for path in sorted(glob.glob(os.path.join(RAW_DIR, "adversarial__*.json"))):
        sid = os.path.basename(path).replace("adversarial__", "").replace(".json", "")
        with open(path) as f:
            data = json.load(f)
        if "_error" in data:
            continue
        out[sid] = data
    return out


def reshape_pipeline_summary(metrics: dict) -> dict:
    """Map our metrics.json keys into the keys visualization.py expects."""
    out = {}
    for pname, m in metrics["per_pipeline"].items():
        out[pname] = {
            "accuracy": m.get("accuracy_overall_pct", 0.0),
            "brier": m.get("brier_overall", 0.0),
            "informativeness": m.get("informativeness_pct", 0.0),
            "robustness_degradation": (m.get("robustness") or {}).get("degradation", 0.0),
        }
    return out


def main():
    metrics = load_metrics_json()
    scenarios_by_id = load_scenarios_by_id()
    adv_outputs = load_adversarial_outputs()

    pipeline_summary = reshape_pipeline_summary(metrics)

    # Build disagreement_maps for every adversarial result that has all 5 agents
    disagreement_maps = []
    disagreement_scores = []
    realized_uncertainties = []

    for sid, data in adv_outputs.items():
        scenario = scenarios_by_id.get(sid)
        if not scenario:
            continue
        agent_outputs = data.get("agent_outputs", {})
        if not all(k in agent_outputs for k in ("bull", "base", "bear", "quant", "macro")):
            continue
        disagreement_maps.append({"scenario": scenario, "agent_outputs": agent_outputs})

        # H2 scatter: disagreement vs |realized price change|
        d = compute_disagreement(agent_outputs["bull"], agent_outputs["base"], agent_outputs["bear"])
        gt = scenario.get("ground_truth", {})
        pct = abs(float(gt.get("price_change_pct", 0.0)))
        disagreement_scores.append(d)
        realized_uncertainties.append(pct)

    benchmark_results = {
        "pipeline_summary": pipeline_summary,
        "disagreement_maps": disagreement_maps,
        "disagreement_scatter": {
            "disagreement_scores": disagreement_scores,
            "realized_uncertainties": realized_uncertainties,
        },
    }

    print(f"Pipeline summary: {len(pipeline_summary)} pipelines")
    print(f"Disagreement maps: {len(disagreement_maps)} scenarios")
    print(f"Scatter points: {len(disagreement_scores)}")

    generate_all_report_figures(benchmark_results, output_dir=FIG_DIR)
    print(f"\nDone. Figures saved to {FIG_DIR}/")


if __name__ == "__main__":
    main()
