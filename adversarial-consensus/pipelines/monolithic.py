"""
pipelines/monolithic.py
Monolithic Baseline - Owner: Harshit Goyal (hgoyal7@wisc.edu)
Due: May 3

TASK:
- Build the monolithic baseline: one single Claude API call
  with one big prompt that does ALL analysis at once.
- This is what we're trying to beat with the adversarial system.
- Complete the run_monolithic() function.
- Make sure output format matches all other agents exactly.
"""

import json
from utils.api_client import call_claude
from utils.helpers import extract_input_data

MONOLITHIC_SYSTEM_PROMPT = """
TODO: Write the monolithic system prompt here.

You are a comprehensive financial analyst. Analyze the given financial scenario
considering ALL of the following:
- Upside potential (bullish factors, growth catalysts)
- Downside risks (bearish factors, regulatory threats)
- Quantitative signals (price momentum, valuation metrics)
- Macro context (interest rates, sector dynamics, geopolitical factors)

Synthesize all perspectives into a single balanced assessment.

IMPORTANT: Your response must be valid JSON only, no preamble or explanation.
Return exactly this format:
{
    "directional_view": "bullish" | "neutral" | "bearish",
    "confidence_score": <integer 0-100>,
    "key_factors": ["factor 1", "factor 2", "factor 3"],
    "reasoning": "A paragraph explaining your comprehensive analysis"
}
"""


def run_monolithic(scenario: dict, use_prod: bool = False) -> dict:
    """
    Run the monolithic baseline on a financial scenario.
    One LLM call, one prompt, all analysis at once.

    Args:
        scenario: Full scenario dict (from JSON file)
        use_prod: If True, uses Sonnet. If False, uses Haiku.

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    # Pass ALL input data to a single prompt
    input_data_str = extract_input_data(scenario)

    result = call_claude(
        system_prompt=MONOLITHIC_SYSTEM_PROMPT,
        user_content=input_data_str,
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

    print(f"Testing Monolithic on: {scenario.get('company', 'Unknown')}")
    result = run_monolithic(scenario)
    print(json.dumps(result, indent=2))
