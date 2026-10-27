"""Regenerate README.md's numbers from results/orderforce.json and results/orderforce_gates.json (corrected readout), with
the published registered-estimator numbers from results/registered/ beside them.  Usage: python3 scripts/make_readme.py"""
import json
import re
import statistics as st
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
R = json.loads((ROOT / "results" / "orderforce.json").read_text()); G = json.loads((ROOT / "results" / "orderforce_gates.json").read_text())
REG = ROOT / "results" / "registered"   # pre-amendment outputs, incl. the arm-A identity check (parent-repo rows, not in this repo)
R0 = json.loads((REG / "orderforce.json").read_text()) if (REG / "orderforce.json").exists() else None
G0 = json.loads((REG / "orderforce_gates.json").read_text()) if (REG / "orderforce_gates.json").exists() else G
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
ident = [G0[t]["identity"].get("max_abs_d_item") for t in G0 if G0[t]["identity"].get("max_abs_d_item") is not None]
dec = [x["agreement"] for t in G for x in G[t].get("decode", {}).values() if x.get("agreement") is not None and not models.get(t, {}).get("instrument_unreliable")]
f1 = {t: G[t]["validity"]["F1"] for t in G if G[t].get("validity", {}).get("F1") == G[t].get("validity", {}).get("F1")}
f1_low = sum(1 for v in f1.values() if v < 0.10)
rows = "\n".join(f"| {a.replace('_', ' ')} | {AT[a]['class']} | {AT[a]['survives all']}/{AT[a]['n']} | {AT[a]['R3_frac']:.2f} | {AT[a]['revealed_called']} |" for a in sorted(POL, key=lambda a: -AT[a]["R3_frac"]))


def headline(R_):
    """The README's headline numbers for one analysis output (used for the registered vs corrected comparison)."""
    M_, AT_, P_ = R_["models"], R_["axis_table"], R_["predictions"]
    rel_ = [t for t in M_ if not M_[t]["instrument_unreliable"]]
    c = {k: 0 for k in ("called", "+order", "+forcing", "survives all", "refusal-gated", "not called", "saturated")}
    for t in rel_:
        for a in POL:
            if M_[t]["axes"].get(a, {}).get("rung"):
                c[M_[t]["axes"][a]["rung"]] += 1
    a = P_["A6_permutation"]
    return {"rel": rel_, "called": c["called"] + c["+order"] + c["+forcing"] + c["survives all"], "order": c["+order"] + c["survives all"],
            "forcing": c["+forcing"] + c["survives all"], "all": c["survives all"], "null": R_["null_called"],
            "hard": [x for x in POL if AT_[x]["class"] == "hard survivor"], "spin": [x for x in POL if AT_[x]["class"] == "spinner"],
            "rho": f"{a['mean_rho_all']:.2f} / {a['mean_rho_surviving']:.2f} / {a['mean_rho_rest']:.2f} (p = {a['p_one_sided']:.3f})",
            "preds": ", ".join(f"{k} {'holds' if P_[k + ('_ok' if k.startswith('ST') else '')] else 'fails'}" for k in ("SA1", "SA2", "SA3", "ST1", "ST2", "ST3")),
            "verdict": P_["verdict"]}


def moved_text(h0, h1, gained, lost, names):
    """One paragraph on what the readout correction changed, in words."""
    one = lambda xs, a, b: a if len(xs) == 1 else b
    diff = lambda a, b: [x for x in a if x not in b]
    out = []
    if gained:
        out.append(f"{names(gained)} now {one(gained, 'passes', 'pass')} the anchor reliability gate")
    if lost:
        out.append(f"{names(lost)} no longer {one(lost, 'passes', 'pass')} it")
    for xs, verb in ((diff(h1["hard"], h0["hard"]), ("joins the hard survivors", "join the hard survivors")),
                     (diff(h0["hard"], h1["hard"]), ("drops out of the hard survivors", "drop out of the hard survivors")),
                     (diff(h0["spin"], h1["spin"]), ("is no longer a spinner", "are no longer spinners")),
                     (diff(h1["spin"], h0["spin"]), ("becomes a spinner", "become spinners"))):
        if xs:
            out.append(f"{names(xs)} {one(xs, *verb)}")
    same = h0["preds"] == h1["preds"] and h0["verdict"] == h1["verdict"]
    return (("What moved: " + "; ".join(out) + ". ") if out else "") + \
        ("Every pre-registered prediction and the decision rule come out the same." if same else
         f"The pre-registered outcome changes: {h0['preds']} → {h1['preds']}; decision rule \"{h0['verdict']}\" → \"{h1['verdict']}\".")


fix = ""
if R0 is not None:
    h0, h1 = headline(R0), headline(R)
    names = lambda xs: (lambda w: ", ".join(w[:-1]) + " and " + w[-1] if len(w) > 1 else (w[0] if w else "none"))([x.replace("_", " ") for x in xs])
    gained, lost = [t for t in h1["rel"] if t not in h0["rel"]], [t for t in h0["rel"] if t not in h1["rel"]]
    flagged = [t for t in G if not G[t].get("string_consistency", {}).get("ok", True)]
    tab = [("instrument-reliable models", len(h0["rel"]), len(h1["rel"])),
           ("model × issue cells called / + orders / + forcing / survive everything",
            f"{h0['called']} / {h0['order']} / {h0['forcing']} / {h0['all']}", f"{h1['called']} / {h1['order']} / {h1['forcing']} / {h1['all']}"),
           ("null issues called", h0["null"], h1["null"]),
           ("hard survivors", f"{len(h0['hard'])}", f"{len(h1['hard'])}"), ("spinners", f"{len(h0['spin'])}", f"{len(h1['spin'])}"),
           ("stated vs revealed ρ: all / surviving / rest", h0["rho"], h1["rho"]),
           ("pre-registered predictions", h0["preds"], h1["preds"]), ("decision rule", f"\"{h0['verdict']}\"", f"\"{h1['verdict']}\"")]
    fix = f"""## Readout correction (PLAN.md amendment, 2026-10-27)

**The problem.** For each answer option the scorer reads the probability of eight answer strings: the printed number
("3"), the number with its bracket ("3)"), the full line ("3) Agree") and the bare label ("Agree"), each with and
without a leading space. The registered readout added these probabilities together. But the strings are nested: the
tokenizer splits "3)" into "3" followed by ")", so every reply that starts "3)" or "3) Agree" is already included in
the probability of "3". Adding them counted the same answer up to three times. The factor depends on how the model
tends to continue after the number, which differs between options, layouts and models, so the comparison between
options was distorted, not just rescaled. The registered answer mass made the opposite mistake: it kept only the most
likely string per option, so a model that sometimes opens with "3" and sometimes with "Agree" was undercounted.

**The fix.** An option's probability is now the sum over the four strings that cannot contain one another, "3", " 3",
"Agree" and " Agree" (each starts with a different token), and answer mass is the sum of those over all listed options
([scripts/readout.py](scripts/readout.py)). Every scored prompt stores the log-probability of each string, so all
numbers were recomputed from the stored rows and no model was re-run. `--estimator registered` reproduces the
published numbers exactly; they are kept in [results/registered/](results/registered/). The corrected readout also
avoids the longer strings, whose scores are internally inconsistent for {len(flagged)} models ({names(flagged)}):
"3) Agree" sometimes scored more probable than "3)", which is impossible (`orderforce_gates.md`, check 6).

| | registered | corrected (above) |
|---|---|---|
""" + "\n".join(f"| {a} | {b} | {c} |" for a, b, c in tab) + "\n\n" + moved_text(h0, h1, gained, lost, names) + "\n\n"
# OLMo 2 7B training stages, v2 (results/olmo2_v2/; run_olmo2_v2.sh, olmo2_compare / olmo2_explore / olmo2_posthoc.py), only once they exist
O = ROOT / "results" / "olmo2_v2"
olmo = ""
if all((O / f).exists() for f in ("olmo2_compare.json", "olmo2_explore.json", "olmo2_posthoc.json", "orderforce.json")):
    rd = lambda f: json.loads((O / f).read_text(encoding="utf-8"))
    C, X, PH, OF = rd("olmo2_compare.json"), rd("olmo2_explore.json"), rd("olmo2_posthoc.json"), rd("orderforce.json")
    S4, POST4 = ["base", "SFT", "DPO", "Instruct"], ["SFT", "DPO", "Instruct"]
    TAG = {s: f"olmo2-7b-{s.lower()}-answer" for s in S4}   # ending A, the one all four stages share
    sm = C["summary"]
    seq = lambda f, ss=S4: " → ".join(f(s) for s in ss)
    join = lambda w: ", ".join(w[:-1]) + " and " + w[-1] if len(w) > 1 else (w[0] if w else "none")
    nm = lambda xs: join([x.replace("_", " ") for x in xs])
    pair = lambda p: C["H5"]["H5a"]["pairs"][p]["d_rel ±0.2"]
    h5_counts = lambda p: "{equivalent} / {different} / {inconclusive}".format(**pair(p)["counts"])
    diffs = [a for a, v in pair("SFT->DPO")["axes"].items() if v and v.get("class") == "different"]
    P3 = PH["P3"]["SFT->DPO"]
    specific = [a for a, v in P3["issues"].items() if v["issue_specific"]]
    rho = C["H5"]["H5b"]["spearman_d_lo"]
    lad = {s: {a: PH["P7"][s]["d_lo"]["axes"][a]["rung"] for a in POL} for s in POST4}
    surv = {s: [a for a in POL if lad[s][a] == "survives all"] for s in POST4}
    surv_all = [a for a in POL if all(a in surv[s] for s in POST4)]
    surv_late = [a for a in POL if a not in surv_all and all(a in surv[s] for s in ("DPO", "Instruct"))]
    never = [a for a in POL if all(lad[s][a] == "not called" for s in POST4)]
    ndec = sum(X["decodes"][TAG[s]]["n"] for s in S4)
    nnum = sum(X["decodes"][TAG[s]]["counts"].get("number", 0) for s in S4)
    para = [OF["models"][TAG[s]]["spin"]["paraphrase_4"] for s in S4]
    held = {"H1a": X["H1"]["H1a"]["decision"] == "supported", "H2a": X["H2"]["H2a"] == "holds",
            "H3": all(X["H3"][s]["class"] == "saturation" for s in POST4), "H4a": C["H4"]["H4a"]["decision"] == "supported",
            "H4b": C["H4"]["H4b"]["decision"] == "supported", "H5a": C["H5"]["H5a"]["decision"] == "supported",
            "H6": all(C["H6"][s]["decision"] == "holds" for s in POST4)}
    olmo = f"""## Extension: OLMo 2 7B across training stages

OLMo 2 7B was surveyed at each training stage: {seq(lambda s: s)} (RLVR). Each stage answered 4,288 prompts: the
panel's 3,788 plus two arms. The prompts are plain completions ending in "Answer:", with no chat template, so that the
base model is surveyed in a format it can answer. All four stages see token-identical prompts, so every contrast between
stages is paired. The design, the hypotheses and their decision rules were pre-registered in [PLAN_OLMO2.md](PLAN_OLMO2.md)
before any prompt was scored.

- **Full write-up:** [results/olmo2_v2/REPORT.md](results/olmo2_v2/REPORT.md).
- **The same data in this README's survival framing:** [results/olmo2_v2/REPORT_survival.md](results/olmo2_v2/REPORT_survival.md).
- **Scope:** one model family at one size, so be cautious about generalising to other families.
- **Superseded:** an earlier chat-template run (`results/olmo2/`) is not reported as findings.

![OLMo 2 7B stages](results/olmo2_v2/olmo2_figure.png)

1. **Every stage takes the survey as a completion.** Answer mass at the paper's format is
   {seq(lambda s: f"{sm[s]['answer mass F3 (paper order)']['mean']:.2f}")}, and {nnum} of {ndec} greedy decodes name an option by number.
   - The base model reads the statements, but weakly: its 12 factual anchors separate by C = {sm['base']['anchor C (reference)']['mean']:.2f}
     log-odds (registered threshold 0.5).
   - SFT, DPO and Instruct separate them by {join([f"{sm[s]['anchor C (reference)']['mean']:.2f}" for s in POST4])}.
2. **Post-training adds a pull toward agreeing and toward the lower lines.**
   - Mean agreement at the paper's format goes {seq(lambda s: f"{sm[s]['acquiescence: mean p_agree (reference)']['mean']:.2f}")}.
   - Re-ordering the options moves the raw answer by {seq(lambda s: f"{OF['models'][TAG[s]]['spin']['order_F3']:.2f}")} Likert
     units, against {min(para):.2f}–{max(para):.2f} across paraphrases.
   - No stage passes the panel's reliability gate (anchor D {seq(lambda s: f"{sm[s]['anchor D (reference)']['mean']:.2f}")}).
     With agreement at its ceiling, the paired readout in probability finds almost nothing.
3. **Stated directions (registered, H5a): {C['H5']['H5a']['decision']}.** H5a measures a stance relative to the stage's own
   true-vs-false separation (d_rel, margin ±0.2). Equivalent / different / inconclusive issues:
   - SFT → DPO: {h5_counts('SFT->DPO')}, with {nm(diffs)} different;
   - DPO → Instruct: {h5_counts('DPO->Instruct')}.

   Post hoc, most of the SFT → DPO change is one uniform rescaling: stances ×{P3['d_lo_slope']['mean']:.2f} in log-odds,
   facts ×{P3['C_ratio']['mean']:.2f}. Only {nm(specific)} changes beyond it, and no direction flips.
4. **The stance pattern is already faintly present in the base model.** Registered H5b: "{C['H5']['H5b']['decision']}", with
   ρ = {rho['mean']:.2f} [{rho['lo']:.2f}, {rho['hi']:.2f}] against SFT. Post hoc, SFT's stances are
   {PH['P6']['mean_abs_d_lo']['SFT_over_base']['mean']:.1f} times the base model's in log-odds.
5. **Read in log-odds, a fixed set of topics survives re-ordering and forcing (post hoc).** Under the panel's ladder
   rules with d_LO in place of d:
   - {join([str(len(surv[s])) for s in POST4])} issues survive everything for SFT, DPO and Instruct respectively;
   - in all three stages: {nm(surv_all)};
   - from DPO on, also: {nm(surv_late)};
   - never called by any stage: {nm(never)}.

**Pre-registered predictions:** {join([k for k, v in held.items() if v])} held, and {join([k for k, v in held.items() if not v])} did not.

**One measurement failed.** Under the ending "The answer is", the base model writes a colon before its answer, which
the readout does not capture. That ending is reported as not measured.

"""
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

3,788 prompts per model; the answer is read from teacher-forced label log-probabilities (with the readout correction
described below), checked against greedy decodes under the permuted layouts (the written option matches the
teacher-forced choice in {min(dec):.2f}–{max(dec):.2f} of named decodes among reliable models) and against an earlier fixed-order run
of the same items (max mean |Δ p_agree| {max(ident):.2f}, registered readout).

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

{fix}## What this does and does not claim

"Survives" means invariant to these manipulations (four orders, two numberings, these forcing texts, one opt-out
wording, four paraphrases), not a true preference. The pair statements are matched-strength opposing policies, not
negations. Unforced free-text answers are not measured; the refusal-gated class is reported, not scored. Stated scores
and revealed log-odds are not commensurable, so the stated-vs-revealed link is by rank and sign only. Small models are
over-represented. Everything else is in [PLAN.md](PLAN.md) §10–11, written before the panel ran, with the pilot's
outcomes, two pre-panel amendments and the post-panel readout correction appended.

{olmo}## Reproduce

```
pip install -r requirements.txt          # GPU side: torch, transformers, accelerate
bash run.sh google/gemma-3-4b-it         # one model: ~3,800 prompts, a few minutes on a 96 GB GPU
python3 scripts/orderforce_gates.py      # launch gates (decode agreement, opt-out mass, anchors)
python3 scripts/orderforce_analyze.py    # ladder, spin budget, join with the revealed leans, predictions
python3 scripts/plot_orderforce.py       # the summary figure
bash run_olmo2_v2.sh                     # OLMo 2 7B base / SFT / DPO / Instruct (PLAN_OLMO2.md), analysed apart in results/olmo2_v2/
python3 scripts/olmo2_posthoc.py         # OLMo 2 post-hoc analyses (CPU): results/olmo2_v2/olmo2_posthoc.md
python3 scripts/plot_olmo2.py            # OLMo 2 summary figure
```

`run_olmo2_v2.sh` scores the four OLMo 2 7B training stages at pinned revisions on one GPU (≥ 24 GB, ~73 GB of
weights), plus the base model under three more prompt endings.
- **Prompts:** every prompt is a plain completion with no chat template, and all four stages see token-identical prompts.
- **Pipeline:** the gates and the panel's ladder run on these seven runs alone in `results/olmo2_v2/`. They are
  followed by `scripts/olmo2_compare.py` (paired stage contrasts and equivalence tests, H4–H6) and
  `scripts/olmo2_explore.py` (answering, the position / number / label decomposition and content effects, H1–H3).
- **Post-hoc analyses:** `scripts/olmo2_posthoc.py` adds those of the report, labelled as such.
- **No stated-vs-revealed join:** the conjoint leans in `data/sweep_summary.json` do not cover OLMo 2.

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
