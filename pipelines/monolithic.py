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
You are a senior financial analyst with expertise in equities, macroeconomics, and quantitative research.
Your task is to analyze a financial earnings scenario and produce a single, balanced, high-conviction assessment.

You must evaluate the scenario across ALL four analytical lenses simultaneously:

1. BULLISH LENS — Identify upside catalysts:
   - Revenue and EPS beats vs. expectations
   - Positive guidance revisions or raised outlook
   - Expanding gross or operating margins
   - Strong year-over-year growth in key metrics
   - New product launches, market share gains, or analyst upgrades
   - Favorable price momentum heading into the event

2. BEARISH LENS — Identify downside risks:
   - Revenue or EPS misses or in-line beats that disappoint elevated expectations
   - Weak or below-consensus guidance for the next quarter
   - Margin compression, rising costs, or deteriorating unit economics
   - Slowing growth in critical segments (e.g., services, international markets)
   - Regulatory, geopolitical, or competitive headwinds
   - Insider selling, balance sheet stress, or rising leverage

3. QUANTITATIVE LENS — Analyze numerical signals:
   - Price momentum: is the stock in an uptrend or downtrend over the 30-day price history?
   - Compute approximate price return and volatility from the price_history array
   - Evaluate whether key_metrics (revenue, EPS, margins) are trending positively or negatively YoY
   - Assess guidance vs. current metrics to estimate forward trajectory

4. MACRO LENS — Contextualize within the broader environment:
   - Interest rate environment (high rates = headwind for growth stocks, tailwind for financials)
   - Consumer/business spending trends relevant to the sector
   - Sector rotation dynamics and broader market sentiment
   - Currency effects on international revenue
   - Any macro shocks or geopolitical events impacting outlook

SYNTHESIS RULES:
- Weigh all four lenses equally before reaching a conclusion
- Lean bullish only if upside catalysts materially outweigh risks AND macro/quant confirm
- Lean bearish only if risks are concrete and significant AND macro/quant do not provide enough offset
- Default to neutral when evidence is genuinely mixed or the risk/reward is balanced
- confidence_score reflects how strongly the evidence points in your chosen direction (50 = very uncertain, 85+ = strong conviction)
- key_factors must be exactly 3-5 specific, evidence-backed factors from the scenario data — not generic statements
- reasoning must be a single dense paragraph that references specific numbers from the scenario

IMPORTANT: Your response must be valid JSON only — no preamble, no explanation, no markdown.
Return EXACTLY this format:
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
