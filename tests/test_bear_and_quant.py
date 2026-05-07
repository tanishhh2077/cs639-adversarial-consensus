
import json
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from agents.bear import run_bear_agent
from agents.quant import run_quant_agent
from utils.helpers import strip_to_numbers, extract_input_data


def pick_three_scenarios() -> list:
    """Pick 3 scenarios for testing — prefer real, fall back to modified."""
    candidates = []
    for sub in ("real", "modified"):
        d = os.path.join("data", "scenarios", sub)
        if not os.path.isdir(d):
            continue
        for f in sorted(os.listdir(d)):
            if f.endswith(".json") and "TEMPLATE" not in f:
                candidates.append(os.path.join(d, f))
    return candidates[:3]


def show_quant_input_preview(scenario: dict) -> None:
    """Sanity check: show that the Quant agent sees no narrative."""
    stripped = json.loads(strip_to_numbers(scenario))
    assert set(stripped.keys()) == {"key_metrics", "price_history"}, (
        f"strip_to_numbers leaked extra fields: {set(stripped.keys())}"
    )
    assert "company" not in stripped
    assert "earnings_summary" not in stripped
    assert "sector" not in stripped
    assert "macro_context" not in stripped


def main() -> None:
    use_prod = bool(int(os.getenv("USE_PROD", "0")))
    scenarios = pick_three_scenarios()
    if len(scenarios) < 3:
        print(f"Need at least 3 scenarios, found {len(scenarios)}.")
        sys.exit(1)

    print(f"Model: {'Sonnet (prod)' if use_prod else 'Haiku (dev)'}")
    print(f"Scenarios: {[os.path.basename(p) for p in scenarios]}\n")

    for path in scenarios:
        with open(path) as f:
            scenario = json.load(f)

        company = scenario.get("company", "?")
        ticker = scenario.get("ticker", "?")
        truth = scenario.get("ground_truth", {}).get("actual_direction", "?")
        print("=" * 72)
        print(f"{os.path.basename(path)}  |  {company} ({ticker})  |  truth={truth}")
        print("=" * 72)

        show_quant_input_preview(scenario)

        bear = run_bear_agent(scenario, use_prod=use_prod)
        print("\n--- BEAR ---")
        print(json.dumps(bear, indent=2))

        quant = run_quant_agent(scenario, use_prod=use_prod)
        print("\n--- QUANT ---")
        print(json.dumps(quant, indent=2))
        print()


if __name__ == "__main__":
    main()
