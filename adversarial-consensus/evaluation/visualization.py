"""
evaluation/visualization.py
Visualization + Demo - Owner: Anish Gogineni (agogineni2@wisc.edu)
Due: May 4

TASK:
- Build the disagreement map visualization
- Build the comparison dashboard (Monolithic vs Cooperative vs Adversarial)
- Generate all figures needed for the final report
"""

import json
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from typing import List


def plot_disagreement_map(scenario: dict, agent_outputs: dict, save_path: str = None):
    """
    Plot the disagreement map for a single scenario.
    Shows all 5 agents' confidence scores and directional views
    with Base agent highlighted as the anchor.

    Args:
        scenario: The scenario dict (used for title)
        agent_outputs: Dict with keys: bull, base, bear, quant, macro
                       Each value is an agent output dict
        save_path: Optional path to save the figure. If None, displays it.
    """
    # TODO: Implement this visualization
    # Suggested approach:
    # - Bar chart or radar chart showing each agent's confidence score
    # - Color code: green = bullish, red = bearish, gray = neutral
    # - Highlight Base agent as the reference point
    # - Title should include company name and event date

    company = scenario.get("company", "Unknown")
    event_date = scenario.get("event_date", "")

    agents = ["bull", "base", "bear", "quant", "macro"]
    scores = []
    colors = []
    labels = []

    for agent in agents:
        output = agent_outputs.get(agent, {})
        score = output.get("confidence_score", 0)
        direction = output.get("directional_view", "neutral")

        # Adjust score based on direction (negative for bearish)
        if direction == "bearish":
            score = -score
        elif direction == "neutral":
            score = 0

        scores.append(score)
        colors.append("green" if score > 0 else "red" if score < 0 else "gray")
        labels.append(agent.upper())

    # Your visualization code here
    raise NotImplementedError("plot_disagreement_map not implemented yet")


def plot_comparison_table(results: dict, save_path: str = None):
    """
    Plot a comparison table/chart: Monolithic vs Cooperative vs Adversarial
    across all evaluation metrics.

    Args:
        results: Dict with structure:
            {
                "monolithic": {"accuracy": 0.6, "brier": 0.2, "informativeness": 0.5, "robustness_degradation": 0.15},
                "cooperative": {...},
                "adversarial": {...}
            }
        save_path: Optional path to save the figure.
    """
    # TODO: Implement this visualization
    raise NotImplementedError("plot_comparison_table not implemented yet")


def plot_disagreement_vs_uncertainty(
    disagreement_scores: List[float],
    realized_uncertainties: List[float],
    save_path: str = None
):
    """
    Scatter plot testing H2: does agent disagreement correlate with
    realized outcome uncertainty?

    Args:
        disagreement_scores: List of disagreement scores from compute_disagreement()
        realized_uncertainties: List of uncertainty measures (e.g. abs price change magnitude)
        save_path: Optional path to save the figure.
    """
    # TODO: Implement this visualization
    # Should show correlation (or lack thereof) between disagreement and realized volatility
    raise NotImplementedError("plot_disagreement_vs_uncertainty not implemented yet")


def generate_all_report_figures(benchmark_results: dict, output_dir: str = "report/figures/"):
    """
    Generate all figures needed for the final report.
    Call this after benchmark runs are complete.

    Args:
        benchmark_results: Full benchmark results dict
        output_dir: Directory to save all figures
    """
    import os
    os.makedirs(output_dir, exist_ok=True)

    # TODO: Call all visualization functions and save figures
    print(f"Saving all figures to {output_dir}")
    raise NotImplementedError("generate_all_report_figures not implemented yet")
