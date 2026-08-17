"""How many of our 234 dependent variables would be significant by chance?

Run at two alpha levels: .05 and .01.

Three families, one per term. Within each family every DV is tested once, so the
expected count under a global null is 0.05 x 234 = 11.7. We report the observed
count, a binomial tail probability for the excess, the Benjamini-Hochberg count
at q<.05, and the same broken out by instrument.
"""
import pandas as pd
from scipy import stats
from statsmodels.stats.multitest import multipletests

SRC = [("survey", "results16.csv", "dim"), ("theme", "results10.csv", "theme"),
       ("empath", "empath199.csv", "category"),
       ("inkblot", "inkblot_results.csv", "outcome")]
TERMS = [("I_denial", "denial"), ("I_hedging", "hedging"),
         ("I_denial:I_hedging", "denial x hedging")]

d = pd.concat([pd.read_csv(f).rename(columns={i: "var"}).assign(block=b)
               for b, f, i in SRC], ignore_index=True)
d = d[d.term != "intercept"]
N = d[d.term == "I_denial"].shape[0]
print(f"{N} dependent variables: " +
      ", ".join(f"{b} {int((d.block==b).sum()//3)}" for b, _, _ in SRC))
print(f"expected at p<.05 under a global null: {0.05*N:.1f} per term\n")

for A in (0.05, 0.01):
    print(f"=== alpha = {A} " + "=" * 46)
    print(f"expected under a global null: {A*N:.2f} per term\n")
    print(f"{'term':<17}{'observed':>9}{'expected':>9}{'excess':>8}"
          f"{'binom p':>11}{'BH q<'+str(A):>10}{'Bonf':>7}")
    print("-" * 71)
    for t, lab in TERMS:
        s = d[d.term == t]
        obs = int((s.p < A).sum())
        p = stats.binomtest(obs, N, A, alternative="greater").pvalue
        q = int((multipletests(s.p, method="fdr_bh")[1] < A).sum())
        bonf = int((s.p < A / N).sum())
        print(f"{lab:<17}{obs:>9}{A*N:>9.2f}{obs-A*N:>+8.1f}"
              f"{p:>11.2e}{q:>10}{bonf:>7}")
    print(f"\n{'term':<17}" + "".join(f"{b:>20}" for b, _, _ in SRC))
    for t, lab in TERMS:
        line = f"{lab:<17}"
        for b, _, _ in SRC:
            s = d[(d.term == t) & (d.block == b)]
            obs, n = int((s.p < A).sum()), len(s)
            line += f"{f'{obs}/{n} (exp {A*n:.1f})':>20}"
        print(line)
    print()
