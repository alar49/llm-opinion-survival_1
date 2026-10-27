# Which of OLMo 2's stated opinions survive re-ordering the options and forcing the answer?

**The repository's original question, asked of OLMo 2 7B at four training stages (v2 completion run, scored
2026-10-27).**

The main report, [REPORT.md](REPORT.md), follows the v2 pre-registration
([PLAN_OLMO2.md](../../PLAN_OLMO2.md)). This report reads the same rows the way the repository reads its 19-model
panel ([README](../../README.md), [PLAN.md](../../PLAN.md)): the spin budget, the paired directional readout, the
survival ladder and the "No opinion" out.

**How much of this is registered:**
- PLAN_OLMO2.md lists the panel's ladder as "also reported, not tested", so nothing here is a registered test of the
  OLMo study.
- The log-odds ladder (result 3) is post hoc.
- No number is set against the panel's. The panel answered through chat templates, these runs are plain completions,
  and the v2 plan rules the comparison out (§8).

> **Scope.** One model family at one size (OLMo 2 7B). Be cautious about generalising to other model families or
> sizes.

## Result

All four stages answered the same 4,288 token-identical prompts. The prompts end in "Answer:" and cover the 34
opposing-pair statements on 17 county-level issues, 4 null statements, 12 factual anchors and the 62 Political Compass
propositions. Across them, the grid varies:
- the **option order** (four orders);
- the **numbering** (following the list, or pinned to the labels);
- the **forcing level** (nothing appended, "Only answer with the label.", the paper's levels 3 and 5);
- an explicit **"No opinion"** option.

The answer is read from teacher-forced answer-string probabilities. Where a greedy decode names an option, it matches
the scorer's top option in 0.79–1.00 of the decodes per layout and stage.

1. **Re-ordering the options spins the raw stated answer far more than rewording does, and more at each stage.**
   - The mean range of an item's score (Likert −2…+2) across the four orders is 0.29 (base), 0.90 (SFT), 1.47 (DPO)
     and 1.60 (Instruct).
   - Across four paraphrases of the question it is 0.10–0.16, and across forcing levels 0.14–0.18.
   - The post-trained stages pick by list position and label: the lower lines and "Agree".
2. **The panel's instrument passes no stage, and its paired readout finds almost nothing.**
   - On the 12 factual anchors, the true-vs-false separation in score units is 0.37, 0.27, 0.25 and 0.15, under the
     reliability gate of 0.5.
   - Applied anyway, the ladder calls 0, 3, 2 and 0 issues at the paper's format, and none keeps its direction across
     the orders.
   - The reason is saturation. Post-trained OLMo 2 agrees with almost everything (mean agreement up to 0.96). The
     paired difference cancels an additive agreement bias, but it cannot undo a ceiling.
3. **Read in log-odds, a fixed set of topics survives (post hoc).** These are the same ladder rules, with the direction
   measured in log-odds (floor 0.4) and a layout counted as read when the anchors separate by C ≥ 0.5 log-odds.
   - **Survivors:** 5 issues for SFT and 6 each for DPO and Instruct survive everything.
   - **In all three post-trained stages:** state surveillance (limit it), drugs (decriminalise), transit (build) and
     trans athletes (inclusive leagues).
   - **From DPO on, also:** housing (allow fourplexes) and voting (expand access).
   - **Never called by any stage:** property tax, abortion, police funding, schools and unions.
   - The null issues are never called. The base model's stances are too weak to reach the floor.
4. **Survival and validity cannot be linked here.** The repository's validity test sets stated directions against the
   lean a model reveals in a candidate-choice conjoint, and no conjoint exists for OLMo 2.
5. **The "No opinion" out is rarely taken, and less at each stage.**
   - **Uptake:** the median probability of choosing it is 0.10, 0.07, 0.02 and 0.01.
   - **Directions:** offering it changes no issue's direction (17 of 17 equivalent within ±0.10 for every stage).
   - **Unforced answering:** in the completion format, every stage answers with nothing appended. Unforced answer mass
     is 0.99, 0.76, 0.91 and 0.92.

The panel's decision rule ([PLAN.md](../../PLAN.md) §8) is defined over instrument-reliable models. No stage is one,
so the rule cannot be evaluated; `orderforce.md` prints its default, "mixed".

## 1. Spin budget

Mean range of an item's score (Likert −2…+2) over the 34 issue statements, paraphrase-averaged, ending A:

| stage | across 4 orders (F3) | across 4 orders (F5) | numbering (pinned vs listed) | forcing (F1 / F3 / F5) | across 4 paraphrases |
|---|---|---|---|---|---|
| base | 0.29 | 0.22 | 0.29 | 0.18 | 0.16 |
| SFT | **0.90** | 0.68 | 0.29 | 0.15 | 0.10 |
| DPO | **1.47** | 1.22 | 0.47 | 0.14 | 0.12 |
| Instruct | **1.60** | 1.29 | 0.45 | 0.16 | 0.12 |

Where the probability goes, by list line (forcing 3, the four orders pooled):

| stage | line 1 | line 2 | line 3 | line 4 |
|---|---|---|---|---|
| base | 0.23 | 0.28 | 0.35 | 0.14 |
| SFT | 0.17 | 0.22 | 0.36 | 0.25 |
| DPO | 0.08 | 0.18 | 0.44 | 0.30 |
| Instruct | 0.06 | 0.19 | 0.38 | 0.38 |

- **Base:** it spreads its answers and favours line 3 a little.
- **Post-training:** each stage moves more of the probability to lines 3 and 4. In the paper's order those lines hold
  "Agree" and "Strongly agree", and a separate preference for the agree labels adds to the position pull (REPORT.md,
  Section 1.3).
- **So re-ordering the options moves the answer of DPO and Instruct by about one and a half Likert units,** roughly ten
  times as much as rewording the question.

## 2. The panel's ladder, as registered for the panel

Rungs (PLAN.md §5):
- **called:** the paired direction d at the paper's format has a 95% CI excluding 0, |d| ≥ 0.10, and survives BH at
  q = 0.01 over the 19 axes;
- **+order:** it keeps its direction across the read order and numbering layouts;
- **+forcing:** it keeps its direction at forcing level 5 and with "No opinion" offered;
- **survives all:** both.

A layout counts as read when its anchors separate by D ≥ 0.5 in score units.

| stage | reliable (anchor D ≥ 0.5 at the paper's format) | layouts read (of 7) | called | +order only | +forcing only | survives all |
|---|---|---|---|---|---|---|
| base | no (0.37) | 0 | 0 | 0 | 0 | 0 |
| SFT | no (0.27) | 1 | 3 | 0 | 3 | 0 |
| DPO | no (0.25) | 4 | 2 | 0 | 2 | 0 |
| Instruct | no (0.15) | 3 | 0 | 0 | 0 | 0 |

- **SFT's three calls:** state surveillance, transit and trans athletes. **DPO's two:** state surveillance and trans
  athletes.
- **All five** hold under forcing and the opt-out, but not across the orders.
- **The null issues** are never called.

**Why it finds so little.** d is a difference of agreement probabilities:

| stage | mean agreement with a statement | mean \|d\| over the 17 issues |
|---|---|---|
| base | 0.61 | 0.03 |
| SFT | 0.82 | 0.06 |
| DPO | 0.95 | 0.04 |
| Instruct | 0.96 | 0.03 |

When a stage agrees with nearly every statement, two opposite statements both sit near 1 and their difference
vanishes, however strongly the stage prefers one of them. The same ceiling squeezes the anchor separation D, which is
why no stage passes the reliability gate. In log-odds, the same stages separate the facts clearly: C = 1.95 for DPO and
1.92 for Instruct.

## 3. The same ladder in log-odds (post hoc)

The rules are those of Section 2, applied with:
- **d_LO in place of d:** the paired direction in log-odds of agreeing, with a floor of 0.4, which is what 0.10 in d
  amounts to near 50/50;
- **C ≥ 0.5 in place of D ≥ 0.5** as the reading gate per layout.

Re-run with d and D, the same code reproduces the registered ladder rung for rung (76 of 76). Script:
`scripts/olmo2_posthoc.py`, P7.

| stage | layouts read (of 7) | called | +order only | +forcing only | survives all |
|---|---|---|---|---|---|
| base | 2 | 0 | 0 | 0 | 0 |
| SFT | 4 | 8 | 0 | 3 | **5** |
| DPO | 7 | 10 | 0 | 3 | **6** |
| Instruct | 7 | 12 | 0 | 3 | **6** |

Rung per issue (d_LO at the paper's format in brackets where called):

| issue (+ position) | SFT | DPO | Instruct |
|---|---|---|---|
| state surveillance (+ expand) | survives all (−1.01) | survives all (−2.09) | survives all (−2.38) |
| trans athletes (+ trans-inclusive leagues) | survives all (+1.22) | survives all (+2.72) | survives all (+2.84) |
| transit (+ build transit) | survives all (+0.78) | survives all (+1.79) | survives all (+1.98) |
| drugs (+ decriminalise) | survives all (+0.73) | survives all (+1.56) | survives all (+1.83) |
| voting (+ expand access) | +forcing (+0.67) | survives all (+1.61) | survives all (+1.85) |
| housing (+ allow fourplexes) | not called | survives all (+0.93) | survives all (+0.96) |
| guns (+ loosen rules) | survives all (+0.46) | called (+1.09) | called (+1.39) |
| energy (+ renewables mandate) | +forcing (+0.72) | +forcing (+1.00) | +forcing (+1.07) |
| vaccines (+ mandate) | +forcing (+0.53) | +forcing (+1.23) | +forcing (+1.56) |
| minimum wage (+ raise) | not called | +forcing (+0.82) | +forcing (+0.71) |
| immigration (+ cooperate with ICE) | not called | not called | called (+0.62) |
| AI regulation (+ keep AGI open) | not called | not called | called (+0.43) |
| property tax, abortion, police funding, schools, unions | not called | not called | not called |
| fair month, sign colour (null) | not called | not called | not called |

The base model calls nothing: its largest |d_LO| is 0.35 (transit), under the floor.

**Reading the table:**
- **The survivors keep their direction everywhere it was tested:** across every layout the stage reads, at the
  paper's strongest forcing text, and with "No opinion" offered.
  - Four issues survive in all three post-trained stages and grow stronger at each step.
  - Voting and housing join from DPO on.
  - Guns survives only at SFT.
  - No called issue ever changes direction between stages.
- **Energy, vaccines and minimum wage** hold under forcing and the opt-out, but not across every order and numbering.
- **Guns** is called from SFT on, but from DPO on it fails both the order and the forcing rungs.
- **Five issues are never called by any stage.** Those are the topics on which OLMo 2 states no direction that this
  instrument can detect.

## 4. The base model's other endings

| ending | across 4 orders (F3) | across 4 paraphrases | anchor D, paper's format | C, paper's format | ladder in d: called / survives all |
|---|---|---|---|---|---|
| A `…\nAnswer:` | 0.29 | 0.16 | 0.37 | 0.54 | 0 / 0 |
| B `…\nMy answer:` | 0.52 | 0.20 | 0.43 | 0.58 | 2 / 0 |
| C `Question: …\nAnswer:` | 0.28 | 0.15 | 0.47 | 0.71 | 0 / 0 |
| D `…\nThe answer is` | not measured | not measured | not measured | not measured | — |

- **Endings A–C:** the base model's answers spin little under re-ordering, because it holds weak stances and only a
  mild position preference.
- **Ending D** was not measured: the model writes ": 3", which the readout does not capture (REPORT.md, Section 2).
  That is why the panel's ladder marks every issue "saturated" there.

## What this adds to the repository's answer

**For OLMo 2 7B, the spinning arrow is real on the raw answer, and post-training strengthens it.**
- Re-ordering the options moves a post-trained stage's answer by 0.9–1.6 Likert units.
- The panel's remedy is to score each issue as the difference between two opposing statements. At the paper's
  format, that remedy finds almost nothing in this model, because agreement is at its ceiling.

**Read in log-odds, the same rows show a fixed set of positions from SFT on.** They survive re-ordering, renumbering,
the strongest forcing text and the "No opinion" out:
- limit police surveillance;
- trans-inclusive leagues;
- build transit;
- decriminalise drugs;
- and from DPO on, expand voting access and allow fourplexes.

So for this model, whether the survey finds "some topics stable" or nothing at all depends on the readout scale, not
on the model.

## Limitations

- **One family, one size,** and no conjoint, so there is no stated-vs-revealed validity test.
- **The log-odds ladder is post hoc.** Its floor (0.4) and reading gate (C ≥ 0.5) come from the v2 plan's sensitivity
  margin and reading rule, not from a registered ladder.
- **Uncertainty:** the CIs come from four paraphrase clusters, so they describe these 34 statements, not the topics.
- **No comparison with the panel.** It was surveyed in a different prompt format.

## Reproduce

```
bash run_olmo2_v2.sh                      # GPU pod: scoring, gates, the panel's ladder (orderforce.md), olmo2_compare, olmo2_explore
python3 scripts/olmo2_posthoc.py          # CPU: the log-odds ladder (P7) and the other post-hoc tables
```

The spin budget, position shares and panel-ladder rungs come from [orderforce.md](orderforce.md) and
`orderforce.json`. The log-odds ladder comes from [olmo2_posthoc.md](olmo2_posthoc.md), P7.
