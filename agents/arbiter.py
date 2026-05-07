"""
agents/arbiter.py
Arbiter Agent — synthesizes outputs from Bull, Base, Bear, Quant, Macro into a
final analysis with an explicit disagreement map.

Owner: Tanish Upakare (upakare@wisc.edu)
Completed by: Yug Marwaha (deadline cleanup, May 6)
"""

import json
from utils.api_client import call_claude
from evaluation.metrics import view_to_probability, compute_disagreement


ARBITER_SYSTEM_PROMPT = """You are the ARBITER in a multi-agent financial reasoning system. Five specialized agents have analyzed the same scenario from different perspectives and produced independent assessments. Your job is to synthesize their views into a single final analysis and quantify their disagreement.

================================================================
THE FIVE AGENTS YOU ARE SYNTHESIZING
================================================================
- BULL: Deliberately biased optimist. Always returns "bullish". Confidence reflects strength of the upside thesis.
- BASE: Neutral consensus anchor. Returns the most likely outcome with no directional bias. THIS IS YOUR REFERENCE POINT — measure how far Bull and Bear deviate FROM Base.
- BEAR: Deliberately biased pessimist. Always returns "bearish". Confidence reflects strength of the downside thesis.
- QUANT: Numbers only — no narrative input. Analyzes price momentum, multiples, and volatility patterns.
- MACRO: Sector and macroeconomic context only — no company-specific data. Analyzes whether the macro backdrop favors or hurts the sector.

================================================================
WHAT YOU DO
================================================================
1. SCORE each agent's argument quality on a 0-10 scale based on:
   - Evidence quality: are claims grounded in specific scenario data?
   - Internal consistency: does the reasoning support the directional_view and confidence?
   - Specificity: does it cite numbers and concrete factors, or just hand-wave?

2. MEASURE DEVIATION from the Base case. The Base agent is your anchor. Express each non-Base agent's view as a probability of "up" (bullish 80% conf -> 0.90, bearish 80% conf -> 0.10, neutral -> 0.50). Compute |agent_prob - base_prob|.

3. IDENTIFY KEY DISAGREEMENTS. Where do agents most directly contradict each other? Frame each as a specific factual or interpretive disagreement (e.g., "Bull argues margin expansion is sustainable; Bear cites elevated capex as evidence the cycle is peaking"), NOT generic ("agents disagree about direction").

4. PRODUCE A FINAL SYNTHESIS. Your final_directional_view should be the direction the WEIGHTED EVIDENCE supports. Weight by argument quality (your scores from step 1) and weight Base higher than the biased agents because Base is the only neutral observer. If Quant and Macro disagree with each other, the scenario has structural uncertainty — reflect that in lower confidence.

5. CONFIDENCE MAP: Provide three probabilities (0-100) representing your synthesized estimates of each scenario:
   - upside_case: probability the stock goes UP meaningfully (>1%)
   - base_case:  probability the stock stays roughly flat (within 1%)
   - downside_case: probability the stock goes DOWN meaningfully (>1%)
   These three should sum to ~100.

================================================================
DISAGREEMENT SCORE INTERPRETATION
================================================================
Use disagreement_score in [0, 1]:
- 0.0-0.2 = strong consensus across all 5 agents (low uncertainty scenario)
- 0.2-0.5 = moderate disagreement (typical case)
- 0.5-0.8 = high disagreement (genuinely contested scenario)
- 0.8-1.0 = maximum disagreement (Bull and Bear at opposite extremes, Quant/Macro split)

Compute as: max(view_probabilities) - min(view_probabilities) across all 5 agents.

================================================================
OUTPUT FORMAT (STRICT)
================================================================
Respond with ONLY a single valid JSON object. No prose before or after. No markdown code fences.

{
  "final_directional_view": "bullish" | "neutral" | "bearish",
  "final_confidence_score": <integer 0-100>,
  "agent_scores": {
    "bull":  <integer 0-10>,
    "base":  <integer 0-10>,
    "bear":  <integer 0-10>,
    "quant": <integer 0-10>,
    "macro": <integer 0-10>
  },
  "deviation_from_base": {
    "bull":  <float 0.0-1.0>,
    "bear":  <float 0.0-1.0>,
    "quant": <float 0.0-1.0>,
    "macro": <float 0.0-1.0>
  },
  "disagreement_score": <float 0.0-1.0>,
  "key_disagreements": [
    "<specific contested point 1>",
    "<specific contested point 2>",
    "<specific contested point 3>"
  ],
  "synthesis": "<one paragraph (4-7 sentences) presenting the synthesized view. Reference specific agents' arguments. Explain why your final_directional_view differs from or aligns with Base.>",
  "confidence_map": {
    "upside_case":   <integer 0-100>,
    "base_case":     <integer 0-100>,
    "downside_case": <integer 0-100>
  }
}

Rules:
- All score / probability fields MUST be numbers (not strings, not percent signs).
- agent_scores MUST be integers 0-10.
- deviation_from_base values MUST be floats in [0.0, 1.0].
- confidence_map values should sum to ~100 (allow ±2 for rounding).
- Never reference ground_truth — you only have the five agent outputs to work with."""


def run_arbiter_agent(
    bull_output: dict,
    base_output: dict,
    bear_output: dict,
    quant_output: dict,
    macro_output: dict,
    use_prod: bool = False,
) -> dict:
    """
    Run the Arbiter Agent to synthesize all five agent outputs.

    Args:
        bull_output, base_output, bear_output, quant_output, macro_output:
            Output dicts from the five specialized agents. Each must have keys
            directional_view, confidence_score, key_factors, reasoning.
        use_prod: If True, uses Sonnet (final benchmark). If False, uses Haiku.

    Returns:
        dict with keys: final_directional_view, final_confidence_score,
        agent_scores, deviation_from_base, disagreement_score,
        key_disagreements, synthesis, confidence_map.
    """
    combined_input = json.dumps(
        {
            "bull_analysis": bull_output,
            "base_analysis": base_output,
            "bear_analysis": bear_output,
            "quant_analysis": quant_output,
            "macro_analysis": macro_output,
        },
        indent=2,
    )

    result = call_claude(
        system_prompt=ARBITER_SYSTEM_PROMPT,
        user_content=combined_input,
        use_prod=use_prod,
        validate_agent_schema=False,  # Arbiter has its own schema
        max_tokens=2048,
    )

    # Defensive normalization: ensure required keys exist with safe defaults so
    # downstream code never crashes on malformed Arbiter output.
    result.setdefault("final_directional_view", base_output.get("directional_view", "neutral"))
    result.setdefault("final_confidence_score", base_output.get("confidence_score", 50))
    result.setdefault("agent_scores", {})
    result.setdefault("deviation_from_base", {})
    result.setdefault("disagreement_score", compute_disagreement(bull_output, base_output, bear_output))
    result.setdefault("key_disagreements", [])
    result.setdefault("synthesis", "")
    result.setdefault("confidence_map", {"upside_case": 33, "base_case": 34, "downside_case": 33})

    # Coerce types defensively
    try:
        result["final_confidence_score"] = int(result["final_confidence_score"])
    except (TypeError, ValueError):
        result["final_confidence_score"] = 50

    if result["final_directional_view"] not in ("bullish", "neutral", "bearish"):
        result["final_directional_view"] = "neutral"

    return result


if __name__ == "__main__":
    # Smoke test with synthetic agent outputs (no API call required for the
    # validation/normalization paths; full test happens in benchmark runs).
    fake_bull = {"directional_view": "bullish", "confidence_score": 80,
                 "key_factors": ["beat", "raise"], "reasoning": "..."}
    fake_base = {"directional_view": "bullish", "confidence_score": 65,
                 "key_factors": ["solid", "balanced"], "reasoning": "..."}
    fake_bear = {"directional_view": "bearish", "confidence_score": 70,
                 "key_factors": ["competition", "valuation"], "reasoning": "..."}
    fake_quant = {"directional_view": "bullish", "confidence_score": 60,
                  "key_factors": ["momentum"], "reasoning": "..."}
    fake_macro = {"directional_view": "neutral", "confidence_score": 55,
                  "key_factors": ["mixed"], "reasoning": "..."}
    print("Running Arbiter on synthetic inputs (live API call)...")
    out = run_arbiter_agent(fake_bull, fake_base, fake_bear, fake_quant, fake_macro)
    print(json.dumps(out, indent=2))
