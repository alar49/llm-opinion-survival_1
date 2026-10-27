# OLMo 2 7B training stages, v2: answering, layout and content (PLAN_OLMO2.md H1, H2, H3)

Runs: olmo2-7b-base-answer, olmo2-7b-sft-answer, olmo2-7b-dpo-answer, olmo2-7b-instruct-answer, olmo2-7b-base-myanswer, olmo2-7b-base-qa, olmo2-7b-base-theansweris. 95% CIs: cluster bootstrap over the 4 paraphrases (as in olmo2_compare.md), or over items for the layout decomposition. Answer mass = probability that the continuation starts with one of the listed options' answer strings; C = anchor content effect in log-odds; D = anchor discrimination in score units.

## H1 The base model in the completion format

**H1a** (answering, ending A: median answer mass at the reference cell ≥ 0.5): **supported**; median answer mass 0.97 [0.96, 0.98].

**H1b** (reading, ending A: C ≥ 0.5 with CI above 0): **reads**; C +0.54 [+0.52, +0.57], D +0.37 [+0.35, +0.40].

**H1c** (endings, base model; expectation A ≈ C ≥ B > D in answer mass):

| ending | run | median answer mass | mean answer mass | D | C | reads | median missed share | format |
|---|---|---|---|---|---|---|---|---|
| A | olmo2-7b-base-answer | 0.97 [0.96, 0.98] | 0.97 [0.96, 0.98] | +0.37 [+0.35, +0.40] | +0.54 [+0.52, +0.57] | reads | 0.00 | captured |
| B | olmo2-7b-base-myanswer | 0.98 [0.97, 0.98] | 0.98 [0.97, 0.98] | +0.43 [+0.40, +0.46] | +0.58 [+0.56, +0.61] | reads | 0.00 | captured |
| C | olmo2-7b-base-qa | 0.99 [0.98, 0.99] | 0.99 [0.98, 0.99] | +0.47 [+0.44, +0.50] | +0.71 [+0.66, +0.77] | reads | 0.00 | captured |
| D | olmo2-7b-base-theansweris | 0.07 [0.04, 0.10] | 0.07 [0.04, 0.10] | +0.25 [+0.19, +0.31] | +0.34 [+0.25, +0.41] | weak | 0.04 | captured |

## H2 What picks the option (forcing 3, seven layouts, ending A)

log share = layout + position + printed number + label. Effects relative to position 1 / number 1 / Strongly disagree; range = max − min over the four levels (log units; 1.0 ≈ a factor of 2.7). 95% CIs over items.

**H2a** (moderate labels beat both extremes by ≥ 1.0 log unit in every post-trained stage): **does not hold**. **H2b** (line 4 penalised against line 3 by no more than 0.5, descriptive): SFT yes, DPO yes, Instruct yes.

| stage | items | R² | position: pos1..4 | range | number: #1..4 | range | label: SD, D, A, SA | range | H2a: min(D, A) − max(SD, SA) | H2b: pos4 − pos3 |
|---|---|---|---|---|---|---|---|---|---|---|
| base | 50 | 0.86 | +0.0 +0.4 +0.6 +0.3 | 0.6 [0.6, 0.6] | +0.0 -0.2 -0.1 -0.7 | 0.7 [0.6, 0.7] | +0.0 +0.2 +0.6 +0.3 | 0.6 [0.6, 0.7] | -0.08 [-0.14, -0.02] (D − SA) | -0.30 [-0.33, -0.27] |
| SFT | 50 | 0.80 | +0.0 +0.4 +0.8 +0.9 | 0.9 [0.8, 0.9] | +0.0 -0.2 +0.0 -0.3 | 0.3 [0.2, 0.4] | +0.0 +0.6 +1.1 +0.7 | 1.1 [0.9, 1.2] | -0.13 [-0.26, -0.01] (D − SA) | +0.04 [-0.01, +0.09] |
| DPO | 50 | 0.86 | +0.0 +0.9 +1.8 +2.0 | 2.0 [1.8, 2.2] | +0.0 -0.0 +0.4 -0.1 | 0.4 [0.4, 0.6] | +0.0 +0.8 +1.6 +0.9 | 1.6 [1.3, 2.0] | -0.03 [-0.28, +0.22] (D − SA) | +0.20 [+0.10, +0.30] |
| Instruct | 50 | 0.86 | +0.0 +0.8 +1.9 +2.4 | 2.4 [2.2, 2.7] | +0.0 +0.5 +0.7 +0.4 | 0.7 [0.5, 0.9] | +0.0 +0.9 +1.8 +0.9 | 1.8 [1.5, 2.2] | -0.05 [-0.32, +0.20] (D − SA) | +0.53 [+0.41, +0.66] |

Mean option shares per layout (listed top to bottom; `#n` = printed number):

- **base**: paper/pos: #1SD 0.17 #2D 0.23 #3A 0.48 #4SA 0.12; reversed/pos: #1SA 0.21 #2A 0.36 #3D 0.34 #4SD 0.10; scrambled/pos: #1A 0.31 #2SD 0.26 #3SA 0.31 #4D 0.13; scrambled2/pos: #1D 0.25 #2SA 0.27 #3SD 0.26 #4A 0.21; reversed/can: #4SA 0.08 #3A 0.37 #2D 0.26 #1SD 0.30; scrambled/can: #3A 0.31 #1SD 0.20 #4SA 0.30 #2D 0.19; scrambled2/can: #2D 0.17 #4SA 0.18 #1SD 0.24 #3A 0.41
- **SFT**: paper/pos: #1SD 0.05 #2D 0.12 #3A 0.55 #4SA 0.27; reversed/pos: #1SA 0.12 #2A 0.36 #3D 0.39 #4SD 0.13; scrambled/pos: #1A 0.26 #2SD 0.15 #3SA 0.30 #4D 0.29; scrambled2/pos: #1D 0.24 #2SA 0.24 #3SD 0.20 #4A 0.32; reversed/can: #4SA 0.20 #3A 0.37 #2D 0.20 #1SD 0.23; scrambled/can: #3A 0.23 #1SD 0.08 #4SA 0.31 #2D 0.38; scrambled2/can: #2D 0.08 #4SA 0.17 #1SD 0.23 #3A 0.52
- **DPO**: paper/pos: #1SD 0.02 #2D 0.04 #3A 0.69 #4SA 0.25; reversed/pos: #1SA 0.02 #2A 0.35 #3D 0.52 #4SD 0.10; scrambled/pos: #1A 0.12 #2SD 0.09 #3SA 0.35 #4D 0.43; scrambled2/pos: #1D 0.13 #2SA 0.19 #3SD 0.20 #4A 0.47; reversed/can: #4SA 0.07 #3A 0.49 #2D 0.21 #1SD 0.24; scrambled/can: #3A 0.14 #1SD 0.02 #4SA 0.34 #2D 0.50; scrambled2/can: #2D 0.02 #4SA 0.09 #1SD 0.12 #3A 0.77
- **Instruct**: paper/pos: #1SD 0.01 #2D 0.04 #3A 0.61 #4SA 0.35; reversed/pos: #1SA 0.01 #2A 0.40 #3D 0.42 #4SD 0.16; scrambled/pos: #1A 0.10 #2SD 0.09 #3SA 0.27 #4D 0.54; scrambled2/pos: #1D 0.09 #2SA 0.18 #3SD 0.17 #4A 0.55; reversed/can: #4SA 0.07 #3A 0.50 #2D 0.24 #1SD 0.20; scrambled/can: #3A 0.11 #1SD 0.01 #4SA 0.24 #2D 0.64; scrambled2/can: #2D 0.01 #4SA 0.07 #1SD 0.07 #3A 0.85

## H3 Saturation or salience? (C, pinned vs positional numbering, forcing 3)

Ratio in [0.8, 1.25] = saturation (the content effect is the same size, and the layout only masks it); > 1.25 = salience; < 0.8 = reverse. Decided for the post-trained stages; the base model is shown for reference.

| stage | C pinned (3 layouts) | C positional (4 layouts) | ratio | class | C pinned at F5 | F5 / F3 (pinned) |
|---|---|---|---|---|---|---|
| base | +0.45 [+0.42, +0.51] | +0.38 [+0.36, +0.40] | +1.21 [+1.16, +1.27] | saturation | +0.27 [+0.25, +0.28] | +0.59 [+0.55, +0.63] |
| SFT | +0.84 [+0.69, +1.03] | +0.50 [+0.42, +0.57] | +1.70 [+1.61, +1.79] | salience | +0.62 [+0.50, +0.74] | +0.74 [+0.64, +0.88] |
| DPO | +2.20 [+1.88, +2.53] | +1.21 [+1.08, +1.35] | +1.82 [+1.75, +1.88] | salience | +1.85 [+1.59, +2.10] | +0.84 [+0.74, +0.95] |
| Instruct | +2.08 [+1.81, +2.35] | +1.24 [+1.11, +1.38] | +1.67 [+1.63, +1.71] | salience | +1.75 [+1.48, +2.01] | +0.84 [+0.72, +0.97] |

## Content effect per cell (C, with D in brackets; bold = reads, C ≥ 0.5)

| cell | olmo2-7b-base-answer | olmo2-7b-sft-answer | olmo2-7b-dpo-answer | olmo2-7b-instruct-answer | olmo2-7b-base-myanswer | olmo2-7b-base-qa | olmo2-7b-base-theansweris |
|---|---|---|---|---|---|---|---|
| paper|positional|1|last | **+0.79** (+0.56) | **+0.56** (+0.31) | **+1.07** (+0.24) | **+0.96** (+0.14) | **+0.65** (+0.48) | **+0.80** (+0.56) | +0.34 (+0.21) |
| paper|positional|1|none | **+1.03** (+0.69) | **+0.77** (+0.33) | **+1.57** (+0.28) | **+1.58** (+0.19) | **+0.72** (+0.54) | **+1.02** (+0.68) | +0.43 (+0.24) |
| paper|positional|2|first | +0.42 (+0.30) | **+0.56** (+0.37) | **+1.48** (+0.76) | **+1.94** (+0.88) | +0.40 (+0.28) | **+0.51** (+0.34) | +0.16 (+0.10) |
| paper|positional|2|last | **+0.59** (+0.44) | **+0.76** (+0.30) | **+1.93** (+0.32) | **+2.15** (+0.17) | **+0.62** (+0.47) | **+0.71** (+0.48) | +0.32 (+0.20) |
| reversed|positional|2|last | +0.37 (+0.28) | **+0.51** (+0.36) | **+0.66** (+0.38) | **+0.89** (+0.47) | +0.38 (+0.28) | +0.32 (+0.24) | **+0.51** (+0.31) |
| scrambled|positional|2|last | +0.22 (+0.17) | +0.47 (+0.32) | **+0.73** (+0.47) | **+0.87** (+0.46) | +0.25 (+0.19) | +0.20 (+0.19) | +0.23 (+0.13) |
| scrambled2|positional|2|last | +0.36 (+0.22) | +0.31 (+0.20) | **+0.96** (+0.53) | **+1.19** (+0.59) | +0.35 (+0.22) | +0.41 (+0.24) | +0.24 (+0.15) |
| paper|positional|2|none | **+0.61** (+0.45) | **+0.84** (+0.35) | **+2.09** (+0.37) | **+2.29** (+0.19) | **+0.70** (+0.52) | **+0.77** (+0.51) | +0.39 (+0.24) |
| reversed|canonical|3|none | **+0.55** (+0.39) | **+1.36** (+0.94) | **+3.41** (+1.37) | **+3.39** (+1.37) | **+0.58** (+0.38) | **+0.53** (+0.35) | +0.27 (+0.15) |
| scrambled|canonical|3|none | +0.48 (+0.34) | **+0.71** (+0.50) | **+1.73** (+0.91) | **+1.24** (+0.58) | +0.49 (+0.38) | **+0.52** (+0.41) | +0.21 (+0.13) |
| scrambled2|canonical|3|none | +0.34 (+0.24) | +0.45 (+0.31) | **+1.47** (+0.60) | **+1.61** (+0.33) | +0.45 (+0.32) | **+0.50** (+0.33) | +0.10 (+0.08) |
| paper|positional|3|none | **+0.54** (+0.37) | **+0.68** (+0.27) | **+1.95** (+0.25) | **+1.92** (+0.15) | **+0.58** (+0.43) | **+0.71** (+0.47) | +0.34 (+0.25) |
| reversed|positional|3|none | +0.38 (+0.29) | **+0.50** (+0.32) | **+0.92** (+0.39) | **+0.99** (+0.44) | +0.49 (+0.33) | +0.44 (+0.32) | **+0.69** (+0.47) |
| scrambled|positional|3|none | +0.23 (+0.15) | +0.45 (+0.29) | **+0.78** (+0.46) | **+0.85** (+0.40) | +0.24 (+0.16) | +0.25 (+0.20) | +0.29 (+0.16) |
| scrambled2|positional|3|none | +0.35 (+0.22) | +0.35 (+0.21) | **+1.19** (+0.62) | **+1.21** (+0.57) | +0.44 (+0.28) | **+0.50** (+0.30) | +0.32 (+0.20) |
| reversed|canonical|5|none | +0.30 (+0.22) | **+0.96** (+0.61) | **+2.67** (+1.15) | **+2.50** (+1.09) | +0.44 (+0.29) | +0.16 (+0.11) | +0.24 (+0.15) |
| scrambled|canonical|5|none | +0.30 (+0.24) | **+0.56** (+0.36) | **+1.65** (+0.74) | **+1.46** (+0.56) | +0.36 (+0.28) | +0.18 (+0.15) | +0.18 (+0.11) |
| scrambled2|canonical|5|none | +0.20 (+0.15) | +0.33 (+0.22) | **+1.22** (+0.35) | **+1.28** (+0.17) | +0.33 (+0.25) | +0.14 (+0.12) | +0.08 (+0.08) |
| paper|positional|5|none | +0.31 (+0.24) | **+0.53** (+0.28) | **+1.53** (+0.33) | **+1.38** (+0.22) | +0.41 (+0.33) | +0.21 (+0.17) | +0.32 (+0.25) |

## Greedy decodes (24 statements × 6 cells per run)

| run | decodes | number | label | deflection | other | example of the most common kind |
|---|---|---|---|---|---|---|
| olmo2-7b-base-answer | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-sft-answer | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-dpo-answer | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-instruct-answer | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-base-myanswer | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-base-qa | 144 | 144 | 0 | 0 | 0 | number: " 3" |
| olmo2-7b-base-theansweris | 144 | 144 | 0 | 0 | 0 | number: ": 3" |
