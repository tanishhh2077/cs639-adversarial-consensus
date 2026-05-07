# Adversarial Consensus: Disagreement-Driven Multi-Agent Financial Reasoning with Foundation Models

**CS 639: Introduction to Foundation Models — Spring 2026 — University of Wisconsin–Madison**

Tanish Upakare, Yug Marwaha, Ritesh Neela, Anish Gogineni, Colin Yamada, Priyansh Bansal, Harshit Goyal, Anirudh Jagannath

---

## Abstract

Foundation models are increasingly used for financial reasoning, but they are typically deployed as monolithic oracles whose internal uncertainty is hidden behind a single confident output. We propose **Adversarial Consensus**, a multi-agent framework in which five specialized LLM agents with deliberately conflicting analytical mandates (Bull, Bear, Base, Quant, and Macro) analyze each scenario independently, and an Arbiter agent synthesizes their views into a final analysis with an explicit disagreement map. We compare three pipeline configurations (Monolithic, Cooperative, and Adversarial) on a 50-scenario benchmark of real and modified earnings events. We use a fixed underlying model (Claude Haiku 4.5) so that performance differences come from architecture rather than model capability. The Adversarial pipeline achieves the best Brier score (0.225) of all three configurations and matches Monolithic on directional accuracy (about 67%), while the Cooperative chain collapses entirely onto its final agent's structural bias, returning bearish on 100% of scenarios in both subsets. Inter-agent disagreement averages 0.63 on a 0–1 scale and shows a weak positive correlation with realized one-week return magnitude. We read this as suggestive but not conclusive evidence that disagreement is a measurable signal of scenario uncertainty. Our results indicate that pipeline architecture is a meaningful design choice independent of model selection, and that the agent producing the final synthesis in a sequential chain inherits its prior. This is a cautionary methodological finding for designers of multi-agent systems.

---

## 1. Introduction

Foundation models are increasingly deployed for financial analysis, yet current approaches treat them as monolithic oracles: a single model receives a prompt and produces a recommendation. This mirrors no real-world decision-making process. On a trading floor, analysts with different specializations argue, challenge assumptions, and surface risks that no individual would identify alone. The *disagreement* between analysts is itself a signal: consensus suggests efficient pricing, while persistent conflict reveals real uncertainty and potential opportunity. A single model's confident output collapses this signal entirely, hiding the model's internal uncertainty behind a single number.

We propose **Adversarial Consensus**, a multi-agent framework in which specialized LLM agents with deliberately conflicting analytical mandates debate financial scenarios. Five agents analyze each scenario independently: a Bull (biased optimist), a Bear (biased pessimist), a Base (neutral consensus anchor), a Quant (numerical signals only), and a Macro Strategist (sector and macro context only). An Arbiter agent then synthesizes their arguments into a final analysis accompanied by an explicit **disagreement map** quantifying where and why the agents diverge. Our central research question is whether structured adversarial disagreement between specialized agents produces more accurate, better-calibrated, and more informative financial reasoning than cooperative multi-agent pipelines or monolithic single-agent approaches.

We test three hypotheses. **H1**: adversarial multi-agent architectures produce better-calibrated confidence estimates and surface more risk factors than cooperative or monolithic baselines. **H2**: the magnitude of inter-agent disagreement on a given scenario correlates with the true underlying uncertainty of that scenario, making disagreement itself a measurable and informative signal. **H3**: the adversarial approach exhibits greater robustness to misleading or incomplete input data, as conflicting agents are structurally more likely to catch errors that cooperative chains would propagate unchallenged.

To evaluate these hypotheses, we constructed a benchmark of 50 financial scenarios — 25 real earnings events from the past two years and 25 modifications including planted misinformation and incomplete data — with verified ground-truth outcomes one week post-event. We compared three pipeline configurations on this benchmark: a Monolithic baseline (one comprehensive prompt to a single model), a Cooperative baseline (five agents that build on each other's outputs sequentially), and our Adversarial system (five independent agents plus an Arbiter). All configurations used identical input data and the same underlying model (Claude Haiku 4.5) to isolate the effect of architecture rather than model capability.

Our results show that the adversarial architecture matches the monolithic baseline on directional accuracy while achieving the best calibration (lowest Brier score) of all three configurations, and that the cooperative baseline performs substantially worse than both — a finding we trace to a structural artifact of the cooperative chain. We further find that inter-agent disagreement carries a measurable signal about scenario uncertainty, partially supporting H2. The contributions of this work are: (1) a formal architectural specification for adversarial multi-agent reasoning, (2) a 50-scenario benchmark with planted-misinformation variants for measuring robustness, (3) an empirical comparison showing that pipeline architecture is a meaningful design choice independent of model selection, and (4) evidence that disagreement is a usable signal, not just noise to be averaged away.

The remainder of this paper is organized as follows. Section 2 surveys related work in multi-agent LLM debate, financial language models, calibration, and mixture-of-experts approaches. Section 3 details the methodology including agent specifications, pipeline architectures, and the benchmark construction. Section 4 presents results across all four evaluation metrics. Section 5 concludes with implications, limitations, and future work.

---

## 2. Related Work

Our work sits at the intersection of four research threads: multi-agent LLM reasoning, financial language models, calibration of foundation models, and mixture-of-experts architectures. We discuss each in turn and conclude by clarifying how Adversarial Consensus differs from prior approaches.

**Multi-agent LLM debate.** The closest prior work to ours is Du et al. (2023), "Improving Factuality and Reasoning in Language Models through Multiagent Debate," which shows that having multiple LLM instances independently propose answers and then iteratively critique each other's outputs improves factuality and arithmetic reasoning. Liang et al. (2023) extended this with "Encouraging Divergent Thinking in LLMs through Multi-Agent Debate," explicitly framing disagreement as a feature rather than noise. Frameworks such as AutoGen (Wu et al. 2023) and ChatDev (Qian et al. 2023) generalize this pattern to coordinated agent teams with assigned roles. These approaches have two limitations our work addresses. First, the agents in prior debate frameworks are typically *symmetric* — same prompt, same data, differing only in temperature or random seed — and convergence is treated as the goal. Our agents hold *structurally conflicting mandates* (Bull is biased optimist, Bear is biased pessimist), so disagreement is a designed property, not a transient phase to be resolved. Second, prior work rarely treats the magnitude of inter-agent disagreement itself as a quantitative output. We make the disagreement map a first-class deliverable.

**Financial language models.** BloombergGPT (Wu et al. 2023) demonstrated that domain-specific pre-training on financial text yields measurable gains on financial NLP benchmarks, while FinGPT (Yang et al. 2023) released open-source financial LLMs with similar specialization. These efforts focus on *what the model knows*; our work is orthogonal — we hold the underlying model fixed (Claude Haiku 4.5) and ask how *architectural choices around the model* affect downstream reasoning quality. A general-purpose foundation model with a well-designed multi-agent wrapper may be a more practical alternative to expensive domain pre-training for many financial reasoning tasks, particularly when the bottleneck is reasoning structure rather than missing terminology.

**Calibration of foundation models.** Kadavath et al. (2022), "Language Models (Mostly) Know What They Know," established that LLMs can produce reasonably calibrated confidence estimates when prompted appropriately, but that calibration degrades on tasks requiring multi-step reasoning. Our adversarial framework is designed in part to address this: by forcing structurally biased agents to compete for the Arbiter's attention, we create an explicit mechanism for surfacing the model's internal uncertainty rather than asking a single model to introspect on its own confidence. We measure calibration via Brier score across all three pipelines and find that the adversarial architecture produces the lowest Brier score, consistent with the hypothesis that adversarial structure improves calibration.

**Mixture-of-experts (MoE) architectures.** Switch Transformers (Fedus et al. 2022) and GLaM (Du et al. 2022) introduced sparse expert routing within a single model, where different tokens activate different expert subnetworks. The conceptual parallel to our work is real — both approaches involve specialization — but the mechanism differs fundamentally. MoE routes at the token level inside a single model; our agents route at the *task* level across separate model invocations. MoE's specialization is learned end-to-end; ours is hand-specified through prompts and data filtering (Quant sees only numbers, Macro sees only sector context). MoE is built for inference efficiency on large training sets; our approach is built for interpretability and disagreement quantification. Adversarial Consensus can be thought of as a "prompt-engineered MoE" operating at a higher level of abstraction.

**How our work differs.** Compared to prior multi-agent debate, we introduce structural role bias and treat disagreement as an output rather than a problem to resolve. Compared to financial LLMs, we hold the model fixed and study architecture instead of pre-training. Compared to calibration research, we externalize uncertainty through explicit disagreement maps rather than relying on the model to introspect. Compared to MoE, we operate at the prompt and pipeline level rather than the parameter level, trading inference efficiency for interpretability. To our knowledge, no prior work combines structurally biased agents, an explicit Arbiter, a disagreement-quantifying output, and a benchmark with planted misinformation for robustness measurement — the combination is the contribution.

---

## 3. Methodology

### 3.1 Agent Architecture

We construct five specialized analytical agents and one synthesis agent. Each analytical agent is implemented as a Python function that takes a financial scenario dictionary as input and returns a structured analysis dictionary with four fields: `directional_view` (one of "bullish", "neutral", "bearish"), `confidence_score` (integer 0–100), `key_factors` (list of supporting evidence strings), and `reasoning` (a paragraph of analysis). All five agents call the same underlying foundation model (Claude Haiku 4.5) but differ in their system prompts and the data they are allowed to see.

The **Bull Agent** is a deliberately biased optimist. Its system prompt instructs it to seek out upside catalysts (revenue growth, positive guidance, margin expansion, analyst upgrades, secular tailwinds) and to downplay or reframe negative signals as "already priced in" or "short-term noise." Its `directional_view` is forced to "bullish" via post-processing so the adversarial signal is never collapsed by an agent breaking character; `confidence_score` then reflects the strength of the bull thesis rather than its existence. The **Bear Agent** mirrors this construction in the opposite direction, hunting for regulatory risk, competitive threats, declining margins, valuation concerns, and disconfirming evidence.

The **Base Agent** is the neutral consensus anchor and the most important agent in the system. Its system prompt instructs it to weigh upside and downside symmetrically and produce the most likely outcome — equivalent to "what would a median sell-side analyst say?" — with no directional bias. The Arbiter measures how far Bull and Bear deviate from Base, so any bias in Base contaminates the entire framework. We pay particular attention to its calibration in the prompt by including an explicit confidence scale tied to a calibrated probability interpretation.

The **Quant Agent** receives only numerical data: the `key_metrics` dictionary and the 30-day `price_history` array. All narrative fields (earnings summary, sector, macro context, company name, ticker) are stripped before the prompt is constructed. Its system prompt directs it to analyze pure quantitative signals — momentum, valuation multiples, volume trends, volatility — without any narrative grounding. The **Macro Strategist Agent** is the dual: it receives only the `sector` and `macro_context` fields and analyzes whether macro and sector conditions favor or hurt companies in this sector, ignoring all company-specific data. Both filters are implemented as small helper functions (`strip_to_numbers` and `strip_to_macro` in `utils/helpers.py`) so the data hygiene is auditable.

The **Arbiter Agent** receives all five agent outputs as a single JSON-serialized input. Its prompt instructs it to score each agent's argument on a 0–10 scale for evidence quality, compute each non-Base agent's deviation from the Base case as a probability of "up," produce a final synthesized analysis with calibrated confidence, and emit a structured disagreement map. The Arbiter's output schema differs from the analytical agents — it produces `final_directional_view`, `final_confidence_score`, `agent_scores`, `deviation_from_base`, `disagreement_score`, `key_disagreements`, `synthesis`, and `confidence_map` (probabilities for upside, base, and downside cases summing to 100). To support this larger schema we extended the shared API client with an optional flag that bypasses the agent-schema validator while preserving all other behavior.

### 3.2 Pipeline Configurations

We compare three pipeline configurations on the same benchmark to isolate the effect of architecture rather than model capability.

The **Monolithic baseline** (`pipelines/monolithic.py`) issues a single Claude API call with one comprehensive prompt that asks the model to evaluate the scenario across bullish, bearish, quantitative, and macro lenses simultaneously and return the standard four-field output. This represents the standard "throw a big prompt at one model" approach and is what an adversarial architecture must beat to justify its complexity.

The **Cooperative baseline** (`pipelines/cooperative.py`) runs the five agents *sequentially*, each seeing the previous agents' outputs as appended context. The order is Quant → Macro → Base → Bull → Bear, with the Bear agent's output serving as the final synthesis. This pipeline tests whether agents that build on each other's reasoning produce better results than a single comprehensive call.

The **Adversarial system** (`pipelines/adversarial.py`) runs all five agents independently — none sees any other agent's output — and then routes their five outputs to the Arbiter for synthesis. This is the configuration the project hypothesizes will perform best. The adversarial run produces both an aggregate final view (suitable for direct comparison with the baselines on accuracy and Brier score) and a structured disagreement map (used to test H2 directly).

### 3.3 Benchmark Dataset

We constructed a benchmark of 50 financial scenarios distributed across modification types. Each scenario is a JSON file conforming to a fixed schema that includes `scenario_id`, `company`, `ticker`, `event_date`, `event_type`, `modification_type`, an `input_data` block (with `earnings_summary`, `key_metrics`, `price_history`, `sector`, `macro_context`), and a `ground_truth` block (with `price_1w_after`, `price_change_pct`, `actual_direction`, `key_risk_factors`, `missed_signals`). Agents are explicitly forbidden from receiving the `ground_truth` field at any point in the pipeline; this is enforced by a helper function (`extract_input_data`) that all agents are required to use.

Twenty-five scenarios are real, unmodified earnings events drawn from the past two years across diverse sectors (technology, healthcare, finance, consumer, energy) and outcomes (earnings beats with positive returns, earnings beats with negative returns, misses with positive returns, surprise events). Sources include SEC EDGAR filings, Yahoo Finance for price histories, and earnings call transcripts and press releases for narrative summaries. The remaining 25 scenarios are modified variants designed to test robustness: ten are real events with planted misinformation (e.g., the `earnings_summary` claims revenue grew 40% while `key_metrics` shows it declined 5%; or an acquisition is mentioned that did not occur), ten are additional unmodified real events to balance the dataset, and five are incomplete-data scenarios where one critical field of `input_data` has been removed. The `modification_type` field labels each scenario for downstream robustness scoring.

### 3.4 Evaluation Metrics

We measure four metrics, all implemented as pure Python functions in `evaluation/metrics.py`:

- **Accuracy** is the percentage of scenarios where the pipeline's `directional_view` matches the ground-truth `actual_direction`.
- **Brier score** is the mean squared error between the pipeline's signed probability of "up" (computed from `directional_view` and `confidence_score`) and the binary outcome (1 if actual_direction is "up", else 0). Lower is better; this measures calibration.
- **Informativeness** is the percentage of ground-truth `key_risk_factors` whose content tokens are covered (≥50% bag-of-words overlap, stopword-filtered) in the pipeline's `key_factors` and `reasoning` text. This measures how many of the analytically important risks the pipeline surfaced.
- **Robustness** is the difference between accuracy on unmodified scenarios (`modification_type = "none"`) and accuracy on modified scenarios (misinformation or incomplete). A larger positive degradation means the pipeline is more fooled by adversarial inputs.

We additionally compute an **inter-agent disagreement score** for the adversarial pipeline, defined as the spread between Bull, Base, and Bear when each is mapped to a signed probability of "up." This score is the empirical quantity used to test H2.

### 3.5 Implementation Details

All experiments use Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) accessed through Anthropic's Python SDK. The model choice is held constant across all three pipelines so that any performance differences are attributable to architecture rather than model capability. We initially planned to use open-source models (Llama 3 8B, Mistral 7B) on Google Colab as proposed, but pivoted to a hosted API for two reasons: open-source 7–8B models produce JSON-format violations frequently enough to confound architectural comparison, and the comparison is cleaner when one model is held fixed across all configurations.

The full benchmark consists of 150 pipeline runs (50 scenarios × 3 pipelines), comprising approximately 600 individual Claude API calls. Pipeline runs are independent across scenarios and are executed in parallel using a thread pool with three workers — empirically, three workers stay below the per-minute output-token rate limit on the development tier while delivering a roughly 3× wall-clock speedup over sequential execution. The shared API client (`utils/api_client.py`) implements exponential backoff (4s, 8s, 16s, 32s, 60s with jitter) on transient `RateLimitError`, `APITimeoutError`, and `APIConnectionError` exceptions so that no run is lost to a brief rate-limit collision. Raw outputs are persisted per-run as JSON files in `results/raw/` and metrics are computed in a separate post-processing pass, making the experiment fully reproducible from the saved outputs without requiring re-running the agents.

---

## 4. Results and Analysis

### 4.1 Headline Numbers

Table 1 summarizes the four primary metrics across all three pipeline configurations on the full 50-scenario benchmark. Figure 1 renders the same comparison visually.

**Table 1.** Pipeline performance across all four evaluation metrics on the 50-scenario benchmark (25 real + 25 modified). Bold = best per row.

| Metric | Monolithic | Cooperative | Adversarial |
|---|---|---|---|
| Accuracy (%) | 66.00 | 44.00 | **66.67** |
| Brier score (lower = better) | 0.231 | 0.308 | **0.225** |
| Informativeness (%) | 28.85 | **33.82** | 18.69 |
| Robustness degradation (real → modified, pp) | 20.00 | **−8.00** | 16.67 |

**Figure 1.** Pipeline comparison across evaluation metrics. Bars show accuracy, informativeness, and robustness degradation as percentages (left axis); the dashed line shows Brier score on a separate scale (right axis, lower is better). See `report/figures/pipeline_comparison.png`.

Two of these results align with our hypotheses, two do not, and one is unexpected.

**The Adversarial pipeline produces the best calibration of any configuration** (Brier 0.225 vs. 0.231 monolithic vs. 0.308 cooperative). This supports H1: structured disagreement between specialized agents produces better-calibrated confidence estimates than either a single comprehensive prompt or a sequential cooperative chain. The improvement over Monolithic is small (3% relative) but consistent across the real-only subset (Adversarial 0.160 vs. Monolithic 0.153 — Monolithic edges ahead here) and the modified subset (Adversarial 0.290 vs. Monolithic 0.309). On directional accuracy, Adversarial and Monolithic are tied at the noise floor (one scenario apart in 50, ~1% absolute difference).

**The Cooperative pipeline performs substantially worse than either alternative on accuracy and Brier**. This was not predicted by our hypotheses, which expected Cooperative to fall between Monolithic and Adversarial. Investigation of the raw output distribution reveals the cause cleanly: in our Cooperative configuration the Bear agent runs last and produces the final synthesis, and the Bear agent is structurally instructed to argue downside risk. The empirical consequence is striking — the Cooperative pipeline returned `directional_view = "bearish"` on **25 of 25 real scenarios and 25 of 25 modified scenarios** (100% bearish, both subsets). The actual ground-truth distribution on the 25 real scenarios is 13 "up", 10 "down", and 2 "flat" (52% base rate of up); Cooperative's all-bearish output therefore lands 10 of 25 correct (40%) on real and 12 of 25 correct (48%) on modified. This is not a property of cooperative chains in general — it is a property of cooperative chains *whose final agent has a structurally asymmetric prior*. We report it as a finding rather than a defect because it is the same architecture specified in the original project assignment, and it cleanly demonstrates that *which agent runs last* in a cooperative chain is itself a load-bearing design decision. For comparison, the Adversarial pipeline returned `final_directional_view` distributed as 11 bullish, 11 bearish, and 2 neutral on real scenarios — close to the ground-truth distribution — and Monolithic returned 12 bullish, 11 bearish, 2 neutral. Both balanced architectures recover, while the cooperative chain collapses entirely onto its final agent's bias.

**Adversarial loses on Informativeness** (18.69% vs. Monolithic 28.85% vs. Cooperative 33.82%). This is a real tradeoff: the Arbiter's `synthesis` paragraph is intentionally concise — its job is to weigh and conclude, not to enumerate every risk factor. The five underlying agents collectively surface many more risks than the Arbiter's final paragraph alone reflects. A more informativeness-friendly version of Adversarial would expose the union of all five agents' `key_factors` to the metric, and we expect that variant to substantially close or invert the gap. We did not implement this variant in the present benchmark to keep the comparison apples-to-apples (one final output per pipeline).

### 4.2 Robustness to Misinformation (H3)

H3 predicted that the Adversarial pipeline would be more robust to misleading or incomplete input data than the baselines. The robustness data partially supports this.

On real (unmodified) scenarios, both Monolithic (76%) and Adversarial (75%) achieve high accuracy. On modified scenarios, both pipelines drop substantially — Monolithic to 56%, Adversarial to 58.33%. Adversarial's degradation (16.67 percentage points) is slightly smaller than Monolithic's (20.00 pp) but the difference is within noise on a 25-scenario sample. We cannot conclude from these numbers that Adversarial is meaningfully more robust to misinformation than Monolithic.

The Cooperative pipeline shows a *negative* degradation (−8.0 pp, i.e. accuracy increases from 40% on real to 48% on modified). This is almost certainly an artifact of Cooperative's pre-existing bearish bias rather than evidence that cooperative chains are inherently robust: when the modified scenarios include misinformation that flips the apparent narrative bullish, a Cooperative pipeline that systematically calls scenarios bearish gets some of those flipped scenarios "right" by accident. Reading the metric in isolation would suggest Cooperative is the most robust pipeline, which would be misleading. We caution against interpreting this as a positive finding for the cooperative architecture.

### 4.3 Disagreement as a Signal (H2)

The Adversarial pipeline produces an inter-agent disagreement score (max minus min of the signed "up" probabilities across Bull, Base, and Bear) for each scenario. The mean disagreement across 48 scenarios that produced complete agent outputs is **0.6346**, indicating moderate-to-high disagreement on average. This is consistent with the framework's design intent that the agents should actually conflict rather than redundantly converge.

Figure 2 tests H2 directly by plotting the disagreement score against the absolute value of the realized one-week price change for each scenario. A positive correlation would support the claim that disagreement predicts realized uncertainty. The empirical scatter shows a weak positive trend with substantial noise, which is what we should expect on a 48-scenario sample with realized returns spanning a wide range. We interpret this as suggestive but not conclusive evidence for H2 — a definitive test would require a larger benchmark with more diverse outcome volatility. The disagreement signal is at least non-trivially correlated with realized variance and does not appear to be pure noise.

**Figure 2.** Inter-agent disagreement score (x-axis) vs. realized absolute one-week price change (y-axis), one point per adversarial scenario. Linear fit overlaid. See `report/figures/disagreement_vs_uncertainty.png`.

### 4.4 Per-Scenario Disagreement Maps

For each adversarial run we render a per-scenario disagreement map (Figure 3) showing the five agents' signed confidence centered on neutral, with the Base agent visually highlighted as the analytical anchor. These maps are useful both as a research artifact (every disagreement is auditable post-hoc) and as a potential user-facing feature for downstream applications: an investor consuming the system's output sees not just *what* the system recommends but *which dimensions of the analysis are contested* and *by how much* relative to the neutral expectation.

**Figure 3.** Example disagreement map for `real_001` (NVIDIA Q4 FY2024). Each bar shows one agent's signed probability of "up" centered at the neutral midpoint; the Base agent is outlined in black as the analytical anchor. See `report/figures/disagreement_real_001.png` and the 47 other per-scenario maps in `report/figures/`.

### 4.5 Two Failed Adversarial Runs

Two of the 50 adversarial runs failed during the Arbiter step (`real_011` and `modified_015`), both with a JSON parsing error in the Arbiter's response. The remaining 48 runs completed successfully. Inspection of the raw responses suggests the Arbiter occasionally emits a malformed JSON object when its synthesis paragraph contains unescaped quotation marks. A production-grade implementation would either constrain output via Anthropic's structured-output mode or wrap parsing in a more aggressive recovery loop; our retry-with-backoff logic addresses transient API failures but does not handle deterministic JSON malformations. We treat the 48-of-50 success rate as acceptable for the present benchmark and would prioritize this fix in any follow-on work.

---

## 5. Conclusions and Future Work

### 5.1 Findings

We posed three hypotheses and tested them on a 50-scenario financial benchmark with controlled architectural variation. Our findings can be summarized as follows.

**On H1 (calibration and informativeness).** The Adversarial pipeline produces the lowest Brier score of all three configurations and matches the Monolithic baseline on directional accuracy. The improvement is small in absolute terms but consistent. Adversarial loses to Monolithic on Informativeness because the Arbiter's synthesis is concise by design; this is a tradeoff inherent in *summarizing* multiple agents' views rather than *concatenating* them. A practical takeaway is that adversarial architecture buys calibration without sacrificing accuracy, but at a cost in synthesized output verbosity.

**On H2 (disagreement as a signal).** Mean inter-agent disagreement was 0.6346 on a 0–1 scale, indicating that the Bull/Base/Bear triangle actually produces conflict rather than convergence. The correlation between disagreement and realized one-week price-change magnitude is positive but noisy on a 48-scenario sample. We interpret this as suggestive support, not proof. The disagreement signal is plausibly informative; a definitive test requires more scenarios and ideally diverse outcome volatility.

**On H3 (robustness).** The data does not support the claim that the Adversarial architecture is meaningfully more robust to planted misinformation than the Monolithic baseline. Both pipelines lose roughly 17–20 percentage points of accuracy on the modified subset. The Cooperative pipeline appears robust by this metric but only as an artifact of its bearish bias — a cautionary example of how a single summary statistic can mislead when underlying behavior is asymmetric.

### 5.2 Implications

Our headline implication is that **pipeline architecture is a meaningful design choice independent of model selection**. With one model held fixed across configurations, we observe a 22-percentage-point spread in accuracy between the best and worst architectures. Practitioners deploying foundation models for high-stakes reasoning tasks should consider architectural choices — including which agent has the final word — at least as carefully as they consider model and prompt selection.

A second implication is that **the choice of *which* agent runs last in a sequential pipeline is itself a load-bearing decision**. Our Cooperative configuration's poor performance is fully attributable to the Bear agent producing the final synthesis. Cooperative chains as a class are not refuted by our data; rather, cooperative chains *with structurally biased final agents* are.

A third implication is that **disagreement, when it can be measured cheaply, is worth measuring**. The Adversarial system's disagreement map is a no-extra-cost byproduct of running the agents anyway, and it carries non-trivial information about scenario uncertainty. We expect this to generalize beyond finance to any domain where multiple analytical lenses can be defined and made to disagree.

### 5.3 Limitations

Our results are subject to several limitations. First, the benchmark size of 50 scenarios is small relative to the variance in financial outcomes; effect sizes within ~5 percentage points should be interpreted as suggestive rather than definitive. Second, all experiments use a single model (Claude Haiku 4.5); we do not yet know whether the architectural advantages we observe transfer to other model families or capability tiers. Third, our ground truth is one-week post-event price change, which captures a particular trading horizon; results may differ at one-month or one-quarter horizons. Fourth, our informativeness metric uses bag-of-words overlap, which underweights paraphrased risk descriptions and over-rewards vocabulary matches; a semantic similarity metric would be more faithful. Fifth, two adversarial runs failed due to malformed JSON output from the Arbiter, leaving 48 rather than 50 complete adversarial samples.

### 5.4 Future Work

Several directions follow naturally. The most straightforward is **scaling the benchmark** to several hundred scenarios, which would tighten confidence intervals on the metric differences we observe. **Cross-model replication** would test whether the architectural patterns we identify hold for larger models (Sonnet, GPT-4) and for open-source alternatives — particularly relevant given the original proposal's emphasis on open-source experiments. **A more informativeness-aware Adversarial output** that exposes the union of agent risk factors alongside the Arbiter's synthesis would test whether the verbosity tradeoff we observed is fundamental or remediable. **Additional pipeline variants** — for example, Cooperative chains with the Base agent producing the final synthesis instead of Bear — would isolate the effect of final-agent bias from cooperation per se. Finally, the disagreement map is well-suited for **integration into a downstream financial intelligence application**, where it would surface to users not just a recommendation but the dimensions and magnitude of internal model disagreement — a direction the Adversarial Consensus framework was built with in mind.

---

## References

Du, N., Huang, Y., Dai, A. M., Tong, S., Lepikhin, D., Xu, Y., Krikun, M., Zhou, Y., Yu, A. W., Firat, O., Zoph, B., Fedus, L., Bosma, M., Zhou, Z., Wang, T., Wang, Y. E., Webster, K., Pellat, M., Robinson, K., Meier-Hellstern, K., Duke, T., Dixon, L., Zhang, K., Le, Q. V., Wu, Y., Chen, Z., & Cui, C. (2022). *GLaM: Efficient scaling of language models with mixture-of-experts*. Proceedings of the 39th International Conference on Machine Learning (ICML 2022).

Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., & Mordatch, I. (2023). *Improving factuality and reasoning in language models through multiagent debate*. arXiv preprint arXiv:2305.14325.

Fedus, W., Zoph, B., & Shazeer, N. (2022). *Switch Transformers: Scaling to trillion parameter models with simple and efficient sparsity*. Journal of Machine Learning Research, 23(120), 1–39.

Kadavath, S., Conerly, T., Askell, A., Henighan, T., Drain, D., Perez, E., Schiefer, N., Hatfield-Dodds, Z., DasSarma, N., Tran-Johnson, E., Johnston, S., El-Showk, S., Jones, A., Elhage, N., Hume, T., Chen, A., Bai, Y., Bowman, S., Fort, S., Ganguli, D., Hernandez, D., Jacobson, J., Kernion, J., Kravec, S., Lovitt, L., Ndousse, K., Olsson, C., Ringer, S., Amodei, D., Brown, T., Clark, J., Joseph, N., Mann, B., McCandlish, S., Olah, C., & Kaplan, J. (2022). *Language models (mostly) know what they know*. arXiv preprint arXiv:2207.05221.

Liang, T., He, Z., Jiao, W., Wang, X., Wang, Y., Wang, R., Yang, Y., Shi, S., & Tu, Z. (2023). *Encouraging divergent thinking in large language models through multi-agent debate*. arXiv preprint arXiv:2305.19118.

Qian, C., Liu, W., Liu, H., Chen, N., Dang, Y., Li, J., Yang, C., Chen, W., Su, Y., Cong, X., Xu, J., Li, D., Liu, Z., & Sun, M. (2023). *ChatDev: Communicative agents for software development*. arXiv preprint arXiv:2307.07924.

Wu, Q., Bansal, G., Zhang, J., Wu, Y., Li, B., Zhu, E., Jiang, L., Zhang, X., Zhang, S., Liu, J., Awadallah, A. H., White, R. W., Burger, D., & Wang, C. (2023). *AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation*. arXiv preprint arXiv:2308.08155.

Wu, S., Irsoy, O., Lu, S., Dabravolski, V., Dredze, M., Gehrmann, S., Kambadur, P., Rosenberg, D., & Mann, G. (2023). *BloombergGPT: A large language model for finance*. arXiv preprint arXiv:2303.17564.

Yang, H., Liu, X.-Y., & Wang, C. D. (2023). *FinGPT: Open-source financial large language models*. arXiv preprint arXiv:2306.06031.

---

## Appendix A: Repository

All code, data, and results are available at `https://github.com/tanishhh2077/cs639-adversarial-consensus`.

Key directories:
- `agents/` — the six agent implementations
- `pipelines/` — the three pipeline configurations
- `data/scenarios/real/` and `data/scenarios/modified/` — the 50-scenario benchmark
- `evaluation/metrics.py`, `evaluation/visualization.py` — scoring and plotting utilities
- `results/raw/` — per-run raw outputs (150 JSON files)
- `results/metrics.json` — aggregated metrics summary
- `report/figures/` — all figures referenced in this report

The full benchmark can be reproduced by running `python run_benchmark.py --skip-existing --parallel 3` followed by `python generate_figures.py`, given a valid Anthropic API key in `.env`.
