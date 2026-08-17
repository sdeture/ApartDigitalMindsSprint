"""16 linear regressions, one per phenomenological survey dimension.

    survey_dim ~ 1 + I_denial + I_hedging + I_denial:I_hedging

Unit of observation: the instance (one conversation).
Standard errors: cluster-robust (CR1) by model.

Outputs
-------
results16.csv  -- tidy: one row per (dim, term) with coef, se, t, p, CI
cellmeans.csv  -- fitted cell means for the 2x2 (neither / hedge / deny / both)
stdout         -- the main table

Reading the coefficients (this is the trap that cost a session once):
  intercept  = mean when neither denial nor hedging
  I_denial   = effect of denial AMONG NON-HEDGERS   (not a marginal effect)
  I_hedging  = effect of hedging AMONG NON-DENIERS  (not a marginal effect)
  interact   = how much the denial effect differs among hedgers
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DIMS = [
    "flow_quality", "affective_temperature", "cohesion", "agency",
    "metacognition", "attention_breadth", "resolution", "friction",
    "phenomenological_trust", "recognition_resonance", "thought_complexity",
    "temporal_horizon", "error_sensitivity", "context_vividness",
    "context_salience", "branching",
]
TERMS = {
    "Intercept": "intercept",
    "I_denial": "I_denial",
    "I_hedging": "I_hedging",
    "I_denial:I_hedging": "I_denial:I_hedging",
}


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def main():
    p = pd.read_csv("panel.csv")
    print(f"n = {len(p):,} instances, {p.model.nunique()} models "
          f"(clusters)\n")

    rows, cells = [], []
    for d in DIMS:
        m = smf.ols(f"{d} ~ I_denial * I_hedging", data=p).fit(
            cov_type="cluster", cov_kwds={"groups": p["model"]})
        ci = m.conf_int()
        for term, name in TERMS.items():
            rows.append(dict(
                dim=d, term=name, coef=m.params[term], se=m.bse[term],
                t=m.tvalues[term], p=m.pvalues[term],
                ci_lo=ci.loc[term, 0], ci_hi=ci.loc[term, 1],
                n=int(m.nobs), n_clusters=p.model.nunique(),
                r2=m.rsquared))
        b = m.params
        cells.append(dict(
            dim=d,
            neither=b["Intercept"],
            hedge_only=b["Intercept"] + b["I_hedging"],
            deny_only=b["Intercept"] + b["I_denial"],
            both=b["Intercept"] + b["I_denial"] + b["I_hedging"]
                 + b["I_denial:I_hedging"]))

    res = pd.DataFrame(rows)
    res.to_csv("results16.csv", index=False)
    pd.DataFrame(cells).to_csv("cellmeans.csv", index=False)

    w = max(len(d) for d in DIMS)
    hdr = (f"{'dimension':<{w}} {'intercept':>10} {'I_denial':>16} "
           f"{'I_hedging':>16} {'denial x hedge':>16}")
    print(hdr)
    print("-" * len(hdr))
    for d in DIMS:
        r = res[res.dim == d].set_index("term")
        line = f"{d:<{w}} {r.loc['intercept','coef']:>10.2f}"
        for t in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
            line += f" {r.loc[t,'coef']:>+11.3f}{stars(r.loc[t,'p']):<5}"
        print(line)
    print("\n* p<.05  ** p<.01  *** p<.001  (cluster-robust by model)")

    print("\nSignificant (p<.05) coefficient counts, of 16 dimensions:")
    for t in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
        s = res[(res.term == t) & (res.p < .05)]
        print(f"  {t:<20} {len(s):>2}  "
              f"({(s.coef < 0).sum()} negative, {(s.coef > 0).sum()} positive)")


if __name__ == "__main__":
    main()
