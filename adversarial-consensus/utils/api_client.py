"""
utils/api_client.py
Shared Claude API wrapper used by all agents.
Do NOT modify this file without checking with Tanish first.
"""

import os
import json
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

DEV_MODEL = os.getenv("DEV_MODEL", "claude-haiku-4-5-20251001")
PROD_MODEL = os.getenv("PROD_MODEL", "claude-sonnet-4-20250514")


def call_claude(system_prompt: str, user_content: str, use_prod: bool = False) -> dict:
    """
    Call the Claude API with a system prompt and user content.
    Returns parsed JSON dict.

    Args:
        system_prompt: The agent's system prompt defining its role and constraints
        user_content: The scenario data to analyze (should be JSON string of input_data only)
        use_prod: If True, uses Sonnet (production). If False, uses Haiku (development/testing).

    Returns:
        dict with keys: directional_view, confidence_score, key_factors, reasoning
    """
    model = PROD_MODEL if use_prod else DEV_MODEL

    response = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_content}
        ]
    )

    raw = response.content[0].text

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Fallback: try to extract JSON from the response
        import re
        match = re.search(r'\{.*\}', raw, re.DOTALL)
        if match:
            result = json.loads(match.group())
        else:
            raise ValueError(f"Could not parse JSON from response: {raw}")

    # Validate output format
    required_keys = {"directional_view", "confidence_score", "key_factors", "reasoning"}
    missing = required_keys - set(result.keys())
    if missing:
        raise ValueError(f"Agent response missing required keys: {missing}")

    if result["directional_view"] not in ["bullish", "neutral", "bearish"]:
        raise ValueError(f"Invalid directional_view: {result['directional_view']}")

    if not isinstance(result["confidence_score"], (int, float)):
        raise ValueError(f"confidence_score must be a number, got: {type(result['confidence_score'])}")

    result["confidence_score"] = int(result["confidence_score"])

    return result
