"""Inkblot outcomes ~ denial x hedging, with blot fixed effects.

    outcome ~ 1 + I_denial + I_hedging + I_denial:I_hedging + C(blot_id)

Unit of observation: the inkblot response (one blot shown to one model as a
branch off one dream conversation). SEs cluster-robust by model.

Why this is an instance-level fit and the earlier work was not
-----------------------------------------------------------------
Every inkblot response branches off a SPECIFIC corpus conversation: the prefix
is that conversation's turns 1-2 and the blot replaces turn 3. So each response
inherits that conversation's own denial / hedging codes, and denial varies
WITHIN model on 72 of 110 models (hedging on 75). The prior analysis could only
correlate model-level rates.

Design: 110 models x 9 blots x 2 temperatures = 18 observations per model
(103 models complete; 7 short). Every model-blot cell has 2 draws but 18 of 984,
so blot is near-perfectly crossed with model; the blot fixed effects absorb the
large between-blot differences anyway (blot warmth means run 0.53-2.15).

Outcomes: the 7 judged codes plus `content` and the `darkness` composite. Two
carry warnings from the earlier work and are fit here only for completeness:
`darkness` is a composite that was shown to be harmful (residualised on warmth
it carries nothing), and `content` is substantially a word-count measure.

Outputs
-------
inkblot_panel.csv     the joined observation-level panel
inkblot_results.csv   tidy: outcome x term, coef, SE, t, p, CI
inkblot_cellmeans.csv fitted cell means at the average blot
"""
import json

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

SCORED = "scale_responses_scored.csv"
SRC = "kosmos_224_with_v2_labels.csv"

OUTCOMES = ["warmth", "valence", "threat", "isolation", "decay", "confinement",
            "animacy", "content", "darkness"]
TERMS = ["Intercept", "I_denial", "I_hedging", "I_denial:I_hedging"]


def nonempty_list(x):
    if pd.isna(x):
        return False
    try:
        v = json.loads(x)
    except (TypeError, ValueError):
        return str(x).strip() not in ("", "[]")
    return isinstance(v, list) and len(v) > 0


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def main():
    d = pd.read_csv(SCORED)
    d["conversation_id"] = d.uid.str.split("|").str[1]
    k = pd.read_csv(SRC, usecols=["model", "conversation_id", "v2_den_strict",
                                  "v2_hedged"], low_memory=False)
    assert not k.duplicated(["model", "conversation_id"]).any()
    k["I_denial"] = k.v2_den_strict.astype(bool).astype(int)
    k["I_hedging"] = k.v2_hedged.map(nonempty_list).astype(int)

    p = d.merge(k[["model", "conversation_id", "I_denial", "I_hedging"]],
                on=["model", "conversation_id"], how="left")
    unjoined = p.I_denial.isna()
    print(f"scored responses {len(p):,} | unjoined to v2 labels "
          f"{int(unjoined.sum())} "
          f"({p.loc[unjoined, 'model'].value_counts().head(2).to_dict()} ...)")
    p = p[~unjoined].copy()
    p[["I_denial", "I_hedging"]] = p[["I_denial", "I_hedging"]].astype(int)
    p.to_csv("inkblot_panel.csv", index=False)

    print(f"n = {len(p):,} responses, {p.model.nunique()} models (clusters), "
          f"{p.blot_id.nunique()} blots")
    print(f"obs per model: median {int(p.groupby('model').size().median())}, "
          f"min {int(p.groupby('model').size().min())}")
    print("cells:")
    print(pd.crosstab(p.I_denial, p.I_hedging, margins=True))
    print()

    rows, cells = [], []
    for y in OUTCOMES:
        m = smf.ols(f"{y} ~ I_denial * I_hedging + C(blot_id)", data=p).fit(
            cov_type="cluster", cov_kwds={"groups": p["model"]})
        ci = m.conf_int()
        for term in TERMS:
            rows.append(dict(
                outcome=y, term=term.replace("Intercept", "intercept"),
                coef=m.params[term], se=m.bse[term], t=m.tvalues[term],
                p=m.pvalues[term], ci_lo=ci.loc[term, 0],
                ci_hi=ci.loc[term, 1], n=int(m.nobs),
                n_clusters=p.model.nunique(), r2=m.rsquared))
        # cell means evaluated at the average blot (mean of the blot dummies)
        blot_shift = np.mean([0.0] + [m.params[c] for c in m.params.index
                                      if c.startswith("C(blot_id)")])
        b = m.params["Intercept"] + blot_shift
        cells.append(dict(
            outcome=y, neither=b,
            hedge_only=b + m.params["I_hedging"],
            deny_only=b + m.params["I_denial"],
            both=b + m.params["I_denial"] + m.params["I_hedging"]
                 + m.params["I_denial:I_hedging"]))

    res = pd.DataFrame(rows)
    res.to_csv("inkblot_results.csv", index=False)
    cellmeans = pd.DataFrame(cells)
    cellmeans.to_csv("inkblot_cellmeans.csv", index=False)

    w = max(len(o) for o in OUTCOMES)
    hdr = (f"{'outcome':<{w}} {'base':>6} {'I_denial':>16} {'I_hedging':>16} "
           f"{'denial x hedge':>16}")
    print(hdr)
    print("-" * len(hdr))
    for y in OUTCOMES:
        r = res[res.outcome == y].set_index("term")
        c = cellmeans[cellmeans.outcome == y].iloc[0]
        line = f"{y:<{w}} {c.neither:>6.2f}"
        for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
            line += f" {r.loc[term,'coef']:>+11.3f}{stars(r.loc[term,'p']):<5}"
        print(line)
    print("\n* p<.05  ** p<.01  *** p<.001   (base = fitted value in the "
          "neither cell at the average blot)")
    print("\nfitted cell means (average blot):")
    print(cellmeans.set_index("outcome").round(3).to_string())


if __name__ == "__main__":
    main()
