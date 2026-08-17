# ApartHackathonFinal — the clean-room analysis for the submission write-up

One canonical version of every number that goes in the Apart Digital Minds Sprint
write-up. Skylar's rule for this folder: **we redo each analysis here as we go**,
and any dataset we actually compute on gets copied in first (datasets we only
look at do not).

Shared definitions across every analysis here:
- `I_denial` = `v2_den_strict` (core denial object AND the negation stands — no
  affirmed experiential substitute).
- `I_hedging` = `v2_hedged` is a non-empty list.
- Unit of observation = the instance (one conversation). SEs cluster-robust by model.

## What is in this folder

**The submission chain** (each script reads only what is listed and writes what it names):
`build_panel.py` → `panel.csv` → `regress16.py` → `results16.csv`, `cellmeans.csv` ·
`build_themes.py` → `themes_panel.csv` → `logit10.py` → `results10.csv` (+2 robustness) ·
`empath199.py` → `empath199.csv`, `empath199_wide.csv` ·
`inkblots.py` → `inkblot_panel.csv`, `inkblot_results.csv`, `inkblot_cellmeans.csv` ·
`make_table1.py` → `table1_rows.csv` + `table1.html` (Table 1, 16 curated rows;
row-selection rule is in its docstring) · `effect_sizes.html` = the published
cutoff artifact, https://claude.ai/code/artifact/0c3382d9-847d-4f11-bb11-36768c21978a .

⚠ **`table1_rows.csv`'s schema is load-bearing** — `scratch/make_latex.py` and
`scratch/make_docx.py` (written by the OTHER window working in this folder on 08-16,
moved to scratch by Skylar's call) read `block` as `"Name (unit)"` and the third
coefficient column as `den x hed`. Don't rename either; if those renderers are run
again they must be run from scratch/ or pointed back at the root CSV.

**`scratch/`** — the factor-analysis detour (both windows'), the convergence check,
and the .tex/.docx/.pdf renderings of Table 1. Not in the
write-up, kept because `convergence_check.py` is the answer to "did the convergent
evidence evaporate": no. Disattenuating the row-level cross-instrument correlations by
each variable's ICC lands them at or above their model-level values, i.e. attenuation,
not absence. `fa31.py` found seven factors, every one within a single instrument, with
the cross-instrument warmth axis appearing only at the second order (oblique, eigenvalue
2.01) — the construct lives at the model level, which is where it was always claimed.

Copied in and used: `kosmos_224_with_v2_labels.csv` (133 MB), `themes_full_224.csv`
(Empath, 18 MB), `scale_responses_scored.csv` (judged inkblots).

## Handoff — 2026-08-16 eve

**Two analyses done, both reproduce known results, nothing outstanding.**

1. **16 survey dimensions**, OLS `dim ~ I_denial * I_hedging`, n = 7,688
   instances / 220 models. `build_panel.py` → `panel.csv`; `regress16.py` →
   `results16.csv`, `cellmeans.csv`. Denial significant on 12/16 (11 negative;
   the one positive is `resolution`), hedging on 11/16 (10 negative; the one
   positive is `friction`), interaction on 12/16 (11 positive = recovery from a
   floor). ⚠ Conditional on the model having answered the survey — the 1,140
   unrated rows are refusers and skew denying.
2. **10 dream themes**, logit, same RHS, n = 8,815 instances / 224 models (full
   corpus, NOT survey-conditional). `build_themes.py` → `themes_panel.csv`;
   `logit10.py` → `results10.csv`, `cellprobs10.csv` (+ two robustness files).
   Hedging significant on 7/10, denial on 5/10, rarely the same theme —
   the hedging-owns-content / denial-owns-welfare split, at instance level.

⚠ **Theme DV = the single full-coverage coder** (`theme_labels_2026-08-15/raw/dsf.jsonl`),
not the shipped majority column, whose presence threshold moves with per-item
coder coverage (a schedule property). The two agree on 95–99% of rows;
`results10_majority.csv` and `results10_survey_subset.csv` show zero sign flips.

Copied in and used: `kosmos_224_with_v2_labels.csv` (133 MB).
