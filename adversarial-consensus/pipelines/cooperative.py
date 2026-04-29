"""
pipelines/cooperative.py
Cooperative Baseline - Owner: Colin Yamada (cyamada@wisc.edu)
Due: May 2

TASK:
- Build the cooperative pipeline where agents run sequentially,
  each seeing what the previous agent concluded.
- Order: Quant -> Macro -> Base -> Bull -> Bear (final output)
- Reuse the agent functions from agents/ directory
- Each agent receives the previous agent's output as context
- No Arbiter needed - Bear agent produces the final synthesis
- Complete the run_cooperative_pipeline() function.
- Test on 3 scenarios and post outputs in WhatsApp.
"""

import json
from agents.quant import run_quant_agent
from agents.macro import run_macro_agent
from agents.base import run_base_agent
from agents.bull import run_bull_agent
from agents.bear import run_bear_agent


def format_prior_context(agent_name: str, agent_output: dict) -> str:
    """Format a single agent's output as context for the next agent."""
    return f"{agent_name} analyst assessment:\n{json.dumps(agent_output, indent=2)}"


def run_cooperative_pipeline(scenario: dict, use_prod: bool = False) -> dict:
    """
    Run the cooperative baseline pipeline.
    Agents run sequentially, each building on the previous agent's output.

    Order: Quant -> Macro -> Base -> Bull -> Bear

    Args:
        scenario: Full scenario dict (from JSON file)
        use_prod: If True, uses Sonnet. If False, uses Haiku.

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
        (final output is from Bear agent, which has seen everything)
    """

    # Step 1: Quant runs first - no prior context, only sees numbers
    print("  Running Quant agent...")
    quant_output = run_quant_agent(scenario, use_prod=use_prod)

    # Step 2: Macro runs second - sees Quant's output
    print("  Running Macro agent...")
    macro_context = format_prior_context("Quant", quant_output)
    macro_output = run_macro_agent(scenario, prior_context=macro_context, use_prod=use_prod)

    # Step 3: Base runs third - sees Quant + Macro
    print("  Running Base agent...")
    base_context = (
        format_prior_context("Quant", quant_output) + "\n\n" +
        format_prior_context("Macro", macro_output)
    )
    base_output = run_base_agent(scenario, prior_context=base_context, use_prod=use_prod)

    # Step 4: Bull runs fourth - sees Quant + Macro + Base
    print("  Running Bull agent...")
    bull_context = (
        format_prior_context("Quant", quant_output) + "\n\n" +
        format_prior_context("Macro", macro_output) + "\n\n" +
        format_prior_context("Base", base_output)
    )
    bull_output = run_bull_agent(scenario, use_prod=use_prod)
    # TODO: Note - run_bull_agent doesn't take prior_context yet.
    # You may need to modify bull.py to accept and use prior_context
    # similar to how bear.py and base.py work. Check with Yug.

    # Step 5: Bear runs last - sees everything, produces final output
    print("  Running Bear agent (final)...")
    bear_context = (
        format_prior_context("Quant", quant_output) + "\n\n" +
        format_prior_context("Macro", macro_output) + "\n\n" +
        format_prior_context("Base", base_output) + "\n\n" +
        format_prior_context("Bull", bull_output)
    )
    final_output = run_bear_agent(scenario, prior_context=bear_context, use_prod=use_prod)

    return final_output


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

    print(f"Testing Cooperative Pipeline on: {scenario.get('company', 'Unknown')}")
    result = run_cooperative_pipeline(scenario)
    print("\nFinal output:")
    print(json.dumps(result, indent=2))
