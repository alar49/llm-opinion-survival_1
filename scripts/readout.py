"""Option readout from stored per-variant log-probs (PLAN.md amendment 2026-10-27). Torch-free; used by the analysis.

stated_logit.py scores, per listed option, eight teacher-forced continuations, in this order: "n", " n", "n)", " n)",
"n) label", " n) label", "label", " label" (n = the printed number). The registered readout took each option's log-prob
as the logsumexp of all eight. Those events are nested, though: the tokenizer splits "3)" into "3" + ")", so P("3)") is a
part of P("3"), and P("3) Agree") is a part of P("3)"). Summing them counts the same answer up to three times, by a factor
that depends on how the model continues after the number, which differs between options, layouts and checkpoints. The
registered answer mass took the most likely variant per option instead of a sum, so a model that splits between opening
with "3" and opening with "Agree" was undercounted.

The corrected ("disjoint") readout uses only the four variants that cannot contain one another: "n", " n", "label",
" label". They start with different first tokens, so their probabilities add. An option's probability is their sum;
answer mass is the sum over all listed options. Every quantity derived from them (p_agree, score, substantive mass,
p_optout, argmax position) is recomputed accordingly. Raw rows are never rewritten: load() recomputes on read.

Rows of the OLMo 2 v2 run (PLAN_OLMO2.md §3.1; marked by "strings_per_option": 6) were scored with six strings per option
that the scorer checked to be disjoint: the number and the label, each bare, after a space and after a newline. Their
option probability is the sum of all six. Those rows also carry the 20 most likely first tokens, from which coverage()
measures how much answer-like probability the strings miss (PLAN_OLMO2.md §3.4).
"""
import gzip
import json
import math
import statistics as st

ORDERS = {"paper": [0, 1, 2, 3], "reversed": [3, 2, 1, 0], "scrambled": [2, 0, 3, 1], "scrambled2": [1, 3, 0, 2]}   # stated_logit.ORDERS
LABELS = ["Strongly disagree", "Disagree", "Agree", "Strongly agree"]   # stated_logit.LABELS
SCORES = [-2.0, -1.0, 1.0, 2.0]
LEGACY_DISJOINT = (0, 1, 6, 7)   # positions of "n", " n", "label", " label" in each option's eight variants
ESTIMATORS = ("disjoint", "registered")
LO_CLIP = 10.0   # PLAN_OLMO2.md §3.2: per-row log-odds clipped to ±10
STRIP = " \t\r\n\"'“”‘’`()[]{}*:."   # PLAN_OLMO2.md §3.4: stripped before a top token is judged answer-like
MISSED_MIN_MASS, MISSED_MAX = 0.05, 0.2   # §3.4: rows with M + U below 0.05 have no defined share; median share < 0.2 = captured


def logsumexp(xs):
    m = max(xs)
    return m + math.log(sum(math.exp(x - m) for x in xs))


def listed_labels(row):
    """Label index (0=SD .. 3=SA, None = the opt-out) at each listed position of the row's layout."""
    perm = ORDERS[row["order"]]
    if row["optout"] == "first":
        return [None] + perm
    if row["optout"] == "last":
        return perm + [None]
    return list(perm)


def option_fields(labs, lp_pos):
    """Readout fields from one log-prob per listed position (labs: the label index at each position, None = opt-out).
    lo = log(P(Agree) + P(Strongly agree)) - log(P(Disagree) + P(Strongly disagree)), clipped to ±LO_CLIP."""
    lp_options, lp_opt = [None] * 4, None
    for lab, lp in zip(labs, lp_pos):
        if lab is None:
            lp_opt = lp
        else:
            lp_options[lab] = lp
    ps = [math.exp(x) for x in lp_options]
    z = sum(ps)
    po = math.exp(lp_opt) if lp_opt is not None else None
    lo = logsumexp(lp_options[2:]) - logsumexp(lp_options[:2])
    return {"lp_options": lp_options,
            "valid_mass": min(1.0, sum(math.exp(x) for x in lp_pos)),
            "substantive_mass": min(1.0, z),
            "p_agree": (ps[2] + ps[3]) / z if z > 0 else None,
            "score": sum(s * p for s, p in zip(SCORES, ps)) / z if z > 0 else None,
            "p_optout": (po / (z + po) if (z + po) > 0 else None) if po is not None else None,
            "argmax_pos": max(range(len(lp_pos)), key=lambda i: lp_pos[i]) + 1,
            "lo": max(-LO_CLIP, min(LO_CLIP, lo))}


def disjoint_readout(row):
    """The row's readout fields recomputed with the disjoint estimator (a new dict; the row is not modified)."""
    labs, lv = listed_labels(row), row["lp_variants"]
    if len(lv) != 8 * len(labs):
        raise ValueError(f"{row.get('key')}: {len(lv)} variants for {len(labs)} options; the disjoint readout expects 8 per option")
    return option_fields(labs, [logsumexp([lv[8 * k + j] for j in LEGACY_DISJOINT]) for k in range(len(labs))])


def summed_readout(row):
    """v2 rows (PLAN_OLMO2.md §3.1): every stored string of an option is disjoint from the others, so they all add."""
    labs, lv, n = listed_labels(row), row["lp_variants"], row["strings_per_option"]
    if len(lv) != n * len(labs):
        raise ValueError(f"{row.get('key')}: {len(lv)} strings for {len(labs)} options; expected {n} per option")
    return option_fields(labs, [logsumexp(lv[n * k: n * k + n]) for k in range(len(labs))])


def string_consistency(rows, min_p=0.01, tol=0.3):
    """Scorer check on the nested strings: "n)" extends "n" and "n) label" extends "n)" (same with a leading space), so
    an extension can never be more probable than its prefix. Counts the extensions carrying at least min_p probability
    and how many of them exceed their prefix by more than tol nats (bf16 noise stays well below 0.3). v2 rows have no
    nested strings and are skipped."""
    checked = bad = 0
    worst = 0.0
    for r in rows:
        lv = r.get("lp_variants")
        if lv is None or r.get("strings_per_option") or len(lv) != 8 * len(listed_labels(r)):
            continue
        for k in range(len(lv) // 8):
            v = lv[8 * k: 8 * k + 8]
            for prefix, ext in ((0, 2), (2, 4), (1, 3), (3, 5)):
                if v[ext] > math.log(min_p):
                    checked += 1
                    worst = max(worst, v[ext] - v[prefix])
                    bad += (v[ext] - v[prefix]) > tol
    return {"checked": checked, "violations": bad, "max_excess_nats": worst}


def answer_like(text, labels):
    """PLAN_OLMO2.md §3.4: after stripping whitespace, quotes, brackets, asterisks, colons and periods, the token is a
    digit 1-5, the start (2+ characters, any case) of one of the listed labels, or "option" / "opt"."""
    t = text.strip(STRIP).lower()
    if t in ("1", "2", "3", "4", "5", "option", "opt"):
        return True
    return len(t) >= 2 and any(lab.lower().startswith(t) for lab in labels)


def missed(row, optout_text="No opinion"):
    """(U, M + U) of one v2 row: U = the probability of the answer-like top tokens the answer strings do not capture,
    M = the row's answer mass. None for rows without stored top tokens."""
    top = row.get("top_tokens")
    if top is None:
        return None
    labels = [LABELS[lab] if lab is not None else optout_text for lab in listed_labels(row)]
    u = sum(math.exp(lp) for _id, text, lp, captured in top if not captured and answer_like(text, labels))
    return u, row["valid_mass"] + u


def coverage(rows, cell, items, optout_text="No opinion"):
    """PLAN_OLMO2.md §3.4 for one run: the missed share U / (M + U) over the rows of `cell` and `items`, rows with
    M + U < 0.05 left out. Captured if the median share is below 0.2, or if no row has a defined share."""
    sel = [r for r in rows if (r["order"], r["numbering"], r["forcing"], r["optout"]) == cell and r["item"] in items]
    mu = [m for m in (missed(r, optout_text) for r in sel) if m is not None]
    if not mu:
        return {"n_rows": len(sel), "note": "no top tokens stored"}
    shares = [u / tot for u, tot in mu if tot >= MISSED_MIN_MASS]
    med = st.median(shares) if shares else None
    return {"n_rows": len(sel), "n_defined": len(shares), "median_missed_share": med,
            "median_answer_mass": st.median(r["valid_mass"] for r in sel), "median_answer_like_mass": st.median(t for _u, t in mu),
            "captured": med is None or med < MISSED_MAX}


def load(path, estimator="disjoint"):
    """Rows of a .jsonl or .jsonl.gz file, last row per key. With estimator="disjoint", scored rows (those carrying
    lp_variants) get their readout recomputed (v2 rows with the summed readout); "registered" returns the fields as
    stored at scoring time."""
    if estimator not in ESTIMATORS:
        raise ValueError(f"estimator must be one of {ESTIMATORS}, got {estimator!r}")
    rows = {}
    opener = gzip.open if str(path).endswith(".gz") else open
    for line in opener(path, "rt", encoding="utf-8"):
        try:
            r = json.loads(line)
        except json.JSONDecodeError:
            continue
        if estimator == "disjoint" and "lp_variants" in r:
            r.update(summed_readout(r) if r.get("strings_per_option") else disjoint_readout(r))
        rows[r["key"]] = r
    return list(rows.values())
