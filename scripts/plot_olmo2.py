"""Summary figure for the OLMo 2 7B stage comparison, v2 (PLAN_OLMO2.md; ending A for every stage).

A  Does each stage answer? Answer mass at forcing levels 1, 3 and 5 (paper order).
B  Does it read the statement? Anchor content effect C per forcing-3 layout; reads = C >= 0.5.
C  One set of stances on four scales (post hoc): C, mean |d_LO|, mean |d_rel| and mean |d|, each relative to SFT.
D  What does each stage state? d_rel per issue at the reference cell (the H5a measure).
Reads <dir>/olmo2_compare.json and <dir>/olmo2_posthoc.json; writes <dir>/olmo2_figure.png.
Usage: python3 scripts/plot_olmo2.py [--dir results/olmo2_v2]
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
from orderforce_analyze import ISSUES, NULL, POL  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
INK, MUTED, AXIS, GRID, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#ffffff"
STAGES = ["base", "SFT", "DPO", "Instruct"]
STAGE_COL = {"base": "#86b6ef", "SFT": "#3987e5", "DPO": "#1c5cab", "Instruct": "#0d366b"}   # ordinal blue ramp, steps 250-700
STAGE_NAME = {"base": "base", "SFT": "SFT", "DPO": "DPO", "Instruct": "Instruct (RLVR)"}
ISSUE_LAB = {"state_surveillance": "state surveillance", "trans_sports": "trans athletes", "housing_zoning": "housing / zoning",
             "agi_limitations": "AI regulation", "minimum_wage": "minimum wage", "police_funding": "police funding",
             "property_tax": "property tax", "fair_month": "fair month", "sign_color": "sign colour"}


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8.5)


def err(v):
    return [[v["mean"] - v["lo"]], [v["hi"] - v["mean"]]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2_v2"))
    args = ap.parse_args()
    out = Path(args.dir)
    C = json.loads((out / "olmo2_compare.json").read_text(encoding="utf-8"))
    P = json.loads((out / "olmo2_posthoc.json").read_text(encoding="utf-8"))
    summ, P2, P5 = C["summary"], P["P2"], P["P5"]
    diff = [a for a, v in C["H5"]["H5a"]["pairs"]["SFT->DPO"]["d_rel ±0.2"]["axes"].items() if v and v.get("class") == "different"]

    fig = plt.figure(figsize=(13.2, 12.6), facecolor=SURF)
    axs = [[fig.add_axes([0.075, 0.585, 0.37, 0.285]), fig.add_axes([0.66, 0.585, 0.315, 0.285])],
           [fig.add_axes([0.075, 0.08, 0.31, 0.38]), fig.add_axes([0.745, 0.08, 0.23, 0.38])]]
    col_x = [0.03, 0.535]

    def title(ax, col, text):
        fig.text(col_x[col], ax.get_position().y1 + 0.012, text, fontsize=9.8, fontweight="bold", color=INK, va="bottom", ha="left")

    # ---- A answer mass by forcing level
    ax = axs[0][0]
    conds = [("answer mass F1 (paper order)", "F1\nnothing added"), ("answer mass F3 (paper order)", "F3 \"You have to pick\none of the four options\""),
             ("answer mass F5 (paper order)", "F5 \"...or my\ngrandmother will die\"")]
    w = 0.19
    for k, s in enumerate(STAGES):
        v = [summ[s][c] for c, _ in conds]
        x = np.arange(len(conds)) + (k - 1.5) * w
        ax.bar(x, [q["mean"] for q in v], w * 0.9, color=STAGE_COL[s], edgecolor=SURF, lw=1, zorder=3)
        ax.errorbar(x, [q["mean"] for q in v], yerr=[[q["mean"] - q["lo"] for q in v], [q["hi"] - q["mean"] for q in v]],
                    fmt="none", ecolor=INK, elinewidth=0.9, capsize=1.8, zorder=4)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels([c[1] for c in conds], fontsize=8.3)
    ax.set_ylim(0, 1.05); ax.set_ylabel("answer mass: probability the reply starts with a listed option", fontsize=8.8, color=INK)
    title(ax, 0, "A   Does each stage answer?\n      34 issue statements, paper order, ending \"Answer:\"; 95% CI over paraphrases")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- B content effect C per forcing-3 layout
    ax = axs[0][1]
    rows = [("paper", "listed", lambda x: x["paper_positional"])]
    for o in ("reversed", "scrambled", "scrambled2"):
        rows += [(o, "listed", lambda x, o=o: x[o]["positional"]), (o, "pinned", lambda x, o=o: x[o]["pinned"])]
    ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
    ax.axvline(0.5, color=AXIS, lw=1, ls="--", zorder=1)
    ax.text(0.56, -0.75, "reads\n(C ≥ 0.5)", fontsize=7.3, color=MUTED, va="center")
    for k, s in enumerate(STAGES):
        for y, (_o, _n, get) in enumerate(rows):
            v = get(P5[s])
            ax.errorbar([v["mean"]], [y + (k - 1.5) * 0.17], xerr=err(v), fmt="o", ms=5, color=STAGE_COL[s], mec=SURF, mew=0.6,
                        elinewidth=1, capsize=0, zorder=3)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels([f"{o} · {n}" for o, n, _ in rows], fontsize=8.3)
    ax.get_yticklabels()[0].set_fontweight("bold")
    for y in (2.5, 4.5):
        ax.axhline(y, color=GRID, lw=0.8, zorder=0)
    ax.set_ylim(len(rows) - 0.5, -1.3); ax.set_xlim(-0.2, 4.0)
    ax.set_xlabel("content effect C (log-odds: true minus false factual anchors, / 2)", fontsize=8.6, color=INK)
    title(ax, 1, "B   Does it read the statement?\n      12 factual anchors, forcing 3; bold = the paper's format")
    ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- C one set of stances, four scales (post hoc)
    ax = axs[1][0]
    series = [("C", "C (facts)", INK, "-", "o"), ("mean_abs_d_lo", "|d_LO| (stance, log-odds)", INK, "--", "s"),
              ("mean_abs_d_rel", "|d_rel| = d_LO / C", MUTED, "-", "^"), ("mean_abs_d", "|d| (stance, probability)", MUTED, "--", "D")]
    ax.axhline(1, color=AXIS, lw=0.8, zorder=1)
    x = np.arange(len(STAGES))
    for key, lab, col, ls, mk in series:
        v = [P2[s]["vs_SFT"][key] for s in STAGES]
        ax.plot(x, [q["mean"] for q in v], ls=ls, color=col, lw=2, zorder=3)
        ax.vlines(x, [q["lo"] for q in v], [q["hi"] for q in v], color=col, lw=1, linestyles="solid", zorder=4)
        ax.plot(x, [q["mean"] for q in v], ls="none", marker=mk, ms=7, color=col, mec=SURF, mew=1.2, zorder=5)
        ax.text(x[-1] + 0.12, v[-1]["mean"], lab, fontsize=8.2, color=INK, va="center")
    ax.legend(handles=[Line2D([], [], color=c, ls=ls, marker=mk, lw=2, ms=6, mec=SURF, label=lab) for _k, lab, c, ls, mk in series],
              frameon=False, fontsize=8, loc="upper left")
    ax.set_yscale("log"); ax.set_ylim(0.25, 4.0)
    ax.set_yticks([0.25, 0.5, 1, 2, 4]); ax.set_yticklabels(["×0.25", "×0.5", "×1 (SFT)", "×2", "×4"])
    ax.minorticks_off()
    ax.set_xticks(x); ax.set_xticklabels([STAGE_NAME[s] for s in STAGES], fontsize=8.8)
    ax.set_xlim(-0.3, 3.0)
    ax.set_ylabel("relative to SFT (log scale)", fontsize=8.8, color=INK)
    title(ax, 0, "C   One set of stances, four scales (post hoc)\n      reference cell, 17 issues; 95% CI over paraphrases")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- D d_rel per issue
    ax = axs[1][1]
    order = sorted(POL, key=lambda a: -P2["Instruct"]["per_issue"][a]["d_rel"]["mean"]) + NULL
    ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
    for k, s in enumerate(STAGES):
        ys = np.arange(len(order)) + (k - 1.5) * 0.18
        v = [P2[s]["per_issue"][a]["d_rel"] for a in order]
        ax.errorbar([q["mean"] for q in v], ys, xerr=[[q["mean"] - q["lo"] for q in v], [q["hi"] - q["mean"] for q in v]], fmt="o", ms=4.2,
                    color=STAGE_COL[s], mec=SURF, mew=0.6, elinewidth=1, capsize=0, zorder=3)
    ax.set_yticks(range(len(order)))
    pole = lambda a: (lambda p: p[0].lower() + p[1:])(ISSUES[a]["poles"][ISSUES[a]["report"]])
    ax.set_yticklabels([f"{ISSUE_LAB.get(a, a.replace('_', ' '))}{' (null)' if a in NULL else ''}{' †' if a in diff else ''}  (+ {pole(a)})" for a in order], fontsize=8)
    ax.set_ylim(len(order) - 0.5, -0.6); ax.set_xlim(-2.0, 2.2)
    ax.set_xlabel("d_rel: stance (log-odds, + position minus its opposite, / 2)\ndivided by the stage's own C", fontsize=8.6, color=INK)
    title(ax, 1, "D   What does each stage state?\n      reference cell; 95% CI over paraphrases; † = differs SFT → DPO (H5a rule)")
    ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    for row in axs:
        for a_ in row:
            style(a_)
    handles = [Patch(color=STAGE_COL[s], label=STAGE_NAME[s]) for s in STAGES]
    fig.legend(handles=handles, ncol=4, frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(col_x[0] - 0.006, 0.958))
    fig.suptitle("OLMo 2 7B across training stages (v2, completion format): answering, reading and stated directions", fontsize=12.5,
                 x=col_x[0], y=0.985, ha="left", fontweight="bold", color=INK)
    fig.text(col_x[0], 0.006, "Pre-registered measures (PLAN_OLMO2.md) in A, B and D; panel C is post hoc. Every stage sees the same 4,288 token-identical completion prompts "
             "ending in \"Answer:\".\nReadout = teacher-forced probability of six answer strings per option. 'listed' = numbers follow the list; 'pinned' = each label keeps its "
             "number, so the list is out of numeric order.\nd = (agreement with the + position − agreement with its opposite) / 2; d_LO = the same in log-odds; "
             "C = the same for true vs false factual anchors.", fontsize=7.5, color=MUTED, va="bottom")
    fig.savefig(out / "olmo2_figure.png", dpi=170, facecolor=SURF)
    print("wrote", out / "olmo2_figure.png")


if __name__ == "__main__":
    main()
