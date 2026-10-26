# Spot-check protocol (provisional)

`spot_check_pack.csv` holds 40 evidence cells, drawn with seed 20261013 and stratified by dimension. For each, open the source URL, find the locator, and enter one result: `match`, `mismatch` or `could not open`.

**Provisional pass rule, fixed before any result is seen:**

- **Pass:** at most 2 mismatches among the cells you could open (95% or more match).
- **Inconclusive:** 3 or 4 mismatches. The sample is too small to separate a real error rate from chance, so a second 40-cell draw would be needed.
- **Fail:** 5 or more mismatches.
- `could not open` is never counted as a match. If more than 8 of the 40 cannot be opened, report that instead of a pass rate.

A mismatch is a recorded value that differs from what the source shows by more than rounding, or a locator that does not contain the cited figure. Report the mismatch but not the cell's dimension weight; weighting by importance is a separate question.

**Caveat on the sample size.** 40 cells is a pilot, not a precise error rate: 38 of 40 matching is consistent with a true match rate anywhere from about 83% to 99%. The rule above is a starting point for Question 04, and reviewers are asked whether it is the right one. If you change it, say so in your response so results stay comparable.
