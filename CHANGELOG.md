# Changelog

## Version 2 (2026-10-26)

**Data change**
- D.C.'s D4 is now 70 (the PD half alone) instead of 0. D4's rules forbid defaulting D.C. to zero; no substitute technology source was logged with points, so the Digital States half is omitted and D4 = pd_points. This is a renormalization: D.C.'s D4 rests on one component, every other state's on two.
  - D.C. composite 40.3 -> 50.8, tier Critical -> Emerging, rank 49 -> 35. States ranked 35th to 48th in version 1 each moved down one place.
  - Tier counts: Critical 10 -> 9, Emerging 10 -> 11. Tier cut points were not re-derived.
  - Jurisdictions carrying a 0: 9 -> 8. D.C. removed from the Question 01 table.

**Figures that changed because the robustness run was repeated on the new data**
- Spearman, published vs equal weights: 0.77 -> 0.75.
- Median share of draws in the published tier: 90% -> 88%; states in tier in at least 90% of draws: 26 -> 25.
- Weight x SD for D4: 2.7 -> 2.2 (order is now D2 6.9, D1 4.4, D3 2.6, D4 2.2, D5 1.5).
- Largest correlation (D4 with D5): 0.37 -> 0.32.
- South Dakota's rank range: 17th-36th -> 17th-37th.

**Consistency checks run before release**
- Before the D.C. change, `robustness_results.json`, `alternatives.csv` and `docs/psai_phase2_scores.csv` were each regenerated from the workbook and matched the files in the repo exactly (0 differences). After it, all were regenerated from the same workbook in one pass.
- Florida is 43.1 in the workbook, scores CSV, alternatives, robustness and dashboard. No file in the repo contains 45.1.
- D2 coverage (turnover 39, vacancy 19, tenure 28 of 51) matches `dimension2_scores.csv`, `methods_spec.csv` and the Dossier.

**Other**
- Workbook now stores computed composite values (it previously opened with a blank Weighted Average column until recalculated) and its Ranked column follows the corrected scores.
- Jurisdiction name unified to "District of Columbia" in `dimension2_scores.csv`, `d3_scores.csv`, `polls.csv`, `d5_evidence.csv`.
- Methods Spec moved to directly after "Setting the Foundation" in the Dossier.
- Questions 02 to 06 now offer a choice of answers, as Question 01 does.
- Added `composite/spot_check_protocol.md` (provisional pass rule) and `composite/regenerate.py`.

**Not changed**
- D3 sentiment articles are not in the repo and not recoverable from the files available here; D1 `score.py` and `d1_scores.xlsx` are still missing; the CPM roster gap is still open; no human error rate has been measured.
