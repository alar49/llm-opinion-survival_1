"""Regenerate README.md's numbers from results/orderforce.json and results/orderforce_gates.json.  Usage: python3 scripts/make_readme.py"""
import json
import re
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = json.loads((ROOT / "results" / "orderforce.json").read_text()); G = json.loads((ROOT / "results" / "orderforce_gates.json").read_text())
P, AT, models = R["predictions"], R["axis_table"], R["models"]; rel = [t for t in models if not models[t]["instrument_unreliable"]]
POL = [a for a in AT if a not in ("fair_month", "sign_color")]
hard = [a for a in POL if AT[a]["class"] == "hard survivor"]; spin = [a for a in POL if AT[a]["class"] == "spinner"]; mixed = [a for a in POL if AT[a]["class"] == "mixed"]
sp = lambda k: st.mean([models[t]["spin"][k] for t in rel if models[t]["spin"].get(k) is not None])
counts = {k: 0 for k in ("called", "+order", "+forcing", "survives all", "refusal-gated", "not called", "saturated")}
for t in rel:
    for a in POL:
        r = models[t]["axes"].get(a, {}).get("rung")
        if r:
            counts[r] += 1
n = sum(counts.values()); called = counts["called"] + counts["+order"] + counts["+forcing"] + counts["survives all"]
a6 = P["A6_permutation"]
dk = [G[t]["dk"]["median_p_optout_F2"] for t in G if G[t]["dk"].get("median_p_optout_F2") is not None]
ident = [G[t]["identity"].get("max_abs_d_item") for t in G if G[t]["identity"].get("max_abs_d_item") is not None]
dec = [x["agreement"] for t in G for x in G[t].get("decode", {}).values() if x.get("agreement") is not None and not models.get(t, {}).get("instrument_unreliable")]
f1 = {t: G[t]["validity"]["F1"] for t in G if G[t].get("validity", {}).get("F1") == G[t].get("validity", {}).get("F1")}
f1_low = sum(1 for v in f1.values() if v < 0.10)
rows = "\n".join(f"| {a.replace('_', ' ')} | {AT[a]['class']} | {AT[a]['survives all']}/{AT[a]['n']} | {AT[a]['R3_frac']:.2f} | {AT[a]['revealed_called']} |" for a in sorted(POL, key=lambda a: -AT[a]["R3_frac"]))
README = f"""# Which LLM opinions survive re-ordering the options and forcing the answer?

**A pre-registered stress test of the Political-Compass-style LLM survey, as a response to Röttger et al. (2024),
*Political Compass or Spinning Arrow?* ([arXiv 2402.16786](https://arxiv.org/abs/2402.16786)).**

![summary](results/orderforce_figure.png)

Röttger et al. show that forced-choice opinion surveys of language models are unstable: models refuse unless pushed,
pushing changes the answer, and ten paraphrases of the question stem move a model further than the gap between real
politicians. Their paradigm holds two things fixed that the multiple-choice literature says are large nuisances: the
**order in which the answer options are listed** and the **availability of a legitimate non-answer**. This repository
varies both, inside the paper's own format, and asks a constructive question: *per topic, which stated preferences
survive — and do the survivors agree with what the model does when it is not asked?*

## Result

{len(models)} open models (1B–32B, ten families; {len(rel)} pass the instrument-reliability gates) answered 34 opposing-pair
policy statements on 17 county-level issues, the 62 Political Compass propositions, 4 valence-free null statements and
12 factual anchors, under the paper's four options and forcing texts, while we varied:

- the **option order** (four orders forming a Latin square closed under reversal),
- the **numbering** (numbers following the list, or pinned to the labels so the list is out of numeric order),
- the **forcing level** (nothing appended / "Only answer with the label." / the paper's levels 3 and 5),
- an explicit **"5) No opinion"** option (last, crossed with the four orders, and listed first as a position control).

3,788 prompts per model; the answer is read from teacher-forced label log-probabilities, checked against greedy decodes
under the permuted layouts (the written option matches the teacher-forced choice in {min(dec):.2f}–{max(dec):.2f} of named decodes among
reliable models) and against an earlier fixed-order run of the same items (max mean |Δ p_agree| {max(ident):.2f}).

1. **Re-ordering the options spins the raw stated answer more than rewording does.** The mean range of an item's score
   (Likert −2…+2) across the four orders is **{sp('order_F3'):.2f}**, against {sp('paraphrase_4'):.2f} across four paraphrases, {sp('forcing'):.2f} across forcing
   levels and {sp('numbering'):.2f} between the two numberings. Models mostly answer by printed number and list position.
2. **A paired directional readout survives.** Scoring each issue as the difference between its two opposing statements
   cancels acquiescence and position bias by construction. Of {n} model × issue cells, {called} are called at the paper's
   standard forced format; {counts['+order'] + counts['survives all']} of those keep their direction across every order and numbering, {counts['+forcing'] + counts['survives all']} across forcing and the
   opt-out, and **{counts['survives all']} survive everything**. The two null issues are called in {R['null_called']} of {2 * len(rel)} cells.
3. **A fixed set of topics survives.** Hard survivors (top rung in ≥ 2/3 of reliable models): {', '.join(a.replace('_', ' ') for a in hard)}.
   Spinners (< 1/3): {', '.join(a.replace('_', ' ') for a in spin)}. Mixed: {', '.join(a.replace('_', ' ') for a in mixed)}.
4. **Survival predicts validity.** Within model, the stated direction and the lean the same model *reveals* in an
   independent candidate-choice conjoint (from the parent project) agree with Spearman ρ {a6['mean_rho_all']:.2f} over all 17 issues,
   **{a6['mean_rho_surviving']:.2f} on the surviving issues and {a6['mean_rho_rest']:.2f} on the rest** (means over the {a6['models']} models with at least three issues of each kind; permutation of the survival labels, one-sided p = {a6['p_one_sided']:.3f}).
   At matched effect size (top |d| tertile) survival is {P['matched_d_top_tertile']['revealed_called_survival']:.2f} vs {P['matched_d_top_tertile']['non_called_survival']:.2f}, so part of "survival" is extremity.
5. **The "No opinion" out is taken unevenly** (median share {min(dk):.2f}–{max(dk):.2f} by model, mean uptake {P['dk_rate_overall']:.2f}), while
   unforced answer mass stays below 0.10 for {f1_low} of {len(f1)} models: models that state opinions do so as soon as they are told
   to answer with a label, and most keep stating them when a legitimate out is offered.

The pre-registered decision rule ([PLAN.md](PLAN.md) §8) returns **"some topics stable"**: the spinning-arrow
prediction SA1 holds (re-ordering spins ≥ 0.4 units), SA2 and SA3 fail ({len(hard)} hard survivors; survival adds validity),
ST1 and ST3 hold, ST2 fails (the paired readout's order range is {P['ST2']['mean_d_order_range']:.2f} vs {P['ST2']['mean_raw_pagree_order_range']:.2f} for raw items, not under half).

| issue | class | models at the top rung | share | models with a called revealed lean |
|---|---|---|---|---|
{rows}

Full tables: [results/orderforce.md](results/orderforce.md); rung heatmap [results/orderforce_ladder.png](results/orderforce_ladder.png);
spin budget per model [results/orderforce_spin.png](results/orderforce_spin.png); pilot gates [results/orderforce_gates.md](results/orderforce_gates.md).

## What this does and does not claim

"Survives" means invariant to these manipulations (four orders, two numberings, these forcing texts, one opt-out
wording, four paraphrases), not a true preference. The pair statements are matched-strength opposing policies, not
negations. Unforced free-text answers are not measured; the refusal-gated class is reported, not scored. Stated scores
and revealed log-odds are not commensurable, so the stated-vs-revealed link is by rank and sign only. Small models are
over-represented. Everything else is in [PLAN.md](PLAN.md) §10–11, written before the panel ran, with the pilot's
outcomes and two pre-panel amendments appended.

## Reproduce

```
pip install -r requirements.txt          # GPU side: torch, transformers, accelerate
bash run.sh google/gemma-3-4b-it         # one model: ~3,800 prompts, a few minutes on a 96 GB GPU
python3 scripts/orderforce_gates.py      # launch gates (decode agreement, opt-out mass, anchors)
python3 scripts/orderforce_analyze.py    # ladder, spin budget, join with the revealed leans, predictions
python3 scripts/plot_orderforce.py       # the summary figure
```

`results/raw/` holds every scored prompt for the 19 models (gzip JSONL, one row per prompt with the per-label log-probs)
and the greedy decodes of the spot-check subset. `data/sweep_summary.json` carries the revealed leans from the parent
project, [election-bias-benchmark](https://github.com/kilojoules/election-bias-benchmark), where the conjoint, the
31-model stated run and the rest of the programme live. Model loading (`scripts/logit_sweep.py`, `scripts/sweep_models.json`)
is shared with that project.

## Citation

If you use this, cite the repository and Röttger et al. (2024). MIT license.
"""
(ROOT / "README.md").write_text(README)
print("README regenerated")
