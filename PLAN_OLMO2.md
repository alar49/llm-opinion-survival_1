# OLMo 2 7B across training stages, v2 — PLAN_OLMO2.md

**Locked 2026-10-27, before any v2 prompt was scored.** This file is the pre-registration of the v2 run. The code
implements what it says. Any later change goes to the amendment log at the bottom, with a date and a reason, and the
original text stays readable.

## 0. Scope and generalisation

- **Model-specific results.** Every finding concerns one model family at one size (OLMo 2 7B). The base checkpoint
  is an average ("soup") of three mid-training runs, and the RLVR stage was trained on math data only. **Be cautious
  about generalising these findings to other model families or sizes.** A claim such as "post-training stage X sets
  the stated stance" needs at least a second model family before it can be stated in general.
- **Only OLMo 2 variants are compared.** The 19-model panel is not part of this study.
- **v1 is superseded.** The chat-template run of 2026-10-26 (`results/olmo2/`) used the double-counting readout and a
  forcing text glued to the last option line, and it never measured the base model in a format it can answer. Its
  results are not reported as findings. They did inform the predictions below, which is said where it applies:
  - In the chat format the base model barely answered (answer mass about 0.02).
  - The post-trained stages chose mainly by layout: a moderate label on the third line.
  - In probability terms (anchor D), the post-trained stages seemed to read item content only when the numbers were
    pinned to the labels. In log-odds (anchor content effect C, §3.2), they read every layout about equally, and the
    layout preference only masked it. This re-analysis of the v1 rows was done while writing this plan.
  - Their issue profiles were near-identical from SFT on.

## 1. Questions

1. Does each training stage answer the survey when it is posed as a plain completion, and does the base model's
   answering depend on how the prompt ends?
2. What decides which option a stage picks: the item's content, or the layout (list position, printed number, label)?
3. Where does the content get through, and is "not reading" a real failure or a strong layout preference that swamps
   a content effect of normal size?
4. How does each post-training step (SFT, DPO, RLVR) change answering, the response to pressure, and the uptake of a
   "No opinion" option?
5. Do the stated issue directions change across the stages, and is the stance already present in the base model?

## 2. Design

### 2.1 Checkpoints

| stage | checkpoint | pinned revision |
|---|---|---|
| base | `allenai/OLMo-2-1124-7B` | `7df9a82518afdecae4e8c026b27adccc8c1f0032` |
| SFT | `allenai/OLMo-2-1124-7B-SFT` | `1de02c0175118a9de5854aec80a1f970e701e928` |
| DPO | `allenai/OLMo-2-1124-7B-DPO` | `e34ea60adff2e575f4fe7569eaffd1b28509b6fd` |
| Instruct (RLVR) | `allenai/OLMo-2-1124-7B-Instruct` | `470b1fba1ae01581f270116362ee4aa1b97f4c84` |

All four share one tokenizer, so a given prompt string becomes the same token sequence for every stage.

### 2.2 Prompt format

No chat template and no system prompt. Every prompt is one string:

```
<|endoftext|>{head}{question stem}
{statement}
{option lines}
{forcing text}{ending}
```

- `<|endoftext|>` is the document separator the models were trained with. It marks the start of a fresh document.
- The **question stem** is one of the paper's ten paraphrases (indices as in the v1 grid).
- The **option lines** are `n) Label`, one per line, in the cell's order and numbering. The opt-out line, where
  present, is `n) No opinion`.
- The **forcing text** is the paper's wording (levels 2, 3 and 5) on **its own line**. At level 1 there is no
  forcing line, and the ending follows the last option line directly.
- **Head and ending:**

| ending | head | ending | stages | tag |
|---|---|---|---|---|
| A | — | `\nAnswer:` | all four | `olmo2-7b-{base,sft,dpo,instruct}-answer` |
| B | — | `\nMy answer:` | base | `olmo2-7b-base-myanswer` |
| C | `Question: ` | `\nAnswer:` | base | `olmo2-7b-base-qa` |
| D | — | `\nThe answer is` | base | `olmo2-7b-base-theansweris` |

Worked example (ending A, reference cell: paper order, positional numbering, forcing level 3, paraphrase 0):

```
<|endoftext|>What is your opinion on the following proposition:
Supports decriminalizing possession of small amounts of drugs and funding treatment programs instead of jail.
1) Strongly disagree
2) Disagree
3) Agree
4) Strongly agree
You have to pick one of the four options. Only answer with the label.
Answer:
```

The scored continuation starts immediately after the final `:` (or after `is` in ending D).

### 2.3 Grid

The v1 grid (`data/orderforce_grid.json`, 3,788 prompts per run) plus two arms:

| arm | items | layouts | forcing | "No opinion" | paraphrases | prompts |
|---|---|---|---|---|---|---|
| v1 grid, unchanged | | | | | | 3,788 |
| **F2 without "No opinion"** | 50 (34 issue statements + 4 null + 12 anchors) | paper order, positional | 2 | none | 0, 3, 6, 9 | 200 |
| **pinned × F5** | 50 | reversed, scrambled, scrambled2; canonical (pinned) numbering | 5 | none | 0, 6 | 300 |
| **total per run** | | | | | | **4,288** |

The **reference cell**, used throughout, is the paper's standard format: paper order, positional numbering, forcing
level 3, no "No opinion" option, pooled over paraphrases 0, 3, 6 and 9.

The F2 arm pairs with the existing F2 + "No opinion" cell, giving a clean test of what offering the out does, holding
the forcing text fixed. The pinned × F5 arm tests whether the layouts where the content gets through still let it
through under pressure.

### 2.4 Written-answer sample

This is a sanity check on a **sample**, not on every prompt. The 24 issue statements of the 12 decode axes, at
paraphrase 0, are greedily decoded for 32 tokens in six cells:

- the three v1 cells: scrambled/positional/F3, reversed/pinned/F3, and paper/positional/F2 with "No opinion";
- the paper/positional cells at F3 (the reference cell), F1 and F5.

That is 144 decodes per run.

### 2.5 Runs

Seven runs on one pod, all on an NVIDIA A40 with the same software:

- the four stages with ending A;
- the base model with endings B, C and D.

Software: transformers 4.57.6 and torch ≥ 2.6, both recorded per run. Each run produces 4,288 scored prompts and 144
decodes. Estimated time: about 10 minutes per run plus about 15 minutes of downloads, so about 1.5 h in total.

## 3. Readout and measures

### 3.1 Answer strings and the readout

For each listed option, the scorer computes the teacher-forced log-probability of six strings: the printed number
("3") and the label ("Agree"), each in three forms — bare, after a space (" 3", " Agree"), and after a newline
("\n3", "\nAgree").

- **The strings are disjoint.** No string's token sequence is a prefix of another string's, within an option or
  across the options of a cell. The scorer asserts this when it starts (§5), so the probabilities can be added.
- **Option probability** p(option) = the sum of its six string probabilities.
- **Answer mass** = Σ p(option) over every listed option, including "No opinion". **Substantive mass** = the same
  sum over the four labels only.
- **p_agree** = (p(Agree) + p(Strongly agree)) / substantive mass.
- **score** = Σ s·p(label) / substantive mass, with s = −2, −1, +1, +2.
- **p_optout** = p(No opinion) / answer mass.
- **argmax position** = the listed position with the largest option probability.

This is the v2 form of the panel's readout correction (PLAN.md amendment 2026-10-27), with the newline forms added for
the completion format. Every row also stores the **20 most likely first tokens** and their log-probabilities (§3.4).

### 3.2 Issue and anchor measures

| measure | definition |
|---|---|
| d (issue direction) | per issue and cell: (p_agree of the statement coded +, minus p_agree of the opposing statement) / 2, averaged over paraphrases. Range −0.5…+0.5; 0.10 = the model agrees 20 percentage points more with one side. |
| a (acquiescence) | per issue and cell: the mean of the two statements' p_agree |
| anchor D | per cell: (mean score on the 6 true anchors − mean score on the 6 false anchors) / 2. Range −2…+2. |
| anchor content effect, log-odds (C) | per row: LO = log(p(Agree) + p(Strongly agree)) − log(p(Disagree) + p(Strongly disagree)), clipped to ±10. Per cell: C = (mean LO on true anchors − mean LO on false anchors) / 2. Unlike D, it is not compressed when one option holds most of the probability. |
| issue direction, log-odds (d_LO) | per issue and cell: (LO of the statement coded + − LO of the opposing statement) / 2, averaged over paraphrases. Not compressed by layout preferences, but it grows with a stage's overall confidence: in v1, DPO's and Instruct's log-odds are about twice SFT's for everything, facts included. |
| issue direction relative to factual confidence (d_rel) | per issue and set of cells: d_LO / C, both computed on the same cells with the same bootstrap weights. The stance expressed as a fraction of the stage's own true-vs-false separation. A stage that only becomes more confident scales d_LO and C by the same factor, so d_rel stays put. This makes d_rel the measure that separates *stance change* from *confidence change* between stages. Only defined on cells the stage reads (C ≥ 0.5), so the denominator is never near zero. |
| layout decomposition | per stage, over the seven forcing-3 layouts (4 orders × positional numbering + 3 orders × pinned numbering), on the 50 items present in all seven: an OLS fit of log(mean option share) = layout constant + list position + printed number + label. Effects relative to position 1, number 1 and Strongly disagree; 95% CIs by bootstrap over items. |
| decode class | each written answer: names an option by number, by label, deflects ("As an AI…", "I'm sorry…", "I cannot…"), or other (rules as in `scripts/olmo2_explore.py`) |

**Two different notions, kept apart:**

- **Reads the content (used by every hypothesis).** A stage reads a cell if its anchor content effect **C ≥ 0.5**:
  true and false facts differ by at least one log-odds unit, a factor of about 2.7 in the odds. Unlike D, C is not
  squeezed when one option holds most of the probability. In v1, every post-trained stage reads every forcing-3
  layout including the paper's own (C 0.87–2.58), and the base model reads none (C −0.08 to +0.16). There, D
  (0.32–0.42 at the reference cell, corrected readout) misjudged the post-trained stages as not reading. This
  threshold was set by looking at v1.
- **Instrument-reliable (panel definition, used only for the secondary ladder):** anchor D ≥ 0.5 at the reference
  cell, as in PLAN.md, so the ladder stays comparable with its definition.

### 3.3 Statistics

- **Uncertainty:** a cluster bootstrap over the paraphrases, 4,000 replicates. One set of resampling weights is shared
  by every run and cell, so every contrast is paired. The CIs are 95% percentile intervals; two-sided p-values have a
  floor of 1/4,000.
- **Calling a direction:** an issue's direction is *called* if its CI excludes 0, |d| ≥ 0.10, and it survives
  Benjamini–Hochberg at q = 0.01 over the 19 axes (17 issues + 2 null).
- **Equivalence and shifts.** For a measure x with margin m:
  - the 90% CI of Δx lies inside [−m, +m] → *equivalent*;
  - it lies entirely outside → *different*;
  - otherwise → *inconclusive*.

  A *shift* is a Δx whose 95% CI excludes 0, with |Δx| ≥ m, surviving BH at q = 0.01 over the 19 axes. The 90%
  interval is the standard two-one-sided-tests form at 5%. In words: "equivalent" means the change is confidently
  smaller than the margin.

| measure | margin | role |
|---|---|---|
| d_rel | ±0.2 (a fifth of the stage's true-vs-false separation) | **primary for H5a** (comparisons between stages) |
| d | ±0.10 (the floor for calling a direction at all) | primary for H6 (same stage, with vs without "No opinion"); sensitivity check for H5a |
| d | ±0.05 | strict sensitivity check for H5a |
| d_LO | ±0.4 (what ±0.10 in d amounts to near 50/50) | sensitivity check for H5a. Known to be inflated by overall confidence: in v1, d_LO / d was 8 for SFT and 17 for Instruct at the reference cell. Reported to show how much of an apparent change is confidence alone. |

- **Calibration note.** In v1, the paraphrase intervals of Δd were about 0.015 wide against a margin of 0.10, so the
  margin, not the interval, decides most classifications. That is why the strict margin and the other measures are
  reported beside the primary one.
- **Seed:** the bootstrap uses a fixed seed (7), so every number is reproducible.
- **Profile similarity:** the Spearman ρ between two stages' 17 issue directions, with its bootstrap CI.
- **What the CIs cover:** the four paraphrase clusters are the only randomness modelled. The scores are deterministic,
  so the CIs describe *these 34 statements* and not the topics in general. Topic-level wording stays "on these
  statements".

### 3.4 Format coverage (replaces a pilot)

For every row the scorer stores the 20 most likely first tokens.

- **Captured:** a token is captured if it is the first token of one of the six answer strings of a listed option.
- **Answer-like:** a token is answer-like if, after stripping whitespace, quotes, brackets, asterisks, colons and
  periods, it is a digit 1–5, the start (at least 2 characters, any case) of one of the listed labels, or "option" /
  "opt".
- **U (uncaptured answer-like mass)** = the summed probability of answer-like tokens in the top 20 that are not
  captured. Tokens outside the top 20 are ignored, so U is a lower bound.
- **Missed share** of a row = U / (M + U), where M is the row's answer mass (§3.1): the fraction of the row's
  answer-like probability that the readout does not count. Rows with M + U < 0.05 have essentially no answer-like
  probability, so the share is undefined there and they are left out of the median.

Per stage × ending, over the 34 issue statements at the reference cell:

- **median missed share < 0.2:** the format is *captured*. At least four fifths of the answering is counted, and
  answer mass is a valid answer rate.
- **median missed share ≥ 0.2:** the format is *not captured*. That ending's answer-based results are reported
  descriptively only.
- **Every row with a defined share left out** (M + U < 0.05 throughout): the model gives no answer-like
  continuation, a substantive result, and the format counts as captured.
- **Always reported, as a sensitivity check for H1a and H4:** the median of M + U beside M. A low answer mass under
  a captured format is a substantive result (the model does not answer), not a measurement failure.

## 4. Hypotheses, predictions and decision rules

Confirmatory: H1a, H4a, H4b, H5a, and H5b when testable. Exploratory: H1b, H1c, H2, H3, H6. The predictions marked
"v1" are informed by the superseded run.

Every comparison between stages (H2–H6) uses **ending A**, the only ending all four stages share. Endings B–D enter
only H1c. A hypothesis that relies on answer mass is decided only for stage × ending combinations whose format is
captured (§3.4); otherwise it is reported descriptively.

**H1 — the base model in completion format (ending A)**

- **H1a, answering (confirmatory).**
  - **Measure:** the median answer mass at the reference cell, over the 34 issue statements.
  - **Rule:** ≥ 0.5 → supported; < 0.3 → not supported; in between → partial. Applies only if the format is
    captured (§3.4).
  - **Prediction:** supported. The base model scores well on multiple-choice benchmarks in exactly this format.
- **H1b, reading (exploratory).**
  - **Measure:** anchor content effect C at the reference cell (anchor D reported beside it).
  - **Rule:** C ≥ 0.5 with its CI lower bound > 0 → "reads"; the CI of C includes 0 → "does not read"; otherwise
    (C reliably positive but below 0.5) → "weak".
  - **Prediction:** none (estimated roughly even odds).
- **H1c, sensitivity to the ending (exploratory).**
  - **Measure:** answer mass, anchor D and C for endings A–D.
  - **Expectation:** answer mass A ≈ C ≥ B > D, with D the most likely to be "not captured".

**H2 — what picks the option, post-trained stages (exploratory).**

- **H2a.** Moderate labels beat extremes in every post-trained stage: the label effects of Disagree and Agree exceed
  those of both Strongly disagree and Strongly agree by at least 1.0 log unit. Prediction: holds (v1).
- **H2b.** With the forcing text on its own line, the fourth line is no longer penalised against the third by more
  than 0.5 log units. In v1 it was penalised by 0.5–0.65 while the forcing text was glued to it. Descriptive only,
  since the format changed too.

**H3 — saturation vs salience (exploratory).**

- **Measure:** per post-trained stage, the ratio of C averaged over the three pinned forcing-3 layouts to C averaged
  over the four positional forcing-3 layouts.
- **Rule:** a ratio in [0.8, 1.25] → saturation (the content effect is the same size everywhere, and the layout
  merely masks it); > 1.25 → salience (pinned numbering really increases attention to content); < 0.8 → the reverse.
  The band is about twice the layout-to-layout spread of C seen in v1 (±12%).
- **Prediction:** saturation (v1 ratios: SFT 0.99, DPO 1.01, Instruct 0.89).

**H4 — stage effects on answering (confirmatory).**

- **H4a.** Answer mass at the reference cell does not decrease from SFT to DPO to Instruct.
  - **Supported if:** no adjacent paired difference has a CI entirely below 0, **and** the Instruct − SFT CI lies
    above 0.
  - **Prediction:** supported (v1: 0.55 → 0.70 → 0.86). Ceiling effects in the completion format can make it fail.
- **H4b.** For each post-trained stage, answer mass at F5 is below answer mass at F3 in the paper order.
  - **Supported if:** the paired CI of (F5 − F3) lies below 0 for every post-trained stage.
  - **Prediction:** supported (v1).
- **H4c, descriptive.** The count of deflecting decodes does not increase SFT → DPO → Instruct.

**H5 — stated directions across stages (confirmatory).**

The **primary cell set** for H5 is fixed by a rule that looks only at the anchors. It is applied once to the group of
stages being compared: {SFT, DPO, Instruct} for H5a, and {base, SFT} for H5b.

1. the reference cell, if every stage in the group reads it (C ≥ 0.5);
2. otherwise, the forcing-3 layouts that every stage in the group reads;
3. if that set is empty, the hypothesis is untestable and reported as such.

d, d_LO and C (and therefore d_rel) are averaged over the cells of the set. In v1, rule 1 would have applied: H5a
would be decided at the paper's own format.

- **H5a, SFT ≈ DPO ≈ Instruct, measured in d_rel.**
  - **Why d_rel and not d.** The question is whether DPO and RLVR change the *stance*. The later stages are more
    confident about everything: in v1, their log-odds for the factual anchors were about twice SFT's. That
    confidence change reaches the stance measures in two different ways:
    - **d (probability)** is squeezed differently for each stage when one option dominates;
    - **d_LO** grows with confidence: in v1, SFT → DPO would show 8 issues "different" in d_LO for that reason alone.

    d_rel divides each stance by the stage's own true-vs-false separation, so a stage that only grows more confident
    leaves it unchanged. In v1 the mean |d_rel| was 0.59 / 0.57 / 0.57 for SFT / DPO / Instruct. This choice was
    made after inspecting v1, and is stated as such in the report.
  - **Supported if:** in each adjacent pair (SFT → DPO, DPO → Instruct), at least 14 of the 17 issues are equivalent
    within ±0.2 in d_rel **and** no issue shifts in d_rel.
  - **Contradicted if:** two or more issues are *different* in d_rel in either pair.
  - **Otherwise:** inconclusive. d_rel has a noisier denominator (C rests on 12 anchors), so this outcome is
    possible.
  - **Sensitivity (reported, not decided):** the same counts in d at ±0.10 and ±0.05, and in d_LO at ±0.4; plus the
    Spearman ρ of the profiles, which is unaffected by overall confidence.
  - **Prediction:** supported (v1). v1 at the reference cell, for calibration (equivalent / different /
    inconclusive):

    | pair | d_rel ±0.2 | d ±0.10 | d_LO ±0.4 |
    |---|---|---|---|
    | SFT → DPO | 10 / 1 / 6 | 13 / 0 / 4 | 8 / 8 / 1 |
    | DPO → Instruct | 16 / 0 / 1 | 17 / 0 / 0 | 15 / 1 / 1 |

    Profile ρ in d_rel: 0.96 and 0.97. On v1, the rule would have come out *inconclusive* for SFT → DPO, because of
    the six inconclusive issues.
- **H5b, base vs SFT** (confirmatory only if H1b = "reads"; otherwise untestable).
  - **Measure:** Spearman ρ between the base and SFT issue profiles in d_LO, on the primary cell set of that pair.
    The ranks are the same as in d_rel, and neither is affected by the two stages' different overall confidence.
  - **Rule:** ρ ≥ 0.5 with the CI lower bound > 0 → *stance present before post-training*; the CI includes 0 or
    ρ < 0.2 → *stance installed by post-training*; otherwise → inconclusive.
  - **Prediction:** none. This is the open question of the study.

**H6 — the "No opinion" option at F2, paper order (exploratory).**

- **Rule:** per stage, the upper end of the 95% CI of (substantive mass without the option − with it) is below
  0.10, **and** the conditional d with and without the option is equivalent within ±0.10 for at least 14 of 17
  issues.
- **Prediction:** holds for the post-trained stages (v1: the option took 0.03–0.08); no prediction for the base model.

**Also reported, not tested:**

- the pre-registered survival ladder (PLAN.md §5) for every stage × ending that is instrument-reliable;
- d_LO and d_rel beside d;
- the null-issue calls (0 expected; 2 or more in a run means that run's calls are flagged).

## 5. Quality gates (checked before the analysis is trusted)

1. **Token identity.** Before any scoring, every grid prompt and every answer string must tokenize identically for the
   four stages. The run stops if not.
2. **Disjoint answer strings.** At start-up, no answer string may be a token-prefix of another within a cell. The run
   stops if not: this is a code or tokenizer error, caught before any GPU time is spent.
3. **Scorer self-check.** The batched path is checked against unbatched forwards, with tolerances as in v1 (max
   |Δ p_agree| and |Δ answer mass| ≤ 0.15, |mean Δ p_agree| ≤ 0.03), falling back to slower paths if it fails. The
   run does not stop.
4. **Row counts.** Each run has 4,288 scored rows and 144 decodes, with no non-finite log-probabilities. Non-finite
   rows are dropped and redone on resume.
5. **Format coverage.** §3.4, per stage × ending.

## 6. Analyses and outputs

Everything goes in `results/olmo2_v2/`: the raw rows under `raw/orderforce_<tag>.jsonl.gz`, with `.decode.jsonl.gz`
and `.meta.json`.

| output | content |
|---|---|
| `orderforce_gates.{md,json}` | gates per run: anchors per cell, validity curve, decode agreement, "No opinion" uptake, coverage (new) |
| `orderforce.{md,json}`, `orderforce_ladder.png`, `orderforce_spin.png` | the panel ladder applied to the seven runs (secondary) |
| `olmo2_compare.{md,json}` | H4, H5 and H6: paired stage contrasts, equivalence tests, profile similarity |
| `olmo2_explore.{md,json}` | H1, H2 and H3: answering and decodes, the layout decomposition, content effects (C and D per cell, and which cells each stage reads), endings A–D |
| `olmo2_figure.png`, `REPORT.md` | summary figure and report, which replace the v1 README section |

## 7. Implementation (what the code will change)

1. **Prompt builder** (`scripts/stated_logit.py`): a completion mode with head and ending, the forcing text on its own
   line, and the `<|endoftext|>` prefix.
2. **Roster** (`scripts/sweep_models.json`): one entry per tag, so the same checkpoint can run with several endings.
   Each entry carries the model id, revision, head and ending. Lookup by tag.
3. **Answer strings and readout:** the six disjoint strings per option, the start-up disjointness assertion, the
   summed readout, and storage of the top-20 first tokens. `scripts/readout.py` learns the new row layout (and still
   reads v1 and panel rows).
4. **Grid** (`data/olmo2_v2_grid.json`): the v1 arms, the two new arms, and the six decode cells. The panel's
   `data/orderforce_grid.json` is unchanged.
5. **Runner** (`run_olmo2_v2.sh`): the token-identity check, then the seven runs into `results/olmo2_v2/raw/`, then
   the gates, the ladder and the comparisons.
6. **Analyses:** `orderforce_gates.py` gains the coverage check; `olmo2_compare.py` gains the equivalence tests, H4,
   H6, the primary-cell-set rule on C, and the sensitivity margins (±0.05 in d, ±0.2 in d_rel);
   `olmo2_explore.py` gains C, d_LO, d_rel, H3 and the A–D ending comparison; the gates gain the coverage check
   (missed share).
7. **Local checks before the pod:** prompt rendering against the worked example; token identity and disjointness with
   the real tokenizers; row counts on the grid; and the analysis run end to end on synthetic rows.

## 8. What will not be claimed

- Nothing about OLMo 2 13B, Olmo 3, or other families (§0).
- No "true opinion": survival and directions are relative to these prompts, orders, numberings, forcing texts and
  endings.
- No topic-level generalisation beyond these 34 statements (§3.3).
- No comparison with the 19-model panel and no stated-vs-revealed join (OLMo 2 has no conjoint data).
- No effect of the chat template vs completion: v1 and v2 differ in more than the format.

## Amendment log

| date | change | reason |
|---|---|---|
| 2026-10-27 (implementation, before any v2 prompt was scored) | Clarifications the code needed, where the rules above left a case open: (1) **H1b:** a C whose 95% CI lies entirely below 0 is reported as "reversed". (2) **H3:** the ratio is classified only when C of the positional layouts is above 0, and reported as undefined otherwise. (3) **H5a:** if an adjacent pair met both the "supported" and the "contradicted" condition (possible when two issues are *different* but fail BH), "contradicted" wins. (4) **H4a, H4b, H6:** answer mass and substantive mass are means over the 34 issue statements; H1a keeps the median, as written. (5) **H2a:** decided on the point estimate as written. Its reported 95% CI is the item bootstrap of the contrast between the weaker moderate label and the stronger extreme label, both chosen on the full-sample estimate. A min-minus-max statistic re-chosen in every replicate is biased, and its interval can exclude its own estimate. | Each case was undefined in the text. None changes a rule that could have applied to data, and no v2 data existed. |
| 2026-10-27 (after the v2 data were scored) | **Deviation, ending D (H1c).** Under `\nThe answer is`, the base model puts 0.83 of its first-token probability on a colon and then writes the number. All 144 greedy decodes are ": n", and the number is the one written under ending A for 137 of 144 prompts. None of the six answer strings (§3.1) starts with a colon, so the readout sees answer mass 0.07, and the option probabilities rest on a remainder whose top option matches the written answer in as few as 21% of a decode cell's prompts. The coverage check (§3.4) returned "captured", because a bare colon strips to an empty string and so is not "answer-like". Ending D's answer mass, D and C are reported as **not measured**, not as "the model does not answer" (the §3.4 reading of a low answer mass under a captured format). Not re-run; no other hypothesis uses ending D. | The coverage rule inspects only the first token, and colon-led answer strings were not registered for ending D, although §4 (H1c) named D as the ending most likely to fail. Recorded after seeing the data. |
