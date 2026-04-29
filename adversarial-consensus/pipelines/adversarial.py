"""
pipelines/adversarial.py
Adversarial Pipeline (Main System) - Owner: Tanish Upakare (upakare@wisc.edu)
Due: May 2

TASK:
- Build the main adversarial pipeline using LangGraph
- All 5 agents run in parallel (they do NOT see each other's outputs)
- Arbiter receives all 5 outputs and produces final synthesis
- Complete run_adversarial_pipeline()
"""

import json
from agents.bull import run_bull_agent
from agents.base import run_base_agent
from agents.bear import run_bear_agent
from agents.quant import run_quant_agent
from agents.macro import run_macro_agent
from agents.arbiter import run_arbiter_agent


def run_adversarial_pipeline(scenario: dict, use_prod: bool = False) -> dict:
    """
    Run the full adversarial pipeline.
    All agents run independently (no shared context between agents).
    Arbiter synthesizes all outputs.

    Args:
        scenario: Full scenario dict (from JSON file)
        use_prod: If True, uses Sonnet. If False, uses Haiku.

    Returns:
        dict with Arbiter's synthesis and full disagreement map
    """

    # TODO: Implement parallel execution with LangGraph
    # For now, running sequentially as a placeholder
    # Replace with LangGraph parallel execution

    print("  Running all agents in parallel...")

    # All agents run independently - they do NOT see each other's outputs
    bull_output = run_bull_agent(scenario, use_prod=use_prod)
    base_output = run_base_agent(scenario, use_prod=use_prod)
    bear_output = run_bear_agent(scenario, use_prod=use_prod)
    quant_output = run_quant_agent(scenario, use_prod=use_prod)
    macro_output = run_macro_agent(scenario, use_prod=use_prod)

    print("  Running Arbiter...")
    arbiter_output = run_arbiter_agent(
        bull_output=bull_output,
        base_output=base_output,
        bear_output=bear_output,
        quant_output=quant_output,
        macro_output=macro_output,
        use_prod=use_prod
    )

    # Return full result including all agent outputs and arbiter synthesis
    return {
        "agent_outputs": {
            "bull": bull_output,
            "base": base_output,
            "bear": bear_output,
            "quant": quant_output,
            "macro": macro_output
        },
        "arbiter": arbiter_output
    }


if __name__ == "__main__":
    import os
    import sys

    test_scenario_path = "data/scenarios/real/"
    scenarios = [f for f in os.listdir(test_scenario_path) if f.endswith(".json")]

    if not scenarios:
        print("No scenarios found.")
        sys.exit(1)

    test_file = os.path.join(test_scenario_path, scenarios[0])
    with open(test_file) as f:
        scenario = json.load(f)

    print(f"Testing Adversarial Pipeline on: {scenario.get('company', 'Unknown')}")
    result = run_adversarial_pipeline(scenario)
    print("\nFull result:")
    print(json.dumps(result, indent=2))
