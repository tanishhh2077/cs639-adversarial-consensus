"""
evaluation/metrics.py
Evaluation Code - Owner: Anish Gogineni (agogineni2@wisc.edu)
Due: May 3

TASK:
- Implement all four scoring functions below
- These are used to compare Monolithic vs Cooperative vs Adversarial
- Test each function with sample data before the benchmark runs
"""

from typing import List


def compute_brier_score(predictions: List[float], outcomes: List[int]) -> float:
    """
    Compute the average Brier score across all predictions.
    Lower is better. Perfect score = 0.0. Worst score = 1.0.

    Args:
        predictions: List of confidence scores as floats (0.0 to 1.0)
                     e.g. [0.8, 0.6, 0.3] means 80%, 60%, 30% confidence of going up
        outcomes: List of actual outcomes (1 = went up, 0 = went down/flat)
                  Must be same length as predictions

    Returns:
        float: Average Brier score (lower = better calibrated)

    Formula: (1/n) * sum((prediction_i - outcome_i)^2)

    Example:
        predictions = [0.8, 0.6, 0.3]
        outcomes    = [1,   1,   0  ]
        scores      = [0.04, 0.16, 0.09]
        average     = 0.097
    """
    # TODO: Implement this function
    if len(predictions) != len(outcomes):
        raise ValueError("predictions and outcomes must have the same length")

    # Your implementation here
    raise NotImplementedError("compute_brier_score not implemented yet")


def score_accuracy(agent_outputs: List[dict], ground_truths: List[dict]) -> float:
    """
    Compute directional accuracy across all scenarios.

    Args:
        agent_outputs: List of agent output dicts, each with 'directional_view'
        ground_truths: List of ground_truth dicts, each with 'actual_direction'
                       actual_direction is "up", "down", or "flat"

    Returns:
        float: Accuracy as percentage (0.0 to 100.0)

    Mapping:
        agent "bullish"  <-> ground truth "up"    = correct
        agent "bearish"  <-> ground truth "down"  = correct
        agent "neutral"  <-> ground truth "flat"  = correct
        anything else = incorrect
    """
    # TODO: Implement this function
    raise NotImplementedError("score_accuracy not implemented yet")


def score_informativeness(agent_outputs: List[dict], ground_truths: List[dict]) -> float:
    """
    Measure how many ground-truth risk factors the agent identified.

    Args:
        agent_outputs: List of agent output dicts, each with 'key_factors' and 'reasoning'
        ground_truths: List of ground_truth dicts, each with 'key_risk_factors' (list of strings)

    Returns:
        float: Average coverage percentage (0.0 to 100.0)
               e.g. if ground truth has 5 risk factors and agent mentioned 3, coverage = 60%

    Implementation hint:
        For each scenario, check how many items from key_risk_factors appear
        (as substrings or keywords) in the agent's key_factors list + reasoning text.
        You can use simple string matching or keyword overlap.
    """
    # TODO: Implement this function
    raise NotImplementedError("score_informativeness not implemented yet")


def compute_disagreement(bull_output: dict, base_output: dict, bear_output: dict) -> float:
    """
    Measure the disagreement between Bull, Base, and Bear agents.

    Args:
        bull_output: Output dict from Bull agent (has 'directional_view', 'confidence_score')
        base_output: Output dict from Base agent
        bear_output: Output dict from Bear agent

    Returns:
        float: Disagreement score from 0.0 (full agreement) to 1.0 (maximum disagreement)

    Implementation hint:
        Convert directional views to numeric scores: bullish=1, neutral=0, bearish=-1
        Weight by confidence scores.
        Measure the spread between them.
        Normalize to 0-1 range.
    """
    # TODO: Implement this function
    raise NotImplementedError("compute_disagreement not implemented yet")


def score_robustness(
    normal_outputs: List[dict],
    normal_ground_truths: List[dict],
    modified_outputs: List[dict],
    modified_ground_truths: List[dict]
) -> dict:
    """
    Measure accuracy degradation on modified (misinformation/incomplete) scenarios
    compared to normal scenarios.

    Args:
        normal_outputs: Agent outputs on normal unmodified scenarios
        normal_ground_truths: Ground truths for normal scenarios
        modified_outputs: Agent outputs on modified scenarios
        modified_ground_truths: Ground truths for modified scenarios

    Returns:
        dict with:
            normal_accuracy: float
            modified_accuracy: float
            degradation: float (normal - modified, higher = less robust)
    """
    # TODO: Implement this function
    raise NotImplementedError("score_robustness not implemented yet")


if __name__ == "__main__":
    # Quick sanity test for Brier score
    predictions = [0.8, 0.6, 0.3, 0.9, 0.4]
    outcomes = [1, 1, 0, 1, 0]
    # Expected: ((0.04 + 0.16 + 0.09 + 0.01 + 0.16) / 5) = 0.092
    score = compute_brier_score(predictions, outcomes)
    print(f"Brier score: {score:.4f} (expected ~0.092)")
