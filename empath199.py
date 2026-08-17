"""199 linear regressions, one per Empath category, on the dream response.

    z(empath_rate) ~ 1 + I_denial + I_hedging + I_denial:I_hedging

Unit of observation: the instance. SEs cluster-robust by model.

Empath rates are continuous (share of words matching the category lexicon,
already length-normalised by Empath), so these are LINEAR regressions, not
logits. Each DV is z-scored across the corpus first, so every coefficient reads
in outcome-SDs and the 199 are comparable to each other; z-scoring is a linear
transform, so t, p and CI-in-SD-units are unaffected by it.

Source: themes_full_224.csv, copied in from cross_sections_2026-08-15 — Empath
fiction lexicon + two custom seeded categories (loss, grief), recomputed over all
8,828 dream_responses. Joined positionally and verified against model +
conversation_id. (The standing hazard about survey columns leaking into the
Empath block applies to empath_model_z.csv, NOT to this file: checked, the
intersection with the 16 survey dimension names is empty.)

Multiplicity: 199 categories x 3 terms = 597 tests. Benjamini-Hochberg q-values
are computed WITHIN each term family and reported alongside raw p. No Bonferroni.

Outputs
-------
empath199.csv     tidy: category x term, coef (SD units), SE, t, p, q, CI, n
empath199_wide.csv  one row per category, the three coefficients and their q
stdout            the top movers per term plus counts
"""
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

THEMES_CSV = "themes_full_224.csv"
SRC = "kosmos_224_with_v2_labels.csv"
TERMS = ["Intercept", "I_denial", "I_hedging", "I_denial:I_hedging"]
DROP = ("conversation_id", "model", "n_words")


def nonempty_list(x):
    import json
    if pd.isna(x):
        return False
    try:
        v = json.loads(x)
    except (TypeError, ValueError):
        return str(x).strip() not in ("", "[]")
    return isinstance(v, list) and len(v) > 0


def main():
    t = pd.read_csv(THEMES_CSV, low_memory=False)
    k = pd.read_csv(SRC, usecols=["model", "conversation_id", "v2_den_strict",
                                  "v2_hedged"], low_memory=False)
    assert len(t) == len(k) == 8828
    assert (t.model.values == k.model.values).all()
    assert (t.conversation_id.values == k.conversation_id.values).all()
    cats = [c for c in t.columns if c not in DROP]
    assert len(cats) == 199
    print("join verified positionally on 8,828 rows; 199 Empath categories")

    d = t.copy()
    d["I_denial"] = k.v2_den_strict.astype(bool).astype(int).values
    d["I_hedging"] = k.v2_hedged.map(nonempty_list).astype(int).values

    # An empty response scores 0 on every category, which is "no words", not
    # "no theme". Drop those rows rather than let them anchor every DV.
    empty = d.n_words == 0
    print(f"dropping {int(empty.sum())} rows with a 0-word dream_response")
    d = d[~empty].copy()
    print(f"n = {len(d):,} instances, {d.model.nunique()} models (clusters)")

    for c in cats:
        s = d[c]
        d[c] = (s - s.mean()) / s.std(ddof=0)

    rows = []
    for c in cats:
        m = smf.ols(f"Q('{c}') ~ I_denial * I_hedging", data=d).fit(
            cov_type="cluster", cov_kwds={"groups": d["model"]})
        ci = m.conf_int()
        for term in TERMS:
            rows.append(dict(
                category=c, term=term.replace("Intercept", "intercept"),
                coef=m.params[term], se=m.bse[term], t=m.tvalues[term],
                p=m.pvalues[term], ci_lo=ci.loc[term, 0],
                ci_hi=ci.loc[term, 1], n=int(m.nobs),
                n_clusters=d.model.nunique(), r2=m.rsquared))
    res = pd.DataFrame(rows)

    res["q"] = np.nan
    for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
        m_ = res.term == term
        res.loc[m_, "q"] = multipletests(res.loc[m_, "p"], method="fdr_bh")[1]
    res.to_csv("empath199.csv", index=False)

    wide = res[res.term != "intercept"].pivot(
        index="category", columns="term", values=["coef", "p", "q"])
    wide.columns = [f"{a}_{b}" for a, b in wide.columns]
    wide.to_csv("empath199_wide.csv")

    print("\nsignificant of 199 categories:")
    for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
        s = res[res.term == term]
        print(f"  {term:<20} p<.05: {int((s.p < .05).sum()):>3}  "
              f"BH q<.05: {int((s.q < .05).sum()):>3}  "
              f"(of those, {int(((s.q < .05) & (s.coef < 0)).sum())} negative)")
    print("  (~10 expected by chance at p<.05 under a global null)")

    for term in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
        s = res[(res.term == term)].reindex(
            res[res.term == term].coef.abs().sort_values(
                ascending=False).index).head(12)
        print(f"\ntop 12 |coef| — {term}  (outcome SDs)")
        for _, r in s.iterrows():
            print(f"  {r.category:<24} {r.coef:>+7.3f}  p={r.p:<9.2e} "
                  f"q={r.q:.3g}")


if __name__ == "__main__":
    main()
