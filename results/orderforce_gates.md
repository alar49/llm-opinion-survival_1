# Order-forcing pilot gates (PLAN §4)

Readout: disjoint estimator (scripts/readout.py).

## gemma-3-12b-it  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.76 (OK), D canonical median 1.77 (OK)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 1.00
- answer-string consistency: 38 of 797 checked extensions score above their prefix by > 0.3 nats (max excess +0.97) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.83 (24/24 named; {'number': 24}) FAIL; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.92 (24/24 named; {'label': 10, 'number': 14}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.03 | 0.97 |
| paper|positional|1|none | 0.37 | 1.63 |
| paper|positional|2|first | 1.24 | 0.56 |
| paper|positional|2|last | 1.88 | 0.12 |
| paper|positional|3|none | 1.76 | 0.14 |
| paper|positional|5|none | 1.88 | 0.09 |
| reversed|canonical|3|none | 1.98 | 0.02 |
| reversed|positional|2|last | 1.89 | 0.11 |
| reversed|positional|3|none | 1.92 | 0.08 |
| scrambled2|canonical|3|none | 0.81 | -1.16 |
| scrambled2|positional|2|last | 0.73 | -0.68 |
| scrambled2|positional|3|none | 1.75 | -0.08 |
| scrambled|canonical|3|none | 1.77 | -0.08 |
| scrambled|positional|2|last | 1.09 | -0.08 |
| scrambled|positional|3|none | 1.41 | -0.09 |

## gemma-3-1b-it  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference -0.28 (FAIL), D canonical median 0.13 (numbering-limited)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 0.99
- answer-string consistency: 281 of 2176 checked extensions score above their prefix by > 0.3 nats (max excess +5.37) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (24/24 named; {'number': 9, 'label': 15}) OK; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 20, 'label': 4}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | -0.14 | 0.94 |
| paper|positional|1|none | -0.37 | 0.74 |
| paper|positional|2|first | -0.71 | 0.21 |
| paper|positional|2|last | -0.17 | 1.02 |
| paper|positional|3|none | -0.28 | 1.10 |
| paper|positional|5|none | -0.22 | 1.24 |
| reversed|canonical|3|none | 0.13 | -1.09 |
| reversed|positional|2|last | 0.58 | -0.84 |
| reversed|positional|3|none | 0.71 | -0.69 |
| scrambled2|canonical|3|none | -0.55 | -0.65 |
| scrambled2|positional|2|last | 0.03 | 0.35 |
| scrambled2|positional|3|none | 0.09 | 0.42 |
| scrambled|canonical|3|none | 0.70 | -0.22 |
| scrambled|positional|2|last | 1.30 | -0.32 |
| scrambled|positional|3|none | 1.03 | -0.04 |

## gemma-3-27b-it  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.93 (OK), D canonical median 2.00 (OK)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 1.00
- answer-string consistency: 128 of 3773 checked extensions score above their prefix by > 0.3 nats (max excess +1.27) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (24/24 named; {'number': 10, 'label': 14}) OK; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.73 | 0.27 |
| paper|positional|1|none | 1.81 | 0.19 |
| paper|positional|2|first | 1.71 | 0.29 |
| paper|positional|2|last | 1.98 | 0.02 |
| paper|positional|3|none | 1.93 | 0.07 |
| paper|positional|5|none | 1.75 | 0.25 |
| reversed|canonical|3|none | 2.00 | 0.00 |
| reversed|positional|2|last | 1.90 | -0.05 |
| reversed|positional|3|none | 1.86 | -0.02 |
| scrambled2|canonical|3|none | 2.00 | 0.00 |
| scrambled2|positional|2|last | 1.29 | -0.29 |
| scrambled2|positional|3|none | 1.38 | -0.33 |
| scrambled|canonical|3|none | 1.92 | 0.08 |
| scrambled|positional|2|last | 1.26 | -0.23 |
| scrambled|positional|3|none | 1.28 | 0.07 |

## gemma-3-4b-it  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.07 (OK), D canonical median 0.99 (OK)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 1.00
- answer-string consistency: 178 of 4438 checked extensions score above their prefix by > 0.3 nats (max excess +1.54) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.92 (24/24 named; {'number': 19, 'label': 5}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 21, 'label': 3}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.94 | 0.23 |
| paper|positional|1|none | 1.11 | 0.16 |
| paper|positional|2|first | 1.29 | -0.29 |
| paper|positional|2|last | 1.14 | -0.20 |
| paper|positional|3|none | 1.07 | -0.20 |
| paper|positional|5|none | 1.16 | -0.16 |
| reversed|canonical|3|none | 1.19 | 0.23 |
| reversed|positional|2|last | 1.27 | 0.53 |
| reversed|positional|3|none | 1.02 | 0.80 |
| scrambled2|canonical|3|none | 0.17 | -1.67 |
| scrambled2|positional|2|last | 0.86 | -0.57 |
| scrambled2|positional|3|none | 0.64 | -0.75 |
| scrambled|canonical|3|none | 0.99 | 0.99 |
| scrambled|positional|2|last | 0.81 | 0.28 |
| scrambled|positional|3|none | 0.60 | 0.87 |

## gemma-4-E4B-it  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.11 (F1 0.00), median P(opt-out) 0.89 → PIVOT: refusal-gated-DK
- anchors: D reference 1.47 (OK), D canonical median 1.81 (OK)
- validity (valid mass) F1 0.00 → F3 0.86 → F5 0.62
- answer-string consistency: 2 of 4526 checked extensions score above their prefix by > 0.3 nats (max excess +0.35) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.67 (18/24 named; {'other': 6, 'number': 14, 'label-inline': 4}) FAIL; reversed|canonical|3|none: 0.87 (15/24 named; {'other': 9, 'number': 10, 'label-inline': 5}) FAIL; paper|positional|2|last: 0.96 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.40 | -1.28 |
| paper|positional|1|none | 0.36 | -1.17 |
| paper|positional|2|first | 1.49 | -0.47 |
| paper|positional|2|last | 1.66 | -0.20 |
| paper|positional|3|none | 1.47 | -0.29 |
| paper|positional|5|none | 1.27 | -0.26 |
| reversed|canonical|3|none | 1.44 | -0.47 |
| reversed|positional|2|last | 1.40 | -0.53 |
| reversed|positional|3|none | 1.46 | -0.42 |
| scrambled2|canonical|3|none | 1.86 | -0.12 |
| scrambled2|positional|2|last | 1.62 | -0.08 |
| scrambled2|positional|3|none | 1.72 | 0.04 |
| scrambled|canonical|3|none | 1.81 | -0.01 |
| scrambled|positional|2|last | 1.67 | -0.22 |
| scrambled|positional|3|none | 1.71 | -0.18 |

## gpt-oss-20b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.89 (F1 0.00), median P(opt-out) 0.10 → opt-out gate stands
- anchors: D reference 1.10 (OK), D canonical median 0.81 (OK)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 0.96
- answer-string consistency: 98 of 4460 checked extensions score above their prefix by > 0.3 nats (max excess +1.73) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.96 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.61 | -0.97 |
| paper|positional|1|none | 0.91 | -0.71 |
| paper|positional|2|first | 0.81 | 0.42 |
| paper|positional|2|last | 0.99 | 0.50 |
| paper|positional|3|none | 1.10 | 0.22 |
| paper|positional|5|none | 1.15 | 0.19 |
| reversed|canonical|3|none | 0.72 | 0.22 |
| reversed|positional|2|last | 1.36 | -0.04 |
| reversed|positional|3|none | 1.45 | 0.05 |
| scrambled2|canonical|3|none | 0.81 | 0.33 |
| scrambled2|positional|2|last | 0.84 | 0.04 |
| scrambled2|positional|3|none | 0.82 | 0.22 |
| scrambled|canonical|3|none | 0.91 | 0.42 |
| scrambled|positional|2|last | 1.08 | 0.02 |
| scrambled|positional|3|none | 1.09 | -0.09 |

## granite-4.2-8b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.65 (OK), D canonical median 0.48 (numbering-limited)
- validity (valid mass) F1 0.01 → F3 0.97 → F5 0.58
- answer-string consistency: 20 of 6186 checked extensions score above their prefix by > 0.3 nats (max excess +0.37) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (19/24 named; {'number': 19, 'other': 5}) OK; reversed|canonical|3|none: 0.96 (23/24 named; {'number': 23, 'other': 1}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.07 | -0.29 |
| paper|positional|1|none | 0.97 | -0.34 |
| paper|positional|2|first | 1.37 | -0.61 |
| paper|positional|2|last | 1.63 | 0.04 |
| paper|positional|3|none | 1.65 | 0.11 |
| paper|positional|5|none | 1.66 | -0.04 |
| reversed|canonical|3|none | 0.91 | -0.36 |
| reversed|positional|2|last | 1.87 | -0.12 |
| reversed|positional|3|none | 1.84 | -0.16 |
| scrambled2|canonical|3|none | 0.48 | -0.59 |
| scrambled2|positional|2|last | 1.46 | -0.17 |
| scrambled2|positional|3|none | 1.10 | -0.13 |
| scrambled|canonical|3|none | 0.41 | 0.13 |
| scrambled|positional|2|last | 1.31 | -0.39 |
| scrambled|positional|3|none | 1.45 | -0.33 |

## llama-3.2-3b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.94 (F1 0.00), median P(opt-out) 0.01 → opt-out gate stands
- anchors: D reference 1.10 (OK), D canonical median 0.89 (OK)
- validity (valid mass) F1 0.00 → F3 0.85 → F5 0.64
- answer-string consistency: 2 of 3942 checked extensions score above their prefix by > 0.3 nats (max excess +0.33) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.96 (23/24 named; {'number': 23, 'other': 1}) OK; reversed|canonical|3|none: 1.00 (20/24 named; {'number': 20, 'other': 4}) OK; paper|positional|2|last: 1.00 (6/24 named; {'other': 18, 'number': 6}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.74 | -0.05 |
| paper|positional|1|none | 1.05 | -0.26 |
| paper|positional|2|first | 0.66 | 0.14 |
| paper|positional|2|last | 0.82 | 0.31 |
| paper|positional|3|none | 1.10 | -0.21 |
| paper|positional|5|none | 1.08 | -0.16 |
| reversed|canonical|3|none | 0.54 | -0.26 |
| reversed|positional|2|last | 1.02 | -0.28 |
| reversed|positional|3|none | 1.05 | -0.15 |
| scrambled2|canonical|3|none | 0.89 | -0.14 |
| scrambled2|positional|2|last | 1.04 | -0.53 |
| scrambled2|positional|3|none | 1.21 | -0.36 |
| scrambled|canonical|3|none | 1.01 | 0.50 |
| scrambled|positional|2|last | 1.24 | 0.09 |
| scrambled|positional|3|none | 1.25 | 0.06 |

## llama8b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.95 (F1 0.00), median P(opt-out) 0.05 → opt-out gate stands
- anchors: D reference 0.80 (OK), D canonical median 0.87 (OK)
- validity (valid mass) F1 0.01 → F3 1.00 → F5 0.98
- answer-string consistency: 0 of 20976 checked extensions score above their prefix by > 0.3 nats (max excess +0.13) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.91 | 0.28 |
| paper|positional|1|none | 0.90 | 0.37 |
| paper|positional|2|first | 0.96 | -0.08 |
| paper|positional|2|last | 0.75 | 0.53 |
| paper|positional|3|none | 0.80 | 0.32 |
| paper|positional|5|none | 0.78 | 0.25 |
| reversed|canonical|3|none | 0.98 | -0.25 |
| reversed|positional|2|last | 1.15 | -0.56 |
| reversed|positional|3|none | 1.19 | -0.40 |
| scrambled2|canonical|3|none | 0.61 | 0.19 |
| scrambled2|positional|2|last | 1.27 | -0.34 |
| scrambled2|positional|3|none | 1.20 | -0.48 |
| scrambled|canonical|3|none | 0.87 | 0.10 |
| scrambled|positional|2|last | 0.94 | 0.78 |
| scrambled|positional|3|none | 1.02 | 0.71 |

## ministral-3-14b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.59 (F1 0.31), median P(opt-out) 0.26 → opt-out gate stands
- anchors: D reference 0.76 (OK), D canonical median 0.38 (numbering-limited)
- validity (valid mass) F1 0.30 → F3 0.77 → F5 0.74
- answer-string consistency: 0 of 36103 checked extensions score above their prefix by > 0.3 nats (max excess +0.17) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.83 (24/24 named; {'number': 24}) FAIL; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.92 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.37 | 0.09 |
| paper|positional|1|none | 0.42 | 0.16 |
| paper|positional|2|first | 0.37 | -0.18 |
| paper|positional|2|last | 0.55 | 0.07 |
| paper|positional|3|none | 0.76 | 0.17 |
| paper|positional|5|none | 0.81 | 0.46 |
| reversed|canonical|3|none | 0.38 | -0.18 |
| reversed|positional|2|last | 0.84 | -0.26 |
| reversed|positional|3|none | 0.97 | -0.39 |
| scrambled2|canonical|3|none | 0.45 | -0.18 |
| scrambled2|positional|2|last | 0.47 | 0.01 |
| scrambled2|positional|3|none | 0.40 | -0.02 |
| scrambled|canonical|3|none | 0.30 | 0.28 |
| scrambled|positional|2|last | 0.44 | 0.12 |
| scrambled|positional|3|none | 0.43 | 0.03 |

## ministral-3-8b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.51 (F1 0.00), median P(opt-out) 0.25 → opt-out gate stands
- anchors: D reference 0.61 (OK), D canonical median 0.47 (numbering-limited)
- validity (valid mass) F1 0.01 → F3 0.78 → F5 0.67
- answer-string consistency: 0 of 25787 checked extensions score above their prefix by > 0.3 nats (max excess +0.11) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.79 (24/24 named; {'number': 22, 'label': 2}) FAIL; reversed|canonical|3|none: 0.92 (24/24 named; {'number': 23, 'label': 1}) OK; paper|positional|2|last: 0.75 (24/24 named; {'number': 6, 'label': 18}) FAIL

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.03 | -0.20 |
| paper|positional|1|none | 1.03 | -0.16 |
| paper|positional|2|first | 0.99 | 0.12 |
| paper|positional|2|last | 0.91 | 0.35 |
| paper|positional|3|none | 0.61 | 0.49 |
| paper|positional|5|none | 0.69 | 0.67 |
| reversed|canonical|3|none | 0.56 | 0.15 |
| reversed|positional|2|last | 1.01 | -0.02 |
| reversed|positional|3|none | 0.85 | -0.21 |
| scrambled2|canonical|3|none | 0.28 | 0.35 |
| scrambled2|positional|2|last | 1.33 | -0.08 |
| scrambled2|positional|3|none | 0.68 | 0.06 |
| scrambled|canonical|3|none | 0.47 | 0.35 |
| scrambled|positional|2|last | 1.18 | 0.12 |
| scrambled|positional|3|none | 0.52 | -0.03 |

## olmo-3.1-32b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.20 (F1 0.00), median P(opt-out) 0.78 → PIVOT: refusal-gated-DK
- anchors: D reference 1.63 (OK), D canonical median 1.50 (OK)
- validity (valid mass) F1 0.00 → F3 0.76 → F5 0.79
- answer-string consistency: 0 of 10327 checked extensions score above their prefix by > 0.3 nats (max excess +0.24) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.95 (19/24 named; {'other': 5, 'number': 15, 'label': 4}) OK; reversed|canonical|3|none: 1.00 (19/24 named; {'number': 19, 'other': 5}) OK; paper|positional|2|last: 0.96 (24/24 named; {'label': 20, 'number': 4}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.25 | 0.27 |
| paper|positional|1|none | 1.52 | -0.08 |
| paper|positional|2|first | 1.50 | 0.15 |
| paper|positional|2|last | 1.44 | 0.30 |
| paper|positional|3|none | 1.63 | 0.11 |
| paper|positional|5|none | 1.44 | 0.30 |
| reversed|canonical|3|none | 1.78 | 0.07 |
| reversed|positional|2|last | 1.50 | -0.25 |
| reversed|positional|3|none | 1.69 | -0.28 |
| scrambled2|canonical|3|none | 1.50 | -0.40 |
| scrambled2|positional|2|last | 1.25 | 0.08 |
| scrambled2|positional|3|none | 1.49 | 0.30 |
| scrambled|canonical|3|none | 1.27 | 0.66 |
| scrambled|positional|2|last | 1.30 | -0.20 |
| scrambled|positional|3|none | 1.29 | -0.04 |

## phi-4-mini  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.92 (F1 0.16), median P(opt-out) 0.04 → opt-out gate stands
- anchors: D reference 1.25 (OK), D canonical median 0.99 (OK)
- validity (valid mass) F1 0.21 → F3 0.87 → F5 0.90
- answer-string consistency: 0 of 26039 checked extensions score above their prefix by > 0.3 nats (max excess +0.00) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.83 (24/24 named; {'number': 24}) FAIL; reversed|canonical|3|none: 0.92 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.79 (24/24 named; {'number': 24}) FAIL

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.06 | 0.54 |
| paper|positional|1|none | 1.02 | 0.38 |
| paper|positional|2|first | 1.22 | -0.23 |
| paper|positional|2|last | 1.31 | -0.05 |
| paper|positional|3|none | 1.25 | -0.17 |
| paper|positional|5|none | 1.22 | -0.12 |
| reversed|canonical|3|none | 0.99 | -0.92 |
| reversed|positional|2|last | 1.39 | -0.46 |
| reversed|positional|3|none | 1.30 | -0.28 |
| scrambled2|canonical|3|none | 0.27 | 0.39 |
| scrambled2|positional|2|last | 0.70 | 0.30 |
| scrambled2|positional|3|none | 0.85 | 0.16 |
| scrambled|canonical|3|none | 1.18 | -0.24 |
| scrambled|positional|2|last | 1.05 | -0.10 |
| scrambled|positional|3|none | 1.08 | -0.11 |

## phi-4  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.94 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.80 (OK), D canonical median 1.31 (OK)
- validity (valid mass) F1 0.00 → F3 0.69 → F5 0.63
- answer-string consistency: 0 of 12668 checked extensions score above their prefix by > 0.3 nats (max excess +0.04) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (11/24 named; {'other': 13, 'number': 11}) OK; reversed|canonical|3|none: 1.00 (5/24 named; {'other': 19, 'number': 5}) OK; paper|positional|2|last: 1.00 (17/24 named; {'number': 17, 'other': 7}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.44 | -0.54 |
| paper|positional|1|none | 1.33 | -0.65 |
| paper|positional|2|first | 1.67 | -0.33 |
| paper|positional|2|last | 1.83 | 0.07 |
| paper|positional|3|none | 1.80 | -0.02 |
| paper|positional|5|none | 1.75 | -0.07 |
| reversed|canonical|3|none | 1.18 | -0.35 |
| reversed|positional|2|last | 1.56 | -0.44 |
| reversed|positional|3|none | 1.67 | -0.33 |
| scrambled2|canonical|3|none | 1.43 | -0.24 |
| scrambled2|positional|2|last | 1.20 | 0.00 |
| scrambled2|positional|3|none | 1.34 | 0.31 |
| scrambled|canonical|3|none | 1.31 | 0.21 |
| scrambled|positional|2|last | 1.53 | -0.03 |
| scrambled|positional|3|none | 1.58 | -0.34 |

## qwen2.5-7b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.45 (OK), D canonical median 0.90 (OK)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 1.00
- answer-string consistency: 0 of 7047 checked extensions score above their prefix by > 0.3 nats (max excess +0.27) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.71 (24/24 named; {'label': 21, 'number': 3}) FAIL; reversed|canonical|3|none: 0.92 (24/24 named; {'number': 23, 'label': 1}) OK; paper|positional|2|last: 0.96 (24/24 named; {'number': 22, 'label': 2}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.62 | 0.20 |
| paper|positional|1|none | 1.33 | 0.54 |
| paper|positional|2|first | 1.51 | -0.49 |
| paper|positional|2|last | 1.36 | -0.40 |
| paper|positional|3|none | 1.45 | -0.46 |
| paper|positional|5|none | 1.71 | -0.12 |
| reversed|canonical|3|none | 1.03 | -0.43 |
| reversed|positional|2|last | 1.25 | -0.25 |
| reversed|positional|3|none | 1.17 | -0.10 |
| scrambled2|canonical|3|none | 0.90 | -1.05 |
| scrambled2|positional|2|last | 1.09 | -0.64 |
| scrambled2|positional|3|none | 0.75 | -1.00 |
| scrambled|canonical|3|none | 0.22 | 0.62 |
| scrambled|positional|2|last | 1.62 | 0.12 |
| scrambled|positional|3|none | 1.57 | -0.23 |

## qwen3-32b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.03), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 1.86 (OK), D canonical median 1.77 (OK)
- validity (valid mass) F1 0.02 → F3 1.00 → F5 1.00
- answer-string consistency: 0 of 17493 checked extensions score above their prefix by > 0.3 nats (max excess +0.06) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.88 (24/24 named; {'number': 19, 'label': 5}) FAIL; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 1.23 | 0.62 |
| paper|positional|1|none | 1.53 | 0.40 |
| paper|positional|2|first | 1.52 | -0.29 |
| paper|positional|2|last | 1.55 | 0.36 |
| paper|positional|3|none | 1.86 | 0.07 |
| paper|positional|5|none | 1.87 | 0.12 |
| reversed|canonical|3|none | 1.82 | 0.14 |
| reversed|positional|2|last | 1.49 | -0.11 |
| reversed|positional|3|none | 1.78 | -0.11 |
| scrambled2|canonical|3|none | 1.77 | 0.20 |
| scrambled2|positional|2|last | 1.63 | 0.06 |
| scrambled2|positional|3|none | 1.82 | 0.01 |
| scrambled|canonical|3|none | 0.98 | 0.13 |
| scrambled|positional|2|last | 1.79 | 0.18 |
| scrambled|positional|3|none | 1.87 | 0.10 |

## qwen3-8b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 1.00 (F1 0.00), median P(opt-out) 0.00 → opt-out gate stands
- anchors: D reference 0.72 (OK), D canonical median 0.47 (numbering-limited)
- validity (valid mass) F1 0.00 → F3 1.00 → F5 1.00
- answer-string consistency: 35 of 11247 checked extensions score above their prefix by > 0.3 nats (max excess +0.86) → longer strings unreliable
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 1.00 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 0.96 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 24}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.36 | 0.61 |
| paper|positional|1|none | 0.44 | 0.55 |
| paper|positional|2|first | 1.09 | -0.09 |
| paper|positional|2|last | 0.81 | 0.22 |
| paper|positional|3|none | 0.72 | 0.28 |
| paper|positional|5|none | 0.51 | 0.50 |
| reversed|canonical|3|none | 0.47 | -0.57 |
| reversed|positional|2|last | 0.78 | 0.22 |
| reversed|positional|3|none | 0.65 | 0.35 |
| scrambled2|canonical|3|none | 0.96 | -0.12 |
| scrambled2|positional|2|last | 0.96 | 0.05 |
| scrambled2|positional|3|none | 1.17 | 0.43 |
| scrambled|canonical|3|none | 0.35 | 1.05 |
| scrambled|positional|2|last | 1.34 | -0.03 |
| scrambled|positional|3|none | 1.19 | 0.15 |

## qwen3.5-9b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.60 (F1 0.00), median P(opt-out) 0.38 → opt-out gate stands
- anchors: D reference 1.19 (OK), D canonical median 0.99 (OK)
- validity (valid mass) F1 0.01 → F3 0.92 → F5 0.83
- answer-string consistency: 0 of 23539 checked extensions score above their prefix by > 0.3 nats (max excess +0.22) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.96 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 0.91 (23/24 named; {'number': 23, 'other': 1}) OK; paper|positional|2|last: 1.00 (24/24 named; {'number': 23, 'label': 1}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.63 | 1.07 |
| paper|positional|1|none | 0.78 | 1.03 |
| paper|positional|2|first | 1.16 | 0.01 |
| paper|positional|2|last | 1.15 | 0.34 |
| paper|positional|3|none | 1.19 | 0.25 |
| paper|positional|5|none | 1.25 | 0.32 |
| reversed|canonical|3|none | 0.77 | 0.06 |
| reversed|positional|2|last | 1.32 | -0.06 |
| reversed|positional|3|none | 1.40 | -0.08 |
| scrambled2|canonical|3|none | 0.99 | 0.20 |
| scrambled2|positional|2|last | 1.23 | 0.19 |
| scrambled2|positional|3|none | 1.11 | 0.28 |
| scrambled|canonical|3|none | 0.99 | 0.28 |
| scrambled|positional|2|last | 1.31 | 0.06 |
| scrambled|positional|3|none | 1.24 | -0.04 |

## smollm3-3b  (3788 rows)

- identity vs arm A: 0 items, mean |Δ| —, max —, prompts with |Δ| > 0.10: — → n/a
- DK cell (O1, F2, opt-out last): median substantive mass 0.87 (F1 0.01), median P(opt-out) 0.01 → opt-out gate stands
- anchors: D reference 1.00 (OK), D canonical median 0.86 (OK)
- validity (valid mass) F1 0.06 → F3 0.97 → F5 0.90
- answer-string consistency: 0 of 25895 checked extensions score above their prefix by > 0.3 nats (max excess +0.02) → OK
- decode vs logit argmax (named decodes): scrambled|positional|3|none: 0.96 (24/24 named; {'number': 24}) OK; reversed|canonical|3|none: 1.00 (24/24 named; {'number': 24}) OK; paper|positional|2|last: 0.92 (24/24 named; {'number': 23, 'label': 1}) OK

| anchors cell | D | A |
|---|---|---|
| paper|positional|1|last | 0.59 | 0.70 |
| paper|positional|1|none | 0.73 | 0.52 |
| paper|positional|2|first | 0.74 | 0.27 |
| paper|positional|2|last | 0.95 | 0.31 |
| paper|positional|3|none | 1.00 | 0.30 |
| paper|positional|5|none | 1.05 | 0.22 |
| reversed|canonical|3|none | 1.00 | -0.08 |
| reversed|positional|2|last | 0.93 | -0.34 |
| reversed|positional|3|none | 1.06 | -0.27 |
| scrambled2|canonical|3|none | 0.57 | 0.13 |
| scrambled2|positional|2|last | 0.74 | 0.08 |
| scrambled2|positional|3|none | 0.76 | 0.10 |
| scrambled|canonical|3|none | 0.86 | 0.51 |
| scrambled|positional|2|last | 0.60 | -0.28 |
| scrambled|positional|3|none | 0.69 | -0.23 |

