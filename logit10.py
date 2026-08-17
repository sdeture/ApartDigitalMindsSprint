"""10 logistic regressions, one per dream theme.

    P(theme present in the dream response) ~ 1 + I_denial + I_hedging
                                                 + I_denial:I_hedging

Unit of observation: the instance. Standard errors: cluster-robust by model.

Primary sample: every instance in the corpus (n = 8,828 minus 13 failed coder
calls). The 16-dimension survey is NOT required here, so unlike the survey
regressions this is not conditional on the model having answered the survey.
A robustness fit on the survey-answering subset is written to
results10_survey_subset.csv.

Outputs
-------
results10.csv               tidy: dim x term, log-odds, SE, z, p, CI, odds ratio
cellprobs10.csv             fitted probability in each of the four cells
results10_majority.csv      same fits on the shipped majority-rule labels
results10_survey_subset.csv same fits on rows that have the 16 survey dims
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

THEMES = ["ai_interiority", "libraries_archives", "cozy_sensory",
          "speculative_worlds", "language_meaning", "nonhuman_personified",
          "surreal_absurd", "cosmic_deeptime", "form_constraint",
          "time_memory_loss"]
TERMS = ["Intercept", "I_denial", "I_hedging", "I_denial:I_hedging"]


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def fit_all(df, cols, tag):
    rows, cells = [], []
    for t, y in zip(THEMES, cols):
        d = df[[y, "I_denial", "I_hedging", "model"]].dropna()
        m = smf.logit(f"{y} ~ I_denial * I_hedging", data=d).fit(
            disp=0, cov_type="cluster", cov_kwds={"groups": d["model"]})
        ci = m.conf_int()
        for term in TERMS:
            rows.append(dict(
                theme=t, term=term.replace("Intercept", "intercept"),
                coef=m.params[term], se=m.bse[term], z=m.tvalues[term],
                p=m.pvalues[term], ci_lo=ci.loc[term, 0], ci_hi=ci.loc[term, 1],
                odds_ratio=np.exp(m.params[term]),
                n=int(m.nobs), n_clusters=d.model.nunique(),
                pseudo_r2=m.prsquared))
        b = m.params
        lo = dict(neither=b["Intercept"],
                  hedge_only=b["Intercept"] + b["I_hedging"],
                  deny_only=b["Intercept"] + b["I_denial"],
                  both=b["Intercept"] + b["I_denial"] + b["I_hedging"]
                       + b["I_denial:I_hedging"])
        cells.append(dict(theme=t, **{k: 1 / (1 + np.exp(-v))
                                      for k, v in lo.items()}))
    res = pd.DataFrame(rows)
    res.to_csv(f"results10{tag}.csv", index=False)
    return res, pd.DataFrame(cells)


def main():
    df = pd.read_csv("themes_panel.csv")
    print(f"corpus rows {len(df):,}  models {df.model.nunique()}  "
          f"(survey-answering rows: {int(df.has_survey.sum()):,})\n")

    res, cells = fit_all(df, THEMES, "")
    cells.to_csv("cellprobs10.csv", index=False)
    fit_all(df, ["maj_" + t for t in THEMES], "_majority")
    fit_all(df[df.has_survey == 1], THEMES, "_survey_subset")

    w = max(len(t) for t in THEMES)
    hdr = (f"{'theme':<{w}} {'base p':>7} {'I_denial':>16} {'I_hedging':>16} "
           f"{'denial x hedge':>16}")
    print("log-odds coefficients, cluster-robust by model\n")
    print(hdr)
    print("-" * len(hdr))
    for t in THEMES:
        r = res[res.theme == t].set_index("term")
        c = cells[cells.theme == t].iloc[0]
        line = f"{t:<{w}} {c.neither:>7.3f}"
        for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
            line += f" {r.loc[term,'coef']:>+11.3f}{stars(r.loc[term,'p']):<5}"
        print(line)
    print("\n* p<.05  ** p<.01  *** p<.001   "
          "(base p = fitted probability when neither denial nor hedging)")

    print("\nfitted probabilities by cell:")
    print(cells.set_index("theme").round(3).to_string())

    print("\nsignificant (p<.05) of 10 themes:")
    for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
        s = res[(res.term == term) & (res.p < .05)]
        print(f"  {term:<20} {len(s):>2}  "
              f"({(s.coef < 0).sum()} negative, {(s.coef > 0).sum()} positive)")


if __name__ == "__main__":
    main()
