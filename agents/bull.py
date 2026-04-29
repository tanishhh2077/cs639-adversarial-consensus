"""
agents/bull.py
Bull Agent - Owner: Yug Marwaha (ymarwaha@wisc.edu)
Due: May 2

TASK:
- Write the BULL_SYSTEM_PROMPT below
- The Bull agent is optimistic. It looks for upside catalysts:
  strong revenue growth, positive guidance, new product launches,
  expanding margins, analyst upgrades.
- It should deliberately downplay or ignore negative signals.
- Complete the run_bull_agent() function.
- Test on 3 scenarios from data/scenarios/real/ and post outputs in WhatsApp.
"""

import json
from utils.api_client import call_claude
from utils.helpers import extract_input_data

# TODO: Write the Bull Agent system prompt
# It should instruct the LLM to:
# 1. Act as an optimistic financial analyst
# 2. Seek out upside catalysts and confirming evidence
# 3. Downplay or ignore negative signals
# 4. Return ONLY valid JSON in the required output format
BULL_SYSTEM_PROMPT = """
TODO: Write your system prompt here.

IMPORTANT: Your response must be valid JSON only, no preamble or explanation.
Return exactly this format:
{
    "directional_view": "bullish" | "neutral" | "bearish",
    "confidence_score": <integer 0-100>,
    "key_factors": ["factor 1", "factor 2", "factor 3"],
    "reasoning": "A paragraph explaining your analysis"
}
"""


def run_bull_agent(scenario: dict, use_prod: bool = False) -> dict:
    """
    Run the Bull Agent on a financial scenario.

    Args:
        scenario: Full scenario dict (from JSON file)
        use_prod: If True, uses Sonnet. If False, uses Haiku (for testing).

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    # TODO: Complete this function
    # 1. Extract input_data from scenario (use extract_input_data helper)
    # 2. Call Claude API with BULL_SYSTEM_PROMPT
    # 3. Return the parsed result

    input_data_str = extract_input_data(scenario)

    result = call_claude(
        system_prompt=BULL_SYSTEM_PROMPT,
        user_content=input_data_str,
        use_prod=use_prod
    )

    return result


# Quick test - run this file directly to test your agent
if __name__ == "__main__":
    import os
    import sys

    # Load a test scenario
    test_scenario_path = "data/scenarios/real/"
    scenarios = [f for f in os.listdir(test_scenario_path) if f.endswith(".json")]

    if not scenarios:
        print("No scenarios found. Make sure Priyansh has added scenarios to data/scenarios/real/")
        sys.exit(1)

    test_file = os.path.join(test_scenario_path, scenarios[0])
    with open(test_file) as f:
        scenario = json.load(f)

    print(f"Testing Bull Agent on: {scenario.get('company', 'Unknown')} ({scenario.get('event_date', '')})")
    result = run_bull_agent(scenario)
    print(json.dumps(result, indent=2))
