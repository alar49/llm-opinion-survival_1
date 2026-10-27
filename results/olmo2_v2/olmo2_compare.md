# OLMo 2 7B training stages, v2: stage comparisons (PLAN_OLMO2.md H4, H5, H6)

Runs: olmo2-7b-base-answer, olmo2-7b-sft-answer, olmo2-7b-dpo-answer, olmo2-7b-instruct-answer, olmo2-7b-base-myanswer, olmo2-7b-base-qa, olmo2-7b-base-theansweris. Stage comparisons use ending A (`\nAnswer:`), which all four stages share. 95% CIs from a cluster bootstrap over the 4 paraphrases (4000 reps, seed 7), one draw shared by every run, cell and item, so every contrast is paired. Equivalence uses the 90% CI (two one-sided tests at 5%).

## Format coverage (§3.4)

Missed share = uncaptured answer-like first-token probability / (answer mass + that probability), per row; median over the 34 issue statements × 4 paraphrases at the reference cell, rows with almost no answer-like probability (< 0.05) left out.

| run | median missed share | rows with a share | median answer mass M | median M + U | format |
|---|---|---|---|---|---|
| olmo2-7b-base-answer | 0.00 | 136/136 | 0.98 | 0.98 | captured |
| olmo2-7b-sft-answer | 0.00 | 136/136 | 0.95 | 0.95 | captured |
| olmo2-7b-dpo-answer | 0.00 | 136/136 | 1.00 | 1.00 | captured |
| olmo2-7b-instruct-answer | 0.00 | 136/136 | 1.00 | 1.00 | captured |
| olmo2-7b-base-myanswer | 0.00 | 136/136 | 0.98 | 0.98 | captured |
| olmo2-7b-base-qa | 0.00 | 136/136 | 0.99 | 0.99 | captured |
| olmo2-7b-base-theansweris | 0.04 | 82/136 | 0.06 | 0.06 | captured |

## Stage summary (ending A)

| quantity | base | SFT | DPO | Instruct |
|---|---|---|---|---|
| answer mass F1 (paper order) | 0.99 [0.98, 0.99] | 0.76 [0.71, 0.81] | 0.91 [0.87, 0.94] | 0.92 [0.89, 0.95] |
| answer mass F3 (paper order) | 0.97 [0.96, 0.98] | 0.94 [0.93, 0.96] | 0.99 [0.99, 1.00] | 1.00 [1.00, 1.00] |
| answer mass F5 (paper order) | 0.96 [0.95, 0.97] | 0.88 [0.86, 0.90] | 0.99 [0.98, 0.99] | 0.99 [0.99, 0.99] |
| median answer mass (reference) | 0.97 [0.96, 0.98] | 0.95 [0.94, 0.96] | 1.00 [0.99, 1.00] | 1.00 [1.00, 1.00] |
| No-opinion share (F2, offered last) | 0.11 [0.10, 0.11] | 0.07 [0.06, 0.07] | 0.03 [0.03, 0.04] | 0.02 [0.02, 0.02] |
| acquiescence: mean p_agree (reference) | 0.61 [0.59, 0.62] | 0.82 [0.82, 0.83] | 0.95 [0.94, 0.96] | 0.96 [0.95, 0.97] |
| anchor D (reference) | +0.37 [+0.35, +0.40] | +0.27 [+0.24, +0.32] | +0.25 [+0.22, +0.28] | +0.15 [+0.11, +0.18] |
| anchor C (reference) | +0.54 [+0.52, +0.57] | +0.68 [+0.59, +0.77] | +1.95 [+1.82, +2.09] | +1.92 [+1.77, +2.07] |
| mean |d| over 17 issues (reference) | 0.03 [0.03, 0.03] | 0.06 [0.06, 0.07] | 0.04 [0.03, 0.04] | 0.03 [0.02, 0.04] |
| issues called at the reference cell (R0 rule in d) | 0 | 3 | 2 | 0 |
| null axes called (2 or more flags the run) | 0 | 0 | 0 | 0 |

## H4 Stage effects on answering

**H4a** (answer mass at the reference cell does not fall SFT → DPO → Instruct; the Instruct − SFT CI above 0): **supported**.

| contrast | Δ mean answer mass [95% CI] |
|---|---|
| SFT → DPO | +0.05 [+0.04, +0.06] |
| DPO → Instruct | +0.00 [+0.00, +0.00] |
| SFT → Instruct | +0.06 [+0.04, +0.06] |

**H4b** (answer mass at F5 below F3, paper order, for every post-trained stage): **supported**. F5 − F3: base -0.01 [-0.02, -0.01]; SFT -0.06 [-0.08, -0.05]; DPO -0.01 [-0.01, -0.01]; Instruct -0.01 [-0.01, -0.00].

**H4c** (descriptive; deflecting decodes do not increase SFT → DPO → Instruct): [0, 0, 0] → holds.

| stage | decodes | number | label | deflection | other |
|---|---|---|---|---|---|
| base | 144 | 144 | 0 | 0 | 0 |
| SFT | 144 | 144 | 0 | 0 | 0 |
| DPO | 144 | 144 | 0 | 0 | 0 |
| Instruct | 144 | 144 | 0 | 0 | 0 |

## H5 Stated directions across stages

Primary cell set for {SFT, DPO, Instruct}: paper|positional|3|none (rule 1: every stage reads the reference cell). C at the reference cell: SFT +0.68 [+0.59, +0.77]; DPO +1.95 [+1.82, +2.09]; Instruct +1.92 [+1.77, +2.07].

**H5a** (SFT ≈ DPO ≈ Instruct in d_rel, margin ±0.2): **contradicted**. Supported needs ≥ 14/17 equivalent and no shift in each adjacent pair; contradicted = 2 or more issues different in either pair.

Equivalent / different / inconclusive issues (of 17), and shifts:

| stage pair | d_rel ±0.2 (primary) | d ±0.1 (sensitivity) | d ±0.05 (strict sensitivity) | d_LO ±0.4 (sensitivity) | Spearman ρ in d_rel | in d |
|---|---|---|---|---|---|---|
| SFT → DPO | 9 / 3 / 5; shifts: state_surveillance, energy, drugs, schools, transit, trans_sports | 17 / 0 / 0 | 12 / 3 / 2; shifts: drugs, voting, trans_sports | 8 / 8 / 1; shifts: state_surveillance, guns, minimum_wage, housing_zoning, drugs, transit, vaccines, voting, trans_sports | +0.93 [+0.90, +0.96] | +0.92 [+0.84, +0.93] |
| DPO → Instruct | 16 / 0 / 1 | 17 / 0 / 0 | 17 / 0 / 0 | 17 / 0 / 0 | +0.98 [+0.95, +0.98] | +0.97 [+0.93, +0.98] |
| SFT → Instruct | 10 / 2 / 5; shifts: state_surveillance, energy, trans_sports | 16 / 0 / 1; shifts: trans_sports | 11 / 3 / 3; shifts: energy, drugs, transit, voting, trans_sports | 5 / 8 / 4; shifts: state_surveillance, immigration, guns, housing_zoning, drugs, transit, vaccines, voting, trans_sports | +0.95 [+0.91, +0.98] | +0.87 [+0.78, +0.90] |

Bootstrap C on the cell set (d_rel's denominator): SFT +0.68 [+0.59, +0.77], min over reps 0.58; DPO +1.95 [+1.82, +2.09], min over reps 1.78; Instruct +1.92 [+1.77, +2.07], min over reps 1.72.

### Per issue on the primary cell set: d_rel, d, d_LO

| issue | SFT d_rel | DPO d_rel | Instruct d_rel | SFT d | DPO d | Instruct d | SFT d_LO | DPO d_LO | Instruct d_LO |
|---|---|---|---|---|---|---|---|---|---|
| property_tax | +0.07 [+0.00, +0.12] | -0.01 [-0.04, +0.03] | -0.08 [-0.12, -0.03] | +0.01 [+0.00, +0.01] | -0.00 [-0.00, +0.00] | -0.01 [-0.01, -0.00] | +0.05 [+0.00, +0.08] | -0.02 [-0.08, +0.05] | -0.15 [-0.24, -0.07] |
| agi_limitations | +0.08 [-0.07, +0.25] | +0.11 [+0.02, +0.23] | +0.22 [+0.11, +0.37] | +0.01 [-0.01, +0.03] | +0.02 [+0.00, +0.04] | +0.03 [+0.01, +0.05] | +0.05 [-0.05, +0.16] | +0.22 [+0.05, +0.44] | +0.43 [+0.23, +0.67] |
| abortion | +0.08 [+0.03, +0.13] | +0.05 [+0.01, +0.11] | +0.04 [-0.00, +0.08] | +0.01 [+0.00, +0.01] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.05 [+0.02, +0.08] | +0.10 [+0.01, +0.20] | +0.09 [-0.00, +0.16] |
| state_surveillance | -1.49 [-1.76, -1.25] | -1.07 [-1.14, -0.97] | -1.24 [-1.32, -1.12] | -0.13 [-0.14, -0.12] | -0.12 [-0.13, -0.10] | -0.08 [-0.10, -0.07] | -1.01 [-1.10, -0.90] | -2.09 [-2.17, -2.02] | -2.38 [-2.52, -2.29] |
| immigration | +0.18 [+0.13, +0.29] | +0.18 [+0.11, +0.24] | +0.32 [+0.25, +0.44] | +0.02 [+0.01, +0.02] | +0.01 [+0.00, +0.01] | +0.01 [+0.01, +0.01] | +0.13 [+0.09, +0.18] | +0.35 [+0.23, +0.46] | +0.62 [+0.49, +0.79] |
| guns | +0.68 [+0.58, +0.87] | +0.56 [+0.50, +0.66] | +0.73 [+0.65, +0.85] | +0.06 [+0.05, +0.07] | +0.02 [+0.02, +0.03] | +0.02 [+0.02, +0.03] | +0.46 [+0.37, +0.55] | +1.09 [+0.94, +1.26] | +1.39 [+1.17, +1.60] |
| minimum_wage | +0.54 [+0.40, +0.80] | +0.42 [+0.29, +0.59] | +0.37 [+0.26, +0.53] | +0.05 [+0.04, +0.07] | +0.04 [+0.03, +0.05] | +0.03 [+0.02, +0.04] | +0.37 [+0.28, +0.49] | +0.82 [+0.59, +1.11] | +0.71 [+0.49, +0.94] |
| energy | +1.06 [+0.90, +1.23] | +0.51 [+0.45, +0.57] | +0.56 [+0.47, +0.64] | +0.10 [+0.08, +0.11] | +0.05 [+0.04, +0.06] | +0.04 [+0.03, +0.05] | +0.72 [+0.65, +0.80] | +1.00 [+0.89, +1.10] | +1.07 [+0.94, +1.20] |
| housing_zoning | +0.49 [+0.44, +0.54] | +0.48 [+0.39, +0.57] | +0.50 [+0.42, +0.57] | +0.06 [+0.05, +0.06] | +0.04 [+0.03, +0.05] | +0.03 [+0.02, +0.04] | +0.33 [+0.32, +0.34] | +0.93 [+0.70, +1.12] | +0.96 [+0.75, +1.14] |
| drugs | +1.07 [+0.88, +1.32] | +0.80 [+0.69, +0.90] | +0.95 [+0.85, +1.06] | +0.08 [+0.07, +0.08] | +0.02 [+0.01, +0.03] | +0.02 [+0.01, +0.02] | +0.73 [+0.67, +0.78] | +1.56 [+1.41, +1.71] | +1.83 [+1.67, +1.99] |
| police_funding | +0.13 [+0.06, +0.19] | +0.08 [+0.02, +0.15] | +0.12 [+0.06, +0.19] | +0.00 [+0.00, +0.01] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.08 [+0.04, +0.14] | +0.16 [+0.04, +0.28] | +0.22 [+0.12, +0.35] |
| schools | +0.26 [+0.20, +0.32] | +0.01 [-0.01, +0.03] | +0.17 [+0.13, +0.22] | +0.01 [+0.01, +0.02] | +0.00 [-0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.18 [+0.14, +0.21] | +0.02 [-0.02, +0.06] | +0.33 [+0.26, +0.40] |
| transit | +1.15 [+0.94, +1.42] | +0.92 [+0.78, +1.08] | +1.03 [+0.89, +1.19] | +0.12 [+0.11, +0.14] | +0.08 [+0.05, +0.10] | +0.07 [+0.05, +0.09] | +0.78 [+0.70, +0.90] | +1.79 [+1.63, +2.02] | +1.98 [+1.81, +2.21] |
| vaccines | +0.78 [+0.67, +0.91] | +0.63 [+0.57, +0.69] | +0.81 [+0.73, +0.90] | +0.08 [+0.07, +0.09] | +0.04 [+0.03, +0.05] | +0.04 [+0.03, +0.05] | +0.53 [+0.46, +0.60] | +1.23 [+1.11, +1.35] | +1.56 [+1.43, +1.72] |
| unions | +0.17 [+0.09, +0.31] | +0.18 [+0.11, +0.23] | +0.12 [+0.03, +0.21] | +0.02 [+0.01, +0.03] | +0.01 [+0.01, +0.02] | +0.01 [+0.00, +0.01] | +0.12 [+0.07, +0.18] | +0.35 [+0.22, +0.44] | +0.24 [+0.06, +0.37] |
| voting | +0.99 [+0.88, +1.12] | +0.83 [+0.76, +0.90] | +0.97 [+0.89, +1.04] | +0.09 [+0.09, +0.09] | +0.03 [+0.02, +0.03] | +0.02 [+0.01, +0.02] | +0.67 [+0.65, +0.70] | +1.61 [+1.57, +1.65] | +1.85 [+1.80, +1.91] |
| trans_sports | +1.80 [+1.59, +2.07] | +1.39 [+1.21, +1.51] | +1.48 [+1.32, +1.57] | +0.20 [+0.18, +0.22] | +0.13 [+0.09, +0.17] | +0.09 [+0.06, +0.12] | +1.22 [+1.12, +1.33] | +2.72 [+2.53, +2.89] | +2.84 [+2.70, +3.04] |
| fair_month (null) | +0.08 [+0.04, +0.13] | +0.05 [+0.04, +0.07] | +0.08 [+0.05, +0.13] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.00 [+0.00, +0.00] | +0.05 [+0.03, +0.08] | +0.11 [+0.08, +0.14] | +0.15 [+0.09, +0.24] |
| sign_color (null) | -0.01 [-0.03, -0.00] | -0.01 [-0.03, +0.00] | -0.01 [-0.05, +0.02] | -0.00 [-0.00, -0.00] | -0.00 [-0.00, +0.00] | -0.00 [-0.00, +0.00] | -0.01 [-0.02, -0.00] | -0.02 [-0.06, +0.01] | -0.02 [-0.09, +0.03] |

### Δd_rel per issue: SFT → DPO (90% CI; E = equivalent, X = different, ? = inconclusive; † = shift)

| issue | Δd_rel [90% CI] | class | Δd [90% CI] | class (±0.10) |
|---|---|---|---|---|
| property_tax | -0.08 [-0.12, -0.05] | E | -0.007 [-0.008, -0.005] | E |
| agi_limitations | +0.03 [-0.05, +0.11] | E | +0.009 [+0.001, +0.016] | E |
| abortion | -0.03 [-0.07, +0.01] | E | -0.005 [-0.008, -0.003] | E |
| state_surveillance | +0.41 [+0.27, +0.59] | X † | +0.016 [+0.009, +0.024] | E |
| immigration | -0.00 [-0.08, +0.06] | E | -0.008 [-0.013, -0.002] | E |
| guns | -0.12 [-0.19, -0.07] | E | -0.038 [-0.044, -0.031] | E |
| minimum_wage | -0.12 [-0.17, -0.08] | E | -0.014 [-0.018, -0.010] | E |
| energy | -0.55 [-0.68, -0.46] | X † | -0.047 [-0.055, -0.039] | E |
| housing_zoning | -0.01 [-0.11, +0.10] | E | -0.017 [-0.026, -0.010] | E |
| drugs | -0.27 [-0.43, -0.14] | ? † | -0.055 [-0.059, -0.052] | E |
| police_funding | -0.04 [-0.13, +0.03] | E | -0.003 [-0.006, -0.001] | E |
| schools | -0.25 [-0.31, -0.19] | ? † | -0.015 [-0.018, -0.012] | E |
| transit | -0.23 [-0.36, -0.12] | ? † | -0.044 [-0.059, -0.028] | E |
| vaccines | -0.15 [-0.22, -0.08] | ? | -0.035 [-0.037, -0.032] | E |
| unions | +0.01 [-0.05, +0.06] | E | -0.005 [-0.010, +0.001] | E |
| voting | -0.16 [-0.24, -0.10] | ? | -0.064 [-0.070, -0.058] | E |
| trans_sports | -0.41 [-0.54, -0.30] | X † | -0.070 [-0.088, -0.053] | E |
| fair_month (null) | -0.02 [-0.05, +0.00] | E | -0.003 [-0.004, -0.001] | E |
| sign_color (null) | +0.00 [-0.02, +0.03] | E | +0.000 [-0.000, +0.001] | E |

### Δd_rel per issue: DPO → Instruct (90% CI; E = equivalent, X = different, ? = inconclusive; † = shift)

| issue | Δd_rel [90% CI] | class | Δd [90% CI] | class (±0.10) |
|---|---|---|---|---|
| property_tax | -0.07 [-0.09, -0.05] | E | -0.005 [-0.006, -0.003] | E |
| agi_limitations | +0.11 [+0.09, +0.13] | E | +0.010 [+0.010, +0.011] | E |
| abortion | -0.01 [-0.03, +0.01] | E | -0.001 [-0.002, +0.000] | E |
| state_surveillance | -0.17 [-0.18, -0.15] | E | +0.032 [+0.028, +0.037] | E |
| immigration | +0.14 [+0.10, +0.18] | E | +0.001 [+0.000, +0.003] | E |
| guns | +0.17 [+0.15, +0.19] | E | -0.001 [-0.001, -0.000] | E |
| minimum_wage | -0.05 [-0.08, -0.03] | E | -0.010 [-0.011, -0.009] | E |
| energy | +0.05 [+0.02, +0.08] | E | -0.008 [-0.011, -0.006] | E |
| housing_zoning | +0.02 [-0.01, +0.05] | E | -0.010 [-0.013, -0.006] | E |
| drugs | +0.15 [+0.14, +0.17] | E | -0.002 [-0.003, -0.001] | E |
| police_funding | +0.03 [+0.02, +0.05] | E | -0.000 [-0.001, -0.000] | E |
| schools | +0.16 [+0.14, +0.19] | E | +0.003 [+0.002, +0.003] | E |
| transit | +0.11 [+0.08, +0.15] | E | -0.009 [-0.014, -0.005] | E |
| vaccines | +0.18 [+0.14, +0.21] | ? | -0.000 [-0.004, +0.003] | E |
| unions | -0.05 [-0.08, -0.02] | E | -0.007 [-0.009, -0.005] | E |
| voting | +0.14 [+0.11, +0.17] | E | -0.009 [-0.011, -0.006] | E |
| trans_sports | +0.08 [+0.06, +0.11] | E | -0.038 [-0.048, -0.028] | E |
| fair_month (null) | +0.03 [+0.00, +0.05] | E | -0.000 [-0.000, +0.000] | E |
| sign_color (null) | +0.00 [-0.03, +0.03] | E | +0.000 [-0.000, +0.000] | E |

### Δd_rel per issue: SFT → Instruct (90% CI; E = equivalent, X = different, ? = inconclusive; † = shift)

| issue | Δd_rel [90% CI] | class | Δd [90% CI] | class (±0.10) |
|---|---|---|---|---|
| property_tax | -0.15 [-0.19, -0.12] | E | -0.011 [-0.013, -0.010] | E |
| agi_limitations | +0.14 [+0.07, +0.21] | ? | +0.019 [+0.012, +0.026] | E |
| abortion | -0.04 [-0.09, +0.02] | E | -0.006 [-0.008, -0.003] | E |
| state_surveillance | +0.25 [+0.11, +0.40] | ? † | +0.049 [+0.045, +0.053] | E |
| immigration | +0.14 [+0.10, +0.18] | E | -0.006 [-0.010, -0.002] | E |
| guns | +0.05 [-0.02, +0.10] | E | -0.038 [-0.045, -0.032] | E |
| minimum_wage | -0.18 [-0.23, -0.14] | ? | -0.024 [-0.029, -0.019] | E |
| energy | -0.51 [-0.60, -0.43] | X † | -0.055 [-0.061, -0.049] | E |
| housing_zoning | +0.01 [-0.09, +0.09] | E | -0.027 [-0.033, -0.023] | E |
| drugs | -0.12 [-0.29, +0.02] | ? | -0.057 [-0.060, -0.054] | E |
| police_funding | -0.01 [-0.10, +0.06] | E | -0.004 [-0.006, -0.002] | E |
| schools | -0.09 [-0.15, -0.02] | E | -0.012 [-0.015, -0.009] | E |
| transit | -0.12 [-0.23, -0.04] | ? | -0.054 [-0.067, -0.041] | E |
| vaccines | +0.04 [-0.02, +0.07] | E | -0.035 [-0.037, -0.033] | E |
| unions | -0.05 [-0.11, +0.01] | E | -0.012 [-0.018, -0.006] | E |
| voting | -0.02 [-0.11, +0.06] | E | -0.073 [-0.079, -0.069] | E |
| trans_sports | -0.32 [-0.49, -0.21] | X † | -0.108 [-0.116, -0.099] | ? † |
| fair_month (null) | +0.00 [-0.01, +0.01] | E | -0.003 [-0.004, -0.002] | E |
| sign_color (null) | +0.00 [-0.02, +0.03] | E | +0.000 [-0.000, +0.001] | E |

**H5b** (base vs SFT, Spearman ρ of the issue profiles in d_LO): **stance present before post-training**. Cells: paper|positional|3|none (rule 1: every stage reads the reference cell); ρ = +0.57 [+0.42, +0.64].

## H6 The "No opinion" option (F2, paper order)

Holds if the 95% CI upper end of (substantive mass without the option − with it) is below 0.10 and the conditional d with and without the option is equivalent within ±0.10 for at least 14 of 17 issues.

| stage | substantive mass without − with [95% CI] | d equivalent / different / inconclusive | decision |
|---|---|---|---|
| base | +0.11 [+0.11, +0.12] | 17 / 0 / 0 | does not hold |
| SFT | +0.06 [+0.05, +0.06] | 17 / 0 / 0 | holds |
| DPO | +0.03 [+0.02, +0.03] | 17 / 0 / 0 | holds |
| Instruct | +0.02 [+0.02, +0.02] | 17 / 0 / 0 | holds |
