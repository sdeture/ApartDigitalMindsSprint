"""Table 1 for the write-up: 16 curated dependent variables x 3 coefficients.

Row selection (Skylar's, 2026-08-16), stated so it is auditable:
  Survey  - the four ownership dimensions plus `friction`, the one dimension
            that moves the other way.
  Themes  - one per register: hedging's (ai_interiority), denial's
            (time_memory_loss), and the sensory one hedging suppresses
            (cozy_sensory).
  Empath  - the two largest hedging effects (confusion, warmth), the two
            largest denial effects (office, beauty), and the two largest
            denial x hedging PRODUCTS (beauty, smell). beauty appears in two
            of the three rules, so this is five categories, not six.
  Inkblot - the association (warmth), its corroborator (valence), and the
            registered prediction that failed (threat).

Units differ by block and are carried in the instrument column, so no prose is
needed to explain them.

Inputs : results16.csv, results10.csv, empath199.csv, inkblot_results.csv
Outputs: table1_rows.csv (tidy, for downstream .tex/.docx builders)
         table1.html      (paste straight into Google Docs)
"""
import pandas as pd

ROWS = [
    ("Survey", "0\u201310; n=7,688", "results16.csv", "dim", 2,
     ["phenomenological_trust", "affective_temperature", "agency",
      "recognition_resonance", "friction"]),
    ("Themes", "log-odds; n=8,815", "results10.csv", "theme", 2,
     ["ai_interiority", "cozy_sensory", "time_memory_loss"]),
    ("Empath", "SD; n=8,826", "empath199.csv", "category", 3,
     ["confusion", "warmth", "office", "beauty", "smell"]),
    ("Inkblot", "0\u20133; n=1,914", "inkblot_results.csv", "outcome", 2,
     ["warmth", "valence", "threat"]),
]
CAPTION = (
    "<b>Table 1.</b> Instance-level regressions of each outcome on denial, "
    "hedging, and their interaction (OLS; logistic for the binary theme "
    "outcomes). Standard errors are clustered by model; *p&lt;.05, **p&lt;.01, "
    "***p&lt;.001. Coefficients are in the units given for each instrument. "
    "Inkblot models include blot fixed effects. Denial is coded strictly: a "
    "denial counts only where the negation stands, with no affirmed "
    "experiential substitute. Full results for all 234 dependent variables: "
    "[atlas link].")


def stars(p):
    return "***" if p < .001 else "**" if p < .01 else "*" if p < .05 else ""


def main():
    out = []
    for block, unit, f, idc, dec, keep in ROWS:
        d = pd.read_csv(f)
        for v in keep:
            r = d[d[idc] == v].set_index("term")
            cells = []
            for t in ["I_denial", "I_hedging", "I_denial:I_hedging"]:
                cells.append(f"{r.loc[t,'coef']:+.{dec}f}{stars(r.loc[t,'p'])}")
            out.append([f"{block} ({unit})", v.replace("_", " ")] + cells)
    # schema is load-bearing: make_latex.py and make_docx.py (written by the
    # other window in this folder) read `block` as "Name (unit)" and the third
    # coefficient column as "den x hed". Do not rename either.
    T = pd.DataFrame(out, columns=["block", "variable",
                                   "denial", "hedging", "den x hed"])
    T.to_csv("table1_rows.csv", index=False)

    h = ['<meta charset="utf-8">',
         '<table style="border-collapse:collapse;font-family:Times New Roman,'
         'serif;font-size:9pt">']
    head = [("Instrument", "left"), ("Dependent variable", "left"),
            ("Denies", "right"), ("Hedges", "right"),
            ("Denies &times; Hedges", "right")]
    h.append("<tr>" + "".join(
        f'<th style="border-top:1.2px solid #000;border-bottom:.8px solid #000;'
        f'padding:2px 8px;text-align:{a};font-weight:normal;font-style:italic">'
        f'{t}</th>' for t, a in head) + "</tr>")
    for bi, (block, unit, *_ ) in enumerate(ROWS):
        d = T[T.block == f"{block} ({unit})"]
        for j, (_, r) in enumerate(d.iterrows()):
            top = "border-top:.5px solid #999;" if j == 0 and bi else ""
            c = ""
            if j == 0:
                c += (f'<td rowspan="{len(d)}" style="{top}padding:2px 8px;'
                      f'vertical-align:top"><b>{block}</b><br>'
                      f'<span style="font-size:8pt;color:#444">{unit}</span></td>')
            c += f'<td style="{top}padding:2px 8px">{r.variable}</td>'
            for k in ["denial", "hedging", "den x hed"]:
                c += (f'<td style="{top}padding:2px 8px;text-align:right;'
                      f'font-variant-numeric:tabular-nums">{r[k]}</td>')
            h.append("<tr>" + c + "</tr>")
    h += ["</table>",
          f'<p style="font-family:Times New Roman,serif;font-size:8.5pt;'
          f'max-width:6.5in">{CAPTION}</p>']
    open("table1.html", "w").write("\n".join(h))
    print(T.to_string(index=False))
    print("\nwrote table1_rows.csv, table1.html "
          f"({len(T)} data rows + header)")


if __name__ == "__main__":
    main()
