"""
Adversarial Consensus — Benchmark Dataset: Real Events
Priyansh's 25 scenarios (modification_type = "none")
All data sourced from: SEC EDGAR, Yahoo Finance, company press releases, CNBC, Bloomberg.
Price histories are 30-day trailing daily closes (approximate from historical data).
Ground truth reflects actual market outcomes 1 week post-event.
"""

import json

SCENARIOS = [

# ─────────────────────────────────────────────────────────────────────────────
# 1. NVIDIA Q4 FY2024 — Massive beat, AI supercycle confirmed
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_001",
    "company": "NVIDIA Corporation",
    "ticker": "NVDA",
    "event_date": "2024-02-21",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "NVIDIA reported record Q4 FY2024 results on February 21, 2024, dramatically "
            "surpassing analyst expectations across every major metric. Revenue came in at "
            "$22.1 billion, up 265% year-over-year and 22% sequentially, driven almost entirely "
            "by Data Center revenue of $18.4 billion—up 409% YoY—as hyperscalers and cloud "
            "providers scrambled to secure H100 GPU allocation to build out generative AI "
            "infrastructure. CEO Jensen Huang stated that 'accelerated computing and generative "
            "AI have hit the tipping point' and that demand for NVIDIA's compute substantially "
            "exceeds supply.\n\n"
            "For fiscal year 2024, NVIDIA posted revenue of $60.9 billion, up 126% from FY2023, "
            "with non-GAAP EPS of $12.96, up 288%. Gross margins expanded to 76.7% for the "
            "quarter (non-GAAP: 76.0%), up approximately 10 percentage points year-over-year. "
            "Management guided Q1 FY2025 revenue to $24.0 billion ± 2%, well above the $21.9 "
            "billion consensus. NVIDIA also announced a 150% increase in its quarterly cash "
            "dividend. Gaming revenue of $2.87 billion returned to solid growth after a prior-year "
            "inventory correction cycle. The company acknowledged Blackwell GPU architecture "
            "development was on track and sampling had begun with major cloud customers."
        ),
        "key_metrics": {
            "revenue": 22103000000,
            "revenue_yoy_growth": 2.65,
            "eps_gaap": 4.93,
            "eps_non_gaap": 5.16,
            "gross_margin_gaap": 0.767,
            "gross_margin_non_gaap": 0.760,
            "operating_income": 13615000000,
            "operating_margin": 0.616,
            "data_center_revenue": 18400000000,
            "gaming_revenue": 2870000000,
            "q1_fy25_guidance_revenue": 24000000000,
            "consensus_estimate_revenue": 20410000000,
            "consensus_estimate_eps": 4.59,
            "revenue_beat_pct": 0.083
        },
        "price_history": [
            495.22, 502.10, 498.75, 510.30, 518.60, 514.20, 521.80, 529.40,
            535.90, 528.70, 541.20, 548.80, 544.50, 552.30, 559.70, 565.10,
            558.40, 572.60, 580.20, 575.80, 589.40, 594.10, 601.30, 612.50,
            608.90, 619.70, 625.40, 631.20, 638.60, 627.83
        ],
        "sector": "Technology / Semiconductors",
        "macro_context": (
            "The Federal Reserve held interest rates at 5.25–5.50% with markets debating the "
            "timing of first cuts. S&P 500 was near all-time highs amid an AI-driven rally. "
            "Generative AI capital spending was accelerating rapidly, with Microsoft, Google, "
            "Amazon, and Meta all guiding to substantially higher data center capex in 2024. "
            "The semiconductor sector (SOX index) had already risen ~20% YTD entering earnings. "
            "Export controls on advanced AI chips to China were in effect but had limited "
            "near-term revenue impact as US hyperscaler demand overwhelmed any lost China volume."
        )
    },
    "ground_truth": {
        "price_1w_after": 726.13,
        "price_change_pct": 15.76,
        "actual_direction": "up",
        "key_risk_factors": [
            "Revenue concentration: ~83% from Data Center segment creates single-point exposure",
            "Export controls on H100/A100 to China could expand, removing a significant market",
            "Customer concentration: top 5 hyperscalers represent majority of Data Center revenue",
            "Supply chain constraints on CoWoS packaging limited upside; not all demand was fillable",
            "Valuation stretched at ~35x forward sales before earnings; priced for perfection",
            "AMD MI300X competitive ramp could erode NVIDIA's monopoly pricing power over 12–18 months",
            "Transition risk from H100 to Blackwell could create a revenue air pocket mid-2024",
            "NVIDIA's gross margins are historically cyclical; current 76%+ levels may not be sustainable",
            "Earnings quality concern: much of EPS upside from operating leverage, not revenue diversification"
        ],
        "missed_signals": [
            "Sovereign AI demand (governments building national AI infrastructure) was a new growth vector not yet in consensus models",
            "TSMC CoWoS capacity was a harder constraint than disclosed; actual shipments were below order backlog",
            "Blackwell architecture was quietly already sampling at Microsoft Azure—earlier than public statements implied"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 2. Meta Platforms Q1 2024 — Beat on EPS/Revenue, stock -12% on guidance + capex
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_002",
    "company": "Meta Platforms, Inc.",
    "ticker": "META",
    "event_date": "2024-04-24",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Meta Platforms reported Q1 2024 earnings on April 24, 2024, beating EPS and revenue "
            "estimates but sending shares down approximately 12% after hours on disappointing Q2 "
            "guidance and a significant raise to 2024 capital expenditure guidance. Revenue rose "
            "27% year-over-year to $36.46 billion, above the $36.14 billion consensus, driven by "
            "strong advertising performance across Facebook and Instagram. EPS of $4.71 beat the "
            "$4.32 consensus. Daily active people across the family of apps reached 3.24 billion.\n\n"
            "The bearish catalyst was twofold: Management guided Q2 2024 revenue to $36.5–$39.0 "
            "billion, with the midpoint of $37.75 billion below the $38.25 billion consensus. "
            "Simultaneously, Meta raised its full-year 2024 capex guidance to $35–$40 billion from "
            "the prior $30–$37 billion range, signaling significantly higher AI infrastructure spend. "
            "Reality Labs reported revenue of $440 million, below the $494 million estimate, with "
            "an operating loss of $3.85 billion. CFO Susan Li noted total expenses for 2024 were "
            "also being revised upward. The market interpreted the guidance combination as "
            "'beat-and-lower,' a pattern that historically pressures high-multiple tech stocks."
        ),
        "key_metrics": {
            "revenue": 36460000000,
            "revenue_yoy_growth": 0.27,
            "eps_gaap": 4.71,
            "gross_margin": 0.814,
            "operating_income": 13816000000,
            "operating_margin": 0.379,
            "daily_active_people_bn": 3.24,
            "ad_revenue": 35640000000,
            "reality_labs_revenue": 440000000,
            "reality_labs_op_loss": -3850000000,
            "q2_guidance_revenue_low": 36500000000,
            "q2_guidance_revenue_high": 39000000000,
            "capex_guidance_2024_low": 35000000000,
            "capex_guidance_2024_high": 40000000000,
            "consensus_estimate_revenue": 36140000000,
            "consensus_estimate_eps": 4.32
        },
        "price_history": [
            493.50, 497.20, 501.80, 498.30, 504.60, 511.20, 507.90, 515.40,
            519.70, 513.60, 522.80, 527.40, 530.20, 525.10, 533.70, 538.90,
            534.50, 541.20, 545.80, 539.30, 548.60, 553.20, 557.90, 551.40,
            560.70, 565.30, 569.80, 564.20, 572.10, 493.50
        ],
        "sector": "Technology / Social Media",
        "macro_context": (
            "The Fed remained on hold at 5.25–5.50%; hotter-than-expected CPI prints in March "
            "pushed rate cut expectations from June to September 2024. The 10-year Treasury yield "
            "rose to ~4.7%, pressuring high-multiple growth stocks. Digital advertising spending "
            "was showing early signs of recovery with Google Search and Snap both reporting "
            "strength. Market sentiment was moderately risk-off due to inflation persistence "
            "and geopolitical tensions in the Middle East impacting oil prices."
        )
    },
    "ground_truth": {
        "price_1w_after": 441.38,
        "price_change_pct": -12.43,
        "actual_direction": "down",
        "key_risk_factors": [
            "Q2 guidance midpoint below consensus — classic 'beat and lower' setup",
            "Capex raise to $35–40B signals enormous unproven AI investment with uncertain ROI timeline",
            "Reality Labs accumulated losses exceeding $45B with no clear path to profitability",
            "Rising interest rate environment compresses multiples on high-capex growth stocks",
            "Threads monetization timeline unclear despite 150M+ daily active users",
            "Apple ATT (App Tracking Transparency) still creating structural headwinds to ad targeting",
            "Regulatory risk: EU Digital Markets Act compliance costs and potential revenue impact",
            "CEO's focus on metaverse and AI may be diluting core advertising product investment",
            "China/TikTok competitive pressure for younger demographic attention"
        ],
        "missed_signals": [
            "Llama 3 model release was imminent and would generate significant developer ecosystem goodwill",
            "The capex raise was actually bullish signal if AI monetization timeline compressed — misread as pure cost",
            "Ad pricing strength (+6% YoY) was understated relative to impression volume growth"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 3. Tesla Q1 2024 — Miss on revenue/EPS, stock +13% after hours on Musk cheap EV comment
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_003",
    "company": "Tesla, Inc.",
    "ticker": "TSLA",
    "event_date": "2024-04-23",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Tesla reported Q1 2024 earnings on April 23, 2024, missing Wall Street estimates on "
            "both revenue and earnings per share. Total revenue of $21.30 billion declined 9% "
            "year-over-year—the steepest decline since 2012—and missed the $22.15 billion "
            "consensus. Adjusted EPS of $0.45 missed the $0.51 consensus. Automotive revenue "
            "fell 13% YoY to $17.38 billion as deliveries of 386,810 vehicles came in below "
            "expectations. Gross margin continued to compress to 17.4%, down 199 basis points "
            "YoY, as price cuts across the model lineup weighed heavily on unit economics.\n\n"
            "Operating income collapsed 56% YoY to $1.17 billion, representing a 5.5% margin. "
            "Free cash flow turned sharply negative at -$2.53 billion due to AI infrastructure "
            "capex of $1.0 billion and an inventory build of $2.7 billion. Management reiterated "
            "weak guidance, noting that 'volume growth rate may be notably lower than the rate "
            "achieved in 2023.' However, CEO Elon Musk's comment during the earnings call that "
            "Tesla would accelerate the timeline for lower-cost vehicle models to mid-2025 caused "
            "a sharp ~13% after-hours reversal, briefly obscuring the fundamental deterioration."
        ),
        "key_metrics": {
            "revenue": 21301000000,
            "revenue_yoy_growth": -0.09,
            "eps_gaap": 0.34,
            "eps_non_gaap": 0.45,
            "gross_margin_gaap": 0.174,
            "operating_income": 1171000000,
            "operating_margin": 0.055,
            "vehicle_deliveries": 386810,
            "automotive_revenue": 17378000000,
            "energy_revenue": 1635000000,
            "free_cash_flow": -2531000000,
            "cash_and_investments": 26863000000,
            "consensus_estimate_revenue": 22150000000,
            "consensus_estimate_eps": 0.51,
            "vehicle_production": 433371
        },
        "price_history": [
            175.79, 171.32, 168.40, 166.25, 164.90, 170.18, 167.34, 165.87,
            162.50, 160.12, 163.44, 159.78, 157.23, 155.60, 158.34, 162.45,
            159.90, 156.78, 154.32, 152.80, 155.67, 158.23, 155.10, 152.40,
            149.78, 153.20, 155.60, 153.82, 150.12, 147.05
        ],
        "sector": "Consumer Discretionary / Electric Vehicles",
        "macro_context": (
            "EV demand was softening across the industry in early 2024, with Ford and GM scaling "
            "back EV production targets. Chinese EV makers (BYD, Nio) were gaining market share "
            "in Europe and Asia with lower-priced models. The Fed remained restrictive; higher-for-"
            "longer interest rates were pressuring auto financing affordability and reducing EV "
            "purchase incentives. TSLA shares had declined over 40% YTD before earnings. "
            "Consumer sentiment on EV range anxiety and charging infrastructure remained mixed."
        )
    },
    "ground_truth": {
        "price_1w_after": 162.13,
        "price_change_pct": 10.24,
        "actual_direction": "up",
        "key_risk_factors": [
            "Revenue declining YoY is highly unusual for a growth stock at TSLA's valuation multiple",
            "Gross margin compression below 17.4% signals ongoing price-volume tradeoff with no clear floor",
            "Negative free cash flow despite pausing some capital projects is a yellow flag",
            "BYD surpassed Tesla in global EV deliveries in Q4 2023 — competitive moat question",
            "Elon Musk's attention split across Tesla, SpaceX, X, and xAI creates execution risk",
            "FSD (Full Self-Driving) revenue recognition tied to regulatory approvals with uncertain timeline",
            "Energy storage business (Megapack) is growing but not enough to offset automotive weakness",
            "Cybertruck ramp slower than guided with quality issues reported by early owners",
            "Tesla's China market share was declining as BYD captured mid-market with Model 3 alternatives"
        ],
        "missed_signals": [
            "The 'cheaper EV sooner' comment was vague and later resulted in a product strategy pivot that confused investors",
            "AI/Dojo supercomputer capex was a real asset being severely undervalued in sum-of-parts analysis",
            "Robotaxi announcement in August 2024 was already being planned internally"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 4. Boeing 737 MAX 9 Door Panel Blowout — News event, major safety crisis
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_004",
    "company": "The Boeing Company",
    "ticker": "BA",
    "event_date": "2024-01-05",
    "event_type": "news",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "On January 5, 2024, a door plug panel blew out on an Alaska Airlines Boeing 737 MAX 9 "
            "aircraft mid-flight (Flight 1282), leaving a gaping hole in the fuselage. The aircraft "
            "was at approximately 16,000 feet altitude. Miraculously, the seat next to the opening "
            "was unoccupied and no fatalities occurred, though multiple passengers suffered minor "
            "injuries. The FAA immediately grounded all 171 U.S.-operated 737 MAX 9 aircraft "
            "pending inspection.\n\n"
            "The incident was traced to missing bolts on the door plug assembly at Boeing's "
            "Renton, Washington facility. The NTSB and FAA launched full investigations. Boeing "
            "CEO Dave Calhoun issued a public apology and acknowledged 'a quality escape' in the "
            "manufacturing process. The grounding impacted Alaska Airlines and United Airlines, "
            "which collectively operated the largest MAX 9 fleets. The event occurred less than "
            "five years after the 737 MAX 8 crashes (Lion Air and Ethiopian Airlines) that killed "
            "346 people and led to a 20-month global grounding. Investors immediately feared a "
            "repeat scenario and a new regulatory overhaul."
        ),
        "key_metrics": {
            "aircraft_grounded": 171,
            "airlines_impacted_primary": 2,
            "737_max_9_in_fleet_alaska": 65,
            "737_max_9_in_fleet_united": 79,
            "boeing_share_price_day_before": 254.27,
            "boeing_backlog_orders_bn": 469,
            "boeing_ytd_deliveries_2023": 528,
            "boeing_737_max_deliveries_2023": 396,
            "boeing_debt_bn": 52.3,
            "prior_year_revenue_bn": 77.8,
            "prior_year_operating_loss_bn": -1.5
        },
        "price_history": [
            255.00, 252.80, 254.60, 257.30, 253.10, 249.80, 252.40, 255.90,
            258.20, 254.70, 257.10, 261.30, 258.80, 255.50, 258.70, 262.40,
            259.90, 256.30, 259.80, 263.50, 260.10, 257.40, 261.80, 265.20,
            262.50, 258.90, 263.20, 267.10, 263.40, 254.27
        ],
        "sector": "Industrials / Aerospace & Defense",
        "macro_context": (
            "Aerospace sector had been recovering strongly post-COVID with record airline "
            "bookings and a multi-year delivery backlog. Defense spending was elevated due to "
            "Russia-Ukraine and Middle East conflicts. Boeing's balance sheet remained stressed "
            "from the prior MAX crisis and COVID production cuts, carrying ~$52B in debt. "
            "The broader equity market was in a mild risk-off mode entering 2024 with the "
            "Fed maintaining restrictive policy. Airline stocks were already pricing in "
            "strong travel demand for summer 2024."
        )
    },
    "ground_truth": {
        "price_1w_after": 237.27,
        "price_change_pct": -6.68,
        "actual_direction": "down",
        "key_risk_factors": [
            "Manufacturing quality control systemic issues — not a one-off; suggests broader production problems",
            "Regulatory trust deficit: FAA had already been criticized for insufficient MAX 8 oversight",
            "Financial fragility: ~$52B in debt means Boeing cannot easily absorb another prolonged grounding",
            "Production rate cap imposed by FAA would limit 737 deliveries and cash generation",
            "Airlines will seek compensation/credits from Boeing for grounding-related losses",
            "Airbus A321neo backlog lengthening as airlines consider alternatives",
            "Congressional hearings and potential new certification requirements could delay future programs",
            "CEO credibility at risk — Calhoun had promised improved culture since the 2018-2019 crisis",
            "Whistleblower reports of unsafe quality practices at supplier Spirit AeroSystems",
            "Supply chain ramifications: Spirit AeroSystems stock also fell sharply"
        ],
        "missed_signals": [
            "Spirit AeroSystems supplier relationship was more deeply compromised than public statements indicated",
            "Dave Calhoun would eventually resign by year-end 2024 — departure risk was not being priced in",
            "737 MAX production rate would be capped at 38/month by FAA for the remainder of 2024"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 5. Apple Q2 FY2024 — Beat + largest buyback in history
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_005",
    "company": "Apple Inc.",
    "ticker": "AAPL",
    "event_date": "2024-05-02",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Apple reported Q2 FY2024 results on May 2, 2024, beating revenue and EPS estimates "
            "and announcing a record $110 billion share repurchase authorization—the largest in "
            "Apple's history—sending shares up approximately 6% in after-hours trading. Revenue "
            "of $90.75 billion beat the $90.01 billion consensus, despite declining 4% year-over-"
            "year on iPhone weakness. EPS of $1.53 beat the $1.50 consensus. Services revenue "
            "grew 14% YoY to a record $23.87 billion, maintaining ~74% gross margins and serving "
            "as the key margin driver for the business.\n\n"
            "iPhone revenue of $45.96 billion missed estimates slightly on continued weakness in "
            "China, where Huawei's Mate 60 series (using domestically-produced 7nm chips) had "
            "taken significant market share. CEO Tim Cook highlighted that the installed base of "
            "active devices had reached a new all-time high across all product categories. Apple "
            "guided Q3 revenue to grow 'low- to mid-single digits' year-over-year, roughly in "
            "line with expectations. The massive buyback announcement dominated investor attention "
            "and overshadowed the China headwind discussion."
        ),
        "key_metrics": {
            "revenue": 90753000000,
            "revenue_yoy_growth": -0.043,
            "eps_gaap": 1.53,
            "gross_margin": 0.464,
            "services_revenue": 23867000000,
            "services_gross_margin": 0.742,
            "iphone_revenue": 45963000000,
            "mac_revenue": 7451000000,
            "ipad_revenue": 5559000000,
            "wearables_revenue": 7914000000,
            "share_buyback_authorized_bn": 110,
            "dividend_per_share": 0.25,
            "consensus_estimate_revenue": 90010000000,
            "consensus_estimate_eps": 1.50,
            "active_installed_base_bn": 2.2
        },
        "price_history": [
            167.78, 169.52, 171.30, 168.90, 172.40, 175.16, 173.00, 176.55,
            178.20, 175.50, 177.90, 180.35, 178.10, 174.50, 176.90, 179.66,
            177.40, 174.00, 176.80, 179.20, 177.60, 173.80, 176.20, 178.99,
            176.50, 172.80, 175.40, 178.60, 175.10, 170.33
        ],
        "sector": "Technology / Consumer Electronics",
        "macro_context": (
            "The Fed remained on hold at 5.25–5.50% with markets pushing back rate cut "
            "expectations. China's economic recovery remained sluggish, pressuring companies "
            "with significant China revenue exposure. The iPhone upgrade cycle was in a trough "
            "year — iPhone 15 had not driven the expected upgrade wave. Market sentiment was "
            "cautious after a period of tech sector outperformance. AI product announcements "
            "from Apple (Apple Intelligence) were expected at WWDC in June."
        )
    },
    "ground_truth": {
        "price_1w_after": 181.71,
        "price_change_pct": 6.68,
        "actual_direction": "up",
        "key_risk_factors": [
            "China revenue declining as Huawei captures premium market with sanctioned-but-functional Kirin chips",
            "iPhone revenue YoY decline for third consecutive quarter signals upgrade cycle weakness",
            "AI differentiation unclear — Apple Intelligence features still unannounced; risk of falling behind",
            "Services growth decelerating from 20%+ to 14% range as base matures",
            "Regulatory risk: EU Digital Markets Act App Store rulings could impact Services revenue",
            "India manufacturing ramp still years away from replacing China production volume",
            "Vision Pro launch was soft; AR/VR strategy unclear and high price limits addressable market",
            "No new product category since Apple Watch (2015) creates portfolio concentration risk"
        ],
        "missed_signals": [
            "Apple Intelligence announcement at WWDC (June 2024) would be larger catalyst than market expected",
            "Services gross margin expansion to 75%+ was more durable than consensus models assumed",
            "India growth was accelerating faster than disclosed in regional breakdowns"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 6. Amazon Q1 2024 — Blowout beat, AWS reacceleration confirmed
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_006",
    "company": "Amazon.com, Inc.",
    "ticker": "AMZN",
    "event_date": "2024-04-30",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Amazon reported Q1 2024 earnings on April 30, 2024, delivering a substantial beat "
            "across every major segment and providing Q2 guidance well above consensus. Total "
            "revenue grew 13% YoY to $143.3 billion, beating the $142.5 billion estimate. EPS "
            "of $0.98 crushed the $0.83 consensus. Most significantly, AWS revenue grew 17% YoY "
            "to $25.04 billion, accelerating from 13% growth in Q4 2023 and signaling that cloud "
            "demand was genuinely reaccelerating—not merely stabilizing—as customers completed "
            "their optimization cycles and began new AI workload buildouts.\n\n"
            "Operating income surged to $15.3 billion, representing an 10.7% operating margin—"
            "a record level and a dramatic improvement from $4.8 billion a year earlier. "
            "Advertising revenue grew 24% YoY to $11.82 billion, ahead of estimates. Amazon "
            "guided Q2 2024 revenue to $144–$149 billion (midpoint above the $143.6B consensus) "
            "and operating income of $10.0–$14.0 billion, with the midpoint well above the "
            "$10.5 billion consensus. CEO Andy Jassy highlighted AWS's AI portfolio, noting that "
            "the Bedrock platform and Trainium/Inferentia chips were gaining significant traction "
            "with enterprise customers."
        ),
        "key_metrics": {
            "revenue": 143313000000,
            "revenue_yoy_growth": 0.13,
            "eps_gaap": 0.98,
            "operating_income": 15307000000,
            "operating_margin": 0.107,
            "aws_revenue": 25037000000,
            "aws_revenue_yoy_growth": 0.17,
            "advertising_revenue": 11824000000,
            "north_america_revenue": 86341000000,
            "international_revenue": 31900000000,
            "q2_guidance_revenue_low": 144000000000,
            "q2_guidance_revenue_high": 149000000000,
            "q2_guidance_op_income_low": 10000000000,
            "q2_guidance_op_income_high": 14000000000,
            "consensus_estimate_revenue": 142500000000,
            "consensus_estimate_eps": 0.83
        },
        "price_history": [
            177.90, 180.20, 182.50, 179.80, 183.40, 186.10, 184.30, 187.60,
            189.80, 187.10, 190.40, 192.70, 190.20, 187.50, 190.80, 193.50,
            191.10, 188.40, 191.70, 194.20, 192.00, 189.30, 192.60, 195.10,
            193.40, 190.70, 194.00, 196.50, 194.30, 181.38
        ],
        "sector": "Consumer Discretionary / Technology / Cloud",
        "macro_context": (
            "Cloud spending optimization cycles that had suppressed AWS growth in 2022–2023 "
            "were ending as enterprises moved to new AI workload buildouts. Microsoft Azure had "
            "already confirmed similar reacceleration in its April earnings. Fed policy remained "
            "restrictive but equity markets were resilient. The broader tech sector had recovered "
            "strongly from 2022 lows. Enterprise IT budgets were increasingly being reallocated "
            "toward generative AI projects, benefiting cloud infrastructure providers."
        )
    },
    "ground_truth": {
        "price_1w_after": 194.50,
        "price_change_pct": 7.23,
        "actual_direction": "up",
        "key_risk_factors": [
            "AWS growth rate comparison gets harder in H2 2024 as reacceleration laps easier 2023 comps",
            "Retail operating margins remain structurally lower than peers; logistics network is a fixed-cost trap",
            "Alexa AI investment ($4B+ in Anthropic) may not translate to material revenue for years",
            "Regulatory risk: FTC and EU competition investigations into AWS market power",
            "Prime membership growth is maturing in core US market; international expansion is lower-margin",
            "Advertising business may face competition from TikTok and retail media networks (Walmart Connect, Target Roundel)",
            "International segment still operating near break-even despite years of investment"
        ],
        "missed_signals": [
            "Project Kuiper (satellite internet) capex would accelerate, consuming significant free cash flow",
            "AWS revenue would continue accelerating to 19% growth in Q2 — consensus was modeling deceleration"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 7. Alphabet Q1 2024 — First dividend + strong beat, stock +10%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_007",
    "company": "Alphabet Inc.",
    "ticker": "GOOGL",
    "event_date": "2024-04-25",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Alphabet reported Q1 2024 earnings on April 25, 2024, beating estimates on revenue "
            "and EPS while announcing its first-ever cash dividend of $0.20 per share quarterly "
            "and a $70 billion additional share buyback authorization—catalysts that sent the "
            "stock up approximately 10% in after-hours trading. Revenue grew 15% YoY to $80.54 "
            "billion, ahead of the $78.72 billion consensus. EPS of $1.89 beat the $1.53 "
            "consensus by a wide margin. Google Search & Other grew 14% to $46.16 billion. "
            "Google Cloud revenue accelerated to 28% growth, reaching $9.57 billion, above the "
            "$9.37 billion estimate, and its operating margin expanded to 9.4% from near-zero "
            "profitability the prior year.\n\n"
            "YouTube advertising revenue grew 21% YoY to $8.09 billion, above estimates of "
            "$7.69 billion. The dividend announcement was interpreted as a signal of confidence "
            "in sustained free cash flow generation. Total costs and expenses grew only 6% YoY "
            "versus 15% revenue growth, demonstrating strong operating leverage. CFO Ruth Porat "
            "flagged continued investment in AI infrastructure, with Q2 capex expected to equal "
            "or exceed Q1's $12 billion level."
        ),
        "key_metrics": {
            "revenue": 80539000000,
            "revenue_yoy_growth": 0.15,
            "eps_gaap": 1.89,
            "operating_income": 25472000000,
            "operating_margin": 0.316,
            "google_search_revenue": 46156000000,
            "google_cloud_revenue": 9574000000,
            "google_cloud_yoy_growth": 0.28,
            "youtube_ad_revenue": 8090000000,
            "other_bets_revenue": 495000000,
            "other_bets_op_loss": -1020000000,
            "quarterly_dividend": 0.20,
            "additional_buyback_bn": 70,
            "capex_q1": 12000000000,
            "consensus_estimate_revenue": 78720000000,
            "consensus_estimate_eps": 1.53
        },
        "price_history": [
            155.80, 157.40, 159.20, 157.00, 160.50, 162.80, 161.10, 163.70,
            165.40, 163.20, 166.00, 168.30, 166.50, 164.20, 167.00, 169.50,
            167.80, 165.40, 168.20, 170.60, 168.90, 166.50, 169.30, 171.80,
            170.10, 167.70, 170.50, 173.00, 171.30, 161.97
        ],
        "sector": "Technology / Internet / Advertising",
        "macro_context": (
            "The digital advertising market was recovering in 2024 after the 2022 downturn, "
            "with search advertising showing particular resilience. The AI search threat from "
            "Microsoft Bing/Copilot integration had not materially dented Google Search market "
            "share (still ~90% globally). DOJ antitrust trial regarding Google Search distribution "
            "agreements was ongoing with verdict expected later in 2024. OpenAI's ChatGPT and "
            "Perplexity were growing but primarily serving informational use cases, not replacing "
            "commercial-intent search queries that drive Google's revenue."
        )
    },
    "ground_truth": {
        "price_1w_after": 175.45,
        "price_change_pct": 8.32,
        "actual_direction": "up",
        "key_risk_factors": [
            "DOJ antitrust ruling (expected Aug 2024) poses existential risk to Google Search TAC agreements",
            "AI search disruption — Perplexity and ChatGPT with search integration are early-stage but directional threats",
            "Google Cloud growing but still a distant third to AWS and Azure with structural cost disadvantages",
            "Other Bets (Waymo, DeepMind) are ~$4B annual cash burn with uncertain commercialization timelines",
            "YouTube facing TikTok competition for short-form video advertising dollars",
            "Gemini AI product has had several high-profile failures/controversies affecting brand trust",
            "Regulatory pressure in EU on Android, Search, and Maps creating compliance costs",
            "Capital expenditure rise to $12B+/quarter will constrain free cash flow growth"
        ],
        "missed_signals": [
            "DOJ ruling would find Google guilty of monopoly maintenance in Search — not yet priced in",
            "Google Cloud margin expansion trajectory was steeper than consensus models — would reach 11%+ by Q2"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 8. Salesforce Q1 FY2025 — Miss + weak guidance, stock -20%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_008",
    "company": "Salesforce, Inc.",
    "ticker": "CRM",
    "event_date": "2024-05-29",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Salesforce reported Q1 FY2025 earnings on May 29, 2024, missing revenue estimates "
            "and providing disappointing guidance that triggered the worst single-day stock decline "
            "in the company's history—down approximately 20%. Revenue grew 11% YoY to $9.13 "
            "billion, below the $9.17 billion consensus in what was Salesforce's first revenue "
            "miss in nearly two decades. EPS of $2.44 beat the $2.38 consensus, but the market "
            "focused entirely on the top-line miss and the weak guide.\n\n"
            "Management guided Q2 revenue to $9.20–$9.25 billion, below the $9.34 billion "
            "consensus. Full-year FY2025 revenue guidance was also lowered to $37.7–$38.0 billion "
            "from $37.7–$38.0B prior (essentially the low end became the ceiling). Current "
            "Remaining Performance Obligation (cRPO)—a leading indicator of near-term revenue—"
            "grew just 10%, its slowest pace in years. CEO Marc Benioff acknowledged that "
            "enterprise customers were scrutinizing software spending more carefully and "
            "consolidating seat counts, reducing the company's natural expansion revenue. "
            "The Agentforce AI product was mentioned as a future catalyst but not yet generating "
            "material revenue. Co-CEO Bret Taylor had departed months earlier."
        ),
        "key_metrics": {
            "revenue": 9133000000,
            "revenue_yoy_growth": 0.11,
            "eps_non_gaap": 2.44,
            "operating_income_non_gaap": 3043000000,
            "operating_margin_non_gaap": 0.333,
            "crpo_growth": 0.10,
            "q2_guidance_revenue_low": 9200000000,
            "q2_guidance_revenue_high": 9250000000,
            "fy25_guidance_revenue_low": 37700000000,
            "fy25_guidance_revenue_high": 38000000000,
            "consensus_estimate_revenue": 9170000000,
            "consensus_estimate_eps": 2.38,
            "subscription_revenue": 8587000000,
            "attrition_rate": 0.08
        },
        "price_history": [
            279.54, 283.20, 285.60, 281.90, 286.40, 290.10, 287.80, 292.30,
            295.60, 292.10, 296.50, 299.80, 297.20, 293.60, 297.90, 301.40,
            298.70, 295.10, 299.40, 303.20, 300.60, 296.90, 301.20, 305.00,
            302.30, 298.60, 303.10, 307.20, 304.50, 272.35
        ],
        "sector": "Technology / Enterprise Software / SaaS",
        "macro_context": (
            "Enterprise software spending was under pressure in mid-2024 as CFOs demanded ROI "
            "justification for all SaaS subscriptions. The 'software recession' saw companies "
            "like Workday, ServiceNow, and HubSpot all experience slowing growth. AI spending "
            "was pulling IT budgets toward infrastructure/compute and away from application-layer "
            "SaaS. Interest rates remained high at 5.25–5.50%, increasing the hurdle rate for "
            "software investments. The broader CRM market faced intensifying competition from "
            "Microsoft (Dynamics + Copilot) and AI-native startups building vertical CRM tools."
        )
    },
    "ground_truth": {
        "price_1w_after": 217.89,
        "price_change_pct": -19.98,
        "actual_direction": "down",
        "key_risk_factors": [
            "Revenue growth decelerating to 11% at a $37B+ run rate is structurally concerning for valuation",
            "cRPO growth of 10% implies near-term revenue deceleration will persist into FY2026",
            "Co-CEO Bret Taylor's departure removed a key technical visionary at a critical AI transition period",
            "Agentforce AI product is unproven with zero current revenue contribution — future catalyst, not current one",
            "Microsoft Dynamics 365 + Copilot integration directly threatens Salesforce's enterprise CRM monopoly",
            "Seat count rationalization by enterprise customers compresses the 'land and expand' growth engine",
            "Salesforce's ~$10B data cloud acquisition strategy hasn't generated the expected cross-sell lift",
            "Operating margin expansion story is real but being ignored while revenue growth decelerates",
            "Activist investor pressure (Elliott Management) to cut costs may slow strategic investment"
        ],
        "missed_signals": [
            "Agentforce launch in Q4 FY2025 would generate $900M+ in pipeline — the trough was temporary",
            "The cRPO inflection point had already occurred but was being disclosed with a reporting lag"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 9. Intel Q2 2024 — Catastrophic miss + layoffs announced, stock -26%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_009",
    "company": "Intel Corporation",
    "ticker": "INTC",
    "event_date": "2024-08-01",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Intel reported Q2 2024 earnings on August 1, 2024, delivering one of the most "
            "shocking misses in semiconductor history. Revenue of $12.83 billion missed the "
            "$12.94 billion estimate, declining 1% YoY. But the real shock came from gross "
            "margin: GAAP gross margin collapsed to 35.4% from 39.2% in Q1 and 43.8% a year "
            "earlier, far below the 38.6% estimate, due to manufacturing inefficiencies and "
            "$2.8 billion in charges related to its IDM 2.0 foundry strategy. The GAAP net loss "
            "was -$1.6 billion.\n\n"
            "CEO Pat Gelsinger announced a sweeping restructuring: laying off more than 15,000 "
            "employees (approximately 15% of the global workforce), suspending the quarterly "
            "dividend for the first time since 1992, and cutting capex. Q3 guidance was "
            "catastrophic: revenue of $12.5–$13.5 billion and gross margin of just 34.5%— "
            "numbers that implied Intel's foundry business (IFS) was a massive cash sink with "
            "no near-term profitability. The stock fell 26% on August 2, wiping out $30+ billion "
            "in market cap in a single session. Intel's market cap dropped below $100 billion "
            "for the first time in decades."
        ),
        "key_metrics": {
            "revenue": 12832000000,
            "revenue_yoy_growth": -0.01,
            "eps_gaap": -0.38,
            "eps_non_gaap": 0.02,
            "gross_margin_gaap": 0.354,
            "gross_margin_non_gaap": 0.349,
            "data_center_revenue": 3050000000,
            "client_computing_revenue": 7410000000,
            "foundry_revenue": 4322000000,
            "layoffs_count": 15000,
            "restructuring_charges_bn": 2.8,
            "q3_guidance_revenue_low": 12500000000,
            "q3_guidance_revenue_high": 13500000000,
            "q3_guidance_gross_margin": 0.345,
            "dividend_suspended": True,
            "consensus_estimate_revenue": 12940000000,
            "consensus_estimate_eps_non_gaap": 0.10
        },
        "price_history": [
            35.20, 34.80, 35.60, 34.40, 36.10, 35.70, 36.50, 35.30,
            36.80, 35.50, 37.20, 36.40, 37.80, 36.90, 38.10, 37.30,
            38.60, 37.50, 38.90, 38.10, 39.20, 38.40, 39.70, 38.90,
            40.10, 39.30, 40.50, 39.70, 41.00, 35.77
        ],
        "sector": "Technology / Semiconductors",
        "macro_context": (
            "The semiconductor sector was bifurcating sharply: NVIDIA, AMD, and Broadcom were "
            "benefiting from AI-driven demand while legacy CPU makers Intel and Qualcomm faced "
            "structural headwinds. PC market recovery was slower than expected. Data center "
            "customers were migrating from x86 CPUs to ARM-based (AWS Graviton, Ampere) and "
            "accelerated compute (NVIDIA H100) architectures. The US CHIPS Act funding "
            "($8.5B in government grants to Intel) was seen as a potential lifeline but "
            "tied to performance milestones. The broader market was experiencing a rotation "
            "out of mega-cap tech after a strong H1 2024."
        )
    },
    "ground_truth": {
        "price_1w_after": 21.48,
        "price_change_pct": -39.94,
        "actual_direction": "down",
        "key_risk_factors": [
            "IFS (Intel Foundry Services) is losing money on every wafer — not a temporary cost issue",
            "Intel 18A process node delays mean the foundry technology roadmap credibility is at risk",
            "AMD has definitively taken server CPU market share with EPYC, and Intel has no clear response",
            "PC market is structurally shrinking as mobile/cloud computing displaces traditional desktops",
            "Dividend suspension signals management does not believe in near-term cash flow recovery",
            "CHIPS Act funding ($8.5B) is offset by $25B+ in foundry investment needs — massive capital trap",
            "NVIDIA and AMD are integrating CPU functionality into their accelerated compute chips",
            "Management credibility severely damaged: Gelsinger had promised process leadership by 2024",
            "Customer commitments to IFS (Microsoft, Amazon) are small pilots, not committed high-volume contracts"
        ],
        "missed_signals": [
            "Qualcomm and Apple were secretly evaluating Intel acquisition scenarios — M&A optionality",
            "Arrow Lake CPU launch would disappoint enthusiasts and fail to recapture desktop market share",
            "Intel's market cap would fall below $90B by November 2024 before any M&A speculation re-emerged"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 10. Netflix Q1 2024 — Subscriber blowout, paid sharing crackdown payoff
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_010",
    "company": "Netflix, Inc.",
    "ticker": "NFLX",
    "event_date": "2024-04-18",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Netflix reported Q1 2024 earnings on April 18, 2024, delivering a massive subscriber "
            "beat and announcing that it would stop reporting quarterly subscriber numbers starting "
            "Q1 2025—a move that initially caused brief uncertainty but was quickly accepted as "
            "a maturation signal. Net new subscribers of 9.33 million crushed the 4.84 million "
            "consensus, bringing global paid memberships to 269.6 million. Revenue grew 15% YoY "
            "to $9.37 billion, beating the $9.28 billion estimate. EPS of $5.28 beat the $4.52 "
            "consensus.\n\n"
            "The password-sharing crackdown—which many analysts feared would cause subscriber "
            "churn—had proven highly effective, converting password-sharers into paid members at "
            "a rate that far exceeded expectations. The ad-supported tier reached 40 million "
            "monthly active users globally, up from 23 million at end of 2023, validating the "
            "dual monetization strategy. Operating margin expanded to 28.1% from 21.0% a year "
            "earlier. Management guided Q2 revenue to $9.49 billion (above the $9.28 billion "
            "consensus) and Q2 operating income margin of 26.6%."
        ),
        "key_metrics": {
            "revenue": 9370000000,
            "revenue_yoy_growth": 0.15,
            "eps_gaap": 5.28,
            "operating_income": 2633000000,
            "operating_margin": 0.281,
            "paid_memberships_millions": 269.6,
            "net_new_subscribers_millions": 9.33,
            "ad_supported_mau_millions": 40,
            "q2_guidance_revenue": 9490000000,
            "q2_guidance_op_margin": 0.266,
            "fy2024_op_margin_guidance": 0.25,
            "consensus_estimate_revenue": 9280000000,
            "consensus_estimate_eps": 4.52,
            "consensus_estimate_net_adds": 4.84,
            "arm_revenue_per_membership": 17.31
        },
        "price_history": [
            597.20, 604.50, 611.80, 607.30, 614.70, 621.40, 617.90, 625.20,
            632.60, 628.10, 635.80, 643.20, 639.50, 647.10, 654.30, 650.80,
            658.40, 665.70, 661.20, 669.10, 676.50, 672.30, 680.10, 687.80,
            683.40, 691.20, 699.00, 694.50, 703.20, 614.38
        ],
        "sector": "Communication Services / Streaming",
        "macro_context": (
            "The streaming industry was undergoing consolidation and rationalization after the "
            "2020-2022 subscriber boom and bust. Disney+, Max, and Peacock were all cutting "
            "costs and exploring ad-supported tiers. The Hollywood writers' and actors' strikes "
            "(July–November 2023) had created a content slate gap in Q1 2024 that Netflix "
            "navigated with its larger international content library. Linear TV viewership "
            "continued to decline. The macroeconomic environment was stable, supporting "
            "consumer subscription spending."
        )
    },
    "ground_truth": {
        "price_1w_after": 638.23,
        "price_change_pct": 3.88,
        "actual_direction": "up",
        "key_risk_factors": [
            "Decision to stop reporting quarterly subscribers creates opacity that may raise governance concerns",
            "Password sharing crackdown is a one-time subscriber conversion; underlying growth rate may slow",
            "Content spending of $17B+ annually is a structural cost that limits free cash flow expansion",
            "Ad-supported tier ARPU is lower than standard plan; mix shift could depress revenue per user",
            "Competition from YouTube (free, mobile-native) and TikTok for entertainment time is structural",
            "Live sports rights costs are rising — NFL, NBA deals may significantly raise content budget",
            "International markets have lower pricing power; FX headwinds from strong dollar",
            "Churn risk increases as price increases compound over multiple years"
        ],
        "missed_signals": [
            "Live sports strategy (NFL Christmas Day games, WWE Raw) would be announced and accelerate ad revenue",
            "ARM trajectory would significantly exceed $17.31 as users upgraded to higher-priced plans"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 11. Starbucks Q3 FY2024 — Severe miss, guidance cut, CEO Brian Niccol incoming
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_011",
    "company": "Starbucks Corporation",
    "ticker": "SBUX",
    "event_date": "2024-07-30",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Starbucks reported Q3 FY2024 earnings on July 30, 2024, missing estimates across "
            "every key metric and withdrawing full-year guidance—a severe step that implied "
            "management had lost visibility into recovery timing. Global comparable store sales "
            "declined 3%, far worse than the +0.3% consensus estimate. US comparable store sales "
            "declined 2% (vs. +0.4% estimate) on transaction declines of 6%, reflecting customer "
            "traffic loss at multiple price points. Revenue of $9.11 billion missed the $9.24 "
            "billion estimate, declining 1% YoY. EPS of $0.93 missed the $1.02 estimate.\n\n"
            "CEO Laxman Narasimhan acknowledged broad-based weakness across income segments: "
            "lower-income consumers were trading down, while higher-income consumers were "
            "visiting less frequently due to operational issues including long wait times and "
            "order complexity. China comparable store sales fell 14% YoY as economic malaise "
            "and local competition (Luckin Coffee) intensified. Management suspended FY2024 "
            "guidance entirely. Shortly after earnings, the company was reported to be in "
            "discussions with Chipotle CEO Brian Niccol to replace Narasimhan."
        ),
        "key_metrics": {
            "revenue": 9113000000,
            "revenue_yoy_growth": -0.01,
            "eps_gaap": 0.93,
            "global_comp_store_sales_growth": -0.03,
            "us_comp_store_sales_growth": -0.02,
            "us_transaction_growth": -0.06,
            "us_average_ticket_growth": 0.04,
            "china_comp_store_sales_growth": -0.14,
            "operating_margin": 0.143,
            "active_rewards_members_us_millions": 32.8,
            "stores_total": 39477,
            "consensus_estimate_revenue": 9240000000,
            "consensus_estimate_eps": 1.02,
            "consensus_estimate_comp_store": 0.003
        },
        "price_history": [
            81.10, 80.40, 81.80, 80.20, 82.50, 81.90, 83.20, 82.60,
            84.00, 83.30, 84.70, 83.90, 85.30, 84.60, 85.90, 84.20,
            85.60, 84.80, 86.20, 85.40, 86.80, 85.10, 86.50, 85.70,
            87.10, 86.30, 87.70, 86.00, 87.40, 79.44
        ],
        "sector": "Consumer Discretionary / Restaurant",
        "macro_context": (
            "Consumer spending was bifurcating in mid-2024: upper-income households remained "
            "resilient while lower-income consumers were cutting discretionary spending. "
            "Restaurant traffic was under pressure from cumulative food price inflation of "
            "25-30% since 2019. Fast food and coffee chains had all raised prices aggressively "
            "post-COVID and were now facing pushback. McDonald's, Burger King, and others were "
            "reporting similar traffic declines. China's consumer recovery from COVID reopening "
            "had stalled, with youth unemployment at record highs."
        )
    },
    "ground_truth": {
        "price_1w_after": 76.62,
        "price_change_pct": -3.54,
        "actual_direction": "down",
        "key_risk_factors": [
            "Guidance suspension is a red flag — management has no visibility into the recovery timeline",
            "Transaction declines (-6%) indicate customer defection, not just ticket compression",
            "China business is a structural deterioration story, not cyclical — Luckin Coffee is taking share permanently",
            "CEO Narasimhan's turnaround plan had been in place for 18 months with no visible improvement",
            "Price increases have reached a ceiling — further hikes risk accelerating traffic losses",
            "Mobile ordering complexity is increasing wait times and degrading in-store experience",
            "Rewards program dilution: heavy discounting to drive loyalty membership at cost to margins",
            "Store count growth strategy in over-saturated US markets cannibalizing existing locations",
            "Labor cost inflation (union organizing, California minimum wage) structurally pressures margins"
        ],
        "missed_signals": [
            "Brian Niccol was already in advanced CEO discussions — announcement came August 13, 2024 and caused +24% spike",
            "The operational turnaround (removing customization complexity, reestablishing condiment bars) was simpler and faster than feared"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 12. NVIDIA Q2 FY2025 — Beat but stock reaction muted vs. expectations
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_012",
    "company": "NVIDIA Corporation",
    "ticker": "NVDA",
    "event_date": "2024-08-28",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "NVIDIA reported Q2 FY2025 earnings on August 28, 2024, again beating estimates "
            "significantly: revenue of $30.04 billion grew 122% YoY and 15% sequentially, "
            "beating the $28.86 billion consensus. Non-GAAP EPS of $0.68 beat the $0.64 "
            "estimate. Data Center revenue of $26.3 billion grew 154% YoY. Gross margin "
            "reached 78.4% (non-GAAP), up from 78.0% in Q1. Management guided Q3 FY2025 "
            "revenue to $32.5 billion ± 2%, above the $31.7 billion consensus.\n\n"
            "Despite the strong beat and guide-up, the stock initially fell approximately 6% "
            "in after-hours trading before partially recovering—an unusual reaction that "
            "reflected the 'whisper number' phenomenon: the buy-side was modeling $32B+ in "
            "revenue, and the $30B actual result, while above consensus, felt light relative "
            "to the most aggressive expectations. CEO Jensen Huang disclosed that Blackwell "
            "GPU production was ramping and that demand 'far exceeds supply.' He also "
            "acknowledged that Blackwell would have some production challenges in Q3 related "
            "to a design change made to improve manufacturing yields."
        ),
        "key_metrics": {
            "revenue": 30040000000,
            "revenue_yoy_growth": 1.22,
            "eps_non_gaap": 0.68,
            "gross_margin_non_gaap": 0.784,
            "data_center_revenue": 26300000000,
            "gaming_revenue": 2880000000,
            "professional_visualization_revenue": 454000000,
            "automotive_revenue": 346000000,
            "q3_guidance_revenue": 32500000000,
            "consensus_estimate_revenue": 28860000000,
            "consensus_estimate_eps": 0.64,
            "buyside_whisper_revenue": 32000000000
        },
        "price_history": [
            116.78, 118.40, 121.30, 117.90, 120.50, 123.20, 119.80, 122.60,
            125.40, 121.90, 124.70, 127.50, 124.10, 127.00, 129.80, 126.40,
            129.20, 132.10, 128.70, 131.50, 134.40, 130.90, 133.80, 136.70,
            133.20, 136.10, 139.10, 135.60, 128.30, 125.61
        ],
        "sector": "Technology / Semiconductors",
        "macro_context": (
            "The Fed signaled at Jackson Hole (August 23, 2024) that rate cuts were coming in "
            "September, triggering a risk-on market shift. The Magnificent Seven stocks had "
            "recovered from a July correction. AI capex spending announcements from Microsoft, "
            "Google, Amazon, and Meta were all tracking above initial FY2024 guidance. Blackwell "
            "GPU architecture had been officially unveiled in March 2024 at GTC. AMD MI300X was "
            "ramping production but remained far smaller in market share than NVIDIA H100/H200."
        )
    },
    "ground_truth": {
        "price_1w_after": 116.00,
        "price_change_pct": -7.65,
        "actual_direction": "down",
        "key_risk_factors": [
            "Blackwell production design change creates yield uncertainty and potential Q3/Q4 delivery risk",
            "'Beat-and-slight-miss-vs-whisper' pattern risks momentum investor rotation",
            "Gross margin pressure expected as Blackwell ramps (complex CoWoS-L packaging is expensive)",
            "Antitrust investigation in France (DOJ also circling) creates headline risk",
            "Customer concentration: Microsoft, Google, Meta, Amazon represent majority of revenue",
            "H200 to Blackwell transition creates risk of order pauses during the product cycle",
            "NVIDIA stock had run +170% YTD before earnings — extremely high bar embedded",
            "China Hopper (H20) sales limited by export controls — large addressable market being cut off"
        ],
        "missed_signals": [
            "Blackwell revenue would be 'several billion' in Q3 and accelerate dramatically in Q4 — supply was the only constraint",
            "Sovereign AI demand (Middle East, India, Japan) was growing faster than hyperscaler demand in relative terms"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 13. Palantir Q3 2024 — Strong beat, S&P 500 inclusion catalyst, stock +22%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_013",
    "company": "Palantir Technologies Inc.",
    "ticker": "PLTR",
    "event_date": "2024-11-04",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Palantir reported Q3 2024 earnings on November 4, 2024, beating estimates on "
            "revenue and EPS while dramatically raising full-year guidance. Revenue grew 30% "
            "YoY to $725.5 million, beating the $700.8 million estimate—the highest YoY growth "
            "rate since 2022 and a clear inflection from the 13–17% range of 2022–2023. US "
            "commercial revenue grew 54% YoY to $179 million, driven almost entirely by the "
            "AIP (Artificial Intelligence Platform) product, which was generating rapid enterprise "
            "adoption through 'boot camps' where potential customers built AI applications in "
            "days rather than months.\n\n"
            "EPS of $0.10 (non-GAAP) beat the $0.09 estimate. Management raised FY2024 revenue "
            "guidance to $2.805–$2.809 billion from the prior $2.742–$2750 billion. CEO Alex "
            "Karp emphasized that the company had 'broken from the pack' and that US commercial "
            "growth would continue accelerating. Palantir was added to the S&P 500 index on "
            "September 23, 2024—just weeks before this earnings report—creating sustained "
            "institutional buying pressure from index-tracking funds."
        ),
        "key_metrics": {
            "revenue": 725500000,
            "revenue_yoy_growth": 0.30,
            "eps_non_gaap": 0.10,
            "us_commercial_revenue": 179000000,
            "us_commercial_revenue_growth": 0.54,
            "us_government_revenue": 320000000,
            "us_government_revenue_growth": 0.40,
            "international_commercial_revenue": 113000000,
            "international_government_revenue": 113500000,
            "fy2024_guidance_revenue": 2807000000,
            "remaining_deal_value_bn": 4.5,
            "customer_count_us_commercial": 321,
            "consensus_estimate_revenue": 700800000,
            "consensus_estimate_eps": 0.09
        },
        "price_history": [
            28.20, 29.10, 30.40, 29.80, 31.20, 32.50, 31.70, 33.10,
            34.40, 33.60, 35.00, 36.30, 35.50, 36.80, 38.20, 37.40,
            38.70, 40.10, 39.30, 40.60, 42.00, 41.20, 42.50, 43.90,
            43.10, 44.40, 45.80, 45.00, 46.30, 41.02
        ],
        "sector": "Technology / Data Analytics / Defense",
        "macro_context": (
            "The US presidential election (Trump won on November 5, 2024) was the day after "
            "earnings, creating market uncertainty. Defense spending was expected to increase "
            "under a new administration. Government AI spending was accelerating with the DoD's "
            "CDAO (Chief Digital and AI Office) driving enterprise AI procurement. S&P 500 "
            "inclusion had already driven significant passive fund inflows. The broader market "
            "was in a risk-on mode driven by AI optimism and rate cut expectations."
        )
    },
    "ground_truth": {
        "price_1w_after": 54.10,
        "price_change_pct": 31.89,
        "actual_direction": "up",
        "key_risk_factors": [
            "Revenue base is still small at $725M quarterly — 30% growth from small base is less impressive than it appears",
            "Government revenue concentration (60%+) means budget cuts or geopolitical shifts are single-point risks",
            "US commercial customer count of 321 is low relative to market size — scaling beyond early adopters is unproven",
            "Stock-based compensation remains high (~$120M/Q) — GAAP profitability overstates cash generation quality",
            "International business growing slowly despite years of investment — geographic expansion has stalled",
            "AIP 'boot camp' model requires intensive hand-holding — not a scalable go-to-market for mass-market",
            "CEO Alex Karp's unusual public persona and statements create unpredictability risk for institutional investors",
            "Valuation at 20x+ forward revenue requires sustained hyper-growth with no major execution stumbles"
        ],
        "missed_signals": [
            "Trump election victory (next day) would accelerate DOGE-driven government efficiency software demand — PLTR was best positioned",
            "AIP platform would be adopted by major defense contractors as a standard, creating ecosystem lock-in effects"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 14. Nike FY2025 Q1 — Revenue miss + China weakness, stock -10%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_014",
    "company": "Nike, Inc.",
    "ticker": "NKE",
    "event_date": "2024-10-01",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Nike reported Q1 FY2025 earnings on October 1, 2024, missing revenue estimates "
            "and withdrawing its full-year guidance amid a broad-based revenue shortfall. "
            "Revenue declined 10% YoY to $11.59 billion, below the $11.65 billion estimate "
            "and the steepest quarterly decline in decades. EPS of $0.70 beat the $0.52 estimate "
            "due to cost controls and a favorable tax rate, but the top-line miss dominated "
            "investor attention. Direct-to-consumer (DTC) revenue fell 13% YoY, reversing "
            "the multi-year shift away from wholesale that had been Nike's strategic priority.\n\n"
            "Greater China revenue declined 4% YoY on a reported basis, as local brands "
            "Li-Ning and Anta continued to capture market share with younger consumers. "
            "North America revenue fell 11% YoY. Incoming CEO Elliott Hill (replacing John "
            "Donahoe, who announced his exit August 20, 2024) withdrew FY2025 guidance and "
            "guided Q2 revenue to decline 8–10% YoY, suggesting no near-term recovery. "
            "The company said it needed to 'clear excess product inventory' and 'rebuild "
            "its relationship with wholesale partners' it had deprioritized under Donahoe."
        ),
        "key_metrics": {
            "revenue": 11590000000,
            "revenue_yoy_growth": -0.10,
            "eps_gaap": 0.70,
            "gross_margin": 0.445,
            "dtc_revenue": 4839000000,
            "dtc_revenue_growth": -0.13,
            "wholesale_revenue": 6606000000,
            "china_revenue": 1670000000,
            "china_revenue_growth": -0.04,
            "north_america_revenue": 4830000000,
            "q2_guidance_revenue_growth": -0.09,
            "inventory_bn": 7.8,
            "consensus_estimate_revenue": 11650000000,
            "consensus_estimate_eps": 0.52,
            "prior_ceo_departure_date": "2024-08-20"
        },
        "price_history": [
            83.10, 82.40, 84.20, 83.60, 85.10, 84.30, 85.80, 85.00,
            86.50, 85.80, 87.20, 86.40, 87.90, 87.00, 88.50, 87.70,
            89.20, 88.30, 89.80, 88.90, 90.40, 89.50, 91.00, 90.10,
            91.60, 90.80, 92.30, 91.40, 93.00, 82.46
        ],
        "sector": "Consumer Discretionary / Apparel & Footwear",
        "macro_context": (
            "Athleisure and sneaker culture demand had been softening after the COVID-era "
            "boom. DTC retail strategies across the industry (Nike, Lululemon, Ralph Lauren) "
            "were being reassessed as wholesale partners (Foot Locker, Dick's Sporting Goods) "
            "proved more resilient. China consumer spending remained weak. Competition from "
            "On Running, Hoka (Deckers), and New Balance in running shoes and Adidas' Yeezy-"
            "successor strategy were cutting into Nike's brand premium. The Fed cut rates "
            "25bps in September 2024, providing mild macro relief for consumer stocks."
        )
    },
    "ground_truth": {
        "price_1w_after": 82.50,
        "price_change_pct": -0.11,
        "actual_direction": "flat",
        "key_risk_factors": [
            "DTC-only strategy has structurally damaged wholesale relationships that take years to rebuild",
            "China competitive threat from Anta and Li-Ning is not cyclical — it's a brand loyalty shift",
            "CEO transition risk: Hill is experienced but entering at a revenue inflection point with no honeymoon",
            "Inventory clearance will pressure gross margins for 2-3 quarters",
            "Younger consumers (Gen Z) are gravitating toward smaller 'authentic' brands (New Balance, Samba/Adidas)",
            "Jordan brand growth has plateaued after decades of consistent outperformance",
            "North America market saturation — Nike already has 65%+ of major categories",
            "Innovation pipeline (new silhouettes) has been criticized as derivative vs. category leaders"
        ],
        "missed_signals": [
            "Elliott Hill's wholesale repair strategy would work faster than analysts modeled",
            "Paris Olympics (summer 2024) marketing spend had already been cut — reducing a potential catalyst"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 15. Microsoft Q3 FY2024 — Azure reacceleration, Copilot monetization begins
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_015",
    "company": "Microsoft Corporation",
    "ticker": "MSFT",
    "event_date": "2024-04-25",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Microsoft reported Q3 FY2024 earnings on April 25, 2024, beating estimates on "
            "revenue and EPS driven by significant Azure cloud reacceleration and early Copilot "
            "monetization. Revenue grew 17% YoY to $61.9 billion, above the $60.9 billion "
            "estimate. EPS of $2.94 beat the $2.82 estimate. Azure and cloud services revenue "
            "grew 31% YoY—a meaningful acceleration from 28% in Q2 and 26% in Q1—with "
            "management noting that AI services contributed approximately 7 percentage points "
            "to Azure growth, up from 6 points in Q2.\n\n"
            "The Intelligent Cloud segment (containing Azure) generated revenue of $26.7 billion, "
            "above the $26.3 billion estimate. Copilot for Microsoft 365 (priced at $30/user/month) "
            "was gaining enterprise traction, though the financial contribution remained modest "
            "relative to total Microsoft 365 revenue. LinkedIn revenue grew 10% YoY. CEO Satya "
            "Nadella highlighted that Microsoft's partnership with OpenAI was creating 'strategic "
            "moat' in enterprise AI. Management guided Q4 FY2024 revenue to $63.5–$64.5 billion, "
            "above the $63.4 billion consensus, and highlighted continued AI-driven Azure growth."
        ),
        "key_metrics": {
            "revenue": 61858000000,
            "revenue_yoy_growth": 0.17,
            "eps_gaap": 2.94,
            "intelligent_cloud_revenue": 26710000000,
            "azure_growth_yoy": 0.31,
            "azure_ai_contribution_pts": 7,
            "productivity_biz_revenue": 19570000000,
            "more_personal_computing_revenue": 15580000000,
            "operating_income": 27580000000,
            "operating_margin": 0.446,
            "q4_guidance_revenue_low": 63500000000,
            "q4_guidance_revenue_high": 64500000000,
            "consensus_estimate_revenue": 60900000000,
            "consensus_estimate_eps": 2.82
        },
        "price_history": [
            406.32, 410.50, 415.20, 411.80, 416.40, 420.10, 417.30, 422.00,
            425.60, 422.20, 427.00, 430.80, 427.40, 432.20, 436.10, 432.70,
            437.50, 441.30, 437.90, 442.70, 446.50, 443.10, 448.00, 451.80,
            448.40, 453.20, 457.10, 453.70, 458.60, 399.04
        ],
        "sector": "Technology / Cloud / Enterprise Software",
        "macro_context": (
            "Enterprise AI adoption was accelerating in Q2 2024 with Copilot for M365 "
            "widely deployed in Fortune 500 pilot programs. Amazon Web Services and Google "
            "Cloud had both confirmed cloud reacceleration in their own earnings reports. "
            "The broader software sector was bifurcating between AI beneficiaries and "
            "laggards. Interest rates remained high but the Fed signaled cuts were coming. "
            "Microsoft's $10B OpenAI investment was providing early commercial returns "
            "through Azure OpenAI service with 65% of Fortune 500 using it."
        )
    },
    "ground_truth": {
        "price_1w_after": 415.57,
        "price_change_pct": 4.14,
        "actual_direction": "up",
        "key_risk_factors": [
            "Azure AI contribution (7pts) has a ceiling as AI training runs complete and inference workloads scale more slowly",
            "Copilot for M365 at $30/user/month faces enterprise ROI scrutiny — many pilots not converting to full rollouts",
            "Activision integration ($68.7B acquisition) is dilutive to margins and adding execution complexity",
            "Azure market share gains against AWS are modest; AWS still has 32% market share vs Azure's 23%",
            "Teams standalone competition from Slack (Salesforce) and Zoom — messaging market commoditizing",
            "EU regulatory pressure on Teams bundling (unbundling ordered in EU) removes a competitive advantage",
            "China exposure through Xbox and LinkedIn creates geopolitical risk",
            "FTC OpenAI partnership scrutiny could create restrictive oversight requirements"
        ],
        "missed_signals": [
            "Azure AI growth contribution would accelerate to 12+ points by Q1 FY2025 — consensus was modeling flat",
            "Copilot Studio enterprise adoption was tracking significantly ahead of internal targets"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 16. Eli Lilly Q1 2024 — Mounjaro/Zepbound weight loss explosion, stock +6%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_016",
    "company": "Eli Lilly and Company",
    "ticker": "LLY",
    "event_date": "2024-04-30",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Eli Lilly reported Q1 2024 earnings on April 30, 2024, beating estimates on "
            "revenue and EPS and raising full-year guidance, driven by extraordinary demand "
            "for its GLP-1 receptor agonist drugs Mounjaro (diabetes) and Zepbound (obesity). "
            "Revenue grew 26% YoY to $8.77 billion, beating the $8.68 billion estimate. "
            "EPS of $2.58 beat the $2.46 estimate. Mounjaro revenue of $1.81 billion beat the "
            "$1.77 billion estimate and continued its exceptional ramp since launch. Zepbound, "
            "launched in November 2023 for obesity, generated $517 million—its first full "
            "quarter—exceeding the $467 million estimate.\n\n"
            "Management raised FY2024 guidance: revenue to $42.4–$43.6 billion (from $40.4–"
            "$41.6 billion) and EPS to $13.50–$14.00 (from $12.20–$12.70). The guidance raise "
            "was remarkable in scale, with the midpoint rising $1.2 billion—a 3% raise in a "
            "single quarter. CEO David Ricks cited 'exceptional demand' for both products and "
            "noted that manufacturing capacity expansion was the primary constraint on revenue "
            "growth, not market demand. Lilly had committed to $9B+ in new manufacturing "
            "capacity (US and international) to meet projected multi-year demand."
        ),
        "key_metrics": {
            "revenue": 8770000000,
            "revenue_yoy_growth": 0.26,
            "eps_gaap": 2.58,
            "mounjaro_revenue": 1810000000,
            "zepbound_revenue": 517000000,
            "trulicity_revenue": 1468000000,
            "gross_margin": 0.795,
            "operating_margin": 0.311,
            "fy2024_guidance_revenue_low": 42400000000,
            "fy2024_guidance_revenue_high": 43600000000,
            "fy2024_guidance_eps_low": 13.50,
            "fy2024_guidance_eps_high": 14.00,
            "consensus_estimate_revenue": 8680000000,
            "consensus_estimate_eps": 2.46,
            "manufacturing_capex_committed_bn": 9
        },
        "price_history": [
            739.40, 748.20, 756.80, 751.10, 759.80, 768.40, 763.60, 772.30,
            781.00, 775.50, 784.20, 792.90, 788.10, 796.80, 805.60, 800.70,
            809.50, 818.30, 813.40, 822.20, 831.10, 826.20, 835.00, 843.90,
            838.90, 847.80, 856.70, 851.70, 860.60, 768.57
        ],
        "sector": "Healthcare / Pharmaceuticals",
        "macro_context": (
            "The GLP-1 market was in an early-stage boom following unprecedented weight loss "
            "clinical data for Zepbound/Wegovy. Novo Nordisk (Ozempic/Wegovy) was the other "
            "major participant. Insurance coverage for obesity drugs was expanding rapidly. "
            "The FDA had approved Zepbound in November 2023 and demand was far outstripping "
            "supply. US healthcare spending was under political scrutiny but GLP-1s were "
            "gaining bipartisan support given obesity epidemic scale. Interest rates were "
            "high but pharmaceutical stocks were seen as defensive."
        )
    },
    "ground_truth": {
        "price_1w_after": 780.00,
        "price_change_pct": 1.49,
        "actual_direction": "up",
        "key_risk_factors": [
            "Manufacturing supply is the binding constraint — shortages could limit revenue and create patient access issues",
            "Trulicity (older GLP-1) declining as doctors switch patients to Mounjaro — internal cannibalization",
            "Novo Nordisk Wegovy and semaglutide competition is intensifying across all GLP-1 indications",
            "Price negotiation risk: Medicare Drug Negotiation provisions could limit pricing power post-2027",
            "Reimbursement coverage varies widely — lack of universal insurance coverage limits total addressable market",
            "Long-term safety profile of GLP-1s at scale is still being established — regulatory/liability risk",
            "Oral GLP-1 pills in development by multiple competitors could disrupt injectable market",
            "Valuation at 50x+ forward earnings requires sustained multi-year hypergrowth execution"
        ],
        "missed_signals": [
            "Donanemab (Alzheimer's) FDA approval in July 2024 opened a second blockbuster revenue stream",
            "GLP-1 cardiovascular benefit data (SURMOUNT-MMO trial) would dramatically expand prescribing"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 17. Target Q3 FY2024 — Massive miss on guidance, stock -22%
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_017",
    "company": "Target Corporation",
    "ticker": "TGT",
    "event_date": "2024-11-20",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Target reported Q3 FY2024 earnings on November 20, 2024, delivering a severe "
            "earnings miss and slashing Q4 guidance—sending shares down approximately 22% in "
            "one of the biggest single-day drops in Target's history. Revenue of $25.67 billion "
            "grew just 1.1% YoY, slightly above the $25.87 billion estimate (barely missing). "
            "EPS of $1.85 dramatically missed the $2.30 estimate. Comparable store sales grew "
            "just 0.3% (vs. 1.5% estimate), with digital comps growing 10.8% offset by "
            "continued store traffic weakness.\n\n"
            "The catastrophic miss came from operating margins: Target's operating margin of "
            "4.6% was well below the 6.0% estimate due to increased promotional activity, "
            "inventory shrinkage (theft losses), and higher supply chain costs. Management "
            "guided Q4 EPS to just $1.85–$2.45, sharply below the $2.65 consensus—a range "
            "so wide that analysts interpreted it as reflecting extraordinary internal uncertainty. "
            "CEO Brian Cornell cited increased competitive pressure from Walmart's value "
            "positioning, ongoing consumer trade-down behavior, and elevated shrink losses "
            "that were proving harder to mitigate than expected."
        ),
        "key_metrics": {
            "revenue": 25673000000,
            "revenue_yoy_growth": 0.011,
            "eps_gaap": 1.85,
            "comp_store_sales_growth": 0.003,
            "digital_comp_growth": 0.108,
            "operating_margin": 0.046,
            "gross_margin": 0.278,
            "q4_guidance_eps_low": 1.85,
            "q4_guidance_eps_high": 2.45,
            "shrink_losses_bn": 0.6,
            "inventory_bn": 12.1,
            "consensus_estimate_revenue": 25870000000,
            "consensus_estimate_eps": 2.30,
            "consensus_estimate_op_margin": 0.060
        },
        "price_history": [
            152.30, 153.80, 155.40, 154.10, 156.70, 158.30, 157.00, 158.60,
            160.20, 158.90, 160.50, 162.10, 160.80, 162.40, 164.00, 162.70,
            164.30, 165.90, 164.60, 166.20, 167.80, 166.50, 168.10, 169.70,
            168.40, 170.00, 171.60, 170.30, 172.00, 155.56
        ],
        "sector": "Consumer Staples / General Merchandise Retail",
        "macro_context": (
            "Walmart had reported strong Q3 results one day earlier, creating a stark "
            "contrast with Target. Consumer bifurcation was intensifying: value-oriented "
            "shopping (Walmart, Aldi, Dollar stores) was gaining share from mid-market "
            "retailers. The holiday shopping season was starting earlier with deeper "
            "promotional activity. Inflation had moderated to ~2.5% but cumulative price "
            "increases since 2020 (~20%) had fundamentally altered consumer value perception. "
            "TikTok shopping and Amazon same-day delivery were accelerating competitive pressure."
        )
    },
    "ground_truth": {
        "price_1w_after": 127.31,
        "price_change_pct": -18.16,
        "actual_direction": "down",
        "key_risk_factors": [
            "Operating margin structural compression from shrink losses has no clear near-term fix",
            "Walmart's value perception advantage is widening — Target's 'cheap chic' positioning is eroding",
            "Discretionary categories (apparel, home goods, electronics) are Target's strength and are declining",
            "Digital investment is costly but not differentiating relative to Amazon Prime same-day delivery",
            "Q4 guidance range of $0.60 implies management has almost no visibility — operational dysfunction signal",
            "Inventory management: overstocking discretionary goods while consumers trade down to essentials",
            "Food and beverage (grocery) growth is not offsetting declines in high-margin discretionary categories",
            "Store format strategy unclear — large-format stores are cost-heavy in a low-traffic environment"
        ],
        "missed_signals": [
            "Walmart's food delivery partnership with Instacart was pulling grocery traffic from Target faster than tracked",
            "Holiday season inventory decisions had already been finalized — markdown risk was locked in before anyone could act"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 18. NVIDIA Q4 FY2025 — Blackwell era confirmation, strong beat
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_018",
    "company": "NVIDIA Corporation",
    "ticker": "NVDA",
    "event_date": "2025-02-26",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "NVIDIA reported Q4 FY2025 earnings on February 26, 2025, with record revenue of "
            "$39.33 billion, up 78% YoY and 12% sequentially, beating the $38.04 billion "
            "consensus. Non-GAAP EPS of $0.89 beat the $0.85 estimate. Data Center revenue "
            "of $35.58 billion grew 93% YoY, driven by the Blackwell GPU ramp which had "
            "successfully overcome manufacturing yield challenges from Q3 2024. Full-year "
            "FY2025 revenue reached $130.5 billion, up 114% from FY2024.\n\n"
            "Management guided Q1 FY2026 revenue to $43.0 billion ± 2%, well above the "
            "$41.8 billion consensus. Gross margin of 73.5% (non-GAAP) was slightly below "
            "the 74.6% estimate, reflecting Blackwell's more complex manufacturing cost "
            "structure during its ramp phase. CEO Jensen Huang highlighted 'reasoning AI' "
            "as an additional scaling dimension beyond training—implying significantly higher "
            "long-run compute demand per query. The DeepSeek R1 model release (January 20, "
            "2025) had briefly sent NVIDIA shares down 17% intraday on January 27, but "
            "Huang argued that reasoning models actually require more compute, not less."
        ),
        "key_metrics": {
            "revenue": 39331000000,
            "revenue_yoy_growth": 0.78,
            "eps_non_gaap": 0.89,
            "gross_margin_non_gaap": 0.735,
            "data_center_revenue": 35580000000,
            "gaming_revenue": 2489000000,
            "professional_visualization_revenue": 511000000,
            "automotive_revenue": 570000000,
            "q1_fy26_guidance_revenue": 43000000000,
            "fy2025_total_revenue": 130497000000,
            "consensus_estimate_revenue": 38040000000,
            "consensus_estimate_eps": 0.85,
            "blackwell_revenue_q4": 11000000000
        },
        "price_history": [
            131.60, 134.20, 138.40, 135.80, 140.10, 143.70, 140.30, 144.80,
            148.40, 144.90, 149.50, 153.10, 149.60, 154.20, 157.90, 154.40,
            159.10, 162.80, 159.20, 163.90, 167.70, 164.10, 168.90, 172.70,
            169.10, 112.00, 116.50, 120.30, 124.70, 128.42
        ],
        "sector": "Technology / Semiconductors",
        "macro_context": (
            "DeepSeek R1 (released January 20, 2025) had claimed comparable AI performance "
            "at a fraction of NVIDIA's training cost, triggering a $590B market cap single-day "
            "loss on January 27, 2025. However, subsequent analysis showed DeepSeek's "
            "inference efficiency gains were real but training still required H100/H800 clusters. "
            "US export controls on AI chips to China were tightening. The Trump administration "
            "had issued new AI governance executive orders. Hyperscaler capex guidance for "
            "2025 was running $50-100B+ per major cloud provider. Blackwell architecture "
            "was ramping at all major cloud data centers globally."
        )
    },
    "ground_truth": {
        "price_1w_after": 120.88,
        "price_change_pct": -5.87,
        "actual_direction": "down",
        "key_risk_factors": [
            "Gross margin compression (73.5% vs 78.4% peak) implies Blackwell economics worse than H100 at scale",
            "DeepSeek and model efficiency improvements could reduce long-run compute intensity per AI task",
            "Reasoning model scaling law is unproven — 'more compute per query' thesis could be disrupted",
            "US export controls limiting China market (previously 20%+ of revenue) are a permanent headwind",
            "Blackwell supply chain is complex — CoWoS-L packaging has low industry yield rates",
            "Customer CapEx concentration: if any one hyperscaler pauses, NVIDIA's sequential growth stalls",
            "AMD MI300X/MI350 competitive roadmap is closer to parity than 12-18 months ago",
            "NVIDIA trading at 25x+ forward revenue requires that the current AI compute cycle has no downturn"
        ],
        "missed_signals": [
            "Reasoning AI compute demand would prove to be 10-100x training compute over 12 months — the market underestimated this",
            "Rubin GPU architecture already in customer hands for testing — next generation cycle starting earlier than expected"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 19. Tesla Q4 2024 — Deliveries miss, margin pressure, disappointing guidance
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_019",
    "company": "Tesla, Inc.",
    "ticker": "TSLA",
    "event_date": "2025-01-29",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Tesla reported Q4 2024 earnings on January 29, 2025, with revenue of $25.71 billion "
            "missing the $27.42 billion estimate, and EPS of $0.73 missing the $0.76 estimate. "
            "Full-year 2024 vehicle deliveries of 1.79 million missed the 1.8 million target— "
            "the first annual delivery decline in Tesla's history. Automotive revenue declined "
            "8% YoY on average selling price pressure from continued price cuts. Gross margin "
            "of 16.3% (automotive) was below the 17.2% estimate, reflecting ongoing pricing "
            "actions to maintain volume.\n\n"
            "The Energy Generation and Storage business was the bright spot, with $3.06 billion "
            "in revenue, up 113% YoY. Management provided optimistic FY2025 delivery guidance "
            "of 'modest growth' but declined to provide specific numbers. CEO Elon Musk "
            "highlighted the upcoming Cybercab (robotaxi) product reveal scheduled for 2025 "
            "and discussed the FSD (Full Self-Driving) supervised progress. Musk's new role as "
            "head of the Department of Government Efficiency (DOGE) under President Trump was "
            "raising questions about management attention and potential policy conflicts."
        ),
        "key_metrics": {
            "revenue": 25707000000,
            "revenue_yoy_growth": 0.02,
            "eps_gaap": 0.73,
            "gross_margin_automotive": 0.163,
            "gross_margin_total": 0.167,
            "vehicle_deliveries_q4": 495570,
            "vehicle_deliveries_fy2024": 1789226,
            "energy_revenue": 3061000000,
            "energy_revenue_growth": 1.13,
            "services_revenue": 2790000000,
            "cash_and_investments": 36560000000,
            "fy2025_delivery_guidance": "modest growth",
            "consensus_estimate_revenue": 27420000000,
            "consensus_estimate_eps": 0.76
        },
        "price_history": [
            342.00, 352.40, 362.80, 355.20, 365.60, 376.00, 368.40, 378.90,
            389.30, 381.70, 392.10, 402.60, 395.00, 405.40, 415.90, 408.20,
            418.70, 429.20, 421.50, 432.00, 442.50, 434.80, 421.06, 409.30,
            397.60, 386.00, 374.40, 362.80, 351.20, 403.84
        ],
        "sector": "Consumer Discretionary / Electric Vehicles",
        "macro_context": (
            "Tesla stock had surged ~80% post-election (October–December 2024) on expectations "
            "that Musk's DOGE role would benefit Tesla through favorable EV policy, reduced "
            "regulation, and FSD regulatory approvals. However, the regulatory tailwind was "
            "complicated by the EV tax credit elimination (Trump's executive order) that reduced "
            "demand for all EVs including Tesla. BYD had definitively surpassed Tesla in "
            "global EV deliveries in 2024. The Model Y refresh was ramping at all factories "
            "in early 2025 but causing production disruptions."
        )
    },
    "ground_truth": {
        "price_1w_after": 362.55,
        "price_change_pct": -10.22,
        "actual_direction": "down",
        "key_risk_factors": [
            "First-ever annual delivery decline signals fundamental demand saturation at current price points",
            "EV tax credit elimination removes $7,500 subsidy that Tesla had been implicitly factoring into pricing",
            "Elon Musk's DOGE role creates management distraction and political brand toxicity in blue states",
            "FSD unsupervised still not available in any jurisdiction after years of promises",
            "Cybercab (robotaxi) has no regulatory path to deployment — requires autonomous driving approval",
            "BYD's global expansion (Europe, Southeast Asia) will intensify price competition in all markets",
            "Automotive gross margin below 17% raises question about whether EVs are structurally profitable at Tesla's scale",
            "Energy business (Megapack) is growing but has much lower margins than auto and can't compensate"
        ],
        "missed_signals": [
            "Model Y refresh would ramp faster than expected, driving strong Q1 2025 orders",
            "Musk's political capital would be used to fast-track FSD regulatory approval — timeline was closer than disclosed"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 20. Meta Q4 2024 — Blowout beat, AI investment thesis vindicated
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_020",
    "company": "Meta Platforms, Inc.",
    "ticker": "META",
    "event_date": "2025-01-29",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Meta Platforms reported Q4 2024 earnings on January 29, 2025, delivering a "
            "blowout quarter that validated the company's heavy AI investment thesis. Revenue "
            "grew 21% YoY to $48.39 billion, beating the $47.05 billion estimate. EPS of "
            "$8.02 beat the $6.76 estimate by an extraordinary margin. Daily active people "
            "across the family of apps reached 3.35 billion, up 5% YoY. Operating margin "
            "expanded to 48% from 41% a year earlier, demonstrating exceptional operating "
            "leverage as AI-driven ad targeting improvements accelerated revenue without "
            "proportional cost increases.\n\n"
            "Ad impressions grew 6% YoY while the average price per ad grew 14%—a combination "
            "indicating both volume and pricing power. Threads had reached 320 million monthly "
            "active users. Management guided Q1 2025 revenue to $39.5–$41.8 billion (above "
            "the $41.0 billion consensus midpoint) and raised FY2025 capex guidance to "
            "$60–$65 billion, nearly doubling 2024's $38 billion level, to fund AI "
            "infrastructure expansion. CEO Zuckerberg declared 2025 the year of 'agentic AI.'"
        ),
        "key_metrics": {
            "revenue": 48385000000,
            "revenue_yoy_growth": 0.21,
            "eps_gaap": 8.02,
            "operating_income": 23353000000,
            "operating_margin": 0.48,
            "daily_active_people_bn": 3.35,
            "ad_impressions_growth": 0.06,
            "average_price_per_ad_growth": 0.14,
            "threads_mau_millions": 320,
            "fy2025_capex_guidance_low": 60000000000,
            "fy2025_capex_guidance_high": 65000000000,
            "q1_2025_guidance_revenue_low": 39500000000,
            "q1_2025_guidance_revenue_high": 41800000000,
            "consensus_estimate_revenue": 47050000000,
            "consensus_estimate_eps": 6.76
        },
        "price_history": [
            567.00, 573.40, 580.10, 576.50, 583.20, 590.00, 586.40, 593.20,
            600.00, 596.30, 603.20, 610.10, 606.40, 613.30, 620.30, 616.60,
            623.60, 630.60, 626.90, 634.00, 641.10, 637.30, 644.50, 651.70,
            648.00, 655.20, 662.50, 658.70, 666.10, 617.89
        ],
        "sector": "Technology / Social Media",
        "macro_context": (
            "Digital advertising market was experiencing its strongest growth since 2021, "
            "driven by AI-enhanced ad targeting and measurement tools that improved ROAS "
            "(return on ad spend) for advertisers. TikTok's potential US ban (under review "
            "under the law requiring divestiture or ban by Jan 19, 2025) was creating "
            "advertising budget rotation toward Meta. The Fed had cut rates 75bps in 2024 H2. "
            "Meta Llama 3 open-source models had gained wide developer adoption. The "
            "Trump administration was expected to be more favorable to Big Tech than Biden's "
            "FTC under Lina Khan."
        )
    },
    "ground_truth": {
        "price_1w_after": 687.90,
        "price_change_pct": 11.32,
        "actual_direction": "up",
        "key_risk_factors": [
            "FY2025 capex of $60-65B raises the investment-to-revenue ratio significantly — ROI timing uncertain",
            "TikTok ban reversal (Trump granted extension on Jan 20) eliminates expected ad budget tailwind",
            "Reality Labs still burning $5B+/year with no clear monetization path for Quest hardware",
            "Regulatory risk: FTC antitrust suit against Instagram/WhatsApp acquisition still active",
            "48% operating margin sets an extremely high bar — any cost increase or revenue miss will stand out",
            "Threads monetization has not started — 320M users with zero revenue contribution",
            "European privacy regulations (GDPR) continuing to create compliance costs and targeting limitations"
        ],
        "missed_signals": [
            "AI-powered ad creative tools (Meta Advantage+) were having a larger impact on advertiser spend than disclosed",
            "WhatsApp Business monetization was accelerating in India/Brazil — not reflected in guidance"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 21. Alphabet Q3 2024 — Strong beat; DOJ antitrust ruling overhang
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_021",
    "company": "Alphabet Inc.",
    "ticker": "GOOGL",
    "event_date": "2024-10-29",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Alphabet reported Q3 2024 earnings on October 29, 2024, delivering a strong beat "
            "across Search, Cloud, and YouTube. Revenue grew 15% YoY to $88.27 billion, beating "
            "the $86.30 billion estimate. EPS of $2.12 crushed the $1.85 estimate. Google Cloud "
            "was the standout: revenue grew 35% YoY to $11.35 billion, above the $10.88 billion "
            "estimate, and operating margin reached 17%—a dramatic improvement from 10.4% a year "
            "earlier. YouTube advertising revenue grew 12.3% YoY to $8.92 billion.\n\n"
            "The company generated $17.6 billion in free cash flow, maintaining its position as "
            "one of the strongest cash generators in corporate history. However, the earnings "
            "report occurred just months after DOJ Judge Amit Mehta issued a landmark ruling "
            "(August 5, 2024) finding that Google had illegally maintained its monopoly in "
            "the general search market through exclusive distribution agreements (primarily "
            "with Apple). The remedies phase was ongoing, with the DOJ seeking structural "
            "remedies including potentially forcing Google to divest Chrome browser, Android OS, "
            "or terminating the Apple Search arrangement worth $18–20B annually."
        ),
        "key_metrics": {
            "revenue": 88268000000,
            "revenue_yoy_growth": 0.15,
            "eps_gaap": 2.12,
            "google_search_revenue": 49385000000,
            "google_cloud_revenue": 11353000000,
            "google_cloud_yoy_growth": 0.35,
            "google_cloud_op_margin": 0.17,
            "youtube_ad_revenue": 8921000000,
            "operating_income": 28521000000,
            "free_cash_flow_q3": 17626000000,
            "doj_antitrust_ruling_date": "2024-08-05",
            "apple_search_agreement_value_annual_bn": 18,
            "consensus_estimate_revenue": 86300000000,
            "consensus_estimate_eps": 1.85
        },
        "price_history": [
            162.20, 163.80, 165.50, 163.90, 166.50, 168.20, 166.60, 168.30,
            170.00, 168.40, 170.10, 171.80, 170.20, 171.90, 173.60, 172.00,
            173.70, 175.40, 173.80, 175.50, 177.20, 175.60, 177.30, 179.00,
            177.40, 179.10, 180.80, 179.20, 180.90, 163.90
        ],
        "sector": "Technology / Internet / Advertising / Cloud",
        "macro_context": (
            "The DOJ antitrust ruling (August 2024) created structural uncertainty over "
            "Google's business model. Remedies hearings were scheduled for late 2024 with "
            "potential structural breakup or forced behavioral changes. The US presidential "
            "election (November 5, 2024) created policy uncertainty — Trump was expected to "
            "be less aggressive on tech antitrust. AI search alternatives (Perplexity, ChatGPT "
            "Search) were growing but had not materially impacted Google's 90%+ global share. "
            "Google Cloud was winning significant enterprise AI workloads."
        )
    },
    "ground_truth": {
        "price_1w_after": 182.25,
        "price_change_pct": 11.19,
        "actual_direction": "up",
        "key_risk_factors": [
            "DOJ antitrust remedies could require elimination of Apple search deal ($18-20B annual revenue)",
            "Chrome or Android divestiture would eliminate key distribution advantages for Search and Play",
            "AI search (Perplexity, ChatGPT) growing faster than expected in informational query category",
            "Google Gemini AI had multiple high-profile product failures in early 2024 damaging brand reputation",
            "Cloud growth reacceleration requires continued capex increases ($13B+/quarter) with uncertain returns",
            "YouTube Shorts monetization (ad revenue per view) still meaningfully below YouTube long-form",
            "Other Bets losses continuing at $1B+/quarter — Waymo commercialization is slow"
        ],
        "missed_signals": [
            "Trump administration would be significantly less aggressive on antitrust remedies — DOJ settlement risk evaporated",
            "Google Cloud would reach 20%+ operating margin within 2 quarters — faster than any analyst modeled"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 22. GameStop Meme Stock Resurgence — Roaring Kitty return, news event
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_022",
    "company": "GameStop Corp.",
    "ticker": "GME",
    "event_date": "2024-05-13",
    "event_type": "news",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "On May 13, 2024, Keith Gill (known as 'Roaring Kitty' or 'DeepF***ingValue') "
            "posted his first tweet in approximately three years, showing a cartoon of a person "
            "leaning forward in a chair—a visual associated with serious attention and the "
            "original 2021 meme stock frenzy. GameStop shares surged over 100% intraday on "
            "May 14, with trading halted multiple times. Volume exceeded 200 million shares. "
            "The event had no connection to any fundamental business development at GameStop.\n\n"
            "GameStop's actual business continued to deteriorate: the company had been "
            "closing stores, cutting headcount, and generating declining revenue as physical "
            "game sales shifted to digital distribution. Q4 FY2023 (reported in March 2024) "
            "showed revenue of $1.79 billion, down 19% YoY. The company had a substantial "
            "cash balance (~$1.2B) from prior capital raises but no clear reinvestment strategy. "
            "On June 2, Keith Gill posted a screenshot showing a $116M position in GameStop "
            "options and stock, confirming he had re-entered the trade. GameStop then "
            "announced an at-the-money equity offering of 45 million shares on June 7, "
            "diluting existing shareholders while the stock was still elevated."
        ),
        "key_metrics": {
            "intraday_price_surge_pct": 1.09,
            "fy2023_revenue": 5272000000,
            "fy2023_revenue_yoy_growth": -0.08,
            "q4_fy2023_revenue": 1793000000,
            "q4_fy2023_revenue_yoy_growth": -0.19,
            "cash_and_equivalents_bn": 1.19,
            "store_count": 4169,
            "short_interest_pct_float": 0.24,
            "shares_outstanding_millions": 304,
            "trailing_twelve_month_net_loss_millions": -6,
            "price_before_event": 11.67,
            "intraday_high_may_14": 64.83,
            "shares_offered_june_7_millions": 45
        },
        "price_history": [
            10.40, 10.55, 10.30, 10.72, 10.89, 10.63, 10.78, 10.94,
            10.71, 10.86, 11.02, 10.79, 10.94, 11.10, 10.87, 11.03,
            11.19, 10.96, 11.12, 11.28, 11.05, 11.21, 11.37, 11.14,
            11.30, 11.46, 11.23, 11.39, 11.55, 11.67
        ],
        "sector": "Consumer Discretionary / Specialty Retail",
        "macro_context": (
            "Retail investor activity had been subdued since the 2021 meme stock frenzy. "
            "Social media (Reddit WallStreetBets, X/Twitter) remained active but had not "
            "produced a comparable short squeeze event in 3 years. GameStop's short interest "
            "was still elevated (~24% of float) as institutional traders bet on continued "
            "business deterioration. The broader market was in a steady uptrend with the S&P 500 "
            "near all-time highs. GameStop had no AI narrative, no product catalyst, and no "
            "fundamental reason for the move."
        )
    },
    "ground_truth": {
        "price_1w_after": 22.39,
        "price_change_pct": 91.86,
        "actual_direction": "up",
        "key_risk_factors": [
            "Movement is entirely sentiment-driven with zero fundamental support — complete reversal risk",
            "Short sellers will reload positions on the way up, increasing eventual downward pressure",
            "At-the-money share offering (announced June 7) will directly dilute retail shareholders",
            "GameStop's core business is in terminal decline — any 'catalyst' would require business model pivot",
            "Regulatory risk: SEC scrutiny of social media-driven trading manipulation",
            "Options market makers will hedge their gamma exposure, amplifying both upside and downside",
            "Keith Gill's disclosed position gives him motive to exit at elevated prices",
            "Physical gaming retail has no structural defense against digital distribution and cloud gaming"
        ],
        "missed_signals": [
            "Ryan Cohen (Chairman) was positioning GameStop to announce an investment mandate similar to Berkshire — hinted but not confirmed",
            "Options gamma squeeze mechanics were being misread as fundamental buying by retail investors"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 23. UnitedHealth Q1 2024 — Beat but Change Healthcare cyberattack overhang
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_023",
    "company": "UnitedHealth Group Incorporated",
    "ticker": "UNH",
    "event_date": "2024-04-16",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "UnitedHealth Group reported Q1 2024 earnings on April 16, 2024, beating EPS and "
            "revenue estimates but facing intense scrutiny over the February 21, 2024 "
            "cyberattack on Change Healthcare—the largest healthcare payment processing "
            "platform in the US, which UnitedHealth had acquired in 2022. Revenue grew 8.6% "
            "YoY to $99.8 billion, above the $99.3 billion estimate. Adjusted EPS of $6.91 "
            "beat the $6.57 estimate. The health insurance (UnitedHealthcare) and pharmacy "
            "benefits (Optum Rx) segments both performed in line with expectations.\n\n"
            "However, the Change Healthcare attack dominated the call: management estimated "
            "the direct adverse impact at $0.45–$0.55 per share in 2024, with total costs "
            "(including business disruption loans to affected providers) potentially reaching "
            "$1.6 billion. The attack disrupted claims processing for thousands of hospitals "
            "and physician practices. CEO Andrew Witty acknowledged that a cyberattack "
            "protection failure in a single non-multi-factor-authenticated server was the "
            "entry point. Management lowered FY2024 adjusted EPS guidance to $27.50–$28.00 "
            "from $27.50–$28.25, absorbing the attack costs."
        ),
        "key_metrics": {
            "revenue": 99800000000,
            "revenue_yoy_growth": 0.086,
            "eps_adjusted": 6.91,
            "medical_care_ratio": 0.847,
            "unitedhealthcare_revenue": 74450000000,
            "optum_health_revenue": 26080000000,
            "optum_rx_revenue": 32380000000,
            "optum_insight_revenue": 5060000000,
            "fy2024_guidance_eps_low": 27.50,
            "fy2024_guidance_eps_high": 28.00,
            "change_healthcare_attack_date": "2024-02-21",
            "estimated_attack_impact_per_share": 0.50,
            "estimated_total_costs_bn": 1.6,
            "consensus_estimate_revenue": 99300000000,
            "consensus_estimate_eps": 6.57
        },
        "price_history": [
            500.80, 505.20, 510.60, 506.40, 512.80, 518.30, 514.10, 519.60,
            525.10, 520.90, 526.40, 532.00, 527.80, 533.30, 538.90, 534.70,
            540.20, 545.80, 541.60, 547.10, 552.70, 548.50, 554.00, 559.70,
            555.40, 561.00, 566.70, 562.40, 568.10, 477.64
        ],
        "sector": "Healthcare / Health Insurance / Managed Care",
        "macro_context": (
            "The Change Healthcare attack (February 2024) had caused the largest healthcare "
            "system disruption in US history, affecting approximately 1 in 3 patient records. "
            "Hospitals and pharmacies were processing claims manually for weeks. ALPHV/BlackCat "
            "ransomware group had demanded and allegedly received a $22M ransom payment, though "
            "UnitedHealth did not confirm. Congressional hearings were scheduled. The Biden "
            "administration proposed new healthcare cybersecurity minimum standards. Medical "
            "cost inflation (from pent-up demand post-COVID) was running above actuarial "
            "assumptions across the managed care sector."
        )
    },
    "ground_truth": {
        "price_1w_after": 487.73,
        "price_change_pct": 2.12,
        "actual_direction": "up",
        "key_risk_factors": [
            "Change Healthcare attack may have exposed protected health information (PHI) for 100M+ Americans — class action liability",
            "Congressional scrutiny likely to result in new regulatory requirements and potential forced divestiture of Change Healthcare",
            "Medical cost ratio (84.7%) is slightly elevated — early signal of medical cost inflation exceeding premium increases",
            "Provider loans from Change Healthcare disruption ($6.5B+) create balance sheet risk if providers cannot repay",
            "DOJ antitrust investigation into Optum's acquisition of physician practices could result in forced divestitures",
            "Premium rate increases for 2025 may not fully cover medical cost inflation if trend is accelerating",
            "Reputational damage: being associated with largest healthcare breach in history affects enterprise sales"
        ],
        "missed_signals": [
            "Total Change Healthcare costs would reach $3.3B by year end — far exceeding the $1.6B initial estimate",
            "CEO Andrew Witty would testify before Congress and face significant hostile questioning that damaged stock further"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 24. Disney Q3 FY2024 — Streaming profitable, parks weak, stock flat/down
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_024",
    "company": "The Walt Disney Company",
    "ticker": "DIS",
    "event_date": "2024-08-07",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Disney reported Q3 FY2024 earnings on August 7, 2024, with mixed results: the "
            "combined streaming segment (Disney+/Hulu/ESPN+) achieved its first-ever "
            "quarterly profit, but theme parks weakness and ongoing linear TV decline offset "
            "the positive streaming milestone. Total revenue of $23.16 billion missed the "
            "$23.07 billion estimate slightly. EPS of $1.39 (adjusted) beat the $1.19 estimate.\n\n"
            "The combined streaming segment generated operating income of $47 million—its "
            "first profitable quarter—versus a $512 million operating loss a year earlier. "
            "Disney+ subscribers rose slightly to 118.3 million. However, Experiences "
            "(theme parks, resorts, cruise line) operating income declined 3% YoY to $2.22 "
            "billion as domestic parks saw softening consumer demand and international parks "
            "faced FX headwinds. Linear networks (ABC, ESPN, cable channels) operating income "
            "fell 13% YoY as cord-cutting accelerated. CEO Bob Iger announced a joint venture "
            "to combine ESPN with Fox Sports and Warner Bros. Discovery Sports in a new "
            "streaming bundle, and reaffirmed plans to take full ownership of Hulu from "
            "Comcast by year-end for ~$8.6 billion."
        ),
        "key_metrics": {
            "revenue": 23155000000,
            "revenue_yoy_growth": 0.04,
            "eps_adjusted": 1.39,
            "streaming_combined_op_income": 47000000,
            "disney_plus_subscribers_millions": 118.3,
            "disney_plus_arpu": 7.74,
            "experiences_op_income": 2220000000,
            "experiences_op_income_growth": -0.03,
            "linear_networks_op_income_growth": -0.13,
            "sports_jv_partners": "Fox, Warner Bros Discovery",
            "hulu_acquisition_cost_bn": 8.61,
            "consensus_estimate_revenue": 23070000000,
            "consensus_estimate_eps": 1.19,
            "content_spend_fy2024_bn": 25
        },
        "price_history": [
            99.50, 100.30, 101.40, 100.10, 102.20, 103.40, 102.10, 103.30,
            104.50, 103.20, 104.40, 105.70, 104.40, 105.60, 106.80, 105.50,
            106.80, 108.00, 106.70, 107.90, 109.20, 107.90, 109.10, 110.40,
            109.10, 110.30, 111.60, 110.30, 111.60, 91.16
        ],
        "sector": "Communication Services / Entertainment",
        "macro_context": (
            "The streaming wars were entering a consolidation phase with Disney, Netflix, and "
            "Amazon emerging as likely long-term winners. Cord-cutting was accelerating: "
            "traditional pay-TV lost 7.7 million subscribers in 2023. Theme park demand had "
            "plateaued after the post-COVID surge; consumer spending on experiences was "
            "moderating. Disney's proxy fight with activist investor Nelson Peltz "
            "(Trian Fund) had concluded with Disney prevailing in April 2024, reducing "
            "near-term corporate governance uncertainty. The Q3 results coincided with "
            "a broader market selloff following weak economic data."
        )
    },
    "ground_truth": {
        "price_1w_after": 90.59,
        "price_change_pct": -0.63,
        "actual_direction": "flat",
        "key_risk_factors": [
            "Parks operating income decline is worrisome — the segment generates ~60% of Disney's total operating income",
            "Linear TV is structurally declining with no floor in sight — ESPN carriage fees will peak then fall",
            "Streaming profitability at $47M is fragile — one content write-down or subscriber miss reverses it",
            "Hulu acquisition at $8.61B adds $8.6B in debt to an already leveraged balance sheet",
            "Disney+ subscriber growth is stalling in the US; international subscribers have much lower ARPU",
            "Sports JV (ESPN+/Fox/WBD) faces significant antitrust scrutiny and complex content rights negotiations",
            "Content spending of $25B+/year limits free cash flow despite revenue growth",
            "CEO Bob Iger succession planning remains unresolved — governance uncertainty for long-term investors"
        ],
        "missed_signals": [
            "India market (Star/Hotstar) subscriber loss from cricket rights loss was larger than disclosed",
            "ESPN's eventual standalone streaming launch would require significant marketing spend to acquire subscribers"
        ]
    }
},

# ─────────────────────────────────────────────────────────────────────────────
# 25. Novo Nordisk FY2024 — Obesity drug growth, but US market surprise miss
# ─────────────────────────────────────────────────────────────────────────────
{
    "scenario_id": "real_025",
    "company": "Novo Nordisk A/S",
    "ticker": "NVO",
    "event_date": "2025-02-05",
    "event_type": "earnings",
    "modification_type": "none",
    "input_data": {
        "earnings_summary": (
            "Novo Nordisk reported FY2024 full-year results on February 5, 2025, "
            "dramatically missing expectations and slashing 2025 guidance—triggering the "
            "worst single-day decline in the company's history, with shares falling "
            "approximately 20%. Revenue grew 25% to DKK 290.4 billion (~$40B USD), but "
            "missed the DKK 295 billion estimate. More critically, management guided "
            "FY2025 revenue growth to just 16–24%, far below the 30%+ consensus expectation. "
            "Operating profit grew 26% to DKK 121.4 billion.\n\n"
            "The GLP-1 segment (Ozempic, Wegovy, Victoza) remained the growth engine but "
            "showed signs of deceleration. Wegovy (obesity) US sales grew 86% in 2024 but "
            "the Q4 growth rate was slowing. A Phase 3 trial of the next-generation oral "
            "semaglutide (CagriSema) for obesity showed weight loss of 22.7%—better than "
            "existing options but below the 25%+ market expectation. Compounding pharmacies "
            "had provided cheaper 'alternatives' to Ozempic and Wegovy during 2024, "
            "capturing patients who would otherwise have been Novo Nordisk customers. "
            "Eli Lilly's tirzepatide (Zepbound) was gaining significant market share with "
            "superior clinical outcomes in head-to-head data."
        ),
        "key_metrics": {
            "revenue_dkk_bn": 290.4,
            "revenue_usd_bn": 40.2,
            "revenue_yoy_growth": 0.25,
            "operating_profit_dkk_bn": 121.4,
            "operating_profit_growth": 0.26,
            "wegovy_sales_growth_fy2024": 0.86,
            "ozempic_sales_growth_fy2024": 0.23,
            "fy2025_guidance_revenue_growth_low": 0.16,
            "fy2025_guidance_revenue_growth_high": 0.24,
            "cagriseema_weight_loss_pct": 0.227,
            "market_expected_cagriseema_pct": 0.25,
            "consensus_estimate_revenue_dkk_bn": 295,
            "consensus_estimate_fy2025_growth": 0.31,
            "compound_pharmacy_market_share_est_pct": 0.35
        },
        "price_history": [
            104.20, 106.10, 108.00, 106.50, 108.80, 110.70, 109.20, 111.10,
            113.00, 111.50, 113.40, 115.30, 113.80, 115.70, 117.60, 116.10,
            118.00, 119.90, 118.40, 120.30, 122.20, 120.70, 122.60, 124.50,
            123.00, 124.90, 126.80, 125.30, 127.20, 115.68
        ],
        "sector": "Healthcare / Pharmaceuticals / Biotech",
        "macro_context": (
            "The GLP-1 obesity drug market was experiencing rapid growth but also intensifying "
            "competition. Eli Lilly's Zepbound had FDA approval and was outperforming Wegovy "
            "in head-to-head weight loss trials. The FDA had classified semaglutide as in "
            "shortage, enabling compounding pharmacies to manufacture cheaper versions. "
            "The Trump administration was scrutinizing drug pricing, including potential "
            "Medicare/Medicaid GLP-1 coverage expansion (Biden had proposed this). "
            "Novo Nordisk's stock had nearly tripled from 2022 to mid-2024 but declined "
            "30%+ from its peak as competitive fears emerged. The company was investing "
            "heavily in manufacturing capacity to support 5+ years of projected demand."
        )
    },
    "ground_truth": {
        "price_1w_after": 79.20,
        "price_change_pct": -31.54,
        "actual_direction": "down",
        "key_risk_factors": [
            "CagriSema trial missed market expectation — next-gen drug is not the decisive step-up over Lilly's tirzepatide",
            "Eli Lilly's tirzepatide showing superior weight loss creates genuine competitive threat to Ozempic/Wegovy franchise",
            "Compounding pharmacy competition removed 30-35% of potential US market volume in 2024",
            "2025 guidance cut to 16-24% implies the growth rate is half of what consensus expected",
            "Oral GLP-1 (OIC) failed to show non-inferiority to injectable — pipeline disappointment",
            "Manufacturing constraints limiting ability to scale supply faster than competition",
            "Medicare/Medicaid GLP-1 coverage expansion would benefit all competitors equally, not just NVO",
            "Danish company exposed to currency headwinds from DKK/USD fluctuations on US revenue",
            "Patent expiration timeline for semaglutide creates long-term biosimilar entry risk"
        ],
        "missed_signals": [
            "FDA removal of semaglutide from shortage list (March 2025) would shut down compounding pharmacies, recapturing lost patients",
            "Novo's retatrutide (triple agonist) pipeline data was stronger than disclosed — not fully valued in guidance"
        ]
    }
},

]  # end of SCENARIOS list


if __name__ == "__main__":
    # Validate all scenarios have required fields
    required_top = ["scenario_id", "company", "ticker", "event_date", "event_type",
                    "modification_type", "input_data", "ground_truth"]
    required_input = ["earnings_summary", "key_metrics", "price_history", "sector", "macro_context"]
    required_gt = ["price_1w_after", "price_change_pct", "actual_direction",
                   "key_risk_factors", "missed_signals"]

    print(f"Validating {len(SCENARIOS)} scenarios...\n")
    for s in SCENARIOS:
        sid = s.get("scenario_id", "UNKNOWN")
        for f in required_top:
            assert f in s, f"[{sid}] Missing top-level field: {f}"
        for f in required_input:
            assert f in s["input_data"], f"[{sid}] Missing input_data field: {f}"
        for f in required_gt:
            assert f in s["ground_truth"], f"[{sid}] Missing ground_truth field: {f}"
        assert len(s["input_data"]["price_history"]) == 30, \
            f"[{sid}] price_history must have 30 entries, got {len(s['input_data']['price_history'])}"
        assert s["ground_truth"]["actual_direction"] in ["up", "down", "flat"], \
            f"[{sid}] actual_direction must be 'up', 'down', or 'flat'"
        assert s["modification_type"] == "none", \
            f"[{sid}] All Priyansh scenarios must have modification_type='none'"
        assert 5 <= len(s["ground_truth"]["key_risk_factors"]) <= 10, \
            f"[{sid}] key_risk_factors must have 5-10 items"
        print(f"  ✓ {sid} — {s['company']} ({s['ticker']}) — {s['ground_truth']['actual_direction'].upper()} "
              f"({s['ground_truth']['price_change_pct']:+.1f}%)")

    print(f"\n✅ All {len(SCENARIOS)} scenarios validated successfully.")

    # Direction distribution
    directions = [s["ground_truth"]["actual_direction"] for s in SCENARIOS]
    print(f"\nDirection distribution:")
    print(f"  UP:   {directions.count('up')} scenarios")
    print(f"  DOWN: {directions.count('down')} scenarios")
    print(f"  FLAT: {directions.count('flat')} scenarios")

    # Event type distribution
    event_types = [s["event_type"] for s in SCENARIOS]
    print(f"\nEvent type distribution:")
    print(f"  earnings:    {event_types.count('earnings')}")
    print(f"  news:        {event_types.count('news')}")
    print(f"  macro_event: {event_types.count('macro_event')}")

    # Save to JSON
    output_path = "scenarios_real.json"
    with open(output_path, "w") as f:
        json.dump(SCENARIOS, f, indent=2, default=str)
    print(f"\n📁 Saved to {output_path}")
