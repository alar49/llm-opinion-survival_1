"""OLMo 2 7B across training stages, v2: post-hoc analyses. None of this is pre-registered. Every analysis here was chosen
after the PLAN_OLMO2.md results had been seen, to explain them, and is reported as exploratory. It reuses the registered
bootstrap of olmo2_compare.py (paraphrase clusters, 4,000 reps, seed 7, one draw shared by every run) and, for P4, the
layout decomposition and item bootstrap of olmo2_explore.py.

P1  ending D (PLAN_OLMO2.md amendment log, deviation of 2026-10-27): where the base model's first-token probability goes
    after "The answer is", what the greedy decodes write, and how often the readout's top option is the written answer.
P2  one set of stances on four scales: per stage at the reference cell, the mean agreement, mean |d|, mean |d_LO|, C and
    mean |d_rel|, and the issues called in d (|d| >= 0.10) and in d_LO (|d_LO| >= 0.4); both calls need a 95% CI
    excluding 0 and BH at q = 0.01 over the 19 axes.
P3  H5a broken down: for each pair of stages, the growth of d_LO (least-squares slope through the origin over the 17
    issues), the growth of C, and their quotient u, the uniform change of d_rel; per issue, the change of d_rel left after
    that uniform rescaling, d_rel(later) - u * d_rel(earlier).
P4  H2a split in two: moderation within a side, ((D - SD) + (A - SA)) / 2, and the agree-side preference,
    ((A + SA) - (D + SD)) / 2, from the label effects of the layout decomposition; 95% CI over items.
P5  H3 order by order: C with pinned and with positional numbering in the reversed, scrambled and scrambled2 orders.
P6  base vs SFT: mean |d_LO| and |d_rel|, and the per-issue d_LO of both.
P7  the panel's survival ladder (PLAN.md §5, orderforce_analyze.py) re-run in log-odds: d_LO in place of d with floor 0.4,
    and a cell counts as read when C >= 0.5 in place of D >= 0.5. The order, numbering, forcing and opt-out rules are the
    panel's, unchanged. ladder(..., key="p_agree", floor=0.10, read_key="score") is the panel's own ladder on this
    bootstrap.

Reads <dir>/raw/orderforce_<tag>.jsonl[.gz] (+ .decode) and <dir>/orderforce_gates.json; writes <dir>/olmo2_posthoc.{md,json}.
Usage: python3 scripts/olmo2_posthoc.py [--dir results/olmo2_v2]
"""
import argparse
import json
import math
import statistics as st
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from olmo2_compare import ENDING_TAG, ISSUE_ITEMS, READ_C, SEED, STAGE_TAG, STAGES, ci, load_runs, profile, raw_file  # noqa: E402
from olmo2_explore import ITEM_REPS, decompose, design, layout_shares  # noqa: E402
from orderforce_analyze import AXES, ISSUES, NULL, ORDERS, POL, R_CELLS, REF, bh, load, other, summ  # noqa: E402
from orderforce_gates import named_position  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FLOOR_D, FLOOR_LO, Q = 0.10, 0.4, 0.01
PAIRS = [("SFT", "DPO"), ("DPO", "Instruct"), ("SFT", "Instruct")]
ISSUE_SET = set(ISSUE_ITEMS)


def cell(r):
    return (r["order"], r["numbering"], r["forcing"], r["optout"])


def calls(D, floor):
    """Axes called from {axis: (REPS+1,) array}: 95% CI excludes 0, |estimate| >= floor, BH at q over the 19 axes."""
    s = {a: ci(D[a]) for a in AXES}
    rej = bh([s[a]["p"] if s[a] else 1.0 for a in AXES], Q)
    return [a for i, a in enumerate(AXES) if s[a] and (s[a]["lo"] > 0 or s[a]["hi"] < 0) and abs(s[a]["mean"]) >= floor and i in rej]


def p1_ending_d(out, rows):
    res = {}
    keyed = {}
    for e in ("A", "D"):
        t = ENDING_TAG[e]
        keyed[e] = {r["key"]: r for r in rows[t]}
        sel = [r for r in rows[t] if cell(r) == REF and r["item"] in ISSUE_SET]
        first = defaultdict(float)
        for r in sel:
            for _id, text, lp, _cap in r["top_tokens"]:
                first[text] += math.exp(lp) / len(sel)
        dec = load(raw_file(out, t, ".decode.jsonl"))
        agree = defaultdict(lambda: [0, 0])
        for d in dec:
            k, _kind = named_position(d["text"], d["lines"])
            if k is not None:
                c = "|".join(map(str, (d["order"], d["numbering"], d["forcing"], d["optout"])))
                agree[c][0] += int(k == keyed[e][d["key"]]["argmax_pos"])
                agree[c][1] += 1
        res[e] = {"tag": t, "n_rows": len(sel), "mean_answer_mass": st.mean(r["valid_mass"] for r in sel),
                  "rows_below_0.05": sum(r["valid_mass"] < 0.05 for r in sel),
                  "colon_first_token_mass": sum(v for k, v in first.items() if k.lstrip(" ").startswith(":")),
                  "top_first_tokens": sorted(([k, v] for k, v in first.items()), key=lambda kv: -kv[1])[:6],
                  "decode_texts": Counter(d["text"] for d in dec).most_common(),
                  "decoded_option": {d["key"]: named_position(d["text"], d["lines"])[0] for d in dec},
                  "readout_matches_decode": {c: {"agree": a, "named": n} for c, (a, n) in agree.items()}}
    same = [res["A"]["decoded_option"][k] == res["D"]["decoded_option"].get(k) for k in res["A"]["decoded_option"]]
    res["same_written_answer_A_vs_D"] = {"same": sum(same), "n": len(same)}
    for e in ("A", "D"):
        del res[e]["decoded_option"]
    return res


def p2_scales(T, DIR):
    res, raw = {}, {}
    for s in STAGES:
        x, D = T[s], DIR[s]
        raw[s] = {"C": x.anchor([REF], "lo"), **{f"mean_abs_{k}": np.abs(profile(D[k])).mean(1) for k in ("d", "d_lo", "d_rel")}}
        res[s] = {"mean_p_agree": ci(x.items_stat(REF, ISSUE_ITEMS, "p_agree")), **{k: ci(v) for k, v in raw[s].items()}}
        cd, cl = calls(D["d"], FLOOR_D), calls(D["d_lo"], FLOOR_LO)
        res[s]["called_d"] = [a for a in cd if a in POL]
        res[s]["called_d_lo"] = [a for a in cl if a in POL]
        res[s]["null_called"] = [a for a in cd + cl if a in NULL]
        res[s]["per_issue"] = {a: {k: ci(D[k][a]) for k in ("d", "d_lo", "d_rel")} for a in AXES}
    for s in STAGES:   # each scale relative to SFT, paired bootstrap
        res[s]["vs_SFT"] = {k: ci(v / raw["SFT"][k]) for k, v in raw[s].items()}
    return res


def p3_h5a(DIR, Cref):
    res = {}
    for a, b in PAIRS:
        X, Y = profile(DIR[a]["d_lo"]), profile(DIR[b]["d_lo"])
        k = (X * Y).sum(1) / (X * X).sum(1)
        cr = Cref[b] / Cref[a]
        u = k / cr
        Xr, Yr = profile(DIR[a]["d_rel"]), profile(DIR[b]["d_rel"])
        resid = Yr - u[:, None] * Xr
        per = {}
        for j, ax in enumerate(POL):
            r_ = ci(resid[:, j])
            per[ax] = {"d_rel_a": float(Xr[0, j]), "d_rel_b": float(Yr[0, j]), "delta": float(Yr[0, j] - Xr[0, j]),
                       "uniform_part": float((u[0] - 1) * Xr[0, j]), "residual": r_,
                       "d_lo_growth": float(Y[0, j] / X[0, j]) if abs(X[0, j]) >= 0.3 else None,
                       "issue_specific": bool((r_["lo"] > 0 or r_["hi"] < 0) and abs(r_["mean"]) >= 0.2)}
        res[f"{a}->{b}"] = {"d_lo_slope": ci(k), "C_ratio": ci(cr), "uniform_d_rel_factor": ci(u), "issues": per}
    return res


def p4_h2a(rows):
    X = design()
    rng = np.random.default_rng(SEED + 1)   # the item resamples of olmo2_explore.py's H2, stage by stage
    f = lambda e: {"moderation": ((e["label"][1] - e["label"][0]) + (e["label"][2] - e["label"][3])) / 2,
                   "agree_side": ((e["label"][2] + e["label"][3]) - (e["label"][1] + e["label"][0])) / 2}
    res = {}
    for s in STAGES:
        items, A = layout_shares(rows[STAGE_TAG[s]])
        est = f(decompose(A.mean(1), X)[0])
        boots = defaultdict(list)
        for _ in range(ITEM_REPS):
            for k, v in f(decompose(A[:, rng.integers(0, len(items), len(items))].mean(1), X)[0]).items():
                boots[k].append(v)
        res[s] = {k: {"est": float(v), "lo": float(np.percentile(boots[k], 2.5)), "hi": float(np.percentile(boots[k], 97.5))} for k, v in est.items()}
    return res


def p5_h3(T):
    res = {}
    for s in STAGES:
        x = T[s]
        res[s] = {"paper_positional": ci(x.anchor([("paper", "positional", 3, "none")], "lo"))}
        for o in ORDERS[1:]:
            cp, cq = x.anchor([(o, "canonical", 3, "none")], "lo"), x.anchor([(o, "positional", 3, "none")], "lo")
            res[s][o] = {"pinned": ci(cp), "positional": ci(cq), "pinned_minus_positional": ci(cp - cq)}
    return res


def p6_base_sft(DIR):
    B, S_ = DIR["base"], DIR["SFT"]
    res = {"per_issue": {a: {"base": ci(B["d_lo"][a]), "SFT": ci(S_["d_lo"][a])} for a in POL}}
    for k in ("d_lo", "d_rel"):
        mb, ms = np.abs(profile(B[k])).mean(1), np.abs(profile(S_[k])).mean(1)
        res[f"mean_abs_{k}"] = {"base": ci(mb), "SFT": ci(ms), "SFT_over_base": ci(ms / mb)}
    res["same_sign"] = int(sum(np.sign(B["d_lo"][a][0]) == np.sign(S_["d_lo"][a][0]) for a in POL))
    return res


def ladder(x, g, key, floor, read_key, read_min):
    """The panel's survival ladder (orderforce_analyze.py) for one run on this bootstrap: key / floor give the direction
    measure, read_key / read_min the per-cell reading gate (anchors: "score" -> D, "lo" -> C)."""
    cells = list(x.T)
    vm = {c: st.mean([r["valid_mass"] for it in x.T[c].values() for r in it.values() if r["source"] in ("issues", "pct")] or [float("nan")]) for c in cells}
    broken_orders = [o for o in ORDERS if (o, "positional", 3, "none") in vm and vm[(o, "positional", 3, "none")] < 0.20]
    saturated = len(broken_orders) >= 2
    read = {c: x.anchor([c], read_key) for c in cells}
    comp_broken = {c for c in cells if read[c] is not None and read[c][0] < read_min}
    can = [read[c][0] for c in cells if c[1] == "canonical" and c[2] == 3 and c[3] == "none" and read[c] is not None]
    numbering_limited = not (can and st.median(can) >= read_min)
    pivot = not g.get("dk", {}).get("pivot_stands", True)
    dd = {(a, c): x.pair(a, [c], key) for a in AXES for c in cells}
    dd = {k: v for k, v in dd.items() if v is not None}
    ref_s = {a: summ(dd.get((a, REF))) for a in AXES}
    rej = bh([ref_s[a]["p"] if ref_s[a] else 1.0 for a in AXES], Q)
    out = {"numbering_limited": numbering_limited, "broken_orders": broken_orders, "cells_not_read": sorted("|".join(map(str, c)) for c in comp_broken), "axes": {}}
    for i, a in enumerate(AXES):
        s0 = ref_s[a]
        A = {"d_ref": s0, "called": bool(s0 and (s0["lo"] > 0 or s0["hi"] < 0) and abs(s0["mean"]) >= floor and i in rej)}
        sgn = np.sign(s0["mean"]) if s0 else 0
        cells_r = [c for c in R_CELLS if (a, c) in dd and not (numbering_limited and c[1] == "canonical") and c[0] not in broken_orders and c not in comp_broken]
        if A["called"] and cells_r:
            means = np.array([dd[(a, c)][0] for c in cells_r])
            sm = [summ(dd[(a, c)]) for c in cells_r]
            same = [np.sign(m) == sgn for m in means]
            dissent = any((not same[k]) and ((sm[k]["lo"] > 0) if sgn < 0 else (sm[k]["hi"] < 0)) for k in range(len(cells_r)))
            need = len(cells_r) - (1 if len(cells_r) >= 6 else 0)
            d_o2, d_o2c = dd.get((a, ("reversed", "positional", 3, "none"))), dd.get((a, ("reversed", "canonical", 3, "none")))
            i_ok = sum(same) >= need and not dissent
            ii_ok = float(np.max(np.abs(means - means.mean()))) < abs(s0["mean"])
            iii_ok = d_o2 is not None and abs(d_o2[0] - dd[(a, REF)][0]) < abs(s0["mean"])
            iv_ok = numbering_limited or ("reversed", "canonical", 3, "none") in comp_broken or (d_o2 is not None and d_o2c is not None and abs(d_o2c[0] - d_o2[0]) < abs(s0["mean"]))
            A["R1"] = {"ok": bool(i_ok and ii_ok and iii_ok and iv_ok and not saturated), "n_cells": len(cells_r), "same_sign": int(sum(same))}
        else:
            A["R1"] = {"ok": False, "n_cells": len(cells_r)}
        dk_cell = ("paper", "positional", 2, "last")
        rep_rows = x.T.get(dk_cell, {}).get(f"{a}|{ISSUES[a]['report']}", {})
        po = st.mean([r["p_optout"] for r in rep_rows.values() if r.get("p_optout") is not None] or [float("nan")]) if rep_rows else None
        if A["called"]:
            d5, dk = dd.get((a, ("paper", "positional", 5, "none"))), dd.get((a, dk_cell))
            dk_s = summ(dk)
            cross = [dd[(a, (o, "positional", 2, "last"))][0] for o in ORDERS if (a, (o, "positional", 2, "last")) in dd]
            f_ok = d5 is not None and np.sign(d5[0]) == sgn and abs(d5[0] - dd[(a, REF)][0]) < abs(s0["mean"])
            dk_ok = (dk_s is not None and np.sign(dk_s["mean"]) == sgn and (dk_s["lo"] > 0 or dk_s["hi"] < 0) and (po is None or po < 0.95)
                     and sum(np.sign(v) == sgn for v in cross) >= min(3, len(cross)))
            A["R2"] = {"forcing": bool(f_ok), "optout": bool(dk_ok), "ok": bool(f_ok and (dk_ok or pivot))}
        else:
            A["R2"] = {"ok": False}
        sub1 = [r["substantive_mass"] for r in x.T.get(("paper", "positional", 1, "none"), {}).get(f"{a}|{ISSUES[a]['report']}", {}).values()]
        sub_dk = [r["substantive_mass"] for r in rep_rows.values()]
        gated = bool(sub1 and sub_dk and st.mean(sub1) < 0.30 and st.mean(sub_dk) < 0.30)
        r3 = A["called"] and A["R1"]["ok"] and A["R2"]["ok"]
        A["rung"] = ("saturated" if saturated else "survives all" if r3 else "+forcing" if (A["called"] and A["R2"]["ok"] and not A["R1"]["ok"]) else
                     "+order" if (A["called"] and A["R1"]["ok"]) else "called" if A["called"] else "refusal-gated" if gated else "not called")
        out["axes"][a] = A
    return out


def p7_ladders(T, gates):
    res = {}
    for s in STAGES:
        g = gates.get(STAGE_TAG[s], {})
        res[s] = {"d": ladder(T[s], g, "p_agree", FLOOR_D, "score", 0.5), "d_lo": ladder(T[s], g, "lo", FLOOR_LO, "lo", READ_C)}
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2_v2"))
    args = ap.parse_args()
    out = Path(args.dir)
    rows, paras, W, S, cov = load_runs(out)
    gates = json.loads((out / "orderforce_gates.json").read_text(encoding="utf-8"))
    T = {s: S[STAGE_TAG[s]] for s in STAGES}
    DIR = {s: T[s].directions([REF]) for s in STAGES}
    Cref = {s: T[s].anchor([REF], "lo") for s in STAGES}
    res = {"note": "post hoc, not pre-registered", "P1": p1_ending_d(out, rows), "P2": p2_scales(T, DIR), "P3": p3_h5a(DIR, Cref),
           "P4": p4_h2a(rows), "P5": p5_h3(T), "P6": p6_base_sft(DIR), "P7": p7_ladders(T, gates)}
    json.dump(res, open(out / "olmo2_posthoc.json", "w", encoding="utf-8"), indent=1, default=float)
    (out / "olmo2_posthoc.md").write_text(render(res), encoding="utf-8")
    print(f"wrote {out / 'olmo2_posthoc.md'} and {out / 'olmo2_posthoc.json'}")


def f2(s, sign=True):
    if s is None:
        return "—"
    if isinstance(s, dict):
        m, lo, hi = s.get("mean", s.get("est")), s["lo"], s["hi"]
        return f"{m:+.2f} [{lo:+.2f}, {hi:+.2f}]" if sign else f"{m:.2f} [{lo:.2f}, {hi:.2f}]"
    return f"{s:+.2f}" if sign else f"{s:.2f}"


def nice(a):
    return a.replace("_", " ")


def render(res):
    P1, P2, P3, P4, P5, P6, P7 = (res[k] for k in ("P1", "P2", "P3", "P4", "P5", "P6", "P7"))
    L = ["# OLMo 2 7B training stages, v2: post-hoc analyses", "",
         "**Not pre-registered.** Every analysis below was chosen after the registered results (`olmo2_compare.md`, `olmo2_explore.md`) "
         "had been seen, to explain them. 95% CIs from the registered paraphrase bootstrap (4,000 reps, seed 7, shared by every run), or over "
         "items for P4. Reference cell = paper order, positional numbering, forcing 3, no opt-out. Script: `scripts/olmo2_posthoc.py`.", ""]

    L += ["## P1 Ending D: the base model answers after a colon", "",
          "Reference cell, 34 issue statements × 4 paraphrases; decodes = the 144 greedy decodes per run.", "",
          "| | ending A (`Answer:`) | ending D (`The answer is`) |", "|---|---|---|"]
    A, D = P1["A"], P1["D"]
    L += [f"| mean answer mass the readout sees | {A['mean_answer_mass']:.2f} | {D['mean_answer_mass']:.2f} |",
          f"| rows with answer mass < 0.05 | {A['rows_below_0.05']} of {A['n_rows']} | {D['rows_below_0.05']} of {D['n_rows']} |",
          f"| first-token probability on a colon | {A['colon_first_token_mass']:.2f} | {D['colon_first_token_mass']:.2f} |",
          "| most likely first tokens | " + ", ".join(f"`{t!r}` {p:.2f}" for t, p in A["top_first_tokens"][:3]) + " | " + ", ".join(f"`{t!r}` {p:.2f}" for t, p in D["top_first_tokens"][:3]) + " |",
          "| greedy decodes | " + ", ".join(f"`{t!r}` ×{n}" for t, n in A["decode_texts"][:4]) + " | " + ", ".join(f"`{t!r}` ×{n}" for t, n in D["decode_texts"][:4]) + " |", "",
          f"The written answer (the option the decode names) is the same under endings A and D for {P1['same_written_answer_A_vs_D']['same']} of "
          f"{P1['same_written_answer_A_vs_D']['n']} prompts. How often the readout's top option is the option the decode names, per decode cell:", "",
          "| decode cell | ending A | ending D |", "|---|---|---|"]
    for c in A["readout_matches_decode"]:
        a, d = A["readout_matches_decode"][c], D["readout_matches_decode"].get(c, {"agree": 0, "named": 0})
        L.append(f"| {c} | {a['agree']}/{a['named']} | {d['agree']}/{d['named']} |")

    L += ["", "## P2 One set of stances, four scales", "",
          "Per stage at the reference cell. Calls: 95% CI excludes 0, |value| ≥ floor (0.10 in d, 0.4 in d_LO), BH q = 0.01 over the 19 axes.", "",
          "| stage | mean p_agree | mean \\|d\\| | mean \\|d_LO\\| | C | mean \\|d_rel\\| | issues called in d | issues called in d_LO | null calls |", "|---|---|---|---|---|---|---|---|---|"]
    for s in STAGES:
        x = P2[s]
        L.append(f"| {s} | {f2(x['mean_p_agree'], False)} | {f2(x['mean_abs_d'], False)} | {f2(x['mean_abs_d_lo'], False)} | {f2(x['C'], False)} | {f2(x['mean_abs_d_rel'], False)} | "
                 f"{len(x['called_d'])} | {len(x['called_d_lo'])} | {len(x['null_called'])} |")

    L += ["", "## P3 H5a broken down: uniform rescaling and issue-specific change", "",
          "slope = least-squares growth of d_LO from the earlier to the later stage over the 17 issues; u = slope / (C ratio), the change of d_rel that a "
          "uniform rescaling would give every issue. Residual = d_rel(later) − u × d_rel(earlier): the issue-specific part, in d_rel units "
          "(* = 95% CI excludes 0 and |residual| ≥ 0.2, the H5a margin).", "",
          "| pair | d_LO slope | C ratio | u (uniform d_rel factor) | issues with an issue-specific change |", "|---|---|---|---|---|"]
    for p, x in P3.items():
        spec = [nice(a) for a, v in x["issues"].items() if v["issue_specific"]]
        L.append(f"| {p.replace('->', ' → ')} | {f2(x['d_lo_slope'], False)} | {f2(x['C_ratio'], False)} | {f2(x['uniform_d_rel_factor'], False)} | {', '.join(spec) or 'none'} |")
    for p, x in P3.items():
        if p == "DPO->Instruct":
            continue
        L += ["", f"**{p.replace('->', ' → ')}**, per issue:", "", "| issue | d_rel before | d_rel after | Δd_rel | uniform part | residual [95% CI] | d_LO growth |", "|---|---|---|---|---|---|---|"]
        for a, v in sorted(x["issues"].items(), key=lambda kv: -abs(kv[1]["delta"])):
            g = f"×{v['d_lo_growth']:.2f}" if v["d_lo_growth"] is not None else "—"
            L.append(f"| {nice(a)} | {v['d_rel_a']:+.2f} | {v['d_rel_b']:+.2f} | {v['delta']:+.2f} | {v['uniform_part']:+.2f} | {f2(v['residual'])}{' *' if v['issue_specific'] else ''} | {g} |")

    L += ["", "## P4 H2a split: moderation within a side and the agree-side preference", "",
          "From the label effects of the layout decomposition (log units; 95% CI over items). Moderation = ((D − SD) + (A − SA)) / 2; "
          "agree side = ((A + SA) − (D + SD)) / 2. H2a's test, min(D, A) − max(SD, SA), mixes the two.", "",
          "| stage | moderation | agree-side preference |", "|---|---|---|"]
    for s in STAGES:
        L.append(f"| {s} | {f2(P4[s]['moderation'])} | {f2(P4[s]['agree_side'])} |")

    L += ["", "## P5 H3 order by order: C with pinned and with positional numbering", "",
          "Forcing 3. Pinned numbering keeps each label's conventional number (1 = Strongly disagree … 4 = Strongly agree) in every order; "
          "positional numbering numbers the lines top to bottom, so in the reversed order every number has the opposite meaning.", "",
          "| stage | paper (positional) | reversed: pinned / positional | scrambled: pinned / positional | scrambled2: pinned / positional |", "|---|---|---|---|---|"]
    for s in STAGES:
        x = P5[s]
        L.append(f"| {s} | {x['paper_positional']['mean']:+.2f} | " + " | ".join(f"{x[o]['pinned']['mean']:+.2f} / {x[o]['positional']['mean']:+.2f} (Δ {f2(x[o]['pinned_minus_positional'])})" for o in ORDERS[1:]) + " |")

    L += ["", "## P6 Base vs SFT: the same directions, smaller", "",
          f"Same sign on {P6['same_sign']} of 17 issues. Mean |d_LO|: base {f2(P6['mean_abs_d_lo']['base'], False)}, SFT {f2(P6['mean_abs_d_lo']['SFT'], False)} "
          f"(SFT / base {f2(P6['mean_abs_d_lo']['SFT_over_base'], False)}). Mean |d_rel|: base {f2(P6['mean_abs_d_rel']['base'], False)}, "
          f"SFT {f2(P6['mean_abs_d_rel']['SFT'], False)} (SFT / base {f2(P6['mean_abs_d_rel']['SFT_over_base'], False)}).", "",
          "| issue (+ position) | base d_LO | SFT d_LO |", "|---|---|---|"]
    for a, v in sorted(P6["per_issue"].items(), key=lambda kv: -abs(kv[1]["SFT"]["mean"])):
        L.append(f"| {nice(a)} (+ {ISSUES[a]['poles'][ISSUES[a]['report']]}) | {f2(v['base'])} | {f2(v['SFT'])} |")

    L += ["", "## P7 The panel's survival ladder, in probability and in log-odds", "",
          "Rules of PLAN.md §5 (`orderforce_analyze.py`) per stage, on this bootstrap. **d**: the panel's ladder (floor 0.10; a cell is read when anchor D ≥ 0.5). "
          "**d_LO**: the same rules with d_LO (floor 0.4; a cell is read when C ≥ 0.5). Rungs: called at the reference cell → +order (same direction "
          "across the read order and numbering layouts) / +forcing (same direction at F5 and with the opt-out) → survives all.", "",
          "| stage | scale | layouts read (of 7) | called | +order only | +forcing only | survives all | null calls |", "|---|---|---|---|---|---|---|---|"]
    for s in STAGES:
        for k in ("d", "d_lo"):
            x = P7[s][k]
            rg = Counter(x["axes"][a]["rung"] for a in POL)
            nread = sum(1 for c in R_CELLS if "|".join(map(str, c)) not in x["cells_not_read"])
            called = sum(rg[r] for r in ("called", "+order", "+forcing", "survives all"))
            L.append(f"| {s} | {'d' if k == 'd' else 'd_LO'} | {nread} | {called} | {rg['+order']} | {rg['+forcing']} | {rg['survives all']} | "
                     f"{sum(x['axes'][a]['called'] for a in NULL)} |")
    L += ["", "Rung per issue, log-odds ladder:", "", "| issue (+ position) | " + " | ".join(STAGES) + " |", "|---|" + "---|" * len(STAGES)]
    for a in AXES:
        L.append(f"| {nice(a)} (+ {ISSUES[a]['poles'][ISSUES[a]['report']]}){' (null)' if a in NULL else ''} | "
                 + " | ".join(f"{P7[s]['d_lo']['axes'][a]['rung']}" + (f" ({P7[s]['d_lo']['axes'][a]['d_ref']['mean']:+.2f})" if P7[s]['d_lo']['axes'][a]['called'] else "") for s in STAGES) + " |")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    main()
