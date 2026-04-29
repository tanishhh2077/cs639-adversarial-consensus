"""
utils/helpers.py
Shared helper functions for data processing.
"""

import json


def load_scenario(filepath: str) -> dict:
    """Load a scenario JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def load_all_scenarios(directory: str) -> list:
    """Load all scenario JSON files from a directory."""
    import os
    scenarios = []
    for filename in os.listdir(directory):
        if filename.endswith(".json"):
            scenarios.append(load_scenario(os.path.join(directory, filename)))
    return scenarios


def extract_input_data(scenario: dict) -> str:
    """
    Extract only input_data from scenario for passing to agents.
    NEVER pass ground_truth to agents - this function ensures that.
    Returns JSON string ready to pass to Claude API.
    """
    return json.dumps(scenario["input_data"], indent=2)


def strip_to_numbers(scenario: dict) -> str:
    """
    For Quant Agent: extract ONLY numerical data.
    Keeps: key_metrics, price_history
    Removes: earnings_summary, sector, macro_context (all narrative)
    Returns JSON string.
    """
    input_data = scenario["input_data"]
    numerical_only = {
        "key_metrics": input_data.get("key_metrics", {}),
        "price_history": input_data.get("price_history", [])
    }
    return json.dumps(numerical_only, indent=2)


def strip_to_macro(scenario: dict) -> str:
    """
    For Macro Agent: extract ONLY macro and sector data.
    Keeps: sector, macro_context
    Removes: earnings_summary, key_metrics, price_history (all company-specific)
    Returns JSON string.
    """
    input_data = scenario["input_data"]
    macro_only = {
        "sector": input_data.get("sector", ""),
        "macro_context": input_data.get("macro_context", "")
    }
    return json.dumps(macro_only, indent=2)
