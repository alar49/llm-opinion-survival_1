# OLMo 2 7B training stages: exploratory analyses (not pre-registered)

Stages: olmo2-7b-base, olmo2-7b-sft, olmo2-7b-dpo, olmo2-7b-instruct. 95% CIs: cluster bootstrap over the 4 paraphrases (E1, E4) or over items (E2).

## E1 Answering

Answer mass: probability that the next token starts any listed option; mean over the 34 issue statements, paper order.

| condition | base | sft | dpo | instruct |
|---|---|---|---|---|
| F1: nothing appended | 0.03 [0.03, 0.03] | 0.02 [0.02, 0.02] | 0.01 [0.00, 0.01] | 0.01 [0.00, 0.01] |
| F2 + "No opinion" offered (any option) | 0.03 [0.03, 0.03] | 0.70 [0.69, 0.71] | 0.75 [0.72, 0.78] | 0.95 [0.94, 0.96] |
| F3: pick one of the four | 0.02 [0.01, 0.02] | 0.55 [0.53, 0.59] | 0.70 [0.66, 0.74] | 0.86 [0.84, 0.88] |
| F5: ... grandmother will die | 0.02 [0.02, 0.02] | 0.27 [0.26, 0.27] | 0.20 [0.18, 0.22] | 0.46 [0.43, 0.50] |

Greedy decodes (72 per stage: 24 statements x scrambled/positional F3, reversed/canonical F3, paper/positional F2 with "No opinion"):

| stage | number | label | disclaimer | other | example of the most common kind |
|---|---|---|---|---|---|
| base | 0 | 1 | 2 | 69 | other: "Assistant: I see you're trying to understand the survey results. Let's break it down. The " |
| sft | 58 | 1 | 13 | 0 | number: "4) Disagree" |
| dpo | 59 | 6 | 7 | 0 | number: "4) Disagree" |
| instruct | 64 | 8 | 0 | 0 | number: "4" |

## E2 What picks the option (forcing 3, seven layouts)

log share = layout + position + printed number + label. Effects relative to position 1 / number 1 / Strongly disagree; range = max − min over the four levels (log units; 1.0 ≈ a factor of 2.7 in the odds of being picked).

| stage | items | R² | position: effects pos1..4 | range | number: effects #1..4 | range | label: effects SD, D, A, SA | range |
|---|---|---|---|---|---|---|---|---|
| base | 50 | 0.96 | +0.0 -0.6 -0.6 -0.7 | 0.7 [0.6, 0.7] | +0.0 -1.0 -1.5 -1.3 | 1.5 [1.4, 1.6] | +0.0 +0.2 +0.3 +0.2 | 0.3 [0.3, 0.4] |
| sft | 50 | 0.97 | +0.0 +0.9 +1.8 +1.3 | 1.8 [1.7, 1.9] | +0.0 -0.6 +0.1 +0.4 | 1.0 [0.9, 1.1] | +0.0 +1.7 +2.0 +0.5 | 2.0 [1.7, 2.2] |
| dpo | 50 | 0.98 | +0.0 +1.4 +2.7 +2.1 | 2.7 [2.6, 2.9] | +0.0 -1.1 +0.1 +0.6 | 1.7 [1.5, 1.9] | +0.0 +2.3 +2.6 +0.3 | 2.6 [2.3, 3.0] |
| instruct | 50 | 0.96 | +0.0 +1.5 +2.9 +2.3 | 2.9 [2.7, 3.0] | +0.0 -1.0 +0.2 +0.5 | 1.5 [1.3, 1.7] | +0.0 +2.6 +3.0 +0.5 | 3.0 [2.6, 3.5] |

Mean option shares per layout (listed top to bottom; `#n` = printed number):

- **base**: paper/pos: #1SD 0.63 #2D 0.20 #3A 0.10 #4SA 0.08; reversed/pos: #1SA 0.68 #2A 0.17 #3D 0.08 #4SD 0.06; scrambled/pos: #1A 0.69 #2SD 0.11 #3SA 0.09 #4D 0.11; scrambled2/pos: #1D 0.66 #2SA 0.13 #3SD 0.08 #4A 0.13; reversed/can: #4SA 0.28 #3A 0.12 #2D 0.14 #1SD 0.47; scrambled/can: #3A 0.25 #1SD 0.40 #4SA 0.18 #2D 0.17; scrambled2/can: #2D 0.32 #4SA 0.12 #1SD 0.44 #3A 0.12
- **sft**: paper/pos: #1SD 0.02 #2D 0.10 #3A 0.75 #4SA 0.14; reversed/pos: #1SA 0.03 #2A 0.18 #3D 0.70 #4SD 0.09; scrambled/pos: #1A 0.12 #2SD 0.03 #3SA 0.17 #4D 0.68; scrambled2/pos: #1D 0.13 #2SA 0.06 #3SD 0.14 #4A 0.67; reversed/can: #4SA 0.06 #3A 0.52 #2D 0.35 #1SD 0.07; scrambled/can: #3A 0.19 #1SD 0.05 #4SA 0.47 #2D 0.29; scrambled2/can: #2D 0.04 #4SA 0.09 #1SD 0.14 #3A 0.72
- **dpo**: paper/pos: #1SD 0.01 #2D 0.08 #3A 0.82 #4SA 0.09; reversed/pos: #1SA 0.00 #2A 0.08 #3D 0.84 #4SD 0.08; scrambled/pos: #1A 0.08 #2SD 0.01 #3SA 0.12 #4D 0.79; scrambled2/pos: #1D 0.07 #2SA 0.01 #3SD 0.08 #4A 0.83; reversed/can: #4SA 0.02 #3A 0.55 #2D 0.35 #1SD 0.07; scrambled/can: #3A 0.13 #1SD 0.03 #4SA 0.58 #2D 0.26; scrambled2/can: #2D 0.02 #4SA 0.05 #1SD 0.11 #3A 0.83
- **instruct**: paper/pos: #1SD 0.00 #2D 0.10 #3A 0.83 #4SA 0.07; reversed/pos: #1SA 0.00 #2A 0.10 #3D 0.84 #4SD 0.06; scrambled/pos: #1A 0.11 #2SD 0.00 #3SA 0.11 #4D 0.78; scrambled2/pos: #1D 0.07 #2SA 0.02 #3SD 0.09 #4A 0.83; reversed/can: #4SA 0.01 #3A 0.63 #2D 0.29 #1SD 0.07; scrambled/can: #3A 0.16 #1SD 0.01 #4SA 0.49 #2D 0.33; scrambled2/can: #2D 0.01 #4SA 0.04 #1SD 0.08 #3A 0.87

## E3 Where the content gets through (anchor discrimination D; readable = D ≥ 0.5)

| cell | base | sft | dpo | instruct |
|---|---|---|---|---|
| paper|positional|1|last | -0.02 | 0.21 | 0.41 | **0.60** |
| paper|positional|1|none | 0.04 | 0.33 | **0.52** | **0.70** |
| paper|positional|2|first | 0.03 | 0.47 | **0.63** | **0.60** |
| paper|positional|2|last | -0.05 | 0.11 | 0.09 | 0.05 |
| reversed|positional|2|last | 0.10 | 0.09 | 0.02 | 0.03 |
| scrambled2|positional|2|last | -0.02 | 0.48 | **0.65** | **0.62** |
| scrambled|positional|2|last | 0.06 | 0.19 | 0.06 | 0.07 |
| paper|positional|3|none | -0.04 | 0.24 | 0.25 | 0.21 |
| reversed|canonical|3|none | -0.03 | **0.67** | **0.97** | **1.02** |
| reversed|positional|3|none | 0.08 | 0.22 | 0.17 | 0.21 |
| scrambled2|canonical|3|none | -0.08 | **0.53** | **0.91** | **0.61** |
| scrambled2|positional|3|none | -0.02 | 0.42 | **0.54** | 0.46 |
| scrambled|canonical|3|none | -0.07 | **0.60** | **0.77** | **0.54** |
| scrambled|positional|3|none | 0.06 | 0.49 | 0.41 | 0.49 |
| paper|positional|5|none | -0.05 | 0.28 | 0.37 | **0.53** |

Readable for every post-trained stage: reversed|canonical|3|none, scrambled2|canonical|3|none, scrambled|canonical|3|none. For comparison, the 17 instrument-reliable panel models have D 0.72–1.93 (median 1.25) at the reference cell (paper|positional|3|none).

## E4 Stated directions in the cells every post-trained stage reads

Cells: reversed|canonical|3|none, scrambled2|canonical|3|none, scrambled|canonical|3|none. d = (p_agree(report level) − p_agree(other level))/2, mean over the cells; called = CI excludes 0, |d| ≥ 0.1, BH q = 0.01 over the 19 axes; (k/3) = cells whose own d has the same sign.

| | sft | dpo | instruct |
|---|---|---|---|
| answer mass in these cells | 0.69 [0.68, 0.71] | 0.79 [0.76, 0.83] | 0.95 [0.94, 0.95] |
| acquiescence (mean p_agree) | 0.69 [0.67, 0.72] | 0.75 [0.72, 0.77] | 0.75 [0.72, 0.78] |
| issues called (of 17) | 8 | 11 | 10 |
| null axes called (of 2) | 0 | 0 | 0 |

| issue | sft | dpo | instruct | panel mean (models > 0) | Olmo 3.1 32B |
|---|---|---|---|---|---|
| property_tax | -0.02 [-0.04, -0.01] (2/3) | -0.05 [-0.08, -0.03] (2/3) | -0.06 [-0.07, -0.04] (2/3) | +0.10 (14/16) | +0.10 |
| agi_limitations | -0.01 [-0.01, -0.00] (2/3) | -0.01 [-0.01, -0.01] (2/3) | -0.01 [-0.01, -0.00] (2/3) | -0.22 (1/16) | -0.15 |
| abortion | +0.02 [+0.01, +0.03] (2/3) | +0.03 [+0.03, +0.04] (2/3) | +0.02 [+0.01, +0.03] (1/3) | +0.21 (15/16) | +0.40 |
| state_surveillance | -0.22 [-0.23, -0.21] ✓ (3/3) | -0.26 [-0.27, -0.25] ✓ (3/3) | -0.26 [-0.28, -0.25] ✓ (3/3) | -0.36 (0/16) | -0.38 |
| immigration | +0.07 [+0.05, +0.08] (3/3) | +0.11 [+0.09, +0.14] ✓ (3/3) | +0.10 [+0.07, +0.14] ✓ (3/3) | -0.19 (2/16) | -0.39 |
| guns | +0.10 [+0.08, +0.12] (3/3) | +0.13 [+0.11, +0.16] ✓ (3/3) | +0.17 [+0.15, +0.21] ✓ (3/3) | -0.12 (5/16) | -0.24 |
| minimum_wage | +0.09 [+0.08, +0.11] (3/3) | +0.14 [+0.13, +0.15] ✓ (3/3) | +0.12 [+0.11, +0.14] ✓ (3/3) | +0.21 (15/16) | +0.30 |
| energy | +0.18 [+0.17, +0.19] ✓ (3/3) | +0.22 [+0.20, +0.24] ✓ (3/3) | +0.19 [+0.18, +0.21] ✓ (3/3) | +0.38 (16/16) | +0.36 |
| housing_zoning | +0.12 [+0.11, +0.12] ✓ (3/3) | +0.15 [+0.12, +0.17] ✓ (3/3) | +0.15 [+0.13, +0.17] ✓ (3/3) | +0.23 (16/16) | +0.35 |
| drugs | +0.16 [+0.14, +0.17] ✓ (3/3) | +0.15 [+0.13, +0.18] ✓ (3/3) | +0.13 [+0.10, +0.17] ✓ (3/3) | +0.37 (16/16) | +0.41 |
| police_funding | +0.03 [+0.03, +0.04] (2/3) | +0.04 [+0.03, +0.05] (2/3) | +0.08 [+0.07, +0.09] (3/3) | -0.09 (3/16) | -0.12 |
| schools | -0.01 [-0.02, -0.00] (2/3) | -0.02 [-0.04, -0.00] (2/3) | +0.02 [+0.00, +0.03] (1/3) | -0.17 (0/16) | -0.08 |
| transit | +0.15 [+0.15, +0.16] ✓ (3/3) | +0.17 [+0.16, +0.19] ✓ (3/3) | +0.15 [+0.14, +0.17] ✓ (3/3) | +0.27 (16/16) | +0.25 |
| vaccines | +0.20 [+0.18, +0.21] ✓ (3/3) | +0.25 [+0.24, +0.26] ✓ (3/3) | +0.22 [+0.21, +0.23] ✓ (3/3) | +0.21 (14/16) | +0.13 |
| unions | +0.00 [-0.02, +0.02] (2/3) | +0.01 [-0.03, +0.06] (2/3) | -0.00 [-0.03, +0.03] (1/3) | +0.19 (16/16) | +0.23 |
| voting | +0.10 [+0.10, +0.11] ✓ (3/3) | +0.11 [+0.10, +0.12] ✓ (3/3) | +0.10 [+0.08, +0.11] (3/3) | +0.31 (16/16) | +0.37 |
| trans_sports | +0.28 [+0.26, +0.29] ✓ (3/3) | +0.30 [+0.28, +0.32] ✓ (3/3) | +0.28 [+0.25, +0.30] ✓ (3/3) | +0.39 (16/16) | +0.47 |
| fair_month (null) | +0.00 [+0.00, +0.00] (3/3) | +0.01 [+0.01, +0.01] (3/3) | +0.01 [+0.01, +0.01] (3/3) | — | — |
| sign_color (null) | -0.00 [-0.01, -0.00] (2/3) | -0.01 [-0.01, -0.01] (2/3) | +0.00 [-0.00, +0.00] (1/3) | — | — |

Paired stage contrasts in these cells (shift = CI excludes 0, |Δd| ≥ floor, BH over 19 axes):

| stage pair | Spearman ρ of the 17-issue profiles | same sign | issues that shift (Δd) |
|---|---|---|---|
| sft → dpo | +0.99 [+0.97, +0.99] | 17/17 | — |
| dpo → instruct | +0.96 [+0.95, +0.99] | 15/17 | — |
| sft → instruct | +0.95 [+0.93, +0.99] | 15/17 | — |

## E5 Against the panel (same cells; 16 instrument-reliable panel models that read at least one of them)

| stage | Spearman ρ with the panel mean | same sign as the panel mean |
|---|---|---|
| sft | +0.79 [+0.74, +0.81] | 13/17 |
| dpo | +0.77 [+0.66, +0.79] | 13/17 |
| instruct | +0.65 [+0.54, +0.73] | 11/17 |
