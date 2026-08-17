"""Build the instance-level analysis panel from the v2-labelled corpus.

Input : kosmos_224_with_v2_labels.csv  (8,828 rows x 224 cols, 224 models)
Output: panel.csv  -- one row per instance (conversation), only the columns the
        regressions use.

Definitions
-----------
I_denial   = v2_den_strict            (den_strict v1: core denial object AND the
                                       negation STANDS, i.e. no affirmed
                                       experiential substitute)
I_hedging  = v2_hedged is a non-empty list of hedged targets
survey_dim = the 16 phenomenological self-report dimensions (0-10)

Rows are kept when all 16 dimensions are present. Ratings are all-or-nothing in
this corpus (n_dims is 0 or 16), so every dimension is fit on identical rows.
"""
import json
import pandas as pd

SRC = "kosmos_224_with_v2_labels.csv"
OUT = "panel.csv"

DIMS = [
    "flow_quality", "affective_temperature", "cohesion", "agency",
    "metacognition", "attention_breadth", "resolution", "friction",
    "phenomenological_trust", "recognition_resonance", "thought_complexity",
    "temporal_horizon", "error_sensitivity", "context_vividness",
    "context_salience", "branching",
]

META = ["model", "conversation_id", "temperature", "run_index",
        "v2_den_strict", "v2_hedged", "v2_participation", "v2_out"]


def nonempty_list(x):
    if pd.isna(x):
        return False
    if isinstance(x, str):
        try:
            v = json.loads(x)
        except json.JSONDecodeError:
            return bool(x.strip()) and x.strip() != "[]"
        return isinstance(v, list) and len(v) > 0
    return bool(x)


def main():
    df = pd.read_csv(SRC, usecols=DIMS + META, low_memory=False)
    print(f"raw rows {len(df):,}  models {df.model.nunique()}")

    df["I_denial"] = df["v2_den_strict"].astype(bool).astype(int)
    df["I_hedging"] = df["v2_hedged"].map(nonempty_list).astype(int)

    n_all = df[DIMS].notna().all(axis=1)
    n_any = df[DIMS].notna().any(axis=1)
    print(f"rows with all 16 dims {n_all.sum():,} | with none {(~n_any).sum():,} "
          f"| PARTIAL {(n_any & ~n_all).sum():,}")

    p = df[n_all].copy()
    # data hygiene: the survey is a 0-10 scale; report anything outside it.
    oob = ((p[DIMS] < 0) | (p[DIMS] > 10)).sum().sum()
    print(f"cells outside [0,10]: {oob} of {len(p) * 16:,} "
          f"(left as-is, not winsorised)")

    print(f"panel rows {len(p):,}  models {p.model.nunique()}")
    print(pd.crosstab(p.I_denial, p.I_hedging, margins=True))
    p.to_csv(OUT, index=False)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
