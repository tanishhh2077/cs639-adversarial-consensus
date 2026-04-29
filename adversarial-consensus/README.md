# Adversarial Consensus
### CS 639: Introduction to Foundation Models | Spring 2026 | UW-Madison

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
adversarial-consensus/
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
  report/            # Final report goes here
  requirements.txt
  .env.example
```

---

## Setup

```bash
git clone https://github.com/[your-username]/adversarial-consensus
cd adversarial-consensus
pip install -r requirements.txt
cp .env.example .env
# Add your Anthropic API key to .env
```

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
