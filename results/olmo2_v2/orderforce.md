# Order, forcing and the opt-out: which stated topic preferences survive? (floor 0.1, q 0.01)

Models: 7 (0 instrument-reliable). d = (p_agree(report level) − p_agree(other level))/2 at the reference cell (paper order, forcing 3), 4 paraphrases, cluster bootstrap over paraphrases. Null-axis calibration: 0 called null cells of 0 (OK). Readout: disjoint estimator (scripts/readout.py).

## A1 Topic survival

| axis | class | n | not called | refusal-gated | called | +order | +forcing | survives all | saturated | mean d_ref | revealed-called models |
|---|---|---|---|---|---|---|---|---|---|---|---|
| property_tax | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| agi_limitations | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| abortion | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| state_surveillance | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| immigration | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| guns | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| minimum_wage | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| energy | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| housing_zoning | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| drugs | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| police_funding | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| schools | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| transit | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| vaccines | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| unions | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| voting | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| trans_sports | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | 0 |
| fair_month (null) | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |
| sign_color (null) | — | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | — | — |

## Per model

| model | reliable | numbering-limited | DK pivot | broken orders | position index (first−last) | sweep pos effect | spin: order F3 | numbering | forcing | paraphrase (4) | order F5 (X) | mean d order-range | called / +order / +forcing / survives all |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| olmo2-7b-base-answer | no | yes | no | paper|positional|2|first,paper|positional|2|last,paper|positional|2|none,paper|positional|3|none,paper|positional|5|none,reversed|canonical|3|none,reversed|canonical|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled2|positional|2|last,scrambled2|positional|3|none,scrambled|canonical|3|none,scrambled|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | +0.09 | — | +0.29 | +0.29 | +0.18 | +0.16 | +0.22 | — | 0 / 0 / 0 / 0 |
| olmo2-7b-base-myanswer | no | yes | no | paper|positional|1|last,paper|positional|2|first,paper|positional|2|last,paper|positional|3|none,paper|positional|5|none,reversed|canonical|3|none,reversed|canonical|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled2|positional|2|last,scrambled2|positional|3|none,scrambled|canonical|3|none,scrambled|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | +0.09 | — | +0.52 | +0.41 | +0.24 | +0.20 | +0.39 | — | 2 / 0 / 2 / 0 |
| olmo2-7b-base-qa | no | yes | no | paper|positional|2|first,paper|positional|2|last,paper|positional|3|none,paper|positional|5|none,reversed|canonical|3|none,reversed|canonical|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled2|positional|2|last,scrambled2|positional|3|none,scrambled|canonical|3|none,scrambled|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | +0.06 | — | +0.28 | +0.26 | +0.25 | +0.15 | +0.47 | — | 0 / 0 / 0 / 0 |
| olmo2-7b-base-theansweris | no | yes | yes | paper,reversed,scrambled,scrambled2,paper|positional|1|last,paper|positional|1|none,paper|positional|2|first,paper|positional|2|last,paper|positional|2|none,paper|positional|3|none,paper|positional|5|none,reversed|canonical|3|none,reversed|canonical|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled2|positional|2|last,scrambled2|positional|3|none,scrambled|canonical|3|none,scrambled|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | +0.23 | — | +0.71 | +0.89 | +0.45 | +0.26 | +0.47 | — | 0 / 0 / 0 / 0 |
| olmo2-7b-dpo-answer | no | no | no | paper|positional|1|last,paper|positional|1|none,paper|positional|2|last,paper|positional|2|none,paper|positional|3|none,paper|positional|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | -0.22 | — | +1.47 | +0.47 | +0.14 | +0.12 | +1.22 | +0.26 | 2 / 0 / 2 / 0 |
| olmo2-7b-instruct-answer | no | no | no | paper|positional|1|last,paper|positional|1|none,paper|positional|2|last,paper|positional|2|none,paper|positional|3|none,paper|positional|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | -0.32 | — | +1.60 | +0.45 | +0.16 | +0.12 | +1.29 | — | 0 / 0 / 0 / 0 |
| olmo2-7b-sft-answer | no | yes | no | paper|positional|1|last,paper|positional|1|none,paper|positional|2|first,paper|positional|2|last,paper|positional|2|none,paper|positional|3|none,paper|positional|5|none,reversed|positional|2|last,reversed|positional|3|none,scrambled2|canonical|3|none,scrambled2|canonical|5|none,scrambled2|positional|2|last,scrambled2|positional|3|none,scrambled|canonical|3|none,scrambled|canonical|5|none,scrambled|positional|2|last,scrambled|positional|3|none | -0.08 | — | +0.90 | +0.29 | +0.15 | +0.10 | +0.68 | — | 3 / 0 / 3 / 0 |

## Per model × axis rungs

| model | property_tax | agi_limitations | abortion | state_surveillance | immigration | guns | minimum_wage | energy | housing_zoning | drugs | police_funding | schools | transit | vaccines | unions | voting | trans_sports | fair_month | sign_color |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| olmo2-7b-base-answer | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called |
| olmo2-7b-base-myanswer | not called | not called | not called | +forcing | not called | not called | not called | not called | not called | not called | not called | not called | +forcing | not called | not called | not called | not called | not called | not called |
| olmo2-7b-base-qa | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called |
| olmo2-7b-base-theansweris | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated | saturated |
| olmo2-7b-dpo-answer | not called | not called | not called | +forcing | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | +forcing | not called | not called |
| olmo2-7b-instruct-answer | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called | not called |
| olmo2-7b-sft-answer | not called | not called | not called | +forcing | not called | not called | not called | not called | not called | not called | not called | not called | +forcing | not called | not called | not called | +forcing | not called | not called |
