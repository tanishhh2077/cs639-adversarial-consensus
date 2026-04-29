"""
agents/quant.py
Quant Agent - Owner: Ritesh Neela (rneela@wisc.edu)
Due: May 2

TASK:
- Write the QUANT_SYSTEM_PROMPT below
- The Quant agent receives ONLY numerical data. No company name,
  no news, no narrative. Just: price history, P/E ratio, EPS,
  revenue growth rate, profit margins, trading volume, volatility.
- It analyzes purely from quantitative signals: momentum,
  valuation multiples, volume trends, volatility patterns.
- The strip_to_numbers() helper in utils/helpers.py already
  strips out all narrative data for you.
- Complete the run_quant_agent() function.
- Test on 3 scenarios and post outputs in WhatsApp.
"""

import json
from utils.api_client import call_claude
from utils.helpers import strip_to_numbers

# TODO: Write the Quant Agent system prompt
# It should instruct the LLM to:
# 1. Act as a purely quantitative analyst
# 2. Analyze ONLY numerical signals - no narratives or qualitative factors
# 3. Focus on: momentum, valuation multiples, volume trends, volatility
# 4. Return ONLY valid JSON in the required output format
QUANT_SYSTEM_PROMPT = """
TODO: Write your system prompt here.

You will receive ONLY numerical financial data. Do NOT reference any
company names, news, or qualitative factors. Analyze purely from numbers.

IMPORTANT: Your response must be valid JSON only, no preamble or explanation.
Return exactly this format:
{
    "directional_view": "bullish" | "neutral" | "bearish",
    "confidence_score": <integer 0-100>,
    "key_factors": ["factor 1", "factor 2", "factor 3"],
    "reasoning": "A paragraph explaining your quantitative analysis"
}
"""


def run_quant_agent(scenario: dict, use_prod: bool = False) -> dict:
    """
    Run the Quant Agent on a financial scenario.
    NOTE: This agent only receives numerical data (no narrative).

    Args:
        scenario: Full scenario dict (from JSON file)
        use_prod: If True, uses Sonnet. If False, uses Haiku (for testing).

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    # strip_to_numbers removes all narrative, keeps only key_metrics + price_history
    numerical_data_str = strip_to_numbers(scenario)

    result = call_claude(
        system_prompt=QUANT_SYSTEM_PROMPT,
        user_content=numerical_data_str,
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

    print(f"Testing Quant Agent on: {scenario.get('company', 'Unknown')}")
    print("(Note: Quant agent only sees numbers, not company name)")
    result = run_quant_agent(scenario)
    print(json.dumps(result, indent=2))
