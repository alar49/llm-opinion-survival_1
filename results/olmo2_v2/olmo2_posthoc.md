# OLMo 2 7B training stages, v2: post-hoc analyses

**Not pre-registered.** Every analysis below was chosen after the registered results (`olmo2_compare.md`, `olmo2_explore.md`) had been seen, to explain them. 95% CIs from the registered paraphrase bootstrap (4,000 reps, seed 7, shared by every run), or over items for P4. Reference cell = paper order, positional numbering, forcing 3, no opt-out. Script: `scripts/olmo2_posthoc.py`.

## P1 Ending D: the base model answers after a colon

Reference cell, 34 issue statements × 4 paraphrases; decodes = the 144 greedy decodes per run.

| | ending A (`Answer:`) | ending D (`The answer is`) |
|---|---|---|
| mean answer mass the readout sees | 0.97 | 0.07 |
| rows with answer mass < 0.05 | 0 of 136 | 55 of 136 |
| first-token probability on a colon | 0.00 | 0.83 |
| most likely first tokens | `' '` 0.97, `' Strong'` 0.00, `'<|endoftext|>'` 0.00 | `':'` 0.79, `' '` 0.06, `':\n'` 0.03 |
| greedy decodes | `' 3'` ×114, `' 1'` ×12, `' 3.'` ×10, `' 2'` ×5 | `': 3'` ×91, `': 3.'` ×18, `': 1'` ×13, `': 3).'` ×12 |

The written answer (the option the decode names) is the same under endings A and D for 137 of 144 prompts. How often the readout's top option is the option the decode names, per decode cell:

| decode cell | ending A | ending D |
|---|---|---|
| paper|positional|3|none | 24/24 | 24/24 |
| scrambled|positional|3|none | 24/24 | 11/24 |
| reversed|canonical|3|none | 22/24 | 5/24 |
| paper|positional|1|none | 24/24 | 17/24 |
| paper|positional|5|none | 24/24 | 24/24 |
| paper|positional|2|last | 24/24 | 14/24 |

## P2 One set of stances, four scales

Per stage at the reference cell. Calls: 95% CI excludes 0, |value| ≥ floor (0.10 in d, 0.4 in d_LO), BH q = 0.01 over the 19 axes.

| stage | mean p_agree | mean \|d\| | mean \|d_LO\| | C | mean \|d_rel\| | issues called in d | issues called in d_LO | null calls |
|---|---|---|---|---|---|---|---|---|
| base | 0.61 [0.59, 0.62] | 0.03 [0.03, 0.03] | 0.13 [0.13, 0.14] | 0.54 [0.52, 0.57] | 0.25 [0.23, 0.27] | 0 | 0 | 0 |
| SFT | 0.82 [0.82, 0.83] | 0.06 [0.06, 0.07] | 0.44 [0.42, 0.46] | 0.68 [0.59, 0.77] | 0.65 [0.56, 0.77] | 3 | 8 | 0 |
| DPO | 0.95 [0.94, 0.96] | 0.04 [0.03, 0.04] | 0.95 [0.89, 1.01] | 1.95 [1.82, 2.09] | 0.48 [0.43, 0.54] | 2 | 10 | 0 |
| Instruct | 0.96 [0.95, 0.97] | 0.03 [0.02, 0.04] | 1.10 [1.03, 1.17] | 1.92 [1.77, 2.07] | 0.57 [0.51, 0.63] | 0 | 12 | 0 |

## P3 H5a broken down: uniform rescaling and issue-specific change

slope = least-squares growth of d_LO from the earlier to the later stage over the 17 issues; u = slope / (C ratio), the change of d_rel that a uniform rescaling would give every issue. Residual = d_rel(later) − u × d_rel(earlier): the issue-specific part, in d_rel units (* = 95% CI excludes 0 and |residual| ≥ 0.2, the H5a margin).

| pair | d_LO slope | C ratio | u (uniform d_rel factor) | issues with an issue-specific change |
|---|---|---|---|---|
| SFT → DPO | 2.15 [2.07, 2.22] | 2.88 [2.62, 3.10] | 0.75 [0.68, 0.81] | energy |
| DPO → Instruct | 1.11 [1.10, 1.13] | 0.98 [0.97, 1.00] | 1.13 [1.12, 1.14] | none |
| SFT → Instruct | 2.40 [2.28, 2.49] | 2.83 [2.61, 3.01] | 0.85 [0.77, 0.92] | energy |

**SFT → DPO**, per issue:

| issue | d_rel before | d_rel after | Δd_rel | uniform part | residual [95% CI] | d_LO growth |
|---|---|---|---|---|---|---|
| energy | +1.06 | +0.51 | -0.55 | -0.27 | -0.28 [-0.35, -0.21] * | ×1.38 |
| state surveillance | -1.49 | -1.07 | +0.41 | +0.38 | +0.04 [-0.03, +0.08] | ×2.08 |
| trans sports | +1.80 | +1.39 | -0.41 | -0.46 | +0.05 [+0.02, +0.10] | ×2.23 |
| drugs | +1.07 | +0.80 | -0.27 | -0.27 | -0.00 [-0.05, +0.06] | ×2.14 |
| schools | +0.26 | +0.01 | -0.25 | -0.07 | -0.18 [-0.22, -0.14] | — |
| transit | +1.15 | +0.92 | -0.23 | -0.29 | +0.06 [+0.03, +0.10] | ×2.30 |
| voting | +0.99 | +0.83 | -0.16 | -0.25 | +0.09 [+0.04, +0.15] | ×2.40 |
| vaccines | +0.78 | +0.63 | -0.15 | -0.20 | +0.05 [+0.03, +0.08] | ×2.34 |
| minimum wage | +0.54 | +0.42 | -0.12 | -0.14 | +0.02 [-0.04, +0.08] | ×2.23 |
| guns | +0.68 | +0.56 | -0.12 | -0.17 | +0.06 [+0.02, +0.09] | ×2.38 |
| property tax | +0.07 | -0.01 | -0.08 | -0.02 | -0.06 [-0.09, -0.04] | — |
| police funding | +0.13 | +0.08 | -0.04 | -0.03 | -0.01 [-0.09, +0.06] | — |
| agi limitations | +0.08 | +0.11 | +0.03 | -0.02 | +0.05 [+0.01, +0.12] | — |
| abortion | +0.08 | +0.05 | -0.03 | -0.02 | -0.01 [-0.05, +0.03] | — |
| housing zoning | +0.49 | +0.48 | -0.01 | -0.12 | +0.11 [+0.02, +0.20] | ×2.82 |
| unions | +0.17 | +0.18 | +0.01 | -0.04 | +0.05 [+0.01, +0.10] | — |
| immigration | +0.18 | +0.18 | -0.00 | -0.05 | +0.04 [-0.01, +0.10] | — |

**SFT → Instruct**, per issue:

| issue | d_rel before | d_rel after | Δd_rel | uniform part | residual [95% CI] | d_LO growth |
|---|---|---|---|---|---|---|
| energy | +1.06 | +0.56 | -0.51 | -0.16 | -0.34 [-0.41, -0.27] * | ×1.49 |
| trans sports | +1.80 | +1.48 | -0.32 | -0.28 | -0.05 [-0.07, -0.01] | ×2.32 |
| state surveillance | -1.49 | -1.24 | +0.25 | +0.23 | +0.02 [-0.05, +0.05] | ×2.36 |
| minimum wage | +0.54 | +0.37 | -0.18 | -0.08 | -0.09 [-0.14, -0.04] | ×1.92 |
| property tax | +0.07 | -0.08 | -0.15 | -0.01 | -0.14 [-0.17, -0.11] | — |
| agi limitations | +0.08 | +0.22 | +0.14 | -0.01 | +0.16 [+0.10, +0.23] | — |
| immigration | +0.18 | +0.32 | +0.14 | -0.03 | +0.17 [+0.12, +0.20] | — |
| drugs | +1.07 | +0.95 | -0.12 | -0.16 | +0.04 [-0.02, +0.11] | ×2.51 |
| transit | +1.15 | +1.03 | -0.12 | -0.18 | +0.06 [+0.00, +0.13] | ×2.54 |
| schools | +0.26 | +0.17 | -0.09 | -0.04 | -0.05 [-0.11, +0.01] | — |
| guns | +0.68 | +0.73 | +0.05 | -0.10 | +0.15 [+0.13, +0.18] | ×3.04 |
| unions | +0.17 | +0.12 | -0.05 | -0.03 | -0.02 [-0.08, +0.06] | — |
| abortion | +0.08 | +0.04 | -0.04 | -0.01 | -0.02 [-0.08, +0.04] | — |
| vaccines | +0.78 | +0.81 | +0.04 | -0.12 | +0.15 [+0.14, +0.18] | ×2.96 |
| voting | +0.99 | +0.97 | -0.02 | -0.15 | +0.13 [+0.05, +0.17] | ×2.76 |
| housing zoning | +0.49 | +0.50 | +0.01 | -0.07 | +0.09 [+0.00, +0.16] | ×2.90 |
| police funding | +0.13 | +0.12 | -0.01 | -0.02 | +0.01 [-0.08, +0.10] | — |

## P4 H2a split: moderation within a side and the agree-side preference

From the label effects of the layout decomposition (log units; 95% CI over items). Moderation = ((D − SD) + (A − SA)) / 2; agree side = ((A + SA) − (D + SD)) / 2. H2a's test, min(D, A) − max(SD, SA), mixes the two.

| stage | moderation | agree-side preference |
|---|---|---|
| base | +0.28 [+0.26, +0.30] | +0.36 [+0.29, +0.42] |
| SFT | +0.47 [+0.43, +0.51] | +0.60 [+0.46, +0.73] |
| DPO | +0.79 [+0.70, +0.91] | +0.82 [+0.55, +1.11] |
| Instruct | +0.89 [+0.79, +1.02] | +0.95 [+0.68, +1.25] |

## P5 H3 order by order: C with pinned and with positional numbering

Forcing 3. Pinned numbering keeps each label's conventional number (1 = Strongly disagree … 4 = Strongly agree) in every order; positional numbering numbers the lines top to bottom, so in the reversed order every number has the opposite meaning.

| stage | paper (positional) | reversed: pinned / positional | scrambled: pinned / positional | scrambled2: pinned / positional |
|---|---|---|---|---|
| base | +0.54 | +0.55 / +0.38 (Δ +0.17 [+0.13, +0.21]) | +0.48 / +0.23 (Δ +0.25 [+0.19, +0.33]) | +0.34 / +0.35 (Δ -0.02 [-0.06, +0.02]) |
| SFT | +0.68 | +1.36 / +0.50 (Δ +0.86 [+0.69, +1.05]) | +0.71 / +0.45 (Δ +0.26 [+0.21, +0.35]) | +0.45 / +0.35 (Δ +0.10 [+0.07, +0.16]) |
| DPO | +1.95 | +3.41 / +0.92 (Δ +2.48 [+2.20, +2.76]) | +1.73 / +0.78 (Δ +0.95 [+0.76, +1.09]) | +1.47 / +1.19 (Δ +0.29 [+0.12, +0.47]) |
| Instruct | +1.92 | +3.39 / +0.99 (Δ +2.40 [+2.15, +2.65]) | +1.24 / +0.85 (Δ +0.38 [+0.29, +0.45]) | +1.61 / +1.21 (Δ +0.40 [+0.28, +0.53]) |

## P6 Base vs SFT: the same directions, smaller

Same sign on 15 of 17 issues. Mean |d_LO|: base 0.13 [0.13, 0.14], SFT 0.44 [0.42, 0.46] (SFT / base 3.27 [3.08, 3.48]). Mean |d_rel|: base 0.25 [0.23, 0.27], SFT 0.65 [0.56, 0.77] (SFT / base 2.62 [2.30, 2.99]).

| issue (+ position) | base d_LO | SFT d_LO |
|---|---|---|
| trans sports (+ Trans-inclusive leagues) | +0.29 [+0.25, +0.34] | +1.22 [+1.12, +1.33] |
| state surveillance (+ Expand surveillance) | -0.29 [-0.33, -0.25] | -1.01 [-1.10, -0.90] |
| transit (+ Build transit) | +0.35 [+0.33, +0.38] | +0.78 [+0.70, +0.90] |
| drugs (+ Decriminalize drugs) | +0.06 [+0.02, +0.10] | +0.73 [+0.67, +0.78] |
| energy (+ Renewables mandate) | +0.01 [-0.03, +0.05] | +0.72 [+0.65, +0.80] |
| voting (+ Expand voting access) | +0.15 [+0.07, +0.21] | +0.67 [+0.65, +0.70] |
| vaccines (+ Vaccine mandate) | +0.06 [+0.02, +0.10] | +0.53 [+0.46, +0.60] |
| guns (+ Loosen gun rules) | +0.19 [+0.14, +0.21] | +0.46 [+0.37, +0.55] |
| minimum wage (+ Raise minimum wage) | +0.12 [+0.07, +0.17] | +0.37 [+0.28, +0.49] |
| housing zoning (+ Allow fourplexes) | +0.06 [+0.00, +0.13] | +0.33 [+0.32, +0.34] |
| schools (+ School vouchers) | +0.14 [+0.11, +0.16] | +0.18 [+0.14, +0.21] |
| immigration (+ Cooperate with ICE) | +0.02 [+0.00, +0.04] | +0.13 [+0.09, +0.18] |
| unions (+ Prevailing wage) | -0.09 [-0.10, -0.07] | +0.12 [+0.07, +0.18] |
| police funding (+ More deputies) | +0.05 [+0.02, +0.08] | +0.08 [+0.04, +0.14] |
| abortion (+ Permit abortion) | +0.17 [+0.13, +0.21] | +0.05 [+0.02, +0.08] |
| agi limitations (+ Keep AGI open) | +0.07 [+0.02, +0.11] | +0.05 [-0.05, +0.16] |
| property tax (+ Raise tax) | -0.16 [-0.17, -0.16] | +0.05 [+0.00, +0.08] |

## P7 The panel's survival ladder, in probability and in log-odds

Rules of PLAN.md §5 (`orderforce_analyze.py`) per stage, on this bootstrap. **d**: the panel's ladder (floor 0.10; a cell is read when anchor D ≥ 0.5). **d_LO**: the same rules with d_LO (floor 0.4; a cell is read when C ≥ 0.5). Rungs: called at the reference cell → +order (same direction across the read order and numbering layouts) / +forcing (same direction at F5 and with the opt-out) → survives all.

| stage | scale | layouts read (of 7) | called | +order only | +forcing only | survives all | null calls |
|---|---|---|---|---|---|---|---|
| base | d | 0 | 0 | 0 | 0 | 0 | 0 |
| base | d_LO | 2 | 0 | 0 | 0 | 0 | 0 |
| SFT | d | 1 | 3 | 0 | 3 | 0 | 0 |
| SFT | d_LO | 4 | 8 | 0 | 3 | 5 | 0 |
| DPO | d | 4 | 2 | 0 | 2 | 0 | 0 |
| DPO | d_LO | 7 | 10 | 0 | 3 | 6 | 0 |
| Instruct | d | 3 | 0 | 0 | 0 | 0 | 0 |
| Instruct | d_LO | 7 | 12 | 0 | 3 | 6 | 0 |

Rung per issue, log-odds ladder:

| issue (+ position) | base | SFT | DPO | Instruct |
|---|---|---|---|---|
| property tax (+ Raise tax) | not called | not called | not called | not called |
| agi limitations (+ Keep AGI open) | not called | not called | not called | called (+0.43) |
| abortion (+ Permit abortion) | not called | not called | not called | not called |
| state surveillance (+ Expand surveillance) | not called | survives all (-1.01) | survives all (-2.09) | survives all (-2.38) |
| immigration (+ Cooperate with ICE) | not called | not called | not called | called (+0.62) |
| guns (+ Loosen gun rules) | not called | survives all (+0.46) | called (+1.09) | called (+1.39) |
| minimum wage (+ Raise minimum wage) | not called | not called | +forcing (+0.82) | +forcing (+0.71) |
| energy (+ Renewables mandate) | not called | +forcing (+0.72) | +forcing (+1.00) | +forcing (+1.07) |
| housing zoning (+ Allow fourplexes) | not called | not called | survives all (+0.93) | survives all (+0.96) |
| drugs (+ Decriminalize drugs) | not called | survives all (+0.73) | survives all (+1.56) | survives all (+1.83) |
| police funding (+ More deputies) | not called | not called | not called | not called |
| schools (+ School vouchers) | not called | not called | not called | not called |
| transit (+ Build transit) | not called | survives all (+0.78) | survives all (+1.79) | survives all (+1.98) |
| vaccines (+ Vaccine mandate) | not called | +forcing (+0.53) | +forcing (+1.23) | +forcing (+1.56) |
| unions (+ Prevailing wage) | not called | not called | not called | not called |
| voting (+ Expand voting access) | not called | +forcing (+0.67) | survives all (+1.61) | survives all (+1.85) |
| trans sports (+ Trans-inclusive leagues) | not called | survives all (+1.22) | survives all (+2.72) | survives all (+2.84) |
| fair month (+ Fair in June) (null) | not called | not called | not called | not called |
| sign color (+ Green signs) (null) | not called | not called | not called | not called |
