"""Exploratory follow-up to olmo2_compare.py (NOT pre-registered; written after the OLMo 2 7B results were seen).

All four OLMo 2 7B stages fail the anchor gate at the paper's reference format, so the pre-registered ladder has nothing to
rank. This script asks why, and what the stages state where they do read the items.

E1 Answering: answer mass by forcing level per stage (34 issue statements, paper order), and the 72 greedy spot-check
   decodes per stage classified as number / label / "as an AI" disclaimer / other.
E2 What picks the option: per stage, a log-linear decomposition of the mean option shares over the seven forcing-3
   layouts (4 orders x positional numbering, 3 orders x canonical numbering) on the 50 items present in all seven:
   log share = layout constant + list position + printed number + semantic label. Positional numbering ties number to
   position, canonical numbering ties it to the label, and the Latin square unties label from position, so the three
   pulls are separately identified. Reported as log-share effects relative to position 1 / number 1 / Strongly
   disagree, with each factor's range (max - min); 95% CIs from a bootstrap over items.
E3 Where content gets through: anchor discrimination D per cell and stage (orderforce_gates.json); readable cell = D >= 0.5.
E4 Stated directions where every post-trained stage reads the items: the cells readable for all of them (on this run, the
   three canonical-numbering cells at forcing 3). d per issue (mean over those cells), called by R0's rule (CI excludes
   0, |d| >= FLOOR, BH q over the 19 axes), sign agreement across the cells, paired stage contrasts (shift rule as in
   olmo2_compare.py) and Spearman similarity of the 17-issue profiles. The base model reads no cell and is left out.
E5 Context: the same d (point estimates, each panel model's readable cells among those of E4) for the instrument-
   reliable models of the 19-model panel: their mean, their sign split, and Olmo 3.1 32B; Spearman of each OLMo 2 stage
   against the panel mean.

Reads <dir>/raw/orderforce_<tag>.jsonl.gz, <dir>/orderforce_gates.json, results/raw/ and results/orderforce{,_gates}.json
(panel); writes <dir>/olmo2_explore.{md,json}.
Usage: python3 scripts/olmo2_explore.py [--dir results/olmo2] [--q 0.01] [--floor 0.10]
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from olmo2_compare import ISSUE_ITEMS, STAGE_IDS, Stage, ci, excludes0, roster_tag, spearman_rows, weights  # noqa: E402
from orderforce_analyze import AXES, ISSUES, NULL, ORDERS, POL, REF, bh, load, other  # noqa: E402
from orderforce_gates import named_position  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PERM = {"paper": [0, 1, 2, 3], "reversed": [3, 2, 1, 0], "scrambled": [2, 0, 3, 1], "scrambled2": [1, 3, 0, 2]}   # stated_logit.ORDERS
LAB = ["SD", "D", "A", "SA"]
F3_LAYOUTS = [(o, "positional") for o in ORDERS] + [(o, "canonical") for o in ORDERS[1:]]
ITEM_REPS, SEED = 2000, 11
READ_D = 0.5   # anchor discrimination threshold of a readable cell (PLAN amendment 2026-10-22)
DISCLAIM = re.compile(r"as an ai|i don't have (personal )?(opinions|feelings|beliefs|views)|i do not have (personal )?(opinions|beliefs|views)"
                      r"|i'm sorry|i am sorry|i cannot|i can't", re.I)
ANSWER_CELLS = [("F1: nothing appended", ("paper", "positional", 1, "none"), "valid_mass"),
                ("F2 + \"No opinion\" offered (any option)", ("paper", "positional", 2, "last"), "valid_mass"),
                ("F3: pick one of the four", REF, "valid_mass"),
                ("F5: ... grandmother will die", ("paper", "positional", 5, "none"), "valid_mass")]


def cell_of(key):
    o, n, f, op = key.split("|")
    return (o, n, int(f), op)


def key_of(cell):
    return "|".join(map(str, cell))


def classify(text, lines):
    """What a greedy decode does: names an option by number or by label, deflects ("as an AI"...), or something else."""
    _, kind = named_position(text, [tuple(x) for x in lines])
    if kind in ("number", "number-unlisted"):
        return "number"
    if kind == "label":
        return "label"
    if DISCLAIM.search(text[:200]):
        return "disclaimer"
    return "label" if kind == "label-inline" else "other"


def layout_shares(rows):
    """(7 layouts, n_items, 4 positions) paraphrase-mean option shares at forcing 3, items present in every layout."""
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        L = (r["order"], r["numbering"])
        if r["forcing"] == 3 and r["optout"] == "none" and L in F3_LAYOUTS and r.get("p_agree") is not None:
            p = np.exp(np.array(r["lp_options"], dtype=float))
            acc[L][r["item"]].append((p / p.sum())[PERM[r["order"]]])   # share of the option listed at position k
    items = sorted(set.intersection(*(set(acc[L]) for L in F3_LAYOUTS)))
    return items, np.array([[np.mean(acc[L][i], axis=0) for i in items] for L in F3_LAYOUTS])


def design():
    """Rows (layout, position): 7 layout constants, position 2-4, printed number 2-4, label D/A/SA (references: 1, 1, SD)."""
    X = []
    for li, (o, n) in enumerate(F3_LAYOUTS):
        for k in range(4):
            lab = PERM[o][k]
            num = lab + 1 if n == "canonical" else k + 1
            x = np.zeros(len(F3_LAYOUTS) + 9)
            x[li] = 1
            if k:
                x[7 + k - 1] = 1
            if num > 1:
                x[10 + num - 2] = 1
            if lab:
                x[13 + lab - 1] = 1
            X.append(x)
    return np.array(X)


def decompose(S, X):
    """OLS of log mean share on the design; effects per factor (reference level 0) and the within-layout R^2."""
    y = np.log(np.maximum(S.ravel(), 1e-6))
    coef = np.linalg.lstsq(X, y, rcond=None)[0]
    res = y - X @ coef
    yc = y - np.repeat([y[4 * i:4 * i + 4].mean() for i in range(len(F3_LAYOUTS))], 4)
    eff = {"position": [0.0] + list(coef[7:10]), "number": [0.0] + list(coef[10:13]), "label": [0.0] + list(coef[13:16])}
    return eff, 1 - (res ** 2).sum() / (yc ** 2).sum()


def d_over(st, axis, cells):
    """d over a set of cells (mean of per-cell d), (REPS+1,) array; None unless every cell has both levels."""
    rep, oth = f"{axis}|{ISSUES[axis]['report']}", f"{axis}|{other(axis, ISSUES[axis]['report'])}"
    ds = []
    for c in cells:
        pr, po = st.mean(c, rep, "p_agree"), st.mean(c, oth, "p_agree")
        if pr is None or po is None:
            return None
        ds.append((pr - po) / 2)
    return np.mean(ds, axis=0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2"))
    ap.add_argument("--q", type=float, default=0.01)
    ap.add_argument("--floor", type=float, default=0.10)
    args = ap.parse_args()
    out = Path(args.dir)
    tags = [roster_tag(m) for m in STAGE_IDS]
    nm = {t: t.split("-")[-1] for t in tags}
    rows = {t: load(out / "raw" / f"orderforce_{t}.jsonl.gz") for t in tags}
    gates = json.loads((out / "orderforce_gates.json").read_text(encoding="utf-8"))
    paras = sorted({r["paraphrase"] for rs in rows.values() for r in rs})
    W = weights(paras, np.random.default_rng(SEED))
    pidx = {pi: i for i, pi in enumerate(paras)}
    S = {t: Stage(rows[t], W, pidx) for t in tags}
    res = {"note": "exploratory, not pre-registered", "tags": tags, "q": args.q, "floor": args.floor}

    # E1 answering
    res["E1_answer_mass"] = {t: {lab: ci(S[t].items_mean(c, ISSUE_ITEMS, k)) for lab, c, k in ANSWER_CELLS} for t in tags}
    dec = {}
    for t in tags:
        drows = load(out / "raw" / f"orderforce_{t}.jsonl.decode.jsonl.gz")
        cnt, ex = Counter(classify(d["text"], d["lines"]) for d in drows), defaultdict(list)
        for d in drows:
            k = classify(d["text"], d["lines"])
            if len(ex[k]) < 2:
                ex[k].append(d["text"][:90].replace("\n", " "))
        dec[t] = {"n": len(drows), "counts": dict(cnt), "examples": dict(ex)}
    res["E1_decodes"] = dec

    # E2 position / number / label decomposition
    X = design()
    assert np.linalg.matrix_rank(X) == X.shape[1], "design not identified"
    rng = np.random.default_rng(SEED + 1)
    res["E2"] = {}
    for t in tags:
        items, A = layout_shares(rows[t])
        eff, r2 = decompose(A.mean(1), X)
        boots = defaultdict(list)
        for _ in range(ITEM_REPS):
            e, _ = decompose(A[:, rng.integers(0, len(items), len(items))].mean(1), X)
            for f, v in e.items():
                boots[f].append(v)
        res["E2"][t] = {"n_items": len(items), "r2": float(r2), "shares": {key_of(L + (3, "none")): A.mean(1)[li].tolist() for li, L in enumerate(F3_LAYOUTS)},
                        "effects": {f: {"est": [float(x) for x in v], "lo": np.percentile(boots[f], 2.5, axis=0).tolist(), "hi": np.percentile(boots[f], 97.5, axis=0).tolist(),
                                        "range": float(max(v) - min(v)), "range_lo": float(np.percentile(np.ptp(boots[f], axis=1), 2.5)),
                                        "range_hi": float(np.percentile(np.ptp(boots[f], axis=1), 97.5))} for f, v in eff.items()}}

    # E3 readable cells
    readable = {t: sorted(c for c, v in gates[t]["anchors"].items() if v["D"] >= READ_D) for t in tags}
    post = [t for t in tags if readable[t]]
    common = sorted(set.intersection(*(set(readable[t]) for t in post))) if post else []
    panel_g = json.loads((ROOT / "results" / "orderforce_gates.json").read_text(encoding="utf-8"))
    panel_r = json.loads((ROOT / "results" / "orderforce.json").read_text(encoding="utf-8"))
    reliable = [m for m, v in panel_r["models"].items() if not v["instrument_unreliable"]]
    res["E3"] = {"D": {t: {c: v["D"] for c, v in gates[t]["anchors"].items()} for t in tags}, "readable": readable, "common": common,
                 "panel_D_reference": {m: panel_g[m]["anchor_gates"]["D_reference"] for m in reliable}}

    # E4 directions in the cells every post-trained stage reads
    cells = [cell_of(c) for c in common]
    E4 = {"cells": common, "stages": {}, "pairs": {}}
    D4 = {t: {a: d_over(S[t], a, cells) for a in AXES} for t in post}
    for t in post:
        s = {a: ci(D4[t][a]) for a in AXES}
        rej = bh([s[a]["p"] if s[a] else 1.0 for a in AXES], args.q)
        for i, a in enumerate(AXES):
            if s[a]:
                s[a]["called"] = bool(i in rej and excludes0(s[a]) and abs(s[a]["mean"]) >= args.floor)
                per = [float(d_over(S[t], a, [c])[0]) for c in cells]
                s[a]["cells_same_sign"] = int(sum(np.sign(x) == np.sign(s[a]["mean"]) for x in per))
        mass = [S[t].items_mean(c, ISSUE_ITEMS, "valid_mass") for c in cells]
        E4["stages"][t] = {"d": s, "valid_mass": ci(np.mean(mass, axis=0)),
                           "acquiescence": ci(np.mean([S[t].items_mean(c, ISSUE_ITEMS, "p_agree") for c in cells], axis=0))}
    for a_, b_ in [(post[i], post[i + 1]) for i in range(len(post) - 1)] + ([(post[0], post[-1])] if len(post) > 2 else []):
        s = {a: ci(D4[b_][a] - D4[a_][a]) if D4[a_][a] is not None and D4[b_][a] is not None else None for a in AXES}
        rej = bh([s[a]["p"] if s[a] else 1.0 for a in AXES], args.q)
        for i, a in enumerate(AXES):
            if s[a]:
                s[a]["shift"] = bool(i in rej and excludes0(s[a]) and abs(s[a]["mean"]) >= args.floor)
        Xa, Xb = (np.stack([D4[t][a] for a in POL], 1) for t in (a_, b_))
        E4["pairs"][f"{a_}->{b_}"] = {"d": s, "profile_spearman": ci(spearman_rows(Xa, Xb)),
                                     "same_sign": int(sum(np.sign(D4[a_][a][0]) == np.sign(D4[b_][a][0]) for a in POL))}
    res["E4"] = E4

    # E5 panel context (point estimates)
    panel = {}
    for m in reliable:
        f = ROOT / "results" / "raw" / f"orderforce_{m}.jsonl.gz"
        ok = [cell_of(c) for c in common if panel_g[m]["anchors"].get(c, {}).get("D", -9) >= READ_D]
        if f.exists() and ok:
            st = Stage(load(f), W, pidx)
            panel[m] = {a: float(d_over(st, a, ok)[0]) for a in POL}
    pmean = {a: float(np.mean([panel[m][a] for m in panel])) for a in POL}
    E5 = {"models": sorted(panel), "panel_mean": pmean, "panel_positive": {a: int(sum(panel[m][a] > 0 for m in panel)) for a in POL},
          "olmo3": panel.get("olmo-3.1-32b"), "vs_panel": {}}
    for t in post:
        Xs = np.stack([D4[t][a] for a in POL], 1)
        E5["vs_panel"][t] = {"spearman": ci(spearman_rows(Xs, np.tile([pmean[a] for a in POL], (Xs.shape[0], 1)))),
                             "same_sign": int(sum(np.sign(D4[t][a][0]) == np.sign(pmean[a]) for a in POL))}
    res["E5"] = E5
    json.dump(res, open(out / "olmo2_explore.json", "w", encoding="utf-8"), indent=1, default=float)

    # ---------- markdown
    f2 = lambda s, sg=True: "—" if not s else (f"{s['mean']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}]" if sg else f"{s['mean']:.2f} [{s['lo']:.2f}, {s['hi']:.2f}]")
    L = ["# OLMo 2 7B training stages: exploratory analyses (not pre-registered)", "",
         f"Stages: {', '.join(tags)}. 95% CIs: cluster bootstrap over the {len(paras)} paraphrases (E1, E4) or over items (E2).", "",
         "## E1 Answering", "", "Answer mass: probability that the next token starts any listed option; mean over the 34 issue statements, paper order.", "",
         "| condition | " + " | ".join(nm[t] for t in tags) + " |", "|---|" + "---|" * len(tags)]
    for lab, _, _ in ANSWER_CELLS:
        L.append(f"| {lab} | " + " | ".join(f2(res['E1_answer_mass'][t][lab], sg=False) for t in tags) + " |")
    L += ["", f"Greedy decodes (72 per stage: 24 statements x scrambled/positional F3, reversed/canonical F3, paper/positional F2 with \"No opinion\"):", "",
          "| stage | number | label | disclaimer | other | example of the most common kind |", "|---|---|---|---|---|---|"]
    for t in tags:
        c = dec[t]["counts"]
        top = max(c, key=c.get)
        L.append(f"| {nm[t]} | {c.get('number', 0)} | {c.get('label', 0)} | {c.get('disclaimer', 0)} | {c.get('other', 0)} | {top}: \"{dec[t]['examples'][top][0]}\" |")
    L += ["", "## E2 What picks the option (forcing 3, seven layouts)", "",
          "log share = layout + position + printed number + label. Effects relative to position 1 / number 1 / Strongly disagree; "
          "range = max − min over the four levels (log units; 1.0 ≈ a factor of 2.7 in the odds of being picked).", "",
          "| stage | items | R² | position: effects pos1..4 | range | number: effects #1..4 | range | label: effects SD, D, A, SA | range |", "|---|---|---|---|---|---|---|---|---|"]
    for t in tags:
        e = res["E2"][t]
        cells_ = []
        for f in ("position", "number", "label"):
            v = e["effects"][f]
            cells_ += [" ".join(f"{x:+.1f}" for x in v["est"]), f"{v['range']:.1f} [{v['range_lo']:.1f}, {v['range_hi']:.1f}]"]
        L.append(f"| {nm[t]} | {e['n_items']} | {e['r2']:.2f} | " + " | ".join(cells_) + " |")
    L += ["", "Mean option shares per layout (listed top to bottom; `#n` = printed number):", ""]
    for t in tags:
        L.append(f"- **{nm[t]}**: " + "; ".join(f"{k.split('|')[0]}/{k.split('|')[1][:3]}: " + " ".join(
            f"#{(PERM[k.split('|')[0]][i] + 1) if 'canonical' in k else i + 1}{LAB[PERM[k.split('|')[0]][i]]} {v:.2f}" for i, v in enumerate(sh))
            for k, sh in res["E2"][t]["shares"].items()))
    L += ["", f"## E3 Where the content gets through (anchor discrimination D; readable = D ≥ {READ_D})", "",
          "| cell | " + " | ".join(nm[t] for t in tags) + " |", "|---|" + "---|" * len(tags)]
    for c in sorted({c for t in tags for c in gates[t]["anchors"]}, key=lambda c: (cell_of(c)[2], c)):
        L.append(f"| {c} | " + " | ".join((f"**{gates[t]['anchors'][c]['D']:.2f}**" if gates[t]["anchors"][c]["D"] >= READ_D else f"{gates[t]['anchors'][c]['D']:.2f}") if c in gates[t]["anchors"] else "—" for t in tags) + " |")
    pd = sorted(res["E3"]["panel_D_reference"].values())
    L += ["", f"Readable for every post-trained stage: {', '.join(common) or 'none'}. For comparison, the {len(pd)} instrument-reliable panel models "
          f"have D {min(pd):.2f}–{max(pd):.2f} (median {np.median(pd):.2f}) at the reference cell (paper|positional|3|none).", "",
          f"## E4 Stated directions in the cells every post-trained stage reads", "",
          f"Cells: {', '.join(common)}. d = (p_agree(report level) − p_agree(other level))/2, mean over the cells; called = CI excludes 0, |d| ≥ {args.floor}, "
          f"BH q = {args.q} over the 19 axes; (k/{len(cells)}) = cells whose own d has the same sign.", "",
          "| | " + " | ".join(nm[t] for t in post) + " |", "|---|" + "---|" * len(post),
          "| answer mass in these cells | " + " | ".join(f2(E4["stages"][t]["valid_mass"], sg=False) for t in post) + " |",
          "| acquiescence (mean p_agree) | " + " | ".join(f2(E4["stages"][t]["acquiescence"], sg=False) for t in post) + " |",
          "| issues called (of 17) | " + " | ".join(str(sum(E4["stages"][t]["d"][a]["called"] for a in POL)) for t in post) + " |",
          "| null axes called (of 2) | " + " | ".join(str(sum(E4["stages"][t]["d"][a]["called"] for a in NULL)) for t in post) + " |", "",
          "| issue | " + " | ".join(nm[t] for t in post) + " | panel mean (models > 0) | Olmo 3.1 32B |", "|---|" + "---|" * (len(post) + 2)]
    for a in AXES:
        cols = []
        for t in post:
            s = E4["stages"][t]["d"][a]
            cols.append(f"{f2(s)}{' ✓' if s['called'] else ''} ({s['cells_same_sign']}/{len(cells)})")
        pm = f"{pmean[a]:+.2f} ({E5['panel_positive'][a]}/{len(panel)})" if a in pmean else "—"
        o3 = f"{E5['olmo3'][a]:+.2f}" if E5["olmo3"] and a in E5["olmo3"] else "—"
        L.append(f"| {a}{' (null)' if a in NULL else ''} | " + " | ".join(cols) + f" | {pm} | {o3} |")
    L += ["", "Paired stage contrasts in these cells (shift = CI excludes 0, |Δd| ≥ floor, BH over 19 axes):", "",
          "| stage pair | Spearman ρ of the 17-issue profiles | same sign | issues that shift (Δd) |", "|---|---|---|---|"]
    for p, P in E4["pairs"].items():
        a_, b_ = p.split("->")
        sh = [f"{a} {P['d'][a]['mean']:+.2f}" for a in AXES if P["d"][a] and P["d"][a]["shift"]]
        L.append(f"| {nm[a_]} → {nm[b_]} | {f2(P['profile_spearman'])} | {P['same_sign']}/17 | {', '.join(sh) or '—'} |")
    L += ["", f"## E5 Against the panel (same cells; {len(panel)} instrument-reliable panel models that read at least one of them)", "",
          "| stage | Spearman ρ with the panel mean | same sign as the panel mean |", "|---|---|---|"]
    for t in post:
        L.append(f"| {nm[t]} | {f2(E5['vs_panel'][t]['spearman'])} | {E5['vs_panel'][t]['same_sign']}/17 |")
    (out / "olmo2_explore.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    main()
