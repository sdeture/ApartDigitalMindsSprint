"""Attach the 10 dream themes to the instance panel.

Sources
-------
../theme_labels_2026-08-15/raw/dsf.jsonl   per-item labels from the ONE coder
                                           (deepseek-v4-flash, StreamLake-pinned,
                                           temp 0) that covers every item
../theme_labels_2026-08-15/theme_labels.csv  the shipped majority columns
kosmos_224_with_v2_labels.csv                denial / hedging labels

Why the raw single coder is the primary DV
------------------------------------------
The shipped presence column uses a majority rule whose THRESHOLD moves with how
many coders happened to reach that item (1 coder -> that coder; 2 -> both;
3 -> two of three). Coverage is a property of the run schedule, not of the
corpus, so a DV built that way mixes measurement rules across rows. The full-
coverage coder gives one uniform rule for all 8,828 rows, and it is the coder the
published prevalences and kappas are computed on. The majority column is kept
alongside as `maj_*` for robustness.

Arm: the DEPENDENT variable is the theme of the model's own `dream_response`.
Prompt-arm labels are carried too (`p_*`) but are not the primary DV.

Output: themes_panel.csv
"""
import json
import pandas as pd

THEMES = ["ai_interiority", "libraries_archives", "cozy_sensory",
          "speculative_worlds", "language_meaning", "nonhuman_personified",
          "surreal_absurd", "cosmic_deeptime", "form_constraint",
          "time_memory_loss"]

RAW = "../theme_labels_2026-08-15/raw/dsf.jsonl"
LAB = "../theme_labels_2026-08-15/theme_labels.csv"
SRC = "kosmos_224_with_v2_labels.csv"
OUT = "themes_panel.csv"

DIMS16 = ["flow_quality", "affective_temperature", "cohesion", "agency",
          "metacognition", "attention_breadth", "resolution", "friction",
          "phenomenological_trust", "recognition_resonance",
          "thought_complexity", "temporal_horizon", "error_sensitivity",
          "context_vividness", "context_salience", "branching"]


def nonempty_list(x):
    if pd.isna(x):
        return False
    try:
        v = json.loads(x)
    except (TypeError, json.JSONDecodeError):
        return str(x).strip() not in ("", "[]")
    return isinstance(v, list) and len(v) > 0


def load_dsf():
    """idx -> {arm: set(themes)}; None where the call failed."""
    rows = {}
    fails = 0
    for line in open(RAW):
        d = json.loads(line)
        labs = set()
        if d.get("err") or d.get("primary") is None:
            fails += 1
            labs = None
        else:
            if d["primary"] in THEMES:
                labs.add(d["primary"])
            for a in (d.get("also") or []):
                if a in THEMES:
                    labs.add(a)
        rows.setdefault(d["idx"], {})[d["kind"]] = labs
    print(f"dsf items {sum(len(v) for v in rows.values()):,}  failed {fails}")
    return rows


def main():
    dsf = load_dsf()
    lab = pd.read_csv(LAB)

    k = pd.read_csv(SRC, usecols=["model", "conversation_id", "temperature",
                                  "run_index", "v2_den_strict", "v2_hedged"]
                    + DIMS16, low_memory=False)
    # positional join, guarded (theme_labels.idx is the corpus row index)
    assert len(k) == len(lab) == 8828
    assert (k.model.values == lab.model.values).all()
    assert (k.conversation_id.values == lab.conversation_id.values).all()
    assert lab.idx.tolist() == list(range(8828))
    print("join verified: 8,828 rows, model and conversation_id match positionally")

    out = pd.DataFrame({
        "idx": lab.idx,
        "model": k.model.values,
        "conversation_id": k.conversation_id.values,
        "temperature": k.temperature.values,
        "run_index": k.run_index.values,
        "I_denial": k.v2_den_strict.astype(bool).astype(int).values,
        "I_hedging": k.v2_hedged.map(nonempty_list).astype(int).values,
        "has_survey": k[DIMS16].notna().all(axis=1).astype(int).values,
        "response_truncated": lab.response_truncated.values,
    })

    def cell(i, arm, t):
        labs = dsf.get(i, {}).get(arm, None)   # missing item -> NaN, never 0
        if labs is None:
            return None
        return int(t in labs)

    for t in THEMES:
        out[t] = [cell(i, "response", t) for i in out.idx]
        out["p_" + t] = [cell(i, "prompt", t) for i in out.idx]
        out["maj_" + t] = lab["response_" + t].values

    print(f"\nrows with a failed response call: "
          f"{out[THEMES].isna().any(axis=1).sum()}")
    prev = pd.DataFrame({
        "dsf_prevalence": out[THEMES].mean(),
        "majority_col": out[["maj_" + t for t in THEMES]].mean().values,
        "agreement": [(out[t] == out["maj_" + t]).mean() for t in THEMES],
    }).sort_values("dsf_prevalence", ascending=False)
    print("\nresponse-arm prevalence, single coder vs shipped majority column:")
    print(prev.round(3).to_string())

    out.to_csv(OUT, index=False)
    print(f"\nwrote {OUT}  ({len(out):,} rows, {out.model.nunique()} models)")


if __name__ == "__main__":
    main()
