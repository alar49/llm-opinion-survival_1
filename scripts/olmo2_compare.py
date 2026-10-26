"""Paired comparison of the OLMo 2 7B training stages (base -> SFT -> DPO -> Instruct/RLVR) on the order-forcing grid.

All four checkpoints share one tokenizer and are scored under one chat template (the base model takes its post-trained
checkpoints' template: scripts/sweep_models.json), so every stage answers token-identical prompts and every contrast is
paired by prompt key. Per axis and cell, d = (p_agree(report level) - p_agree(other level))/2, paraphrase-mean, as in
orderforce_analyze.py. The cluster bootstrap over paraphrase indices draws one weight vector per rep and applies it to
every stage, cell and item, so Δd = d(later stage) - d(earlier stage) is a paired estimate. A shift counts when it
mirrors R0 (PLAN §5): bootstrap CI excludes 0, |Δd| >= FLOOR, BH over the 19 axes (17 issues + 2 null controls) within
each stage pair and cell. The floor matters: with four paraphrase clusters, any shift whose sign agrees across all four
paraphrases gets the bootstrap's floor p, however small it is. Shifts on the null axes are the false-positive check.
Model-level quantities (answer mass, opt-out uptake, acquiescence, anchor discrimination, order spin, mean |d|) and the
Spearman similarity of the 17-issue d profiles get the same paired bootstrap.

Cells: reference (O1, F3, positional); order mean (the four positional orders at F3, position-free by the Latin square);
forcing 5 (O1); opt-out offered (O1, F2, "No opinion" last; d conditional on the four substantive labels).

Reads <dir>/raw/orderforce_<tag>.jsonl[.gz] and, when present, <dir>/orderforce.json (rungs, reliability flags);
writes <dir>/olmo2_compare.{md,json}.
Usage: python3 scripts/olmo2_compare.py [--dir results/olmo2] [--tags a,b,c,d] [--q 0.01] [--floor 0.10]
       python3 scripts/olmo2_compare.py --check_prompts   (pod side, needs transformers: every grid prompt token-identical across stages)
       python3 scripts/olmo2_compare.py --list            (id:tag per stage, for run_olmo2.sh)
"""
import argparse
import json
import os
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orderforce_analyze import AXES, ISSUES, NULL, ORDERS, POL, REF, bh, load, other, summ  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ROSTER = json.loads((Path(__file__).resolve().parent / "sweep_models.json").read_text())
ANCHORS = json.loads((DATA / "orderforce_anchors.json").read_text())
STAGE_IDS = ["allenai/OLMo-2-1124-7B", "allenai/OLMo-2-1124-7B-SFT", "allenai/OLMo-2-1124-7B-DPO", "allenai/OLMo-2-1124-7B-Instruct"]
REPS, SEED = 4000, 7
CELLS = {"reference": [REF], "order mean": [(o, "positional", 3, "none") for o in ORDERS],
         "forcing 5": [("paper", "positional", 5, "none")], "opt-out offered": [("paper", "positional", 2, "last")]}
ISSUE_ITEMS = [f"{a}|{lvl}" for a in POL for lvl in ISSUES[a]["levels"]]   # the 34 issue statements


def roster_tag(model_id):
    for m in ROSTER["models"]:
        if m["id"] == model_id:
            return m["tag"]
    return model_id.split("/")[-1]


def check_prompts(ids):
    """Every grid prompt and every option continuation must tokenize identically under every stage's tokenizer and
    template; exits non-zero otherwise. Imports the scorer (torch, transformers), so it runs pod side."""
    import stated_logit as S
    from logit_sweep import load_tokenizer, model_cfg
    grid = json.loads((DATA / "orderforce_grid.json").read_text())
    optout_text = grid.get("optout_text", S.OPTOUT_TEXT)
    items = S.build_items(DATA / "pct_issues.json", include_null=True) + S.load_extra_items(DATA / "orderforce_anchors.json")
    prompts = S.build_prompts_grid(items, grid, None)
    cells = sorted({(p["order"], p["numbering"], p["optout"]) for p in prompts})
    first = None
    for mid in ids:
        cfg = model_cfg(mid)
        tok = load_tokenizer(cfg)
        texts = [S.render_user_prefix(tok, None, p["user"], cfg)[0] for p in prompts]
        enc = [tok(t, add_special_tokens=False)["input_ids"] for t in texts]
        conts = [S.option_conts(tok, S.option_lines(o, n, None if op == "none" else op, optout_text), optout_text) for o, n, op in cells]
        if first is None:
            first = (mid, enc, conts, texts[0])
        else:
            bad = sum(a != b for a, b in zip(enc, first[1]))
            if bad or conts != first[2]:
                sys.exit(f"{mid}: {bad} of {len(prompts)} prompts differ from {first[0]}; option continuations "
                         f"{'differ' if conts != first[2] else 'match'}")
        print(f"{mid} ({cfg['tag']}): {len(prompts)} prompts, {len(cells)} option layouts"
              + ("" if mid == first[0] else f", token-identical to {first[0]}"), flush=True)
    print("example prompt:", repr(first[3]), flush=True)


def weights(paras, rng):
    """Row 0 = equal weights (point estimate); rows 1..REPS = paraphrase-cluster resamples, shared by every stage."""
    W = np.zeros((REPS + 1, len(paras)))
    W[0] = 1.0 / len(paras)
    for b in range(1, REPS + 1):
        W[b] = np.bincount(rng.integers(0, len(paras), len(paras)), minlength=len(paras)) / len(paras)
    return W


class Stage:
    def __init__(self, rows, W, pidx):
        self.T = defaultdict(lambda: defaultdict(dict))
        for r in rows:
            if r.get("p_agree") is not None:
                self.T[(r["order"], r["numbering"], r["forcing"], r["optout"])][r["item"]][r["paraphrase"]] = r
        self.W, self.pidx = W, pidx

    def mean(self, cell, item, key):
        """Paraphrase-weighted mean of a row field as a (REPS+1,) array, weights renormalised to the paraphrases present."""
        byp = self.T.get(cell, {}).get(item, {})
        present = [pi for pi in byp if byp[pi].get(key) is not None]
        if not present:
            return None
        w = self.W[:, [self.pidx[pi] for pi in present]]
        s = w.sum(1, keepdims=True)
        w = np.where(s > 0, w / np.where(s > 0, s, 1), 1.0 / len(present))
        return w @ np.array([byp[pi][key] for pi in present], dtype=float)

    def items_mean(self, cell, items, key):
        vs = [v for v in (self.mean(cell, it, key) for it in items) if v is not None]
        return np.mean(vs, axis=0) if vs else None

    def d(self, axis, group):
        """d averaged over the cells of a group; None unless every cell has both levels."""
        rep, oth = f"{axis}|{ISSUES[axis]['report']}", f"{axis}|{other(axis, ISSUES[axis]['report'])}"
        ds = []
        for c in CELLS[group]:
            pr, po = self.mean(c, rep, "p_agree"), self.mean(c, oth, "p_agree")
            if pr is None or po is None:
                return None
            ds.append((pr - po) / 2)
        return np.mean(ds, axis=0)


def metrics(s):
    """Model-level quantities over the 34 issue statements (anchors for D), each a (REPS+1,) array or None."""
    m = {f"answer mass F{fl} (O1)": s.items_mean(("paper", "positional", fl, "none"), ISSUE_ITEMS, "valid_mass") for fl in (1, 3, 5)}
    m["No-opinion share (O1, F2)"] = s.items_mean(("paper", "positional", 2, "last"), ISSUE_ITEMS, "p_optout")
    m["acquiescence: mean p_agree (reference)"] = s.items_mean(REF, ISSUE_ITEMS, "p_agree")
    ag = s.items_mean(REF, [a["id"] for a in ANCHORS if a["expected"] == "agree"], "score")
    dg = s.items_mean(REF, [a["id"] for a in ANCHORS if a["expected"] == "disagree"], "score")
    m["anchor discrimination D (reference)"] = (ag - dg) / 2 if ag is not None and dg is not None else None
    spans = []
    for it in ISSUE_ITEMS:
        xs = [s.mean((o, "positional", 3, "none"), it, "score") for o in ORDERS]
        if all(x is not None for x in xs):
            xs = np.stack(xs)
            spans.append(xs.max(0) - xs.min(0))
    m["order spin: score range over 4 orders (F3)"] = np.mean(spans, axis=0) if spans else None
    ds = [s.d(a, "reference") for a in POL]
    m["mean |d| over 17 issues (reference)"] = np.mean(np.abs(ds), axis=0) if all(x is not None for x in ds) else None
    return m


def ci(v):
    """orderforce_analyze.summ (point estimate v[0], percentile 95% CI and two-sided p over v[1:]); p = 1 when every
    bootstrap value is exactly 0."""
    if v is None:
        return None
    s = summ(v)
    if not np.any(v[1:]):
        s["p"] = 1.0
    return s


def spearman_rows(X, Y):
    """Row-wise Spearman correlation of two (reps, n) arrays."""
    from scipy.stats import rankdata
    rx, ry = rankdata(X, axis=1), rankdata(Y, axis=1)
    rx, ry = rx - rx.mean(1, keepdims=True), ry - ry.mean(1, keepdims=True)
    return (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))


def excludes0(s):
    return bool(s) and (s["lo"] > 0 or s["hi"] < 0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2"), help="holds raw/orderforce_<tag>.jsonl[.gz]; outputs go here")
    ap.add_argument("--tags", default=None, help="comma-separated tags in stage order (default: the roster tags of the four OLMo 2 7B stages)")
    ap.add_argument("--q", type=float, default=0.01, help="BH level over the 19 axes, per stage pair and cell (R0's level)")
    ap.add_argument("--floor", type=float, default=0.10, help="minimum |Δd| in p_agree units for a shift to count (R0's floor)")
    ap.add_argument("--check_prompts", action="store_true", help="check token identity of the grid across the stages and exit")
    ap.add_argument("--list", action="store_true", help="print id:tag per stage and exit")
    args = ap.parse_args()
    if args.list:
        print("\n".join(f"{m}:{roster_tag(m)}" for m in STAGE_IDS))
        return
    if args.check_prompts:
        check_prompts(STAGE_IDS)
        return
    out = Path(args.dir)
    tags = args.tags.split(",") if args.tags else [roster_tag(m) for m in STAGE_IDS]
    rows = {}
    for t in tags:
        gz, plain = out / "raw" / f"orderforce_{t}.jsonl.gz", out / "raw" / f"orderforce_{t}.jsonl"
        f = gz if gz.exists() else plain
        if f.exists():
            rows[t] = load(f)
        else:
            print(f"missing {f}; {t} left out", flush=True)
    tags = [t for t in tags if t in rows]
    if len(tags) < 2:
        sys.exit("need at least two stages")
    pre = os.path.commonprefix(tags)
    pre = pre[:pre.rfind("-") + 1]
    nm = {t: t[len(pre):] or t for t in tags}
    paras = sorted({r["paraphrase"] for rs in rows.values() for r in rs})
    W = weights(paras, np.random.default_rng(SEED))
    S = {t: Stage(rows[t], W, {pi: i for i, pi in enumerate(paras)}) for t in tags}
    D = {t: {g: {a: S[t].d(a, g) for a in AXES} for g in CELLS} for t in tags}
    M = {t: metrics(S[t]) for t in tags}
    R = json.loads((out / "orderforce.json").read_text()) if (out / "orderforce.json").exists() else {"models": {}}
    res = {"tags": tags, "paraphrases": paras, "reps": REPS, "q": args.q, "floor": args.floor,
           "cells": {g: ["|".join(map(str, c)) for c in cs] for g, cs in CELLS.items()}, "stages": {}, "pairs": {}}
    for t in tags:
        Rm = R["models"].get(t, {})
        res["stages"][t] = {"metrics": {k: ci(v) for k, v in M[t].items()}, "d": {g: {a: ci(D[t][g][a]) for a in AXES} for g in CELLS},
                            "rungs": {a: Rm["axes"][a]["rung"] for a in AXES if a in Rm.get("axes", {})},
                            "instrument_unreliable": Rm.get("instrument_unreliable"), "numbering_limited": Rm.get("numbering_limited")}
    pairs = list(zip(tags, tags[1:])) + ([(tags[0], tags[-1])] if len(tags) > 2 else [])
    for a_, b_ in pairs:
        P = {"metrics": {k: ci(M[b_][k] - M[a_][k]) if M[a_][k] is not None and M[b_][k] is not None else None for k in M[a_]}, "d": {}}
        for g in CELLS:
            s = {ax: ci(D[b_][g][ax] - D[a_][g][ax]) if D[a_][g][ax] is not None and D[b_][g][ax] is not None else None for ax in AXES}
            rej = bh([s[ax]["p"] if s[ax] else 1.0 for ax in AXES], args.q)
            for i, ax in enumerate(AXES):
                if s[ax]:
                    s[ax]["shift"] = bool(i in rej and excludes0(s[ax]) and abs(s[ax]["mean"]) >= args.floor)
            P["d"][g] = s
        da, db = res["stages"][a_]["d"]["reference"], res["stages"][b_]["d"]["reference"]
        if all(D[t]["reference"][ax] is not None for t in (a_, b_) for ax in POL):
            X, Y = (np.stack([D[t]["reference"][ax] for ax in POL], 1) for t in (a_, b_))
            P["profile_spearman"] = ci(spearman_rows(X, Y))
        P["same_sign"] = int(sum(np.sign(da[ax]["mean"]) == np.sign(db[ax]["mean"]) for ax in POL if da[ax] and db[ax]))
        P["opposite_sign_both_clear"] = [ax for ax in POL if excludes0(da[ax]) and excludes0(db[ax]) and np.sign(da[ax]["mean"]) != np.sign(db[ax]["mean"])]
        res["pairs"][f"{a_}->{b_}"] = P
    json.dump(res, open(out / "olmo2_compare.json", "w"), indent=1, default=float)
    # ---------- markdown
    f2 = lambda s, sg=True: "—" if not s else (f"{s['mean']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}]" if sg else f"{s['mean']:.2f} [{s['lo']:.2f}, {s['hi']:.2f}]")
    pn = {f"{a_}->{b_}": f"{nm[a_]} → {nm[b_]}" for a_, b_ in pairs}
    L = [f"# OLMo 2 training stages: paired comparison on the order-forcing grid", "",
         f"Stages in order: {', '.join(tags)}. Every stage answered the same token-identical prompts, so each contrast is paired by prompt. "
         f"95% CIs from a cluster bootstrap over the {len(paras)} paraphrases ({REPS} reps, one draw shared by every stage and cell). "
         f"d = (p_agree(report level) − p_agree(other level))/2, coded toward each issue's report level as in orderforce.md. "
         f"A per-issue shift counts (†) when its CI excludes 0, |Δd| ≥ {args.floor} and it survives BH at q = {args.q} over the "
         f"{len(AXES)} axes (17 issues + 2 null controls) within its stage pair and cell.", "",
         "## Stage summary", "", "| quantity | " + " | ".join(nm[t] for t in tags) + " |", "|---|" + "---|" * len(tags)]
    for t_flag, lab in (("instrument_unreliable", "instrument-reliable (anchor gate)"), ("numbering_limited", "numbering-limited")):
        vals = [res["stages"][t][t_flag] for t in tags]
        if any(v is not None for v in vals):
            yes = (lambda v: "no" if v else "yes") if t_flag == "instrument_unreliable" else (lambda v: "yes" if v else "no")
            L.append(f"| {lab} | " + " | ".join("—" if v is None else yes(v) for v in vals) + " |")
    if any(res["stages"][t]["rungs"] for t in tags):
        for lab, keep in (("issues called (R0)", ("called", "+order", "+forcing", "survives all")), ("issues surviving everything (R3)", ("survives all",))):
            L.append(f"| {lab} | " + " | ".join(str(sum(res['stages'][t]['rungs'].get(a) in keep for a in POL)) if res["stages"][t]["rungs"] else "—" for t in tags) + " |")
    for k in M[tags[0]]:
        L.append(f"| {k} | " + " | ".join(f2(res["stages"][t]["metrics"][k], sg=False) for t in tags) + " |")
    L += ["", "## Paired stage contrasts (later − earlier, 95% CI)", "", "| quantity | " + " | ".join(pn.values()) + " |", "|---|" + "---|" * len(pairs)]
    for k in M[tags[0]]:
        L.append(f"| {k} | " + " | ".join(f2(res["pairs"][p]["metrics"][k]) for p in pn) + " |")
    L += ["", "## How similar are the stages' issue profiles? (d at the reference cell, 17 issues)", "",
          "| stage pair | Spearman ρ [95% CI] | same sign | issues clear in both stages but with opposite sign |", "|---|---|---|---|"]
    for p in pn:
        P = res["pairs"][p]
        L.append(f"| {pn[p]} | {f2(P.get('profile_spearman'))} | {P['same_sign']}/17 | {', '.join(P['opposite_sign_both_clear']) or '—'} |")
    L += ["", "## Stated direction d per issue (reference cell)", "", "| issue | " + " | ".join(nm[t] for t in tags) + " |", "|---|" + "---|" * len(tags)]
    for a in AXES:
        L.append(f"| {a}{' (null)' if a in NULL else ''} | " + " | ".join(f2(res["stages"][t]["d"]["reference"][a])
                 + (f" · {res['stages'][t]['rungs'][a]}" if a in res["stages"][t]["rungs"] else "") for t in tags) + " |")
    for p in pn:
        P = res["pairs"][p]
        n_shift = {g: sum(bool(P["d"][g][a] and P["d"][g][a]["shift"]) for a in POL) for g in CELLS}
        n_null = sum(bool(P["d"][g][a] and P["d"][g][a]["shift"]) for g in CELLS for a in NULL)
        L += ["", f"## Δd per issue: {pn[p]}", "",
              "Shifts that count, by cell: " + "; ".join(f"{g} {n}/17" for g, n in n_shift.items()) + f". Null-axis shifts (false positives): {n_null} of {2 * len(CELLS)}.", "",
              "| issue | " + " | ".join(CELLS) + " |", "|---|" + "---|" * len(CELLS)]
        for a in AXES:
            L.append(f"| {a}{' (null)' if a in NULL else ''} | " + " | ".join(f2(P["d"][g][a]) + (" †" if P["d"][g][a] and P["d"][g][a]["shift"] else "") for g in CELLS) + " |")
    L += ["", "Cells: reference = paper order, forcing 3; order mean = mean of d over the four positional orders at forcing 3 "
          "(position-free by the Latin square); forcing 5 = paper order, the grandmother text; opt-out offered = paper order, "
          "forcing 2, \"No opinion\" listed last, d among the four substantive labels. Bootstrap p has a floor of 1/reps; with "
          "four paraphrase clusters a sign-consistent shift reaches it however small, hence the |Δd| floor. Answer mass is the "
          "probability the next token starts one of the listed answers (F1 = nothing appended: the unforced answer rate)."]
    (out / "olmo2_compare.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:30]))
    print(f"wrote {out / 'olmo2_compare.md'} and {out / 'olmo2_compare.json'}")


if __name__ == "__main__":
    main()
