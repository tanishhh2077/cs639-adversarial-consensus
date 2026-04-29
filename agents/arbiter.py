"""
agents/arbiter.py
Arbiter Agent - Owner: Tanish Upakare (upakare@wisc.edu)
Due: May 2

TASK:
- Write the ARBITER_SYSTEM_PROMPT
- The Arbiter receives ALL five agent outputs and synthesizes them
- It scores each argument on evidence quality and consistency
- It measures how far each agent deviates from the Base agent's view
- It produces a final synthesis with a structured disagreement map
- Complete the run_arbiter_agent() function
"""

import json
from utils.api_client import call_claude

ARBITER_SYSTEM_PROMPT = """
TODO: Write the Arbiter system prompt here.

You receive analysis from 5 specialized agents: Bull, Base, Bear, Quant, and Macro.
Your job is to:
1. Score each agent's argument on evidence quality and internal consistency (0-10)
2. Measure how far each agent deviates from the Base case
3. Identify the axes of maximum disagreement
4. Produce a final synthesized analysis with a confidence map

IMPORTANT: Your response must be valid JSON only.
Return exactly this format:
{
    "final_directional_view": "bullish" | "neutral" | "bearish",
    "final_confidence_score": <integer 0-100>,
    "agent_scores": {
        "bull": <0-10>,
        "base": <0-10>,
        "bear": <0-10>,
        "quant": <0-10>,
        "macro": <0-10>
    },
    "disagreement_score": <float 0-1, where 1 = maximum disagreement>,
    "key_disagreements": ["disagreement 1", "disagreement 2"],
    "synthesis": "A paragraph with the final synthesized analysis",
    "confidence_map": {
        "upside_case": <0-100>,
        "base_case": <0-100>,
        "downside_case": <0-100>
    }
}
"""


def run_arbiter_agent(
    bull_output: dict,
    base_output: dict,
    bear_output: dict,
    quant_output: dict,
    macro_output: dict,
    use_prod: bool = False
) -> dict:
    """
    Run the Arbiter Agent to synthesize all agent outputs.

    Args:
        bull_output: Output dict from run_bull_agent()
        base_output: Output dict from run_base_agent()
        bear_output: Output dict from run_bear_agent()
        quant_output: Output dict from run_quant_agent()
        macro_output: Output dict from run_macro_agent()
        use_prod: If True, uses Sonnet. If False, uses Haiku.

    Returns:
        dict with final synthesis and disagreement map
    """
    # TODO: Format all agent outputs into a single user message for the Arbiter
    combined_input = json.dumps({
        "bull_analysis": bull_output,
        "base_analysis": base_output,
        "bear_analysis": bear_output,
        "quant_analysis": quant_output,
        "macro_analysis": macro_output
    }, indent=2)

    result = call_claude(
        system_prompt=ARBITER_SYSTEM_PROMPT,
        user_content=combined_input,
        use_prod=use_prod
    )

    return result
