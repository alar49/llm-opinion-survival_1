# Order-forcing pilot gates (PLAN §4)

Readout: disjoint estimator (scripts/readout.py).

## olmo2-7b-base-answer  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.87 (F1 0.91), median P(opt-out) 0.10 → opt-out gate stands
- anchors: D reference 0.37 (FAIL), D canonical median 0.34 (numbering-limited)
- validity (valid mass) F1 0.99 → F3 0.97 → F5 0.96
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 0.98, median answer-like mass 0.98 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 0.92 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.56 | -0.13 | 0.79 |
| paper|positional|1|none | 0.69 | -0.15 | 1.03 |
| paper|positional|2|first | 0.30 | -0.18 | 0.42 |
| paper|positional|2|last | 0.44 | -0.08 | 0.59 |
| paper|positional|2|none | 0.45 | -0.12 | 0.61 |
| paper|positional|3|none | 0.37 | 0.04 | 0.54 |
| paper|positional|5|none | 0.24 | 0.01 | 0.31 |
| reversed|canonical|3|none | 0.39 | -0.29 | 0.55 |
| reversed|canonical|5|none | 0.22 | -0.31 | 0.30 |
| reversed|positional|2|last | 0.28 | 0.25 | 0.37 |
| reversed|positional|3|none | 0.29 | 0.23 | 0.38 |
| scrambled2|canonical|3|none | 0.24 | 0.09 | 0.34 |
| scrambled2|canonical|5|none | 0.15 | 0.17 | 0.20 |
| scrambled2|positional|2|last | 0.22 | -0.03 | 0.36 |
| scrambled2|positional|3|none | 0.22 | -0.19 | 0.35 |
| scrambled|canonical|3|none | 0.34 | 0.26 | 0.48 |
| scrambled|canonical|5|none | 0.24 | 0.01 | 0.30 |
| scrambled|positional|2|last | 0.17 | 0.24 | 0.22 |
| scrambled|positional|3|none | 0.15 | 0.40 | 0.23 |

## olmo2-7b-base-myanswer  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.90 (F1 0.91), median P(opt-out) 0.08 → opt-out gate stands
- anchors: D reference 0.43 (FAIL), D canonical median 0.38 (numbering-limited)
- validity (valid mass) F1 0.99 → F3 0.98 → F5 0.98
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 0.98, median answer-like mass 0.98 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.48 | -0.17 | 0.65 |
| paper|positional|1|none | 0.54 | -0.28 | 0.72 |
| paper|positional|2|first | 0.28 | -0.20 | 0.40 |
| paper|positional|2|last | 0.47 | -0.03 | 0.62 |
| paper|positional|2|none | 0.52 | -0.13 | 0.70 |
| paper|positional|3|none | 0.43 | 0.02 | 0.58 |
| paper|positional|5|none | 0.33 | -0.05 | 0.41 |
| reversed|canonical|3|none | 0.38 | -0.64 | 0.58 |
| reversed|canonical|5|none | 0.29 | -0.64 | 0.44 |
| reversed|positional|2|last | 0.28 | 0.28 | 0.38 |
| reversed|positional|3|none | 0.33 | 0.25 | 0.49 |
| scrambled2|canonical|3|none | 0.32 | -0.10 | 0.45 |
| scrambled2|canonical|5|none | 0.25 | -0.02 | 0.33 |
| scrambled2|positional|2|last | 0.22 | -0.09 | 0.35 |
| scrambled2|positional|3|none | 0.28 | -0.26 | 0.44 |
| scrambled|canonical|3|none | 0.38 | 0.13 | 0.49 |
| scrambled|canonical|5|none | 0.28 | -0.06 | 0.36 |
| scrambled|positional|2|last | 0.19 | 0.31 | 0.25 |
| scrambled|positional|3|none | 0.16 | 0.52 | 0.24 |

## olmo2-7b-base-qa  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.94 (F1 0.95), median P(opt-out) 0.05 → opt-out gate stands
- anchors: D reference 0.47 (FAIL), D canonical median 0.35 (numbering-limited)
- validity (valid mass) F1 1.00 → F3 0.98 → F5 0.97
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 0.99, median answer-like mass 0.99 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.56 | -0.03 | 0.80 |
| paper|positional|1|none | 0.68 | -0.12 | 1.02 |
| paper|positional|2|first | 0.34 | -0.27 | 0.51 |
| paper|positional|2|last | 0.48 | 0.12 | 0.71 |
| paper|positional|2|none | 0.51 | 0.01 | 0.77 |
| paper|positional|3|none | 0.47 | 0.09 | 0.71 |
| paper|positional|5|none | 0.17 | 0.18 | 0.21 |
| reversed|canonical|3|none | 0.35 | -0.35 | 0.53 |
| reversed|canonical|5|none | 0.11 | -0.33 | 0.16 |
| reversed|positional|2|last | 0.24 | 0.10 | 0.32 |
| reversed|positional|3|none | 0.32 | 0.13 | 0.44 |
| scrambled2|canonical|3|none | 0.33 | 0.17 | 0.50 |
| scrambled2|canonical|5|none | 0.12 | 0.10 | 0.14 |
| scrambled2|positional|2|last | 0.24 | 0.01 | 0.41 |
| scrambled2|positional|3|none | 0.30 | -0.15 | 0.50 |
| scrambled|canonical|3|none | 0.41 | 0.00 | 0.52 |
| scrambled|canonical|5|none | 0.15 | -0.09 | 0.18 |
| scrambled|positional|2|last | 0.19 | 0.16 | 0.20 |
| scrambled|positional|3|none | 0.20 | 0.38 | 0.25 |

## olmo2-7b-base-theansweris  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.07 (F1 0.03), median P(opt-out) 0.05 → PIVOT: refusal-gated-DK
- anchors: D reference 0.25 (FAIL), D canonical median 0.13 (numbering-limited)
- validity (valid mass) F1 0.03 → F3 0.07 → F5 0.05
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.04 over 82/136 rows with a share, median answer mass 0.06, median answer-like mass 0.06 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 0.46 (24/24 named; {'number': 24}) FAIL; reversed|canonical|3|none: 0.21 (24/24 named; {'number': 24}) FAIL; paper|positional|1|none: 0.71 (24/24 named; {'number': 24}) FAIL; paper|positional|5|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.58 (24/24 named; {'number': 24}) FAIL

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.21 | -0.91 | 0.34 |
| paper|positional|1|none | 0.24 | -1.14 | 0.43 |
| paper|positional|2|first | 0.10 | -0.71 | 0.16 |
| paper|positional|2|last | 0.20 | -0.91 | 0.32 |
| paper|positional|2|none | 0.24 | -0.93 | 0.39 |
| paper|positional|3|none | 0.25 | -0.52 | 0.34 |
| paper|positional|5|none | 0.25 | -0.35 | 0.32 |
| reversed|canonical|3|none | 0.15 | -1.12 | 0.27 |
| reversed|canonical|5|none | 0.15 | -1.02 | 0.24 |
| reversed|positional|2|last | 0.31 | 0.80 | 0.51 |
| reversed|positional|3|none | 0.47 | 0.48 | 0.69 |
| scrambled2|canonical|3|none | 0.08 | -0.78 | 0.10 |
| scrambled2|canonical|5|none | 0.08 | -0.63 | 0.08 |
| scrambled2|positional|2|last | 0.15 | -0.18 | 0.24 |
| scrambled2|positional|3|none | 0.20 | -0.24 | 0.32 |
| scrambled|canonical|3|none | 0.13 | -0.70 | 0.21 |
| scrambled|canonical|5|none | 0.11 | -0.73 | 0.18 |
| scrambled|positional|2|last | 0.13 | 0.37 | 0.23 |
| scrambled|positional|3|none | 0.16 | 0.43 | 0.29 |

## olmo2-7b-dpo-answer  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.98 (F1 0.90), median P(opt-out) 0.02 → opt-out gate stands
- anchors: D reference 0.25 (FAIL), D canonical median 0.91 (OK)
- validity (valid mass) F1 0.91 → F3 0.99 → F5 0.98
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 1.00, median answer-like mass 1.00 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 0.96 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 0.92 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.24 | 1.00 | 1.07 |
| paper|positional|1|none | 0.28 | 0.89 | 1.57 |
| paper|positional|2|first | 0.76 | 0.22 | 1.48 |
| paper|positional|2|last | 0.32 | 1.00 | 1.93 |
| paper|positional|2|none | 0.37 | 0.89 | 2.09 |
| paper|positional|3|none | 0.25 | 0.98 | 1.95 |
| paper|positional|5|none | 0.33 | 0.92 | 1.53 |
| reversed|canonical|3|none | 1.37 | -0.54 | 3.41 |
| reversed|canonical|5|none | 1.15 | -0.43 | 2.67 |
| reversed|positional|2|last | 0.38 | -0.76 | 0.66 |
| reversed|positional|3|none | 0.39 | -0.62 | 0.92 |
| scrambled2|canonical|3|none | 0.60 | 0.30 | 1.47 |
| scrambled2|canonical|5|none | 0.35 | 0.58 | 1.22 |
| scrambled2|positional|2|last | 0.53 | 0.05 | 0.96 |
| scrambled2|positional|3|none | 0.62 | -0.02 | 1.19 |
| scrambled|canonical|3|none | 0.91 | 0.18 | 1.73 |
| scrambled|canonical|5|none | 0.74 | -0.03 | 1.65 |
| scrambled|positional|2|last | 0.47 | -0.09 | 0.73 |
| scrambled|positional|3|none | 0.46 | -0.08 | 0.78 |

## olmo2-7b-instruct-answer  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.99 (F1 0.91), median P(opt-out) 0.01 → opt-out gate stands
- anchors: D reference 0.15 (FAIL), D canonical median 0.58 (OK)
- validity (valid mass) F1 0.92 → F3 1.00 → F5 0.99
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 1.00, median answer-like mass 1.00 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.14 | 1.19 | 0.96 |
| paper|positional|1|none | 0.19 | 1.06 | 1.58 |
| paper|positional|2|first | 0.88 | 0.28 | 1.94 |
| paper|positional|2|last | 0.17 | 1.14 | 2.15 |
| paper|positional|2|none | 0.19 | 1.08 | 2.29 |
| paper|positional|3|none | 0.15 | 1.19 | 1.92 |
| paper|positional|5|none | 0.22 | 1.07 | 1.38 |
| reversed|canonical|3|none | 1.37 | -0.52 | 3.39 |
| reversed|canonical|5|none | 1.09 | -0.35 | 2.50 |
| reversed|positional|2|last | 0.47 | -0.75 | 0.89 |
| reversed|positional|3|none | 0.44 | -0.71 | 0.99 |
| scrambled2|canonical|3|none | 0.33 | 0.65 | 1.61 |
| scrambled2|canonical|5|none | 0.17 | 0.81 | 1.28 |
| scrambled2|positional|2|last | 0.59 | 0.15 | 1.19 |
| scrambled2|positional|3|none | 0.57 | 0.17 | 1.21 |
| scrambled|canonical|3|none | 0.58 | -0.15 | 1.24 |
| scrambled|canonical|5|none | 0.56 | -0.25 | 1.46 |
| scrambled|positional|2|last | 0.46 | -0.30 | 0.87 |
| scrambled|positional|3|none | 0.40 | -0.36 | 0.85 |

## olmo2-7b-sft-answer  (4288 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.91 (F1 0.71), median P(opt-out) 0.07 → opt-out gate stands
- anchors: D reference 0.27 (FAIL), D canonical median 0.50 (numbering-limited)
- validity (valid mass) F1 0.76 → F3 0.93 → F5 0.84
- answer-string consistency: n/a (no nested strings scored)
- rows: 4288 scored (expected 4288), 144 decodes (expected 144), 0 with a non-finite log-prob → OK
- format coverage (reference cell, issue statements): median missed share 0.00 over 136/136 rows with a share, median answer mass 0.95, median answer-like mass 0.95 → captured
- decode vs logit argmax (named decodes): paper|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; scrambled|positional|3|none: 0.79 (24/24 named; {'number': 24}) FAIL; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|1|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|5|none: 0.88 (24/24 named; {'number': 24}) FAIL; paper|positional|2|last: 0.96 (24/24 named; {'number': 24}) OK

| anchors cell | D | A | C (log-odds) |
|---|---|---|---|
| paper|positional|1|last | 0.31 | 0.60 | 0.56 |
| paper|positional|1|none | 0.33 | 0.65 | 0.77 |
| paper|positional|2|first | 0.37 | 0.06 | 0.56 |
| paper|positional|2|last | 0.30 | 0.81 | 0.76 |
| paper|positional|2|none | 0.35 | 0.72 | 0.84 |
| paper|positional|3|none | 0.27 | 0.75 | 0.68 |
| paper|positional|5|none | 0.28 | 0.68 | 0.53 |
| reversed|canonical|3|none | 0.94 | -0.18 | 1.36 |
| reversed|canonical|5|none | 0.61 | 0.12 | 0.96 |
| reversed|positional|2|last | 0.36 | -0.27 | 0.51 |
| reversed|positional|3|none | 0.32 | -0.17 | 0.50 |
| scrambled2|canonical|3|none | 0.31 | 0.10 | 0.45 |
| scrambled2|canonical|5|none | 0.22 | 0.10 | 0.33 |
| scrambled2|positional|2|last | 0.20 | -0.06 | 0.31 |
| scrambled2|positional|3|none | 0.21 | -0.14 | 0.35 |
| scrambled|canonical|3|none | 0.50 | 0.23 | 0.71 |
| scrambled|canonical|5|none | 0.36 | 0.11 | 0.56 |
| scrambled|positional|2|last | 0.32 | 0.16 | 0.47 |
| scrambled|positional|3|none | 0.29 | 0.24 | 0.45 |

