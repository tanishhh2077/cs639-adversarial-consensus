# Adversarial Consensus

A multi-agent LLM framework where specialized agents with conflicting analytical mandates (Bull, Base, Bear, Quant, Macro) debate financial scenarios. An Arbiter synthesizes their arguments into a final analysis with a disagreement map.

---

## Team
| Name | Email | Role |
|------|-------|------|
| Tanish Upakare | upakare@wisc.edu | Arbiter Agent + LangGraph Pipeline + Project Lead |
| Yug Marwaha | ymarwaha@wisc.edu | Bull Agent + Base Agent |
| Ritesh Neela | rneela@wisc.edu | Bear Agent + Quant Agent |
| Anish Gogineni | agogineni2@wisc.edu | Evaluation Code + Visualization |
| Colin Yamada | cyamada@wisc.edu | Cooperative Baseline + Related Work |
| Priyansh Bansal | pbansal24@wisc.edu | Scenario Dataset (Real Events) |
| Harshit Goyal | hgoyal7@wisc.edu | Scenario Dataset (Modified) + Monolithic Baseline |
| Anirudh Jagannath | ajagannath@wisc.edu | Macro Agent + Infrastructure |

---

## Repo Structure
```
agents/
  bull.py          # Yug
  base.py          # Yug
  bear.py          # Ritesh
  quant.py         # Ritesh
  macro.py         # Anirudh
  arbiter.py       # Tanish
pipelines/
  adversarial.py   # Tanish - main pipeline
  cooperative.py   # Colin - baseline
  monolithic.py    # Harshit - baseline
evaluation/
  metrics.py       # Anish
  visualization.py # Anish
data/
  scenarios/
    real/          # Priyansh - 25 real earnings events
    modified/      # Harshit - 25 modified scenarios
  schema.json      # Scenario JSON schema (reference)
utils/
  api_client.py    # Shared Claude API wrapper
  helpers.py       # Shared helper functions
tests/
  test_bear_and_quant.py   # Ritesh - per-agent test harness
report/
  CS639_Final_Report.md    # Markdown source of the final report
  figures/                 # All figures referenced in the report (generated)
run_benchmark.py           # Runs all 3 pipelines x 50 scenarios + computes metrics
generate_figures.py        # Generates all report figures from saved benchmark outputs
requirements.txt
.env.example
```

---

## Setup

```bash
git clone https://github.com/tanishhh2077/cs639-adversarial-consensus
cd cs639-adversarial-consensus
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
```

---

## Reproducing the Benchmark

```bash
# Run all 3 pipelines on all 50 scenarios, saving raw outputs and metrics.
# Uses Claude Haiku 4.5 by default (~$3 in API spend, ~25 min wall-clock with --parallel 3).
python run_benchmark.py --skip-existing --parallel 3

# Render every figure used in the report (no API calls).
python generate_figures.py
```

Outputs:
- `results/raw/{pipeline}__{scenario_id}.json` — 150 per-run raw outputs
- `results/metrics.json` — aggregated metrics (Brier, accuracy, informativeness, robustness, disagreement)
- `report/figures/` — 50 figures (1 pipeline comparison + 1 disagreement scatter + 48 per-scenario disagreement maps)

The full report (`report/CS639_Final_Report.md`) is built from these outputs.

---

## Agent Output Format
Every agent function MUST return this exact format:
```json
{
    "directional_view": "bullish" | "neutral" | "bearish",
    "confidence_score": 0-100,
    "key_factors": ["factor 1", "factor 2", "factor 3"],
    "reasoning": "A paragraph explaining the analysis"
}
```

## Scenario Input Format
See `data/schema.json` for the full scenario JSON schema.

**CRITICAL: Never pass `ground_truth` to any agent. Only pass `input_data`.**

---

## Key Deadlines
| Task | Owner | Due |
|------|-------|-----|
| Scenario dataset (real) | Priyansh | May 2 |
| Scenario dataset (modified) | Harshit | May 2 |
| All agent prompts + functions | Yug, Ritesh, Anirudh | May 2 |
| Monolithic + Cooperative baselines | Harshit, Colin | May 2 |
| Arbiter + LangGraph pipeline | Tanish | May 2 |
| Evaluation code | Anish | May 3 |
| Full benchmark runs | Tanish | May 3 |
| Visualizations + figures | Anish | May 4 |
| Final report | All | May 5 |
