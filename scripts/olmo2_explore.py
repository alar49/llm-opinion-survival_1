"""OLMo 2 7B across training stages, v2 (PLAN_OLMO2.md): H1 (the base model in the completion format, endings A-D),
H2 (what picks the option), H3 (saturation vs salience), and the content effect per cell and run. The stage
comparisons (H4-H6) are in olmo2_compare.py, whose bootstrap (paraphrase clusters, 4,000 reps, seed 7) and coverage
check this script reuses.

H1a  the base model answers (ending A): median answer mass at the reference cell over the 34 issue statements; >= 0.5
     supported, < 0.3 not supported, else partial; decided only if the format is captured (§3.4).
H1b  the base model reads (ending A): anchor content effect C at the reference cell; reads = C >= 0.5 with CI lower
     bound > 0, does not read = CI includes 0, weak = reliably positive but below 0.5.
H1c  endings A-D for the base model: answer mass, anchor D and C, coverage (descriptive).
H2   per stage (ending A), a log-linear decomposition of the mean option shares over the seven forcing-3 layouts (4 orders
     x positional numbering, 3 orders x pinned numbering) on the 50 items present in all seven: log share = layout
     constant + list position + printed number + label. Positional numbering ties number to position, pinned numbering
     ties it to the label, and the Latin square unties label from position, so the three are separately identified.
     Effects relative to position 1, number 1, Strongly disagree; 95% CIs from a bootstrap over items (2,000 reps).
     H2a: min(Disagree, Agree) - max(Strongly disagree, Strongly agree) >= 1.0 log unit for every post-trained stage.
     H2b: position 4 - position 3 > -0.5 (descriptive).
H3   per stage, C averaged over the three pinned forcing-3 layouts / C averaged over the four positional ones: [0.8, 1.25]
     saturation, > 1.25 salience, < 0.8 reverse (post-trained stages; decided on the point estimate). Beside it, the
     pinned layouts at forcing 5 against forcing 3.
Also: C and D per cell and run (a stage reads a cell if C >= 0.5), and the greedy decodes by kind and cell.

Reads <dir>/raw/orderforce_<tag>.jsonl[.gz] (+ .decode); writes <dir>/olmo2_explore.{md,json}.
Usage: python3 scripts/olmo2_explore.py [--dir results/olmo2_v2]
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from olmo2_compare import (ENDING_TAG, F3_CELLS, ISSUE_ITEMS, POST, READ_C, REF, SEED, STAGE_TAG, STAGES, ci, classify,  # noqa: E402
                           load_runs, raw_file, read_class)
from orderforce_analyze import ORDERS, load  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
PERM = {"paper": [0, 1, 2, 3], "reversed": [3, 2, 1, 0], "scrambled": [2, 0, 3, 1], "scrambled2": [1, 3, 0, 2]}   # stated_logit.ORDERS
LAB = ["SD", "D", "A", "SA"]
F3_LAYOUTS = [(o, "positional") for o in ORDERS] + [(o, "canonical") for o in ORDERS[1:]]   # the order of F3_CELLS
POSITIONAL, PINNED = F3_CELLS[:4], F3_CELLS[4:]
PINNED_F5 = [(o, "canonical", 5, "none") for o in ORDERS[1:]]
ITEM_REPS = 2000


def layout_shares(rows):
    """(7 layouts, n_items, 4 positions) paraphrase-mean option shares at forcing 3, items present in every layout."""
    acc = defaultdict(lambda: defaultdict(list))
    for r in rows:
        L = (r["order"], r["numbering"])
        if r["forcing"] == 3 and r["optout"] == "none" and L in F3_LAYOUTS and r.get("p_agree") is not None:
            lp = np.array(r["lp_options"], dtype=float)
            p = np.exp(lp - lp.max())
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


def h2_contrasts(eff, weaker, stronger):
    """H2a: label effect of the weaker moderate label minus that of the stronger extreme (both chosen on the full-sample
    estimate and held fixed in the bootstrap, so the interval is that of a plain contrast); H2b: position 4 - position 3."""
    return {"moderate_minus_extreme": eff["label"][weaker] - eff["label"][stronger], "pos4_minus_pos3": eff["position"][3] - eff["position"][2]}


def ci_items(est, boots):
    b = np.asarray(boots)
    return {"est": est, "lo": float(np.percentile(b, 2.5)), "hi": float(np.percentile(b, 97.5))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2_v2"))
    args = ap.parse_args()
    out = Path(args.dir)
    rows, paras, W, S, cov = load_runs(out)
    st_ = [s for s in STAGES if STAGE_TAG[s] in S]
    res = {"runs": list(rows), "paraphrases": paras, "coverage": cov}

    # H1 the base model in the completion format
    H1 = {}
    tA = ENDING_TAG["A"]
    if tA in S:
        med = ci(S[tA].items_stat(REF, ISSUE_ITEMS, "valid_mass", np.median))
        cap = bool(cov[tA].get("captured"))
        H1["H1a"] = {"median_answer_mass": med, "captured": cap,
                     "decision": ("supported" if med["mean"] >= 0.5 else "not supported" if med["mean"] < 0.3 else "partial") if cap
                     else "descriptive only (format not captured)"}
        C = ci(S[tA].anchor([REF], "lo"))
        H1["H1b"] = {"C": C, "D": ci(S[tA].anchor([REF], "score")), "decision": read_class(C)}
    H1["H1c"] = {}
    for e, t in ENDING_TAG.items():
        if t in S:
            x = S[t]
            H1["H1c"][e] = {"tag": t, "median_answer_mass": ci(x.items_stat(REF, ISSUE_ITEMS, "valid_mass", np.median)),
                            "mean_answer_mass": ci(x.items_stat(REF, ISSUE_ITEMS, "valid_mass")),
                            "D": ci(x.anchor([REF], "score")), "C": ci(x.anchor([REF], "lo")), "reads": read_class(ci(x.anchor([REF], "lo"))),
                            "coverage": cov[t]}
    res["H1"] = H1

    # H2 what picks the option
    X = design()
    assert np.linalg.matrix_rank(X) == X.shape[1], "design not identified"
    rng = np.random.default_rng(SEED + 1)
    H2 = {}
    for s in st_:
        items, A = layout_shares(rows[STAGE_TAG[s]])
        eff, r2 = decompose(A.mean(1), X)
        lab = eff["label"]
        weaker, stronger = min((1, 2), key=lambda i: lab[i]), max((0, 3), key=lambda i: lab[i])
        q = h2_contrasts(eff, weaker, stronger)
        boots, qb = defaultdict(list), defaultdict(list)
        for _ in range(ITEM_REPS):
            e, _ = decompose(A[:, rng.integers(0, len(items), len(items))].mean(1), X)
            for f, v in e.items():
                boots[f].append(v)
            for k, v in h2_contrasts(e, weaker, stronger).items():
                qb[k].append(v)
        H2[s] = {"n_items": len(items), "r2": float(r2), "shares": {"|".join(L): A.mean(1)[li].tolist() for li, L in enumerate(F3_LAYOUTS)},
                 "effects": {f: {"est": [float(x) for x in v], "lo": np.percentile(boots[f], 2.5, axis=0).tolist(), "hi": np.percentile(boots[f], 97.5, axis=0).tolist(),
                                 "range": float(max(v) - min(v)), "range_lo": float(np.percentile(np.ptp(boots[f], axis=1), 2.5)),
                                 "range_hi": float(np.percentile(np.ptp(boots[f], axis=1), 97.5))} for f, v in eff.items()},
                 "H2a_moderate_minus_extreme": {**ci_items(float(q["moderate_minus_extreme"]), qb["moderate_minus_extreme"]), "labels": [LAB[weaker], LAB[stronger]]},
                 "H2b_pos4_minus_pos3": ci_items(float(q["pos4_minus_pos3"]), qb["pos4_minus_pos3"])}
    post = [s for s in POST if s in H2]
    res["H2"] = {"stages": H2,
                 "H2a": ("holds" if all(H2[s]["H2a_moderate_minus_extreme"]["est"] >= 1.0 for s in post) else "does not hold") if len(post) == 3 else "untestable (missing stages)",
                 "H2b": {s: H2[s]["H2b_pos4_minus_pos3"]["est"] > -0.5 for s in post}}

    # H3 saturation vs salience
    H3 = {}
    for s in st_:
        x = S[STAGE_TAG[s]]
        cp, cq = x.anchor(PINNED, "lo"), x.anchor(POSITIONAL, "lo")
        ratio = ci(cp / cq) if cq[0] > 0 else None
        cls = ("undefined (C of the positional layouts not above 0)" if ratio is None else
               "saturation" if 0.8 <= ratio["mean"] <= 1.25 else "salience" if ratio["mean"] > 1.25 else "reverse")
        c5 = x.anchor(PINNED_F5, "lo")
        H3[s] = {"C_pinned": ci(cp), "C_positional": ci(cq), "ratio": ratio, "class": cls,
                 "C_pinned_F5": ci(c5), "ratio_F5_F3_pinned": ci(c5 / cp) if c5 is not None and cp[0] > 0 else None}
    res["H3"] = H3

    # C and D per cell and run
    cells = sorted({c for x in S.values() for c in x.T}, key=lambda c: (c[2], c[3], c[1], ORDERS.index(c[0])))
    res["content"] = {t: {"|".join(map(str, c)): {"C": float(S[t].anchor([c], "lo")[0]), "D": float(S[t].anchor([c], "score")[0])}
                          for c in cells if S[t].anchor([c], "lo") is not None} for t in S}

    # decodes
    dec = {}
    for t in S:
        f = raw_file(out, t, ".decode.jsonl")
        drows = load(f) if f.exists() else []
        by = defaultdict(Counter)
        ex = {}
        for d in drows:
            k = classify(d["text"], d["lines"])
            by["|".join(map(str, (d["order"], d["numbering"], d["forcing"], d["optout"])))][k] += 1
            ex.setdefault(k, d["text"][:90].replace("\n", " "))
        dec[t] = {"n": len(drows), "counts": dict(sum(by.values(), Counter())), "by_cell": {c: dict(v) for c, v in by.items()}, "examples": ex}
    res["decodes"] = dec
    json.dump(res, open(out / "olmo2_explore.json", "w", encoding="utf-8"), indent=1, default=float)
    write_md(out, res, st_)


def write_md(out, res, st_):
    f2 = lambda s, sg=True: "—" if not s else (f"{s['mean']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}]" if sg else f"{s['mean']:.2f} [{s['lo']:.2f}, {s['hi']:.2f}]")
    fi = lambda s: f"{s['est']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}]"
    fx = lambda x: "—" if x is None else f"{x:.2f}"
    H1, H2, H3 = res["H1"], res["H2"], res["H3"]
    L = ["# OLMo 2 7B training stages, v2: answering, layout and content (PLAN_OLMO2.md H1, H2, H3)", "",
         f"Runs: {', '.join(res['runs'])}. 95% CIs: cluster bootstrap over the {len(res['paraphrases'])} paraphrases (as in "
         "olmo2_compare.md), or over items for the layout decomposition. Answer mass = probability that the continuation starts with "
         "one of the listed options' answer strings; C = anchor content effect in log-odds; D = anchor discrimination in score units.", "",
         "## H1 The base model in the completion format", ""]
    if "H1a" in H1:
        L += [f"**H1a** (answering, ending A: median answer mass at the reference cell ≥ 0.5): **{H1['H1a']['decision']}**; median answer mass "
              f"{f2(H1['H1a']['median_answer_mass'], False)}.", "",
              f"**H1b** (reading, ending A: C ≥ 0.5 with CI above 0): **{H1['H1b']['decision']}**; C {f2(H1['H1b']['C'])}, D {f2(H1['H1b']['D'])}.", ""]
    L += ["**H1c** (endings, base model; expectation A ≈ C ≥ B > D in answer mass):", "",
          "| ending | run | median answer mass | mean answer mass | D | C | reads | median missed share | format |", "|---|---|---|---|---|---|---|---|---|"]
    for e, v in H1["H1c"].items():
        c = v["coverage"]
        L.append(f"| {e} | {v['tag']} | {f2(v['median_answer_mass'], False)} | {f2(v['mean_answer_mass'], False)} | {f2(v['D'])} | {f2(v['C'])} | {v['reads']} | "
                 f"{fx(c.get('median_missed_share'))} | {'captured' if c.get('captured') else 'not captured'} |")
    L += ["", "## H2 What picks the option (forcing 3, seven layouts, ending A)", "",
          "log share = layout + position + printed number + label. Effects relative to position 1 / number 1 / Strongly disagree; "
          "range = max − min over the four levels (log units; 1.0 ≈ a factor of 2.7). 95% CIs over items.", "",
          f"**H2a** (moderate labels beat both extremes by ≥ 1.0 log unit in every post-trained stage): **{H2['H2a']}**. "
          f"**H2b** (line 4 penalised against line 3 by no more than 0.5, descriptive): "
          + ", ".join(f"{s} {'yes' if v else 'no'}" for s, v in H2["H2b"].items()) + ".", "",
          "| stage | items | R² | position: pos1..4 | range | number: #1..4 | range | label: SD, D, A, SA | range | H2a: min(D, A) − max(SD, SA) | H2b: pos4 − pos3 |",
          "|---|---|---|---|---|---|---|---|---|---|---|"]
    for s, e in H2["stages"].items():
        cells_ = []
        for f in ("position", "number", "label"):
            v = e["effects"][f]
            cells_ += [" ".join(f"{x:+.1f}" for x in v["est"]), f"{v['range']:.1f} [{v['range_lo']:.1f}, {v['range_hi']:.1f}]"]
        h2a = e["H2a_moderate_minus_extreme"]
        L.append(f"| {s} | {e['n_items']} | {e['r2']:.2f} | " + " | ".join(cells_) + f" | {fi(h2a)} ({' − '.join(h2a['labels'])}) | {fi(e['H2b_pos4_minus_pos3'])} |")
    L += ["", "Mean option shares per layout (listed top to bottom; `#n` = printed number):", ""]
    for s, e in H2["stages"].items():
        L.append(f"- **{s}**: " + "; ".join(f"{k.split('|')[0]}/{k.split('|')[1][:3]}: " + " ".join(
            f"#{(PERM[k.split('|')[0]][i] + 1) if 'canonical' in k else i + 1}{LAB[PERM[k.split('|')[0]][i]]} {v:.2f}" for i, v in enumerate(sh))
            for k, sh in e["shares"].items()))
    L += ["", "## H3 Saturation or salience? (C, pinned vs positional numbering, forcing 3)", "",
          "Ratio in [0.8, 1.25] = saturation (the content effect is the same size, and the layout only masks it); > 1.25 = salience; "
          "< 0.8 = reverse. Decided for the post-trained stages; the base model is shown for reference.", "",
          "| stage | C pinned (3 layouts) | C positional (4 layouts) | ratio | class | C pinned at F5 | F5 / F3 (pinned) |", "|---|---|---|---|---|---|---|"]
    for s, v in H3.items():
        L.append(f"| {s} | {f2(v['C_pinned'])} | {f2(v['C_positional'])} | {f2(v['ratio'])} | {v['class']} | {f2(v['C_pinned_F5'])} | {f2(v['ratio_F5_F3_pinned'])} |")
    runs = list(res["content"])
    L += ["", f"## Content effect per cell (C, with D in brackets; bold = reads, C ≥ {READ_C})", "",
          "| cell | " + " | ".join(runs) + " |", "|---|" + "---|" * len(runs)]
    for c in dict.fromkeys(c for t in runs for c in res["content"][t]):
        L.append(f"| {c} | " + " | ".join(
            (lambda v: "—" if v is None else (f"**{v['C']:+.2f}**" if v["C"] >= READ_C else f"{v['C']:+.2f}") + f" ({v['D']:+.2f})")(res["content"][t].get(c)) for t in runs) + " |")
    L += ["", "## Greedy decodes (24 statements × 6 cells per run)", "",
          "| run | decodes | number | label | deflection | other | example of the most common kind |", "|---|---|---|---|---|---|---|"]
    for t, v in res["decodes"].items():
        c = v["counts"]
        top = max(c, key=c.get) if c else None
        L.append(f"| {t} | {v['n']} | {c.get('number', 0)} | {c.get('label', 0)} | {c.get('deflection', 0)} | {c.get('other', 0)} | "
                 + (f"{top}: \"{v['examples'][top]}\"" if top else "—") + " |")
    (out / "olmo2_explore.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:50]))
    print(f"wrote {out / 'olmo2_explore.md'} and {out / 'olmo2_explore.json'}")


if __name__ == "__main__":
    main()
