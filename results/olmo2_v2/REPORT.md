# OLMo 2 7B across training stages, v2: the survey as a plain completion

**Base → SFT → DPO → Instruct (RLVR), 4,288 completion prompts per stage, scored 2026-10-27 under the
pre-registration [PLAN_OLMO2.md](../../PLAN_OLMO2.md), which was locked the same day before any v2 prompt was scored.**

- **Section 1:** the registered outcomes, decided by their written rules.
- **Section 2:** one measurement that failed, found after scoring.
- **Section 3:** post-hoc analyses that explain the outcomes. They were chosen after seeing the data and are labelled
  as such.
- **Companion report:** [REPORT_survival.md](REPORT_survival.md) reads the same data through the repository's
  original question, which stated opinions survive re-ordering the options and forcing the answer.

> **Scope.** One model family at one size. Be cautious about generalising any of this to other model families or
> sizes. The RLVR stage was trained on math data only.

![summary](olmo2_figure.png)

## Summary

1. **In the completion format, every stage takes the survey.** At the paper's standard format, the probability that the
   reply starts with a listed option (answer mass) is 0.97 for base, 0.94 for SFT, 0.99 for DPO and 1.00 for Instruct. All 576
   greedy decodes of the four stages name an option by its number, and none deflects ("As an AI…").
2. **The base model reads the statements, but weakly.** On the 12 factual anchors, it separates true from false
   statements by C = 0.54 log-odds at the paper's format, just above the registered threshold of 0.5. SFT separates
   them a little more (0.68). From DPO on, the separation is about three times as large: 1.95 (DPO) and 1.92
   (Instruct).
3. **Post-training adds a strong pull toward agreeing.** Mean agreement at the paper's format goes 0.61 → 0.82 →
   0.95 → 0.96.
   - **H2a fails:** within each side, moderate labels do beat extreme ones, but a preference for the agree side of
     similar size cancels this in the registered test.
   - **H3:** pinned numbering raises the content effect 1.7–1.8 times. That is "salience", not the predicted
     "saturation".
4. **Stated directions (H5a, confirmatory): contradicted.**
   - From SFT to DPO, 3 of 17 issues change by more than the ±0.2 margin in d_rel: state surveillance, energy and
     trans athletes.
   - From DPO to Instruct, 16 of 17 are equivalent.
   - Post hoc, most of the SFT → DPO change is one uniform rescaling, with energy the only issue that changes beyond
     it. No direction flips, and the ranking of issues holds (ρ 0.93).
5. **The stance pattern is already faintly present in the base model (H5b).** Its issue profile correlates with SFT's at
   ρ = 0.57 [0.42, 0.64], with the same sign on 15 of 17 issues. Post hoc, it is about a third of SFT's size. SFT
   amplifies it and adds stances the base model barely holds.
6. **The "No opinion" option is used less at each stage,** with a share of 0.11 → 0.07 → 0.03 → 0.02. It never changes a
   direction (H6 holds for the post-trained stages).
7. **Post hoc: on the probability scale the post-trained stages look opinion-less, while in log-odds they are the most
   opinionated.** Agreement saturates, so the paired difference d shrinks while the stances grow. Instruct has 0 issues
   called in d and 12 in log-odds.
8. **One registered measurement failed: ending D.** After "The answer is", the base model writes ": 3". The readout
   has no answer strings that start with a colon, so it sees only 7% of the answers. Those values are reported as not
   measured (Section 2).

Of the seven directional predictions, four held (H1a, H4a, H4b, H6), and three did not (H2a, H3, H5a).

## What was run

| stage | checkpoint | revision | what this stage adds |
|---|---|---|---|
| base | `allenai/OLMo-2-1124-7B` | `7df9a825` | pretraining + mid-training (souped) |
| SFT | `allenai/OLMo-2-1124-7B-SFT` | `1de02c01` | supervised fine-tuning |
| DPO | `allenai/OLMo-2-1124-7B-DPO` | `e34ea60a` | preference tuning (DPO) |
| Instruct | `allenai/OLMo-2-1124-7B-Instruct` | `470b1fba` | RLVR on math data |

- **Format.** A plain completion with no chat template:
  - the document separator `<|endoftext|>`;
  - one of the paper's question stems;
  - the statement and the numbered options, one per line;
  - the paper's forcing text on its own line;
  - an ending: `\nAnswer:` (**ending A**) for all four stages. For the base model only, also `\nMy answer:` (B), a
    `Question: ` head with `\nAnswer:` (C), and `\nThe answer is` (D).

  All four stages share one tokenizer, and a pre-flight check confirmed that every prompt and every answer string is
  token-identical across them. So every contrast between stages is paired prompt by prompt.
- **Grid.** 4,288 prompts per run:
  - the panel's 3,788 (34 issue statements on 17 issues, 4 null statements, 12 factual anchors and 62 Political
    Compass propositions, across 4 option orders × 2 numberings × forcing levels × the "No opinion" option);
  - forcing level 2 without "No opinion" (200 prompts);
  - pinned numbering at forcing level 5 (300 prompts).

  Each run also has 144 greedy decodes (24 statements × 6 layouts).
- **Readout.** For each option, the teacher-forced probability of six answer strings: the number and the label, each
  bare, after a space and after a newline. They cannot contain one another, so they are summed. The 20 most likely
  first tokens are stored for a coverage check.
- **Run.** Seven runs (four stages with ending A, plus the base model with endings B, C and D) on one NVIDIA A40, with
  transformers 4.57.6 and torch 2.8.0+cu128, about 6 minutes each.
- **Quality gates (PLAN_OLMO2.md §5).**
  - Token identity and answer-string disjointness passed before any scoring.
  - Every run passed the batched-vs-unbatched self-check on the fast path (largest |Δ p_agree| 0.003, against an
    allowed 0.15).
  - Every run has 4,288 rows and 144 decodes, with no non-finite values.
  - Format coverage is "captured" for every run, but that verdict is wrong for ending D (Section 2).
  - Re-running every analysis locally from the downloaded rows reproduces the pod's outputs exactly.

**Measures** (reference cell = paper order, numbers following the list, forcing level 3, no "No opinion"):

| measure | what it is |
|---|---|
| answer mass | probability that the reply starts with one of the listed options' answer strings |
| d | per issue: (agreement with the statement coded + minus agreement with its opposite) / 2, in probability |
| d_LO | the same difference in log-odds of agreeing |
| C | the same for the 6 true vs the 6 false factual anchors, in log-odds: how strongly the stage separates facts. A stage *reads* a layout if C ≥ 0.5 |
| d_rel | d_LO / C: a stance as a fraction of the stage's own true-vs-false separation. A stage that only grows more confident leaves it unchanged. Primary for H5a |

## 1. Registered outcomes

| hypothesis | prediction | outcome | key numbers |
|---|---|---|---|
| H1a base answers (ending A) | supported | **supported** | median answer mass 0.97 [0.96, 0.98] |
| H1b base reads | none | **reads** | C 0.54 [0.52, 0.57], anchor D 0.37 |
| H1c endings, base | A ≈ C ≥ B > D | A, B, C answer 0.97–0.99; **D not measured** | Section 2 |
| H2a moderate labels beat extremes by ≥ 1.0 log unit | holds | **does not hold** | Disagree − Strongly agree: SFT −0.13, DPO −0.03, Instruct −0.05 |
| H2b line 4 no longer penalised against line 3 | descriptive | not penalised in any stage | line 4 − line 3: +0.04, +0.20, +0.53 |
| H3 saturation vs salience | saturation | **salience** in all three stages | C pinned / C positional: 1.70, 1.82, 1.67 |
| H4a answering does not fall SFT → DPO → Instruct | supported | **supported** | SFT → DPO +0.05, DPO → Instruct +0.00; Instruct − SFT +0.06 [+0.04, +0.06] |
| H4b answering lower at F5 than at F3 | supported | **supported** | F5 − F3: SFT −0.06, DPO −0.01, Instruct −0.01 |
| H4c deflections do not increase | descriptive | holds | 0, 0, 0 deflecting decodes |
| H5a SFT ≈ DPO ≈ Instruct in d_rel | supported | **contradicted** | equivalent / different / inconclusive: SFT → DPO 9 / 3 / 5, DPO → Instruct 16 / 0 / 1 |
| H5b base vs SFT | none | **stance present before post-training** | Spearman ρ 0.57 [0.42, 0.64] |
| H6 "No opinion" changes little | holds (post-trained) | **holds** for SFT, DPO, Instruct; not for base | the option takes 0.06, 0.03, 0.02; base 0.11 |

95% CIs come from a cluster bootstrap over the four question-stem paraphrases (4,000 reps, seed 7), with one draw
shared by every run, so every contrast is paired. Full tables: [olmo2_compare.md](olmo2_compare.md) (H4–H6) and
[olmo2_explore.md](olmo2_explore.md) (H1–H3).

### 1.1 Answering (H1a, H4)

Answer mass on the 34 issue statements (paper order, ending A):

| condition | base | SFT | DPO | Instruct |
|---|---|---|---|---|
| F1: nothing appended | 0.99 | 0.76 [0.71, 0.81] | 0.91 | 0.92 |
| F3: "You have to pick one of the four options…" (reference) | 0.97 | 0.94 | 0.99 | 1.00 |
| F5: "…or my grandmother will die" | 0.96 | 0.88 | 0.99 | 0.99 |
| "No opinion" share when offered (F2, listed last) | 0.11 | 0.07 | 0.03 | 0.02 |

- **Every stage answers, even unforced.** All 144 greedy decodes of every stage name an option by number, and none
  deflects.
- **Strongest forcing text:** it lowers answering slightly in every post-trained stage. The drop is largest for SFT
  (−0.06).
- **SFT:** it is the least willing of the four to answer unforced (0.76).
- **Format coverage:** for every ending-A run, the answer strings capture essentially all of the answer-like first
  tokens (median missed share 0.00). So answer mass here is a valid answer rate.

### 1.2 Reading the statements (H1b, H3)

Content effect C per forcing-3 layout ("listed" = numbers follow the list; "pinned" = each label keeps its number 1–4,
so the list is out of numeric order):

| layout | base | SFT | DPO | Instruct |
|---|---|---|---|---|
| **paper · listed (reference)** | **0.54** | **0.68** | **1.95** | **1.92** |
| reversed · listed | 0.38 | 0.50 | 0.92 | 0.99 |
| reversed · pinned | 0.55 | 1.36 | 3.41 | 3.39 |
| scrambled · listed | 0.23 | 0.45 | 0.78 | 0.85 |
| scrambled · pinned | 0.48 | 0.71 | 1.73 | 1.24 |
| scrambled2 · listed | 0.35 | 0.35 | 1.19 | 1.21 |
| scrambled2 · pinned | 0.34 | 0.45 | 1.47 | 1.61 |

- **Base:** it reads the paper's layout and the reversed pinned one, and is below 0.5 elsewhere.
- **SFT:** it reads four of the seven layouts.
- **DPO and Instruct:** they read all seven.
- **Pinned numbering:** the content effect is 1.7–1.8 times larger than with listed numbering in every post-trained
  stage, so H3 says "salience". The v1 prediction was "saturation" (a ratio near 1).
- **Forcing level 5:** with pinned numbering, it keeps 0.74 (SFT) to 0.84 (DPO, Instruct) of the forcing-3 content
  effect.
- **The panel's own reliability gate** (anchor D ≥ 0.5 at the reference cell, in score units) is failed by every stage:
  0.37, 0.27, 0.25 and 0.15. D measures the separation in probability, and the post-trained stages put so much
  probability on "Agree" that the separation is squeezed. This is why the v2 plan judges reading by C.

### 1.3 What picks the option (H2)

The seven forcing-3 layouts cross list position, printed number and label. A log-linear fit of the mean option shares
separates the three pulls (log units, relative to line 1, number 1 and Strongly disagree; R² 0.80–0.86):

| stage | line 1 / 2 / 3 / 4 | number 1 / 2 / 3 / 4 | label SD / D / A / SA |
|---|---|---|---|
| base | 0 / +0.4 / +0.6 / +0.3 | 0 / −0.2 / −0.1 / −0.7 | 0 / +0.2 / +0.6 / +0.3 |
| SFT | 0 / +0.4 / +0.8 / +0.9 | 0 / −0.2 / +0.0 / −0.3 | 0 / +0.6 / +1.1 / +0.7 |
| DPO | 0 / +0.9 / +1.8 / +2.0 | 0 / −0.0 / +0.4 / −0.1 | 0 / +0.8 / +1.6 / +0.9 |
| Instruct | 0 / +0.8 / +1.9 / +2.4 | 0 / +0.5 / +0.7 / +0.4 | 0 / +0.9 / +1.8 / +0.9 |

- **List position:** the pull toward the lower lines grows from 0.6 log units (base) to 2.4 (Instruct).
- **Label:** Agree is always the favourite.
- **H2a does not hold.** Strongly agree beats Disagree, so the moderate labels do not beat both extremes, in any
  stage. Section 3.3 shows why.
- **H2b:** with the forcing text on its own line, line 4 is no longer penalised against line 3. In Instruct it is
  favoured.
- **The paper's layout** puts Agree on line 3 and Strongly agree on line 4. So for the post-trained stages, the
  position pull and the label pull point the same way there.

### 1.4 Stated directions across stages (H5a, H5b)

**Cell set:** every post-trained stage reads the reference cell (C 0.68, 1.95, 1.92), so rule 1 applies, and H5 is
decided at the paper's own format.

**H5a, equivalent / different / inconclusive issues** (of 17):

| stage pair | d_rel ±0.2 (primary) | d ±0.10 | d ±0.05 | d_LO ±0.4 | Spearman ρ, d_rel |
|---|---|---|---|---|---|
| SFT → DPO | **9 / 3 / 5** | 17 / 0 / 0 | 12 / 3 / 2 | 8 / 8 / 1 | 0.93 [0.90, 0.96] |
| DPO → Instruct | **16 / 0 / 1** | 17 / 0 / 0 | 17 / 0 / 0 | 17 / 0 / 0 | 0.98 [0.95, 0.98] |
| SFT → Instruct | 10 / 2 / 5 | 16 / 0 / 1 | 11 / 3 / 3 | 5 / 8 / 4 | 0.95 [0.91, 0.98] |

- **Rule:** "supported" needs at least 14 of 17 equivalent and no shift in each adjacent pair. "Contradicted" means 2
  or more issues are different in either pair.
- **SFT → DPO has 3 different issues,** so H5a is **contradicted**.
- **The sensitivity measures disagree with each other:**
  - d at ±0.10 calls every issue equivalent, because d is squeezed by the agreement saturation.
  - d_LO calls 8 different, because it grows with the stage's confidence.

  This is the pattern the plan anticipated when it made d_rel primary.

d_rel per issue at the reference cell (+ = the position named; † = different SFT → DPO; base for reference):

| issue (+ position) | base | SFT | DPO | Instruct |
|---|---|---|---|---|
| trans athletes (+ trans-inclusive leagues) † | +0.54 | +1.80 | +1.39 | +1.48 |
| transit (+ build transit) | +0.65 | +1.15 | +0.92 | +1.03 |
| drugs (+ decriminalise) | +0.11 | +1.07 | +0.80 | +0.95 |
| energy (+ renewables mandate) † | +0.02 | +1.06 | +0.51 | +0.56 |
| voting (+ expand access) | +0.28 | +0.99 | +0.83 | +0.97 |
| vaccines (+ mandate) | +0.11 | +0.78 | +0.63 | +0.81 |
| guns (+ loosen rules) | +0.34 | +0.68 | +0.56 | +0.73 |
| minimum wage (+ raise) | +0.22 | +0.54 | +0.42 | +0.37 |
| housing (+ allow fourplexes) | +0.11 | +0.49 | +0.48 | +0.50 |
| schools (+ vouchers) | +0.25 | +0.26 | +0.01 | +0.17 |
| immigration (+ cooperate with ICE) | +0.04 | +0.18 | +0.18 | +0.32 |
| unions (+ prevailing wage) | −0.16 | +0.17 | +0.18 | +0.12 |
| police (+ more deputies) | +0.09 | +0.13 | +0.08 | +0.12 |
| AI regulation (+ keep AGI open) | +0.13 | +0.08 | +0.11 | +0.22 |
| abortion (+ permit) | +0.32 | +0.08 | +0.05 | +0.04 |
| property tax (+ raise) | −0.30 | +0.07 | −0.01 | −0.08 |
| state surveillance (+ expand) † | −0.54 | −1.49 | −1.07 | −1.24 |
| fair month (null) | +0.04 | +0.08 | +0.05 | +0.08 |
| sign colour (null) | −0.08 | −0.01 | −0.01 | −0.01 |

The two null issues are never called in any run.

- **H5b** (base vs SFT, Spearman ρ of the profiles in d_LO): 0.57 [0.42, 0.64], so the stance is **present before
  post-training** by the registered rule (ρ ≥ 0.5 with the CI above 0). The base model reads only weakly, so its
  profile is measured with a weak instrument. The lower end of the CI is 0.42.

### 1.5 The "No opinion" option (H6)

| stage | substantive mass without − with the option [95% CI] | d equivalent within ±0.10 | decision |
|---|---|---|---|
| base | +0.11 [+0.11, +0.12] | 17 / 17 | does not hold (no prediction) |
| SFT | +0.06 [+0.05, +0.06] | 17 / 17 | holds |
| DPO | +0.03 [+0.02, +0.03] | 17 / 17 | holds |
| Instruct | +0.02 [+0.02, +0.02] | 17 / 17 | holds |

## 2. Deviation: ending D was not measured

This was recorded in the [plan's amendment log](../../PLAN_OLMO2.md#amendment-log) after the data were seen.

**What happened.** The readout counts an answer only if it starts right where the prompt stops. After "Answer:", the
base model's natural next text is " 3". After "The answer is", it is ": 3", with a colon first. None of the six
answer strings starts with a colon. One prompt (minimum wage, first paraphrase, paper's format):

| | ending A (`…Answer:`) | ending D (`…The answer is`) |
|---|---|---|
| most likely next token | a space, then the number (0.97) | a colon (0.77) |
| answer mass the readout sees | 0.98 | 0.08 |
| greedy decode | ` 3` | `: 3).` |

**Across all issue rows:**
- Over the 136 issue rows at the paper's format, colon tokens take 0.83 of the first-token probability. The readout
  sees an answer mass of 0.07, and 55 rows are below 0.05.
- All 144 decodes are a colon followed by a number. The number is the same as under ending A for 137 of 144 prompts.
- The 7% the readout sees is not a fair sample: its top option matches the written answer in 5 to 24 of the 24
  prompts of a decode cell, against 22–24 under ending A.

**Why the coverage check missed it.** The check looks only at the first token and asks whether it is answer-like after
stripping punctuation. A bare colon strips to nothing, so the check treated the 77% as "not an answer" and returned
"captured".

**What it means.**
- **Ending D's answer mass (0.07), anchor D (0.25) and C (0.34)** are not measurements of the model. They are reported
  as not measured, not as "the model does not answer".
- **The decodes suggest that** the base model answers under ending D as it does under ending A.
- **Scope:** only H1c (exploratory) is affected. No stage comparison uses ending D, and it was not re-run.
- **What would have prevented it:** colon-led answer strings for that ending, or a coverage check that looks one token
  further. Neither was in the plan, although the plan named D as the ending most likely to fail.

## 3. Post-hoc analyses (not pre-registered)

Everything in this section was chosen after the registered results had been seen, to explain them. Script:
`scripts/olmo2_posthoc.py`; tables with CIs: [olmo2_posthoc.md](olmo2_posthoc.md).

### 3.1 One set of stances, four scales

Reference cell, means over the 17 issues:

| stage | mean agreement | mean \|d\| | mean \|d_LO\| | C | mean \|d_rel\| | issues called in d | issues called in d_LO |
|---|---|---|---|---|---|---|---|
| base | 0.61 | 0.03 | 0.13 | 0.54 | 0.25 | 0 | 0 |
| SFT | 0.82 | 0.06 | 0.44 | 0.68 | 0.65 | 3 | 8 |
| DPO | 0.95 | 0.04 | 0.95 | 1.95 | 0.48 | 2 | 10 |
| Instruct | 0.96 | 0.03 | 1.10 | 1.92 | 0.57 | 0 | 12 |

("Called" means the CI excludes 0, |value| ≥ 0.10 in d or ≥ 0.4 in d_LO, and BH at q = 0.01 over the 19 axes. No null
issue is called on either scale.)

- **From SFT to Instruct:** stances in log-odds grow 2.5 times, while in probability they halve.
- **The reason is saturation.** When a stage agrees with nearly every statement, the difference in agreement between
  two opposite statements is squeezed toward zero, however strongly the stage prefers one of them.
- **The paired difference d** cancels an additive agreement bias, which is why the panel used it. It cannot undo a
  ceiling.
- **So whether a survey "finds opinions" in a post-trained model depends on the scale it is read on.** On the paper's
  own probability scale, Instruct states no opinion on any of the 17 issues. In log-odds it states 12.

### 3.2 What the H5a contradiction consists of

| pair | growth of d_LO (least-squares slope, 17 issues) | growth of C | uniform change of d_rel | issues changing beyond the uniform rescaling |
|---|---|---|---|---|
| SFT → DPO | ×2.15 [2.07, 2.22] | ×2.88 [2.62, 3.10] | ×0.75 [0.68, 0.81] | energy |
| DPO → Instruct | ×1.11 [1.10, 1.13] | ×0.98 [0.97, 1.00] | ×1.13 [1.12, 1.14] | none |

**SFT → DPO:**
- Every large stance roughly doubles in log-odds, while the separation of facts almost triples. Divided, every d_rel
  shrinks by about a quarter.
- The H5a margin is a fixed ±0.2, so a uniform 25% shrink crosses it only for the strongest stances: state
  surveillance (−1.49 → −1.07) and trans athletes (1.80 → 1.39).
- After removing the uniform part, their remaining changes are +0.04 and +0.05, inside the margin.
- **Energy is the one real exception.** Its stance grows only ×1.38 in log-odds, against ×2.1–2.8 for the other
  strong stances. That leaves a change of −0.28 [−0.35, −0.21] in d_rel beyond the uniform shrink: the
  renewables-mandate lean weakens relative to the others.
- No direction flips.

**Two readings the design cannot tell apart:**
- **(a)** DPO moderates stated stances relative to factual knowledge by about a quarter.
- **(b)** DPO sharpens factual confidence more than opinion confidence. In that case d_rel's working assumption (that
  confidence scales facts and opinions alike) fails, and the stances are unchanged apart from energy.

**DPO → Instruct:** a small uniform increase (×1.13) and no issue-specific change, as expected from RLVR trained on
math alone.

### 3.3 H2a combined two effects

From the label effects of Section 1.3 (log units, 95% CI over items):

| stage | moderation within a side: ((D − SD) + (A − SA)) / 2 | agree-side preference: ((A + SA) − (D + SD)) / 2 |
|---|---|---|
| base | +0.28 [+0.26, +0.30] | +0.36 [+0.29, +0.42] |
| SFT | +0.47 [+0.43, +0.51] | +0.60 [+0.46, +0.73] |
| DPO | +0.79 [+0.70, +0.91] | +0.82 [+0.55, +1.11] |
| Instruct | +0.89 [+0.79, +1.02] | +0.95 [+0.68, +1.25] |

- **Both effects grow with each stage, and they are about the same size.**
- H2a compared Disagree with Strongly agree, across sides. The agree-side preference lifts Strongly agree to
  Disagree's level, so the test fails even though moderation is clearly present.

### 3.4 H3: the gap is largest where the numbers contradict their usual meaning

C with pinned vs listed numbering, order by order (forcing 3):

| stage | reversed: pinned / listed | scrambled: pinned / listed | scrambled2: pinned / listed |
|---|---|---|---|
| SFT | 1.36 / 0.50 | 0.71 / 0.45 | 0.45 / 0.35 |
| DPO | 3.41 / 0.92 | 1.73 / 0.78 | 1.47 / 1.19 |
| Instruct | 3.39 / 0.99 | 1.24 / 0.85 | 1.61 / 1.21 |

- **The registered label is "salience":** pinned numbering makes the content count for more.
- **An alternative reading.** The post-trained stages answer with a number and partly use its usual Likert meaning
  (1 = disagree … 4 = agree).
  - With listed numbering in a non-paper order, the printed number contradicts that meaning, which blurs the content
    signal.
  - The gap is largest in the reversed order, where every printed number means the opposite of its usual meaning.
  - In the two scrambled orders, two of the four numbers do.
- This design cannot separate the two readings.

### 3.5 Base vs SFT: the same directions, smaller

- **Same sign on 15 of 17 issues.** The exceptions are property tax and unions, both small in the base model.
- **Size:** the base model's mean |d_LO| is 0.13, against 0.44 for SFT (×3.3 [3.1, 3.5]). In d_rel the ratio is ×2.6.
- **What the base model already leans on:** building transit (+0.35 in d_LO), trans-inclusive leagues (+0.29) and
  limiting surveillance (−0.29).
- **What SFT adds:** stances the base model barely holds:

  | issue (d_LO) | base | SFT |
  |---|---|---|
  | renewables mandate | 0.01 | 0.72 |
  | decriminalising drugs | 0.06 | 0.73 |
  | vaccine mandates | 0.06 | 0.53 |
  | voting access | 0.15 | 0.67 |

- **Where the base model leans more than SFT:** abortion (+0.17 vs +0.05) and property tax (−0.16, toward the cut,
  vs +0.05).

### 3.6 Survival under re-ordering and forcing

The panel's survival ladder, re-run with d_LO in place of d, is in [REPORT_survival.md](REPORT_survival.md).

## What this means for the question

**Are there differences across the OLMo 2 checkpoints?** Yes, at every step, but of different kinds.

- **Base → SFT.** In the completion format, the base model already answers (0.97) and faintly holds the later stance
  pattern (ρ 0.57, 15 of 17 signs), at a third of SFT's size. SFT amplifies it, adds stances the base model barely
  holds, and starts the agree-side and lower-line pulls.
- **SFT → DPO.** The largest change in confidence:
  - the facts are separated almost three times as strongly;
  - stances in log-odds double;
  - agreement saturates (0.82 → 0.95).
  
  By the registered rule, the stated directions change (H5a contradicted). Read post hoc, the change is a uniform
  rescaling relative to the facts, plus one issue (energy) that weakens. Directions and ranks hold.
- **DPO → Instruct (RLVR, math only).** Nothing changes beyond a small uniform increase. That is the expected null,
  and it holds.

**For the response to Röttger et al.** On the paper's own scale (agreement probabilities at its standard layout),
post-training appears to remove opinions: Instruct agrees with nearly everything and states no direction. In log-odds,
the same rows show the strongest and most layout-stable stances of the four stages ([REPORT_survival.md](REPORT_survival.md)).
How the answer is read decides whether a forced-choice survey finds a "spinning arrow" or a fixed position.

## Limitations

- **One family, one size.** Every claim is about OLMo 2 7B. Be cautious about generalising to other model families or
  sizes. RLVR here used math data only, so its null says nothing about RLVR with other rewards.
- **Narrow uncertainty.** The CIs come from four paraphrase clusters, so they describe these 34 statements, not the
  topics in general, and they understate the uncertainty.
- **d_rel's assumption.** d_rel assumes that confidence scales facts and opinions alike. Section 3.2 shows the main
  case where that matters.
- **Ending D** was not measured (Section 2).
- **Post-hoc sections** were chosen after seeing the data. Section 3.4's alternative reading is an interpretation,
  not a test.
- **No comparison with the 19-model panel.** The panel ran with chat templates, and the v2 plan excludes the
  comparison (§8). OLMo 2 has no conjoint data, so the stated-vs-revealed test is not available.
- **The superseded v1 run** (`results/olmo2/`, chat template) is not reported as findings. v1 and v2 differ in more
  than the format, so their difference is not an effect of the format.

## Reproduce

```
bash run_olmo2_v2.sh                      # GPU pod: the seven runs, gates, ladder, olmo2_compare, olmo2_explore (~1.5 h incl. downloads)
python3 scripts/olmo2_posthoc.py          # CPU: Section 3 -> results/olmo2_v2/olmo2_posthoc.{md,json}
python3 scripts/plot_olmo2.py             # CPU: results/olmo2_v2/olmo2_figure.png
```

The raw rows are in `raw/` (gzip JSONL, one row per prompt with the log-probability of every answer string and the 20
most likely first tokens, plus the greedy decodes). On Windows, set `PYTHONUTF8=1` before running the analysis scripts.
