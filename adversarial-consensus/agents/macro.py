"""
agents/macro.py
Macro Strategist Agent - Owner: Anirudh Jagannath (ajagannath@wisc.edu)
Due: May 2

TASK:
- Write the MACRO_SYSTEM_PROMPT below
- The Macro agent ONLY sees big-picture data: interest rates, GDP,
  inflation, sector trends, geopolitical events, sector classification.
- It does NOT receive any company-specific data.
- The strip_to_macro() helper in utils/helpers.py strips the data for you.
- Complete the run_macro_agent() function.
- Test on 3 scenarios and post outputs in WhatsApp.
"""

import json
from utils.api_client import call_claude
from utils.helpers import strip_to_macro

# TODO: Write the Macro Strategist system prompt
# It should instruct the LLM to:
# 1. Act as a macro economist / sector strategist
# 2. Assess whether macro conditions favor or hurt companies in this sector
# 3. ONLY use macro and sector data - ignore any company-specific details
# 4. Return ONLY valid JSON in the required output format
MACRO_SYSTEM_PROMPT = """
TODO: Write your system prompt here.

You will receive ONLY macro-economic context and sector classification.
Do NOT reference specific companies, earnings, or price data.
Assess purely from macro conditions and sector dynamics.

IMPORTANT: Your response must be valid JSON only, no preamble or explanation.
Return exactly this format:
{
    "directional_view": "bullish" | "neutral" | "bearish",
    "confidence_score": <integer 0-100>,
    "key_factors": ["factor 1", "factor 2", "factor 3"],
    "reasoning": "A paragraph explaining your macro analysis"
}
"""


def run_macro_agent(scenario: dict, prior_context: str = None, use_prod: bool = False) -> dict:
    """
    Run the Macro Strategist Agent on a financial scenario.
    NOTE: This agent only receives macro + sector data.

    Args:
        scenario: Full scenario dict (from JSON file)
        prior_context: Optional string of prior agent outputs (used in cooperative pipeline)
        use_prod: If True, uses Sonnet. If False, uses Haiku (for testing).

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    # strip_to_macro removes all company-specific data, keeps only sector + macro_context
    macro_data_str = strip_to_macro(scenario)

    if prior_context:
        user_content = f"{macro_data_str}\n\nPrior analyst assessments:\n{prior_context}"
    else:
        user_content = macro_data_str

    result = call_claude(
        system_prompt=MACRO_SYSTEM_PROMPT,
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

    print(f"Testing Macro Agent on sector: {scenario['input_data'].get('sector', 'Unknown')}")
    print("(Note: Macro agent only sees sector + macro context, not company details)")
    result = run_macro_agent(scenario)
    print(json.dumps(result, indent=2))
