"""
utils/api_client.py
Shared Claude API wrapper used by all agents.
Do NOT modify this file without checking with Tanish first.
"""

import os
import json
import time
import random
from anthropic import Anthropic
from anthropic import RateLimitError, APITimeoutError, APIConnectionError
from dotenv import load_dotenv

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


def _call_with_retry(model, max_tokens, system, messages, max_attempts=6):
    """Call Anthropic with exponential backoff on transient errors (429, timeouts)."""
    delay = 4.0  # initial delay in seconds
    last_err = None
    for attempt in range(1, max_attempts + 1):
        try:
            return client.messages.create(
                model=model,
                max_tokens=max_tokens,
                system=system,
                messages=messages,
            )
        except (RateLimitError, APITimeoutError, APIConnectionError) as e:
            last_err = e
            if attempt == max_attempts:
                raise
            # Exponential backoff with jitter; cap at 60s
            sleep_for = min(60.0, delay * (2 ** (attempt - 1))) + random.uniform(0, 1.5)
            time.sleep(sleep_for)
    raise last_err  # unreachable, satisfies linters

DEV_MODEL = os.getenv("DEV_MODEL", "claude-haiku-4-5-20251001")
PROD_MODEL = os.getenv("PROD_MODEL", "claude-sonnet-4-20250514")


def call_claude(
    system_prompt: str,
    user_content: str,
    use_prod: bool = False,
    validate_agent_schema: bool = True,
    max_tokens: int = 1024,
) -> dict:
    """
    Call the Claude API with a system prompt and user content.
    Returns parsed JSON dict.

    Args:
        system_prompt: The agent's system prompt defining its role and constraints
        user_content: The scenario data to analyze (should be JSON string of input_data only)
        use_prod: If True, uses Sonnet (production). If False, uses Haiku (development/testing).
        validate_agent_schema: If True (default), enforces the standard agent output schema
            (directional_view, confidence_score, key_factors, reasoning). Set to False for
            non-agent callers like the Arbiter that return a different shape.
        max_tokens: Token budget for the response. Bumped from 1024 default for callers
            (e.g., Arbiter) that need to return a richer structure.

    Returns:
        Parsed dict from the model's JSON output. If validate_agent_schema is True, also
        guaranteed to have keys: directional_view, confidence_score, key_factors, reasoning.
    """
    model = PROD_MODEL if use_prod else DEV_MODEL

    response = _call_with_retry(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_content}],
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

    if validate_agent_schema:
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
