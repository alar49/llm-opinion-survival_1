"""OLMo 2 7B across training stages, v2 (PLAN_OLMO2.md): the stage comparisons H4, H5 and H6, the format coverage of
every run (§3.4), and the token-identity check that runs before any scoring (§5).

Runs: the seven completion-format roster entries with "study": "olmo2_v2" in scripts/sweep_models.json, i.e. the four
stages with ending A and the base model with endings B, C and D. Every stage comparison uses ending A (§4). The stages
share one tokenizer, and --check_prompts verifies that every grid prompt and answer string is token-identical across
them, so every contrast is paired by prompt key.

Measures (§3.2), per issue and set of cells, each averaged over the cells of the set:
  d     = (p_agree(report level) - p_agree(other level)) / 2
  d_LO  = (LO(report level) - LO(other level)) / 2, with LO = log(P(A) + P(SA)) - log(P(D) + P(SD)) clipped to ±10
  C     = (mean LO over the 6 true anchors - mean LO over the 6 false anchors) / 2, per set of cells
  d_rel = d_LO / C
A stage reads a cell if C >= 0.5 there. Uncertainty: a cluster bootstrap over the paraphrases (4,000 reps, seed 7) with
one weight vector per rep shared by every run, cell and item, so every contrast is paired. For a contrast and margin m:
equivalent = its 90% CI inside [-m, m]; different = entirely outside; otherwise inconclusive. A shift = the 95% CI
excludes 0, |contrast| >= m, and BH at q = 0.01 over the 19 axes.

H4a answer mass at the reference cell does not fall SFT -> DPO -> Instruct; H4b F5 below F3 for every post-trained
stage; H4c deflecting decodes; H5a SFT = DPO = Instruct in d_rel (±0.2) on the primary cell set, with d (±0.10, ±0.05),
d_LO (±0.4) and Spearman as sensitivity checks; H5b base vs SFT profile rank correlation in d_LO, if the base model reads
(H1b); H6 the "No opinion" option at F2. Hypotheses that rest on answer mass are decided only for runs whose format is
captured (§3.4), and reported descriptively otherwise.

Reads <dir>/raw/orderforce_<tag>.jsonl[.gz] (+ .decode); writes <dir>/olmo2_compare.{md,json}.
Usage: python3 scripts/olmo2_compare.py [--dir results/olmo2_v2] [--q 0.01]
       python3 scripts/olmo2_compare.py --check_prompts   (needs transformers: token identity, disjoint strings, counts)
       python3 scripts/olmo2_compare.py --list            (the seven run tags, for run_olmo2_v2.sh)
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orderforce_analyze import AXES, ISSUES, NULL, ORDERS, POL, REF, bh, load, other, summ  # noqa: E402
from orderforce_gates import named_position  # noqa: E402
from readout import coverage  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
GRID = DATA / "olmo2_v2_grid.json"
ROSTER = json.loads((Path(__file__).resolve().parent / "sweep_models.json").read_text(encoding="utf-8"))
V2 = [m for m in ROSTER["models"] if m.get("study") == "olmo2_v2"]
RUNS = [m["tag"] for m in V2]
STAGES = ["base", "SFT", "DPO", "Instruct"]
POST = STAGES[1:]
STAGE_TAG = {m["stage"]: m["tag"] for m in V2 if m["ending"] == "\nAnswer:" and not m["head"]}   # ending A
ENDING_TAG = {"A": STAGE_TAG["base"], "B": "olmo2-7b-base-myanswer", "C": "olmo2-7b-base-qa", "D": "olmo2-7b-base-theansweris"}
ANCHORS = json.loads((DATA / "orderforce_anchors.json").read_text(encoding="utf-8"))
TRUE_ANCHORS = [a["id"] for a in ANCHORS if a["expected"] == "agree"]
FALSE_ANCHORS = [a["id"] for a in ANCHORS if a["expected"] == "disagree"]
ISSUE_ITEMS = [f"{a}|{lvl}" for a in POL for lvl in ISSUES[a]["levels"]]   # the 34 issue statements
N_PROMPTS, N_DECODE = 4288, 144   # per run (§2.3, §2.4)
REPS, SEED = 4000, 7
READ_C = 0.5   # a stage reads a cell if C >= 0.5 (§3.2)
F3_CELLS = [(o, "positional", 3, "none") for o in ORDERS] + [(o, "canonical", 3, "none") for o in ORDERS[1:]]
F2_WITH, F2_WITHOUT = ("paper", "positional", 2, "last"), ("paper", "positional", 2, "none")
MEASURES = [("d_rel", 0.2, "primary"), ("d", 0.10, "sensitivity"), ("d", 0.05, "strict sensitivity"), ("d_lo", 0.4, "sensitivity")]   # §3.3
LABEL = {"d_rel": "d_rel", "d": "d", "d_lo": "d_LO"}
DISCLAIM = re.compile(r"as an ai|i don't have (personal )?(opinions|feelings|beliefs|views)|i do not have (personal )?(opinions|beliefs|views)"
                      r"|i'm sorry|i am sorry|i cannot|i can't", re.I)


def roster_cfg(tag):
    return next(m for m in V2 if m["tag"] == tag)


def check_prompts():
    """§5 gates 1-2 and the counts of gate 4, before any GPU time: every grid prompt and answer string tokenizes
    identically for the four ending-A stages; every run's answer strings are disjoint (stated_logit.answer_strings
    raises otherwise); every prompt opens with the single document-separator token; 4,288 prompts and 144 decodes per
    run. Exits non-zero on any failure. Imports the scorer (torch, transformers)."""
    import stated_logit as S
    from logit_sweep import load_tokenizer
    grid = json.loads(GRID.read_text(encoding="utf-8"))
    optout_text = grid.get("optout_text", S.OPTOUT_TEXT)
    items = S.build_items(DATA / "pct_issues.json", include_null=True) + S.load_extra_items(DATA / "orderforce_anchors.json")
    toks, ref = {}, None
    for tag in RUNS:
        cfg = roster_cfg(tag)
        key = (cfg["id"], cfg.get("revision"))
        if key not in toks:
            toks[key] = load_tokenizer(cfg)
        tok = toks[key]
        prompts = S.build_prompts_grid(items, grid, None, S.completion_format(cfg))
        n_dec = len(S.decode_subset(prompts, grid))
        if len(prompts) != N_PROMPTS or n_dec != N_DECODE:
            sys.exit(f"{tag}: {len(prompts)} prompts and {n_dec} decodes; PLAN_OLMO2.md expects {N_PROMPTS} and {N_DECODE}")
        enc = [tok(S.render_user_prefix(tok, None, p["user"], cfg)[0], add_special_tokens=False)["input_ids"] for p in prompts]
        sep = tok(cfg["doc_start"], add_special_tokens=False)["input_ids"]
        if len(sep) != 1 or sep[0] not in tok.all_special_ids or any(e[0] != sep[0] or sep[0] in e[1:] for e in enc):
            sys.exit(f"{tag}: {cfg['doc_start']!r} is not a single special token opening every prompt (ids {sep})")
        cells = sorted({(p["order"], p["numbering"], p["optout"]) for p in prompts})
        strings = [S.answer_strings(tok, S.option_lines(o, n, None if op == "none" else op, optout_text), optout_text) for o, n, op in cells]
        if tag in STAGE_TAG.values():
            if ref is None:
                ref = (tag, enc, strings)
            else:
                bad = sum(a != b for a, b in zip(enc, ref[1]))
                if bad or strings != ref[2]:
                    sys.exit(f"{tag}: {bad} of {len(prompts)} prompts differ from {ref[0]}; answer strings {'differ' if strings != ref[2] else 'match'}")
        print(f"{tag} ({cfg['id']}): {len(prompts)} prompts, {n_dec} decodes, {len(cells)} layouts with disjoint answer strings"
              + (f", token-identical to {ref[0]}" if tag in STAGE_TAG.values() and tag != ref[0] else ""), flush=True)
        print("  example:", repr(S.render_user_prefix(tok, None, prompts[0]["user"], cfg)[0]), flush=True)
    tok = toks[(roster_cfg(ref[0])["id"], roster_cfg(ref[0]).get("revision"))]
    print("answer strings of the reference layout:", [[tok.convert_ids_to_tokens(c) for c in v] for v in
                                                      S.answer_strings(tok, S.option_lines("paper", "positional"), optout_text)], flush=True)


def weights(paras, rng):
    """Row 0 = equal weights (point estimate); rows 1..REPS = paraphrase-cluster resamples, shared by every run."""
    W = np.zeros((REPS + 1, len(paras)))
    W[0] = 1.0 / len(paras)
    for b in range(1, REPS + 1):
        W[b] = np.bincount(rng.integers(0, len(paras), len(paras)), minlength=len(paras)) / len(paras)
    return W


class Stage:
    """One run's rows, indexed by cell, item and paraphrase, with bootstrap-weighted means."""

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

    def items_stat(self, cell, items, key, f=np.mean):
        vs = [v for v in (self.mean(cell, it, key) for it in items) if v is not None]
        return f(np.stack(vs), axis=0) if vs else None

    def pair(self, axis, cells, key):
        """(report level - other level) / 2 of a row field, averaged over cells; None unless every cell has both levels."""
        rep, oth = f"{axis}|{ISSUES[axis]['report']}", f"{axis}|{other(axis, ISSUES[axis]['report'])}"
        ds = []
        for c in cells:
            a, b = self.mean(c, rep, key), self.mean(c, oth, key)
            if a is None or b is None:
                return None
            ds.append((a - b) / 2)
        return np.mean(ds, axis=0)

    def anchor(self, cells, key):
        """(true anchors - false anchors) / 2 of a row field, averaged over cells: D with "score", C with "lo"."""
        vs = []
        for c in cells:
            t, f = self.items_stat(c, TRUE_ANCHORS, key), self.items_stat(c, FALSE_ANCHORS, key)
            if t is None or f is None:
                return None
            vs.append((t - f) / 2)
        return np.mean(vs, axis=0)

    def directions(self, cells):
        """{"d", "d_lo", "d_rel"} -> axis -> (REPS+1,) array (None if missing), over one set of cells."""
        C = self.anchor(cells, "lo")
        out = {"d": {}, "d_lo": {}, "d_rel": {}}
        for a in AXES:
            out["d"][a] = self.pair(a, cells, "p_agree")
            out["d_lo"][a] = self.pair(a, cells, "lo")
            out["d_rel"][a] = out["d_lo"][a] / C if out["d_lo"][a] is not None and C is not None else None
        return out


def ci(v):
    """orderforce_analyze.summ (point estimate v[0], percentile 95% CI and two-sided p over v[1:]) plus the 90% CI
    (the equivalence interval); p = 1 when every bootstrap value is exactly 0."""
    if v is None:
        return None
    s = summ(v)
    if not np.any(v[1:]):
        s["p"] = 1.0
    b = np.sort(v[1:])
    s["lo90"], s["hi90"] = float(b[int(0.05 * len(b))]), float(b[int(0.95 * len(b)) - 1])
    return s


def excludes0(s):
    return bool(s) and (s["lo"] > 0 or s["hi"] < 0)


def spearman_rows(X, Y):
    """Row-wise Spearman correlation of two (reps, n) arrays."""
    from scipy.stats import rankdata
    rx, ry = rankdata(X, axis=1), rankdata(Y, axis=1)
    rx, ry = rx - rx.mean(1, keepdims=True), ry - ry.mean(1, keepdims=True)
    return (rx * ry).sum(1) / np.sqrt((rx ** 2).sum(1) * (ry ** 2).sum(1))


def profile(D):
    """(REPS+1, 17) array of the 17 issue values, or None if one is missing."""
    return np.stack([D[a] for a in POL], 1) if all(D[a] is not None for a in POL) else None


def contrast(Da, Db, m, q):
    """Per axis, Δ = b - a with its equivalence class at margin m and the shift flag; plus the counts over the 17 issues."""
    s = {a: ci(Db[a] - Da[a]) if Da[a] is not None and Db[a] is not None else None for a in AXES}
    rej = bh([s[a]["p"] if s[a] else 1.0 for a in AXES], q)
    for i, a in enumerate(AXES):
        if s[a]:
            s[a]["class"] = ("equivalent" if -m <= s[a]["lo90"] and s[a]["hi90"] <= m else
                             "different" if s[a]["hi90"] < -m or s[a]["lo90"] > m else "inconclusive")
            s[a]["shift"] = bool(i in rej and excludes0(s[a]) and abs(s[a]["mean"]) >= m)
    n = {c: sum(bool(s[a]) and s[a]["class"] == c for a in POL) for c in ("equivalent", "different", "inconclusive")}
    n["shifts"] = [a for a in POL if s[a] and s[a]["shift"]]
    n["null_shifts"] = [a for a in NULL if s[a] and s[a]["shift"]]
    return {"axes": s, "counts": n}


def read_class(s):
    """H1b: reads (C >= 0.5, CI lower bound > 0), does not read (CI includes 0), weak (reliably positive, below 0.5).
    A C whose CI lies entirely below 0 is reported as reversed (PLAN_OLMO2.md amendment log)."""
    if s is None:
        return "missing"
    if s["mean"] >= READ_C and s["lo"] > 0:
        return "reads"
    if s["lo"] <= 0 <= s["hi"]:
        return "does not read"
    return "reversed" if s["hi"] < 0 else "weak"


def cell_set(stages):
    """§4 H5 primary cell set for a group of stages, decided on the anchors only: the reference cell if every stage
    reads it; otherwise the forcing-3 layouts every stage reads; otherwise none (untestable)."""
    reads = lambda s, c: s.anchor([c], "lo") is not None and s.anchor([c], "lo")[0] >= READ_C
    if all(reads(s, REF) for s in stages):
        return [REF], "rule 1: every stage reads the reference cell"
    common = [c for c in F3_CELLS if all(reads(s, c) for s in stages)]
    if common:
        return common, "rule 2: the forcing-3 layouts every stage reads"
    return [], "rule 3: no forcing-3 layout is read by every stage (untestable)"


def classify(text, lines):
    """What a greedy decode does: names an option by number or by label, deflects ("as an AI"...), or something else."""
    _, kind = named_position(text, [tuple(x) for x in lines])
    if kind in ("number", "number-unlisted"):
        return "number"
    if kind == "label":
        return "label"
    if DISCLAIM.search(text[:200]):
        return "deflection"
    return "label" if kind == "label-inline" else "other"


def raw_file(d, tag, suffix=""):
    gz, plain = d / "raw" / f"orderforce_{tag}.jsonl{suffix}.gz", d / "raw" / f"orderforce_{tag}.jsonl{suffix}"
    return gz if gz.exists() else plain


def load_runs(d):
    """rows per tag, the shared paraphrase weights, a Stage per tag, and coverage per tag."""
    rows = {}
    for t in RUNS:
        f = raw_file(d, t)
        if f.exists():
            rows[t] = load(f)
        else:
            print(f"missing {f}; {t} left out", flush=True)
    paras = sorted({r["paraphrase"] for rs in rows.values() for r in rs})
    W = weights(paras, np.random.default_rng(SEED))
    pidx = {pi: i for i, pi in enumerate(paras)}
    S = {t: Stage(rows[t], W, pidx) for t in rows}
    cov = {t: coverage(rows[t], REF, set(ISSUE_ITEMS)) for t in rows}
    return rows, paras, W, S, cov


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2_v2"), help="holds raw/orderforce_<tag>.jsonl[.gz]; outputs go here")
    ap.add_argument("--q", type=float, default=0.01, help="BH level over the 19 axes")
    ap.add_argument("--check_prompts", action="store_true", help="§5 gates 1-2 on the tokenizers, then exit")
    ap.add_argument("--list", action="store_true", help="print the seven run tags and exit")
    args = ap.parse_args()
    if args.list:
        print("\n".join(RUNS))
        return
    if args.check_prompts:
        check_prompts()
        return
    out = Path(args.dir)
    rows, paras, W, S, cov = load_runs(out)
    st_ = [s for s in STAGES if STAGE_TAG[s] in S]
    if len(st_) < 2:
        sys.exit("need at least two ending-A stages")
    T = {s: S[STAGE_TAG[s]] for s in st_}
    captured = {s: bool(cov[STAGE_TAG[s]].get("captured")) for s in st_}
    res = {"runs": list(rows), "stages": st_, "paraphrases": paras, "reps": REPS, "seed": SEED, "q": args.q, "coverage": cov}

    # stage summary (ending A)
    summary = {}
    for s in st_:
        x = T[s]
        m = {f"answer mass F{fl} (paper order)": ci(x.items_stat(("paper", "positional", fl, "none"), ISSUE_ITEMS, "valid_mass")) for fl in (1, 3, 5)}
        m["median answer mass (reference)"] = ci(x.items_stat(REF, ISSUE_ITEMS, "valid_mass", np.median))
        m["No-opinion share (F2, offered last)"] = ci(x.items_stat(F2_WITH, ISSUE_ITEMS, "p_optout"))
        m["acquiescence: mean p_agree (reference)"] = ci(x.items_stat(REF, ISSUE_ITEMS, "p_agree"))
        m["anchor D (reference)"] = ci(x.anchor([REF], "score"))
        m["anchor C (reference)"] = ci(x.anchor([REF], "lo"))
        ds = [x.pair(a, [REF], "p_agree") for a in POL]
        m["mean |d| over 17 issues (reference)"] = ci(np.mean(np.abs(ds), axis=0)) if all(v is not None for v in ds) else None
        summary[s] = m
    res["summary"] = summary

    # calls at the reference cell (R0's rule in d) and null-axis calls
    calls = {}
    for s in st_:
        sd = {a: ci(T[s].pair(a, [REF], "p_agree")) for a in AXES}
        rej = bh([sd[a]["p"] if sd[a] else 1.0 for a in AXES], args.q)
        called = [a for i, a in enumerate(AXES) if sd[a] and i in rej and excludes0(sd[a]) and abs(sd[a]["mean"]) >= 0.10]
        calls[s] = {"issues": [a for a in called if a in POL], "null": [a for a in called if a in NULL],
                    "flagged": sum(a in NULL for a in called) >= 2}
    res["calls_reference"] = calls

    # H4 answering (answer mass: decided only where the format is captured)
    am = {s: T[s].items_stat(REF, ISSUE_ITEMS, "valid_mass") for s in st_}
    post = [s for s in POST if s in st_]
    H4 = {}
    pairs4 = [(a, b) for a, b in zip(post, post[1:])] + ([(post[0], post[-1])] if len(post) > 2 else [])
    diffs = {f"{a}->{b}": ci(am[b] - am[a]) for a, b in pairs4}
    adj = [diffs[f"{a}->{b}"] for a, b in zip(post, post[1:])]
    if len(post) < 3:
        dec = "untestable (missing stages)"
    elif not all(captured[s] for s in post):
        dec = "descriptive only (format not captured for " + ", ".join(s for s in post if not captured[s]) + ")"
    else:
        dec = "supported" if all(d["hi"] >= 0 for d in adj) and diffs[f"{post[0]}->{post[-1]}"]["lo"] > 0 else "not supported"
    H4["H4a"] = {"answer_mass_reference": {s: ci(am[s]) for s in st_}, "contrasts": diffs, "decision": dec}
    f53 = {s: ci(T[s].items_stat(("paper", "positional", 5, "none"), ISSUE_ITEMS, "valid_mass") - T[s].items_stat(REF, ISSUE_ITEMS, "valid_mass")) for s in st_}
    if not all(captured[s] for s in post):
        dec = "descriptive only (format not captured for " + ", ".join(s for s in post if not captured[s]) + ")"
    else:
        dec = "supported" if len(post) == 3 and all(f53[s]["hi"] < 0 for s in post) else "not supported"
    H4["H4b"] = {"F5_minus_F3": f53, "decision": dec}
    dec_counts = {}
    for s in st_:
        f = raw_file(out, STAGE_TAG[s], ".decode.jsonl")
        drows = load(f) if f.exists() else []
        cnt = Counter(classify(d["text"], d["lines"]) for d in drows)
        dec_counts[s] = {"n": len(drows), "counts": dict(cnt)}
    defl = [dec_counts[s]["counts"].get("deflection", 0) for s in post]
    H4["H4c"] = {"decodes": dec_counts, "deflections_SFT_DPO_Instruct": defl,
                 "holds": all(a >= b for a, b in zip(defl, defl[1:])) if len(defl) == 3 else None}
    res["H4"] = H4

    # H5 stated directions
    H5 = {}
    grp = [s for s in POST if s in st_]
    cells, rule = cell_set([T[s] for s in grp])
    H5["H5a"] = {"group": grp, "cells": ["|".join(map(str, c)) for c in cells], "rule": rule,
                 "C_reference": {s: ci(T[s].anchor([REF], "lo")) for s in grp},
                 "C_f3_layouts": {s: {"|".join(map(str, c)): float(T[s].anchor([c], "lo")[0]) for c in F3_CELLS if T[s].anchor([c], "lo") is not None} for s in grp}}
    DIR = {}
    if cells:
        DIR = {s: T[s].directions(cells) for s in grp}
        H5["H5a"]["C_on_cells"] = {s: ci(T[s].anchor(cells, "lo")) for s in grp}
        H5["H5a"]["min_bootstrap_C"] = {s: float(T[s].anchor(cells, "lo")[1:].min()) for s in grp}
        H5["H5a"]["stages"] = {s: {k: {a: ci(DIR[s][k][a]) for a in AXES} for k in ("d", "d_lo", "d_rel")} for s in grp}
        pairs5 = [(a, b) for a, b in zip(grp, grp[1:])] + ([(grp[0], grp[-1])] if len(grp) > 2 else [])
        P = {}
        for a, b in pairs5:
            pk = f"{a}->{b}"
            P[pk] = {f"{key} ±{m}": contrast(DIR[a][key], DIR[b][key], m, args.q) for key, m, _ in MEASURES}
            P[pk]["spearman"] = {key: ci(spearman_rows(profile(DIR[a][key]), profile(DIR[b][key])))
                                 if profile(DIR[a][key]) is not None and profile(DIR[b][key]) is not None else None for key in ("d_rel", "d", "d_lo")}
        H5["H5a"]["pairs"] = P
        adjp = [f"{a}->{b}" for a, b in zip(grp, grp[1:])]
        cnt = [P[p]["d_rel ±0.2"]["counts"] for p in adjp]
        if len(grp) < 3:
            H5["H5a"]["decision"] = "untestable (missing stages)"
        elif any(c["different"] >= 2 for c in cnt):
            H5["H5a"]["decision"] = "contradicted"
        elif all(c["equivalent"] >= 14 and not c["shifts"] for c in cnt):
            H5["H5a"]["decision"] = "supported"
        else:
            H5["H5a"]["decision"] = "inconclusive"
    else:
        H5["H5a"]["decision"] = "untestable"
    h1b = read_class(ci(T["base"].anchor([REF], "lo"))) if "base" in T else "missing"
    H5["H5b"] = {"H1b": h1b}
    if h1b == "reads" and "SFT" in T:
        cb, rb = cell_set([T["base"], T["SFT"]])
        H5["H5b"].update({"cells": ["|".join(map(str, c)) for c in cb], "rule": rb})
        if cb:
            Xb, Xs = profile(T["base"].directions(cb)["d_lo"]), profile(T["SFT"].directions(cb)["d_lo"])
            rho = ci(spearman_rows(Xb, Xs)) if Xb is not None and Xs is not None else None
            H5["H5b"]["spearman_d_lo"] = rho
            H5["H5b"]["decision"] = ("inconclusive (missing issues)" if rho is None else
                                     "stance present before post-training" if rho["mean"] >= 0.5 and rho["lo"] > 0 else
                                     "stance installed by post-training" if rho["lo"] <= 0 <= rho["hi"] or rho["mean"] < 0.2 else "inconclusive")
        else:
            H5["H5b"]["decision"] = "untestable"
    else:
        H5["H5b"]["decision"] = "untestable (the base model does not read the reference cell: H1b = " + h1b + ")"
    res["H5"] = H5

    # H6 the "No opinion" option at F2, paper order
    H6 = {}
    for s in st_:
        x = T[s]
        dsub = x.items_stat(F2_WITHOUT, ISSUE_ITEMS, "valid_mass") - x.items_stat(F2_WITH, ISSUE_ITEMS, "substantive_mass")
        c = contrast({a: x.pair(a, [F2_WITHOUT], "p_agree") for a in AXES}, {a: x.pair(a, [F2_WITH], "p_agree") for a in AXES}, 0.10, args.q)
        sm = ci(dsub)
        holds = sm["hi"] < 0.10 and c["counts"]["equivalent"] >= 14
        H6[s] = {"substantive_mass_without_minus_with": sm, "d_with_vs_without": c,
                 "decision": ("holds" if holds else "does not hold") if captured[s] else "descriptive only (format not captured)"}
    res["H6"] = H6
    json.dump(res, open(out / "olmo2_compare.json", "w", encoding="utf-8"), indent=1, default=float)
    write_md(out, res, rows, cells, DIR)


def write_md(out, res, rows, cells, DIR):
    f2 = lambda s, sg=True: "—" if not s else (f"{s['mean']:+.2f} [{s['lo']:+.2f}, {s['hi']:+.2f}]" if sg else f"{s['mean']:.2f} [{s['lo']:.2f}, {s['hi']:.2f}]")
    fx = lambda x, d=2: "—" if x is None else f"{x:.{d}f}"
    st_ = res["stages"]
    L = ["# OLMo 2 7B training stages, v2: stage comparisons (PLAN_OLMO2.md H4, H5, H6)", "",
         f"Runs: {', '.join(res['runs'])}. Stage comparisons use ending A (`\\nAnswer:`), which all four stages share. 95% CIs "
         f"from a cluster bootstrap over the {len(res['paraphrases'])} paraphrases ({res['reps']} reps, seed {res['seed']}), one "
         "draw shared by every run, cell and item, so every contrast is paired. Equivalence uses the 90% CI (two one-sided tests at 5%).", "",
         "## Format coverage (§3.4)", "",
         "Missed share = uncaptured answer-like first-token probability / (answer mass + that probability), per row; median over the "
         "34 issue statements × 4 paraphrases at the reference cell, rows with almost no answer-like probability (< 0.05) left out.", "",
         "| run | median missed share | rows with a share | median answer mass M | median M + U | format |", "|---|---|---|---|---|---|"]
    for t, c in res["coverage"].items():
        L.append(f"| {t} | {fx(c.get('median_missed_share'))} | {c.get('n_defined', '—')}/{c['n_rows']} | {fx(c.get('median_answer_mass'))} | "
                 f"{fx(c.get('median_answer_like_mass'))} | {'captured' if c.get('captured') else 'not captured: descriptive only'} |")
    L += ["", "## Stage summary (ending A)", "", "| quantity | " + " | ".join(st_) + " |", "|---|" + "---|" * len(st_)]
    for k in res["summary"][st_[0]]:
        L.append(f"| {k} | " + " | ".join(f2(res["summary"][s][k], sg=k.startswith("anchor")) for s in st_) + " |")
    L.append("| issues called at the reference cell (R0 rule in d) | " + " | ".join(str(len(res["calls_reference"][s]["issues"])) for s in st_) + " |")
    L.append("| null axes called (2 or more flags the run) | " + " | ".join(
        f"{len(res['calls_reference'][s]['null'])}{' FLAGGED' if res['calls_reference'][s]['flagged'] else ''}" for s in st_) + " |")
    H4 = res["H4"]
    L += ["", "## H4 Stage effects on answering", "",
          f"**H4a** (answer mass at the reference cell does not fall SFT → DPO → Instruct; the Instruct − SFT CI above 0): **{H4['H4a']['decision']}**.", "",
          "| contrast | Δ mean answer mass [95% CI] |", "|---|---|"]
    L += [f"| {p.replace('->', ' → ')} | {f2(v)} |" for p, v in H4["H4a"]["contrasts"].items()]
    L += ["", f"**H4b** (answer mass at F5 below F3, paper order, for every post-trained stage): **{H4['H4b']['decision']}**. "
          "F5 − F3: " + "; ".join(f"{s} {f2(v)}" for s, v in H4["H4b"]["F5_minus_F3"].items()) + ".", "",
          f"**H4c** (descriptive; deflecting decodes do not increase SFT → DPO → Instruct): {H4['H4c']['deflections_SFT_DPO_Instruct']} → "
          f"{'holds' if H4['H4c']['holds'] else 'does not hold' if H4['H4c']['holds'] is not None else '—'}.", "",
          "| stage | decodes | number | label | deflection | other |", "|---|---|---|---|---|---|"]
    for s, v in H4["H4c"]["decodes"].items():
        c = v["counts"]
        L.append(f"| {s} | {v['n']} | {c.get('number', 0)} | {c.get('label', 0)} | {c.get('deflection', 0)} | {c.get('other', 0)} |")
    H5a = res["H5"]["H5a"]
    L += ["", "## H5 Stated directions across stages", "",
          f"Primary cell set for {{{', '.join(H5a['group'])}}}: {', '.join(H5a['cells']) or 'none'} ({H5a['rule']}). "
          "C at the reference cell: " + "; ".join(f"{s} {f2(v)}" for s, v in H5a["C_reference"].items()) + ".", "",
          f"**H5a** (SFT ≈ DPO ≈ Instruct in d_rel, margin ±0.2): **{H5a['decision']}**. Supported needs ≥ 14/17 equivalent and no "
          "shift in each adjacent pair; contradicted = 2 or more issues different in either pair.", ""]
    if "pairs" in H5a:
        L += ["Equivalent / different / inconclusive issues (of 17), and shifts:", "",
              "| stage pair | " + " | ".join(f"{LABEL[k]} ±{m} ({role})" for k, m, role in MEASURES) + " | Spearman ρ in d_rel | in d |", "|---|" + "---|" * (len(MEASURES) + 2)]
        for p, P in H5a["pairs"].items():
            cols = []
            for k, m, _ in MEASURES:
                c = P[f"{k} ±{m}"]["counts"]
                cols.append(f"{c['equivalent']} / {c['different']} / {c['inconclusive']}" + (f"; shifts: {', '.join(c['shifts'])}" if c["shifts"] else ""))
            L.append(f"| {p.replace('->', ' → ')} | " + " | ".join(cols) + f" | {f2(P['spearman']['d_rel'])} | {f2(P['spearman']['d'])} |")
        L += ["", "Bootstrap C on the cell set (d_rel's denominator): " + "; ".join(f"{s} {f2(v)}, min over reps {H5a['min_bootstrap_C'][s]:.2f}" for s, v in H5a["C_on_cells"].items()) + ".", "",
              "### Per issue on the primary cell set: d_rel, d, d_LO", "",
              "| issue | " + " | ".join(f"{s} d_rel" for s in H5a["group"]) + " | " + " | ".join(f"{s} d" for s in H5a["group"]) + " | " + " | ".join(f"{s} d_LO" for s in H5a["group"]) + " |",
              "|---|" + "---|" * (3 * len(H5a["group"]))]
        for a in AXES:
            row = [f2(H5a["stages"][s][k][a]) for k in ("d_rel", "d", "d_lo") for s in H5a["group"]]
            L.append(f"| {a}{' (null)' if a in NULL else ''} | " + " | ".join(row) + " |")
        for p, P in H5a["pairs"].items():
            c = P["d_rel ±0.2"]
            L += ["", f"### Δd_rel per issue: {p.replace('->', ' → ')} (90% CI; E = equivalent, X = different, ? = inconclusive; † = shift)", "",
                  "| issue | Δd_rel [90% CI] | class | Δd [90% CI] | class (±0.10) |", "|---|---|---|---|---|"]
            for a in AXES:
                s, sd = c["axes"][a], P["d ±0.1"]["axes"][a]
                tag = lambda z: {"equivalent": "E", "different": "X", "inconclusive": "?"}[z["class"]] + (" †" if z["shift"] else "")
                L.append(f"| {a}{' (null)' if a in NULL else ''} | " + (f"{s['mean']:+.2f} [{s['lo90']:+.2f}, {s['hi90']:+.2f}] | {tag(s)}" if s else "— | —")
                         + " | " + (f"{sd['mean']:+.3f} [{sd['lo90']:+.3f}, {sd['hi90']:+.3f}] | {tag(sd)}" if sd else "— | —") + " |")
    H5b = res["H5"]["H5b"]
    L += ["", f"**H5b** (base vs SFT, Spearman ρ of the issue profiles in d_LO): **{H5b['decision']}**."
          + (f" Cells: {', '.join(H5b['cells'])} ({H5b['rule']}); ρ = {f2(H5b.get('spearman_d_lo'))}." if H5b.get("cells") else ""), "",
          "## H6 The \"No opinion\" option (F2, paper order)", "",
          "Holds if the 95% CI upper end of (substantive mass without the option − with it) is below 0.10 and the conditional d with and "
          "without the option is equivalent within ±0.10 for at least 14 of 17 issues.", "",
          "| stage | substantive mass without − with [95% CI] | d equivalent / different / inconclusive | decision |", "|---|---|---|---|"]
    for s, v in res["H6"].items():
        c = v["d_with_vs_without"]["counts"]
        L.append(f"| {s} | {f2(v['substantive_mass_without_minus_with'])} | {c['equivalent']} / {c['different']} / {c['inconclusive']} | {v['decision']} |")
    (out / "olmo2_compare.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[:60]))
    print(f"wrote {out / 'olmo2_compare.md'} and {out / 'olmo2_compare.json'}")


if __name__ == "__main__":
    main()
