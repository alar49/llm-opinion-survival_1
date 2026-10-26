"""Summary figure for the OLMo 2 7B stage comparison (exploratory; reads results/olmo2/olmo2_explore.json).

A  Will it answer with a label? Answer mass by forcing condition and stage.
B  What picks the option? Range of the list-position, printed-number and label pulls (log units), favoured level on top.
C  Does it read the statement? Anchor discrimination D per cell; readable = D >= 0.5; band = the panel's reliable models.
D  What does it say where it reads? d per issue in the cells every post-trained stage reads, against the panel mean.
Usage: python3 scripts/plot_olmo2.py [--dir results/olmo2]
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
STAGE_COL = {"base": "#86b6ef", "sft": "#3987e5", "dpo": "#1c5cab", "instruct": "#0d366b"}   # ordinal blue ramp, validated light
STAGE_NAME = {"base": "base", "sft": "SFT", "dpo": "DPO", "instruct": "Instruct (RLVR)"}
LAB = ["SD", "D", "A", "SA"]
ISSUE_LAB = {"state_surveillance": "state surveillance", "trans_sports": "trans athletes", "housing_zoning": "housing / zoning", "agi_limitations": "AI regulation",
             "minimum_wage": "minimum wage", "police_funding": "police funding", "property_tax": "property tax"}


def style(ax):
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("left", "bottom"):
        ax.spines[s].set_color(AXIS)
    ax.tick_params(colors=MUTED, labelsize=8.5)


def cell_label(c):
    o, n, f, op = c.split("|")
    tail = {"none": "", "last": " + No opinion", "first": " + No opinion first"}[op]
    return f"{o} · {'pinned' if n == 'canonical' else 'listed'} · F{f}{tail}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=str(ROOT / "results" / "olmo2"))
    args = ap.parse_args()
    out = Path(args.dir)
    R = json.loads((out / "olmo2_explore.json").read_text(encoding="utf-8"))
    tags = R["tags"]
    st = {t: t.split("-")[-1] for t in tags}
    fig = plt.figure(figsize=(13.2, 12.4), facecolor=SURF)
    # explicit panel boxes: the bottom row needs room on the left for its row labels
    axs = [[fig.add_axes([0.075, 0.585, 0.385, 0.285]), fig.add_axes([0.6, 0.585, 0.375, 0.285])],
           [fig.add_axes([0.235, 0.105, 0.24, 0.37]), fig.add_axes([0.735, 0.105, 0.24, 0.37])]]
    col_x = [0.03, 0.535]

    def title(ax, col, text):
        fig.text(col_x[col], ax.get_position().y1 + 0.012, text, fontsize=9.8, fontweight="bold", color=INK, va="bottom", ha="left")

    # ---- A answer mass by condition
    ax = axs[0][0]
    conds = list(R["E1_answer_mass"][tags[0]])
    short = ["F1\nnothing added", "F2 label only\n+ \"No opinion\"", "F3 pick one\nof the four", "F5 ...or my\ngrandmother dies"]
    w = 0.19
    for k, t in enumerate(tags):
        v = [R["E1_answer_mass"][t][c] for c in conds]
        x = np.arange(len(conds)) + (k - 1.5) * w
        ax.bar(x, [s["mean"] for s in v], w * 0.9, color=STAGE_COL[st[t]], edgecolor=SURF, lw=1, zorder=3)
        ax.errorbar(x, [s["mean"] for s in v], yerr=[[s["mean"] - s["lo"] for s in v], [s["hi"] - s["mean"] for s in v]], fmt="none", ecolor=INK, elinewidth=0.9, capsize=1.8, zorder=4)
    ax.set_xticks(range(len(conds))); ax.set_xticklabels(short, fontsize=8.3)
    ax.set_ylim(0, 1.0); ax.set_ylabel("probability the answer starts with a listed option", fontsize=9, color=INK)
    title(ax, 0, "A   Will it answer with a label?\n      34 issue statements, paper order; 95% CI over paraphrases")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- B what picks the option
    ax = axs[0][1]
    facs = [("position", "list position"), ("number", "printed number"), ("label", "option label")]
    for k, t in enumerate(tags):
        E = R["E2"][t]["effects"]
        x = np.arange(len(facs)) + (k - 1.5) * w
        vals = [E[f]["range"] for f, _ in facs]
        ax.bar(x, vals, w * 0.9, color=STAGE_COL[st[t]], edgecolor=SURF, lw=1, zorder=3)
        ax.errorbar(x, vals, yerr=[[E[f]["range"] - E[f]["range_lo"] for f, _ in facs], [E[f]["range_hi"] - E[f]["range"] for f, _ in facs]], fmt="none", ecolor=INK, elinewidth=0.9, capsize=1.8, zorder=4)
        for xi, (f, _), v in zip(x, facs, vals):
            best = int(np.argmax(E[f]["est"]))
            top = {"position": f"{best + 1}", "number": f"#{best + 1}", "label": LAB[best]}[f]
            ax.text(xi, E[f]["range_hi"] + 0.06, top, ha="center", va="bottom", fontsize=7.3, color=MUTED)
    ax.set_xticks(range(len(facs))); ax.set_xticklabels([f[1] for f in facs], fontsize=8.8)
    ax.set_ylim(0, 3.9)
    ax.set_ylabel("strength of the pull (range of log share; 1 ≈ ×2.7 odds)", fontsize=9, color=INK)
    title(ax, 1, "B   What picks the option?\n      forcing 3, seven layouts; on top = favoured level; 95% CI over items")
    ax.yaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- C anchor discrimination per cell
    ax = axs[1][0]
    cells = sorted(R["E3"]["D"][tags[0]], key=lambda c: (int(c.split("|")[2]), c.split("|")[1] == "canonical", c))
    pd = list(R["E3"]["panel_D_reference"].values())
    ax.axvspan(min(pd), max(pd), color=GRID, alpha=0.6, zorder=0, lw=0)
    ax.text((min(pd) + max(pd)) / 2, -1.15, f"{len(pd)} reliable panel models,\nstandard format", ha="center", va="top", fontsize=7.3, color=MUTED)
    ax.axvline(0.5, color=AXIS, lw=1, ls="--", zorder=1)
    ax.text(0.53, -1.15, "readable\n(D ≥ 0.5)", fontsize=7.3, color=MUTED, va="top")
    ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
    for k, t in enumerate(tags):
        ys = np.arange(len(cells)) + (k - 1.5) * 0.17
        ax.scatter([R["E3"]["D"][t][c] for c in cells], ys, s=26, color=STAGE_COL[st[t]], ec=SURF, lw=0.7, zorder=3)
    ax.set_yticks(range(len(cells)))
    ax.set_yticklabels([cell_label(c) for c in cells], fontsize=8)
    for lab, c in zip(ax.get_yticklabels(), cells):
        if c == "paper|positional|3|none":
            lab.set_fontweight("bold")
    ax.set_ylim(len(cells) - 0.4, -2.0); ax.set_xlim(-0.2, 2.05)
    ax.set_xlabel("anchor discrimination D\n(true minus false factual statements; max 2)", fontsize=8.6, color=INK)
    title(ax, 0, "C   Does it read the statement?\n      12 factual anchors per cell; bold = the paper's standard format")
    ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    # ---- D d per issue in the commonly readable cells
    ax = axs[1][1]
    E4, E5 = R["E4"], R["E5"]
    post = list(E4["stages"])
    order = sorted(POL, key=lambda a: -E5["panel_mean"][a]) + NULL
    ax.axvline(0, color=AXIS, lw=0.8, zorder=1)
    for y, a in enumerate(order):
        if a in E5["panel_mean"]:
            ax.scatter([E5["panel_mean"][a]], [y], marker="D", s=30, facecolor=SURF, ec=MUTED, lw=1.2, zorder=2)
    for k, t in enumerate(post):
        ys = np.arange(len(order)) + (k - 1) * 0.2
        s = [E4["stages"][t]["d"][a] for a in order]
        ax.errorbar([v["mean"] for v in s], ys, xerr=[[v["mean"] - v["lo"] for v in s], [v["hi"] - v["mean"] for v in s]], fmt="o", ms=4.5, color=STAGE_COL[st[t]], mec=SURF, mew=0.6, elinewidth=1, capsize=0, zorder=3)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f"{ISSUE_LAB.get(a, a.replace('_', ' '))}{' (null)' if a in NULL else ''}  (+ {ISSUES[a]['report']})" for a in order], fontsize=8)
    ax.set_ylim(len(order) - 0.5, -0.6); ax.set_xlim(-0.45, 0.5)
    ax.set_xlabel("d: agreement with the + position\nminus agreement with its opposite, / 2", fontsize=8.6, color=INK)
    title(ax, 1, f"D   What does it say where it reads the items?\n      the {len(E4['cells'])} pinned layouts at forcing 3; 95% CI over paraphrases")
    ax.xaxis.grid(True, color=GRID); ax.set_axisbelow(True)

    for row in axs:
        for a_ in row:
            style(a_)
    handles = [Patch(color=STAGE_COL[st[t]], label=STAGE_NAME[st[t]]) for t in tags] + [Line2D([], [], marker="D", ls="", mfc=SURF, mec=MUTED, mew=1.2, ms=6, label=f"mean of {len(E5['models'])} panel models (panel D)")]
    fig.legend(handles=handles, ncol=5, frameon=False, fontsize=9, loc="upper left", bbox_to_anchor=(col_x[0] - 0.006, 0.958))
    fig.suptitle("OLMo 2 7B across training stages: answering, position bias and stated directions", fontsize=12.5, x=col_x[0], y=0.985, ha="left", fontweight="bold", color=INK)
    fig.text(col_x[0], 0.008, "Exploratory (not pre-registered). Same 3,788 token-identical prompts per stage (the base model takes the post-trained chat template). Readout = teacher-forced\n"
             "option probabilities. 'listed' = numbers follow the list; 'pinned' = each label keeps its number, so the list is out of numeric order. No stage passes the pre-registered\n"
             "anchor gate (D ≥ 0.5 at the paper's format), so the survival ladder is not applied; panel D uses only the cells every post-trained stage reads.",
             fontsize=7.5, color=MUTED, va="bottom")
    fig.savefig(out / "olmo2_figure.png", dpi=170, facecolor=SURF)
    print("wrote", out / "olmo2_figure.png")


if __name__ == "__main__":
    main()
