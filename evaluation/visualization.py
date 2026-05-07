"""
evaluation/visualization.py
Visualization + Demo - Owner: Anish Gogineni (agogineni2@wisc.edu)

Figures for the final report:
- Disagreement map (per scenario): all 5 agents' signed confidence, Base highlighted
- Pipeline comparison dashboard: Monolithic vs Cooperative vs Adversarial across metrics
- Disagreement vs realized uncertainty scatter (tests H2)
"""

from __future__ import annotations

import os
from typing import List, Optional

import matplotlib.pyplot as plt
import numpy as np

from evaluation.metrics import view_to_probability


_AGENT_ORDER = ["bull", "base", "bear", "quant", "macro"]
_BASE_COLOR = "#1f77b4"
_BULL_COLOR = "#2ca02c"
_BEAR_COLOR = "#d62728"
_NEUTRAL_COLOR = "#7f7f7f"


def _direction_color(direction: str) -> str:
    d = (direction or "").lower()
    if d == "bullish":
        return _BULL_COLOR
    if d == "bearish":
        return _BEAR_COLOR
    return _NEUTRAL_COLOR


def plot_disagreement_map(
    scenario: dict,
    agent_outputs: dict,
    save_path: Optional[str] = None,
):
    """
    Bar chart of each agent's signed confidence (probability of "up", centered at 0.5).
    Base agent is highlighted with a thicker outline as the anchor.
    Args:
        scenario: Dictionary with company, ticker, and event_date
        agent_outputs: Dictionary with agent names as keys and output dicts as values
        save_path: Optional path to save the figure
    Returns:
        Figure object
    """
    company = scenario.get("company", "Unknown")
    ticker = scenario.get("ticker", "")
    event_date = scenario.get("event_date", "")

    agents, probs, colors, edges, linewidths = [], [], [], [], []
    for name in _AGENT_ORDER:
        out = agent_outputs.get(name)
        if not out:
            continue
        agents.append(name.upper())
        probs.append(view_to_probability(out))
        colors.append(_direction_color(out.get("directional_view")))
        if name == "base":
            edges.append("black")
            linewidths.append(2.5)
        else:
            edges.append("none")
            linewidths.append(0.0)

    fig, ax = plt.subplots(figsize=(8, 4))
    centered = [p - 0.5 for p in probs]
    bars = ax.bar(agents, centered, color=colors, edgecolor=edges, linewidth=linewidths)

    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylim(-0.5, 0.5)
    ax.set_yticks([-0.5, -0.25, 0, 0.25, 0.5])
    ax.set_yticklabels(["bearish 1.0", "bearish 0.5", "neutral", "bullish 0.5", "bullish 1.0"])
    ax.set_ylabel("Signed P(up) — centered at neutral")
    ax.set_title(f"Disagreement map: {company} ({ticker}) — {event_date}")

    for bar, p in zip(bars, probs):
        h = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h + (0.02 if h >= 0 else -0.04),
            f"{p:.2f}",
            ha="center",
            va="bottom" if h >= 0 else "top",
            fontsize=9,
        )

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close(fig)
    else:
        plt.show()
    return fig


def plot_comparison_table(
    results: dict,
    save_path: Optional[str] = None,
):
    """
    Grouped bar chart: pipelines on x-axis, one bar per metric within each group.
    Expected shape:
        results = {
            "monolithic":  {"accuracy": 60.0, "brier": 0.22, "informativeness": 45.0, "robustness_degradation": 18.0},
            "cooperative": {...},
            "adversarial": {...},
        }
    Brier is plotted on a secondary axis (lower is better, different scale).
    Args:
        results: Dictionary with pipeline names as keys and metric dicts as values
        save_path: Optional path to save the figure
    Returns:
        Figure object
    """
    pipelines = list(results.keys())
    pct_metrics = ["accuracy", "informativeness", "robustness_degradation"]
    pct_labels = ["Accuracy %", "Informativeness %", "Robustness degradation %"]

    x = np.arange(len(pipelines))
    width = 0.22

    fig, ax = plt.subplots(figsize=(10, 5))
    for i, (key, label) in enumerate(zip(pct_metrics, pct_labels)):
        vals = [results[p].get(key, 0.0) for p in pipelines]
        ax.bar(x + (i - 1) * width, vals, width, label=label)

    ax.set_xticks(x + width)
    ax.set_xticklabels([p.capitalize() for p in pipelines])
    ax.set_ylabel("Percent (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Pipeline comparison across evaluation metrics")
    ax.legend(loc="upper left")

    ax2 = ax.twinx()
    brier_vals = [results[p].get("brier", 0.0) for p in pipelines]
    ax2.plot(x + width, brier_vals, "o--", color="black", label="Brier score (lower = better)")
    ax2.set_ylabel("Brier score")
    ax2.set_ylim(0, max(brier_vals + [0.3]) * 1.2)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close(fig)
    else:
        plt.show()
    return fig


def plot_disagreement_vs_uncertainty(
    disagreement_scores: List[float],
    realized_uncertainties: List[float],
    save_path: Optional[str] = None,
):
    """
    Scatter: agent disagreement (x) vs |actual price change| (y), with linear fit.
    Hypothesis: disagreement predicts realized volatility.
    Args:
        disagreement_scores: List of disagreement scores
        realized_uncertainties: List of realized uncertainties
        save_path: Optional path to save the figure
    Returns:
        Figure object
    """
    if len(disagreement_scores) != len(realized_uncertainties):
        raise ValueError("disagreement_scores and realized_uncertainties must have the same length")

    x = np.array(disagreement_scores, dtype=float)
    y = np.array(realized_uncertainties, dtype=float)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(x, y, alpha=0.7)

    if len(x) >= 2 and np.std(x) > 0:
        slope, intercept = np.polyfit(x, y, 1)
        xs = np.linspace(x.min(), x.max(), 50)
        ax.plot(xs, slope * xs + intercept, "r--", label=f"fit: y = {slope:.2f}x + {intercept:.2f}")
        corr = np.corrcoef(x, y)[0, 1]
        ax.text(0.05, 0.95, f"Pearson r = {corr:.2f}", transform=ax.transAxes, va="top")
        ax.legend()

    ax.set_xlabel("Agent disagreement score (max-min P(up))")
    ax.set_ylabel("Realized |price change| (%)")
    ax.set_title("Does disagreement predict realized uncertainty?")

    plt.tight_layout()
    if save_path:
        os.makedirs(os.path.dirname(save_path) or ".", exist_ok=True)
        plt.savefig(save_path, dpi=150)
        plt.close(fig)
    else:
        plt.show()
    return fig


def generate_all_report_figures(
    benchmark_results: dict,
    output_dir: str = "report/figures/",
):
    """
    Render every figure for the report.
    Args:
        benchmark_results: Dictionary with pipeline summary, disagreement maps, and disagreement scatter
        output_dir: Directory to save the figures
    Returns:
        None
    Expected benchmark_results shape:
        {
            "pipeline_summary": { "monolithic": {...metrics...}, "cooperative": {...}, "adversarial": {...} },
            "disagreement_maps": [
                { "scenario": {...}, "agent_outputs": { "bull": {...}, "base": {...}, ... } },
                ...
            ],
            "disagreement_scatter": {
                "disagreement_scores": [...],
                "realized_uncertainties": [...],
            },
        }
    """
    os.makedirs(output_dir, exist_ok=True)

    summary = benchmark_results.get("pipeline_summary")
    if summary:
        plot_comparison_table(summary, save_path=os.path.join(output_dir, "pipeline_comparison.png"))

    for i, item in enumerate(benchmark_results.get("disagreement_maps", [])):
        scen = item["scenario"]
        sid = scen.get("scenario_id", f"scenario_{i:03d}")
        plot_disagreement_map(
            scen,
            item["agent_outputs"],
            save_path=os.path.join(output_dir, f"disagreement_{sid}.png"),
        )

    scatter = benchmark_results.get("disagreement_scatter")
    if scatter:
        plot_disagreement_vs_uncertainty(
            scatter["disagreement_scores"],
            scatter["realized_uncertainties"],
            save_path=os.path.join(output_dir, "disagreement_vs_uncertainty.png"),
        )

    print(f"Saved figures to {output_dir}")


def _stub_benchmark_results() -> dict:
    """Hand-crafted fake results so we can exercise every plot without real pipelines.
    Args:
        None
    Returns:
        Dictionary with pipeline summary, disagreement maps, and disagreement scatter
    """
    return {
        "pipeline_summary": {
            "monolithic":  {"accuracy": 56.0, "brier": 0.24, "informativeness": 38.0, "robustness_degradation": 22.0},
            "cooperative": {"accuracy": 62.0, "brier": 0.21, "informativeness": 51.0, "robustness_degradation": 17.0},
            "adversarial": {"accuracy": 64.0, "brier": 0.19, "informativeness": 63.0, "robustness_degradation":  9.0},
        },
        "disagreement_maps": [
            {
                "scenario": {"scenario_id": "demo_001", "company": "NVIDIA Corp", "ticker": "NVDA", "event_date": "2023-11-21"},
                "agent_outputs": {
                    "bull":  {"directional_view": "bullish", "confidence_score": 90},
                    "base":  {"directional_view": "bullish", "confidence_score": 60},
                    "bear":  {"directional_view": "bearish", "confidence_score": 70},
                    "quant": {"directional_view": "bullish", "confidence_score": 75},
                    "macro": {"directional_view": "neutral", "confidence_score": 50},
                },
            },
        ],
        "disagreement_scatter": {
            "disagreement_scores":    [0.10, 0.30, 0.55, 0.80, 0.45, 0.20, 0.65, 0.35],
            "realized_uncertainties": [0.8,  2.1,  4.5,  6.8,  3.0,  1.2,  5.5,  2.7],
        },
    }


if __name__ == "__main__":
    generate_all_report_figures(_stub_benchmark_results(), output_dir="report/figures/")
    print("Demo run complete. Open report/figures/ to view the figures.")
