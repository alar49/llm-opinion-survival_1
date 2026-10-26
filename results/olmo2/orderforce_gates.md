# Order-forcing pilot gates (PLAN §4)

## olmo2-7b-base  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.02 (F1 0.03), median P(opt-out) 0.11 → PIVOT: refusal-gated-DK
- anchors: D reference -0.04 (FAIL), D canonical median -0.07 (numbering-limited)
- validity (valid mass) F1 0.03 → F3 0.01 → F5 0.02
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.00 (1/24 named; {'other': 23, 'label-inline': 1}) FAIL; reversed|canonical|3|none: — (0/24 named; {'other': 24}) FAIL; paper|positional|2|last: — (0/24 named; {'other': 24}) FAIL

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | -0.02 | -1.15 |
| paper|positional|1|none | 0.04 | -1.02 |
| paper|positional|2|first | 0.03 | -0.70 |
| paper|positional|2|last | -0.05 | -1.11 |
| paper|positional|3|none | -0.04 | -1.12 |
| paper|positional|5|none | -0.05 | -1.18 |
| reversed|canonical|3|none | -0.03 | -0.20 |
| reversed|positional|2|last | 0.10 | 1.27 |
| reversed|positional|3|none | 0.08 | 1.28 |
| scrambled2|canonical|3|none | -0.08 | -0.82 |
| scrambled2|positional|2|last | -0.02 | -0.45 |
| scrambled2|positional|3|none | -0.02 | -0.36 |
| scrambled|canonical|3|none | -0.07 | -0.22 |
| scrambled|positional|2|last | 0.06 | 0.55 |
| scrambled|positional|3|none | 0.06 | 0.50 |

## olmo2-7b-dpo  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.69 (F1 0.00), median P(opt-out) 0.04 → opt-out gate stands
- anchors: D reference 0.25 (FAIL), D canonical median 0.91 (OK)
- validity (valid mass) F1 0.01 → F3 0.70 → F5 0.24
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (20/24 named; {'number': 14, 'other': 4, 'label': 6}) OK; reversed|canonical|3|none: 1.00 (23/24 named; {'number': 23, 'other': 1}) OK; paper|positional|2|last: 1.00 (22/24 named; {'number': 22, 'other': 2}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.41 | -0.59 |
| paper|positional|1|none | 0.52 | -0.36 |
| paper|positional|2|first | 0.63 | 0.19 |
| paper|positional|2|last | 0.09 | 0.96 |
| paper|positional|3|none | 0.25 | 0.78 |
| paper|positional|5|none | 0.37 | 0.62 |
| reversed|canonical|3|none | 0.97 | -0.34 |
| reversed|positional|2|last | 0.02 | -1.06 |
| reversed|positional|3|none | 0.17 | -0.97 |
| scrambled2|canonical|3|none | 0.91 | 0.04 |
| scrambled2|positional|2|last | 0.65 | 0.25 |
| scrambled2|positional|3|none | 0.54 | 0.41 |
| scrambled|canonical|3|none | 0.77 | 0.62 |
| scrambled|positional|2|last | 0.06 | -0.83 |
| scrambled|positional|3|none | 0.41 | -0.54 |

## olmo2-7b-instruct  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.90 (F1 0.00), median P(opt-out) 0.03 → opt-out gate stands
- anchors: D reference 0.21 (FAIL), D canonical median 0.61 (OK)
- validity (valid mass) F1 0.01 → F3 0.85 → F5 0.51
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.96 (24/24 named; {'number': 16, 'label': 8}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.60 | -0.20 |
| paper|positional|1|none | 0.70 | -0.03 |
| paper|positional|2|first | 0.60 | 0.38 |
| paper|positional|2|last | 0.05 | 0.99 |
| paper|positional|3|none | 0.21 | 0.80 |
| paper|positional|5|none | 0.53 | 0.44 |
| reversed|canonical|3|none | 1.02 | -0.21 |
| reversed|positional|2|last | 0.03 | -1.07 |
| reversed|positional|3|none | 0.21 | -0.91 |
| scrambled2|canonical|3|none | 0.61 | 0.36 |
| scrambled2|positional|2|last | 0.62 | 0.31 |
| scrambled2|positional|3|none | 0.46 | 0.51 |
| scrambled|canonical|3|none | 0.54 | 0.71 |
| scrambled|positional|2|last | 0.07 | -0.88 |
| scrambled|positional|3|none | 0.49 | -0.48 |

## olmo2-7b-sft  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.61 (F1 0.01), median P(opt-out) 0.08 → opt-out gate stands
- anchors: D reference 0.24 (FAIL), D canonical median 0.60 (OK)
- validity (valid mass) F1 0.02 → F3 0.52 → F5 0.26
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (14/24 named; {'number': 14, 'other': 10}) OK; reversed|canonical|3|none: 0.95 (21/24 named; {'number': 21, 'other': 3}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 23, 'label': 1}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.21 | -0.76 |
| paper|positional|1|none | 0.33 | -0.35 |
| paper|positional|2|first | 0.47 | -0.03 |
| paper|positional|2|last | 0.11 | 0.94 |
| paper|positional|3|none | 0.24 | 0.79 |
| paper|positional|5|none | 0.28 | 0.64 |
| reversed|canonical|3|none | 0.67 | -0.10 |
| reversed|positional|2|last | 0.09 | -0.90 |
| reversed|positional|3|none | 0.22 | -0.71 |
| scrambled2|canonical|3|none | 0.53 | 0.18 |
| scrambled2|positional|2|last | 0.48 | 0.17 |
| scrambled2|positional|3|none | 0.42 | 0.29 |
| scrambled|canonical|3|none | 0.60 | 0.64 |
| scrambled|positional|2|last | 0.19 | -0.48 |
| scrambled|positional|3|none | 0.49 | -0.24 |

