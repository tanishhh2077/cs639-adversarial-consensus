"""
evaluation/metrics.py
Evaluation Code - Owner: Anish Gogineni (agogineni2@wisc.edu)

Scoring functions used to compare Monolithic vs Cooperative vs Adversarial pipelines.
All functions are pure: take plain Python data, return numbers. No API calls here.
"""

from __future__ import annotations

import re
from typing import List, Dict


_DIRECTION_TO_SIGN = {"bullish": 1, "neutral": 0, "bearish": -1}
_GT_TO_SIGN = {"up": 1, "flat": 0, "down": -1}


def view_to_probability(agent_output: dict) -> float:
    """
    Helper:
    Convert an agent output dict to a probability that the stock goes UP.

    bullish 80 -> 0.5 + 0.5 * 0.80 = 0.90
    bearish 80 -> 0.5 - 0.5 * 0.80 = 0.10
    neutral *  -> 0.50
    """
    view = agent_output.get("directional_view", "neutral").lower()
    conf = float(agent_output.get("confidence_score", 0)) / 100.0
    conf = max(0.0, min(1.0, conf))
    if view == "bullish":
        return 0.5 + 0.5 * conf
    if view == "bearish":
        return 0.5 - 0.5 * conf
    return 0.5


def direction_matches(agent_view: str, actual_direction: str) -> bool:
    """
    Helper:
    Check if the agent's view matches the actual direction.
    """
    if agent_view is None or actual_direction is None:
        return False
    return _DIRECTION_TO_SIGN.get(agent_view.lower()) == _GT_TO_SIGN.get(actual_direction.lower())


def compute_brier_score(predictions: List[float], outcomes: List[int]) -> float:
    """
    Average Brier score: (1/n) * sum((p_i - o_i)^2). Lower is better; range [0, 1].
    predictions: probabilities of "up" in [0, 1]
    outcomes:    1 if actual direction was up, else 0
    """
    if len(predictions) != len(outcomes):
        raise ValueError("predictions and outcomes must have the same length")
    if not predictions:
        return 0.0
    total = 0.0
    for p, o in zip(predictions, outcomes):
        total += (float(p) - float(o)) ** 2
    return total / len(predictions)


def score_accuracy(agent_outputs: List[dict], ground_truths: List[dict]) -> float:
    """
    Percentage of scenarios where directional_view matches actual_direction.
    Args: 
        agent_outputs: List of agent output dicts, each with 'directional_view'
        ground_truths: List of ground_truth dicts, each with 'actual_direction'
                       actual_direction is "up", "down", or "flat"
    Returns:
        Percentage of scenarios where directional_view matches actual_direction.
    """
    if len(agent_outputs) != len(ground_truths):
        raise ValueError("agent_outputs and ground_truths must have the same length")
    if not agent_outputs:
        return 0.0
    correct = sum(
        1 for a, g in zip(agent_outputs, ground_truths)
        if direction_matches(a.get("directional_view"), g.get("actual_direction"))
    )
    return 100.0 * correct / len(agent_outputs)


_STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "being", "as", "at", "by", "from",
    "that", "this", "these", "those", "it", "its", "their", "them", "they",
    "may", "might", "could", "would", "should", "will", "can", "has", "have",
    "had", "not", "no", "than", "then", "so", "if", "into", "out", "up", "down",
    "more", "less", "most", "least", "other", "some", "any", "all", "each",
}


def _tokens(text: str) -> set:
    return {w for w in re.findall(r"[a-z0-9]+", text.lower()) if w not in _STOPWORDS and len(w) > 2}


def _factor_covered(factor: str, agent_text: str, threshold: float = 0.5) -> bool:
    """A risk factor is 'covered' if >= threshold of its content tokens appear in agent_text."""
    factor_tokens = _tokens(factor)
    if not factor_tokens:
        return False
    text_tokens = _tokens(agent_text)
    overlap = len(factor_tokens & text_tokens)
    return (overlap / len(factor_tokens)) >= threshold


def score_informativeness(agent_outputs: List[dict], ground_truths: List[dict], threshold: float = 0.5) -> float:
    """
    Average coverage % of ground-truth key_risk_factors in agent's key_factors + reasoning.
    Uses bag-of-words overlap with stopword filtering. threshold = required token overlap fraction.
    Args:
        agent_outputs: List of agent output dicts, each with 'key_factors' and 'reasoning'
        ground_truths: List of ground truth dicts, each with 'key_risk_factors'
        threshold: Required token overlap fraction
    Returns:
        Average coverage % of ground-truth key_risk_factors in agent's key_factors + reasoning.
    """
    if len(agent_outputs) != len(ground_truths):
        raise ValueError("agent_outputs and ground_truths must have the same length")
    if not agent_outputs:
        return 0.0

    coverages: List[float] = []
    for agent, gt in zip(agent_outputs, ground_truths):
        risks = gt.get("key_risk_factors") or []
        if not risks:
            continue
        agent_text = " ".join(agent.get("key_factors") or []) + " " + (agent.get("reasoning") or "")
        hits = sum(1 for r in risks if _factor_covered(r, agent_text, threshold))
        coverages.append(hits / len(risks))

    if not coverages:
        return 0.0
    return 100.0 * sum(coverages) / len(coverages)


def compute_disagreement(bull_output: dict, base_output: dict, bear_output: dict) -> float:
    """
    Spread between Bull, Base, Bear in [0, 1].
    Each agent is mapped to a signed probability of "up" via view_to_probability,
    so the natural max spread is 1.0 (one says 0.0, another says 1.0).
    Returns max(p) - min(p).
    """
    probs = [
        view_to_probability(bull_output),
        view_to_probability(base_output),
        view_to_probability(bear_output),
    ]
    return max(probs) - min(probs)


def score_robustness(
    normal_outputs: List[dict],
    normal_ground_truths: List[dict],
    modified_outputs: List[dict],
    modified_ground_truths: List[dict],
) -> Dict[str, float]:
    """
    Accuracy on unmodified vs modified scenarios; degradation = normal - modified.
    Higher degradation = less robust to misinformation / incomplete data.
    Args:
        normal_outputs: List of agent output dicts, each with 'directional_view'
        normal_ground_truths: List of ground truth dicts, each with 'actual_direction'
        modified_outputs: List of agent output dicts, each with 'directional_view'
        modified_ground_truths: List of ground truth dicts, each with 'actual_direction'
    Returns:
        Dictionary with normal_accuracy, modified_accuracy, and degradation.
    """
    normal_acc = score_accuracy(normal_outputs, normal_ground_truths) if normal_outputs else 0.0
    modified_acc = score_accuracy(modified_outputs, modified_ground_truths) if modified_outputs else 0.0
    return {
        "normal_accuracy": normal_acc,
        "modified_accuracy": modified_acc,
        "degradation": normal_acc - modified_acc,
    }



def brier_from_outputs(agent_outputs: List[dict], ground_truths: List[dict]) -> float:
    """Convenience wrapper: compute Brier directly from agent output dicts + ground truths."""
    if len(agent_outputs) != len(ground_truths):
        raise ValueError("agent_outputs and ground_truths must have the same length")
    preds = [view_to_probability(a) for a in agent_outputs]
    outcomes = [1 if (g.get("actual_direction", "").lower() == "up") else 0 for g in ground_truths]
    return compute_brier_score(preds, outcomes)


# ---------------------------------------------------------------------------
# Sanity tests
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    # Brier
    preds = [0.8, 0.6, 0.3, 0.9, 0.4]
    outs = [1, 1, 0, 1, 0]
    expected = (0.04 + 0.16 + 0.09 + 0.01 + 0.16) / 5
    got = compute_brier_score(preds, outs)
    print(f"Brier: {got:.4f}  (expected {expected:.4f})")
    assert abs(got - expected) < 1e-9

    # view_to_probability
    assert abs(view_to_probability({"directional_view": "bullish", "confidence_score": 80}) - 0.9) < 1e-9
    assert abs(view_to_probability({"directional_view": "bearish", "confidence_score": 80}) - 0.1) < 1e-9
    assert abs(view_to_probability({"directional_view": "neutral", "confidence_score": 50}) - 0.5) < 1e-9

    # Accuracy
    agents = [
        {"directional_view": "bullish"},
        {"directional_view": "bearish"},
        {"directional_view": "neutral"},
        {"directional_view": "bullish"},
    ]
    gts = [
        {"actual_direction": "up"},
        {"actual_direction": "down"},
        {"actual_direction": "flat"},
        {"actual_direction": "down"},
    ]
    acc = score_accuracy(agents, gts)
    print(f"Accuracy: {acc:.1f}%  (expected 75.0%)")
    assert acc == 75.0

    # Informativeness
    agent_out = [{
        "key_factors": ["China market revenue is declining sharply"],
        "reasoning": "Services growth is decelerating and regulatory pressure on App Store is rising in EU.",
    }]
    gt = [{"key_risk_factors": [
        "China market revenue declining for third consecutive quarter",
        "Services revenue growth rate decelerating from 20% to 14%",
        "Regulatory pressure on App Store in EU",
        "Gross margin guidance below current quarter",
    ]}]
    info = score_informativeness(agent_out, gt)
    print(f"Informativeness: {info:.1f}%  (expected 75.0%, 3 of 4 covered)")

    # Disagreement
    bull = {"directional_view": "bullish", "confidence_score": 90}
    base = {"directional_view": "neutral", "confidence_score": 50}
    bear = {"directional_view": "bearish", "confidence_score": 80}
    d = compute_disagreement(bull, base, bear)
    print(f"Disagreement: {d:.3f}  (expected 0.850 = 0.95 - 0.10)")
    assert abs(d - 0.85) < 1e-9

    # Robustness
    rob = score_robustness(agents, gts, agents[:2], gts[:2])
    print(f"Robustness: {rob}")

    print("\nAll sanity checks passed.")
