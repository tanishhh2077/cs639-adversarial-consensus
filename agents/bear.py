"""
agents/bear.py
Bear Agent - Owner: Ritesh Neela (rneela@wisc.edu)
Due: May 2

TASK:
- Write the BEAR_SYSTEM_PROMPT below
- The Bear agent finds everything that could go wrong:
  regulatory risk, competitive threats, declining margins,
  insider selling, sector headwinds, overvaluation.
- It should be skeptical of positive narratives and look for
  what the bulls are missing.
- Complete the run_bear_agent() function.
- Test on 3 scenarios and post outputs in WhatsApp.
"""

import json
from utils.api_client import call_claude
from utils.helpers import extract_input_data

# TODO: Write the Bear Agent system prompt
# It should instruct the LLM to:
# 1. Act as a pessimistic, risk-focused financial analyst
# 2. Seek out disconfirming evidence and downside risks
# 3. Be skeptical of positive narratives
# 4. Return ONLY valid JSON in the required output format
BEAR_SYSTEM_PROMPT = """
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


def run_bear_agent(scenario: dict, prior_context: str = None, use_prod: bool = False) -> dict:
    """
    Run the Bear Agent on a financial scenario.

    Args:
        scenario: Full scenario dict (from JSON file)
        prior_context: Optional string of prior agent outputs (used in cooperative pipeline)
        use_prod: If True, uses Sonnet. If False, uses Haiku (for testing).

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    input_data_str = extract_input_data(scenario)

    if prior_context:
        user_content = f"{input_data_str}\n\nPrior analyst assessments:\n{prior_context}"
    else:
        user_content = input_data_str

    result = call_claude(
        system_prompt=BEAR_SYSTEM_PROMPT,
        user_content=user_content,
        use_prod=use_prod
    )

    return result


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

    print(f"Testing Bear Agent on: {scenario.get('company', 'Unknown')} ({scenario.get('event_date', '')})")
    result = run_bear_agent(scenario)
    print(json.dumps(result, indent=2))
