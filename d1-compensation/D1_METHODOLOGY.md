# How Dimension 1 Was Built

**Dimension 1 (D1) of the Public Service Appreciation Index asks one question: does working for this state government pay well enough to attract and keep good people?**

It covers all 50 states plus Washington, D.C. — 51 jurisdictions. It carries 30% of a state's total PSAI score, more than any other dimension. Errors here move a state's final position more than errors anywhere else.

This document explains how it was built, what was decided along the way, and where it falls short. It is written for someone who has never worked with government wage data. Every technical term is explained the first time it appears.

---

## 1. What went wrong before

The previous version of D1 was audited in August 2026. The verdict was **REBUILD** — not "fix this," but "start over." The audit examined 30 of the 51 states in full before stopping, and found problems that were properties of the design rather than mistakes in individual files.

Here is what it found, plainly.

**The pay numbers came from commercial websites, not government data.** Twelve states took their salary benchmark from GovSalaries, a company that scrapes payroll records and sells access. Massachusetts used OpenGovPay and a data-visualization blog called Visual Capitalist. Montana used OpenPayrolls. Illinois used a figure from the *St. Louis Post-Dispatch*. Kentucky used Indeed, CareerExplorer, and Classet — job-advertising boards. Arizona used an advocacy think tank. Of 30 states, only 12 used a federal statistical source at all, and 2 cited no source whatsoever.

**Five states worked their numbers backwards from the answer.** California's workbook records a private-sector wage of $108,672 with the note *"Estimated, Derived from median ratio (86.5%)"* — and then records the ratio as *"Calculated: Public median / private avg."* Each number was computed from the other. The same file contains *"Tech investment per employee $400, Estimated, Derived so that Tech score = 80."* Minnesota manufactured all ten of its state wages by applying an assumed pay-gap factor to all-industry wages; the resulting ratios take only three values (95.0, 100.0, 105.0) because they *are* the assumption. Maine approximated its private median "at $76k reflecting 15% higher than state salary," then divided by it. Michigan's source field for a $70,000 private median contains the single word `estimated`. New York recorded $65,000 and $55,000, both marked "Approximate," both round to the nearest $5,000, with no agency and no year.

**States were measured in different years and compared as though they weren't.** Maryland's salary figure was from 2022. Kentucky's was from a "Social Worker Salary by State 2026" projection. That is a four-year spread inside a single like-for-like comparison. Eleven states carried mixed years *inside their own single ratio* — Montana compared a 2023 public average to an FY2025 private average; Arizona compared an FY2024 salary to a June 2025 wage.

**Nineteen states were published as scoring zero while their own files held real scores.** The master index marked them "Not Assessed" with a D1 of 0. The auditor opened 10 of those 19 workbooks. All 10 contained a fully computed, non-zero score: Kansas 89.4, Missouri 85.5, Maine 84.4, Connecticut 84.0, Iowa 81.0, Idaho 88.0, Alaska 77.3, Hawaii 77.6, Montana 77.3. Those zeros were data loss, not measurement.

**And the scoring rules differed by state.** Kansas, Maine, and Missouri each multiplied by 100 where every other state multiplied by 70 — worth about 10 D1 points each, purely from the choice of multiplier. Hawaii used three formulas found nowhere else. Six different benefits rubrics were in use, with pension ceilings ranging from 25 to 40 points.

The result: **13.3% of cells could be traced to their stated source and confirmed. Zero of thirty salary figures could.** And the effect ran in a diagnosable direction — North Carolina, the one state that built its benchmark rigorously, ranked 16 places *lower* than it would have with D1 removed. The dimension rewarded laxity and punished rigour.

That is the failure this rebuild exists to prevent. Everything below follows from it.

---

## 2. Three rules

The rebuild follows three rules. Each one closes a specific door that the old version left open.

**Rule 1 — every number traces to a file that was downloaded and read.** Not a web page, not a search result, not a recollection. Six source files were downloaded and stored, each with a cryptographic fingerprint (a `sha256` — a long code that changes if even one byte of the file changes, so anyone can confirm they have the identical file). Each of the 255 recorded values names its file *and* the exact spot inside it. Wisconsin's pay figure records `sheet 'state_industry_M2024'!M44210`. That is a cell address. You can open the file and look.

This prevents GovSalaries. It also prevents "estimated."

**Rule 2 — three possible answers, not two.** Every value is recorded as one of:

- `FOUND` — we opened the file and read the value.
- `CONFIRMED_ABSENT` — it is genuinely zero or does not apply, and we can say why.
- `COULDNT_CHECK` — we could not find it.

The third category is the point. **A missing value is never scored as zero.** It is removed from the calculation, and the state's score is computed from the portion we could measure. Without this category, "we don't know" quietly becomes a number — which is exactly how 19 states ended up published at zero.

**Rule 3 — scores are generated from the evidence file, never typed in.** A single script ([score.py](d1-build/work/score.py)) reads the evidence file and produces every score. No score exists anywhere that a human entered by hand. This is what makes the four-incompatible-normalization-rules problem structurally impossible: there is one rule, in one place, applied to all 51.

---

## 3. Why every state uses the same source

All 51 figures for a given indicator come from the *same national file*. Wisconsin's pay figure and Florida's pay figure are two rows in one spreadsheet published by the Bureau of Labor Statistics — the federal agency that measures employment and wages. Not two files. One file, two rows.

This is enforced by how collection works, not by asking nicely. The build downloads six files, then looks up 51 rows in them. There is no step at which a state could get its own source, because there is no per-state search.

The old version searched state by state. That is the whole explanation for how 51 different sources got in. When you search for "Kentucky state employee salary," you find whatever ranks highest — and what ranks highest is a job board. Nobody chose Indeed as a statistical source. The method chose it.

---

## 4. Why 2024, and the two exceptions

**Every indicator uses 2024.** Not the newest data available — 2024.

The binding constraint was cost of living. The Bureau of Economic Analysis publishes *Regional Price Parities* — a measure of what the same basket of goods costs in each state, with the national average set at 100. Mississippi's 2024 value is 86.95, meaning things cost about 13% less than the national average. Hawaii's is near the top. The 2025 figures were not yet published when this was built.

So the choice was: use 2024 everywhere, or use 2025 for some indicators and 2024 for cost of living. **Having everything on one year matters more than having one thing be newer.** A state's score should not depend on which of its inputs happened to have a fresher release. That is precisely the failure that produced a four-year spread in the old version.

Two exceptions are documented.

**Retirement data is from late 2025.** The National Association of State Retirement Administrators (NASRA) — the professional body for state pension systems — publishes a single current file at a fixed web address and overwrites it. There is no 2024 edition reachable from the publisher. The alternative was to pull an archived copy from a third-party web archive, which was declined: an archive copy is not a publisher copy, and the whole point of Rule 1 is that the file came from the source. So the current edition was used, applied identically to all 51.

**Rent data is HUD's fiscal year 2025.** The Department of Housing and Urban Development publishes *Fair Market Rents* — its estimate of what a modest apartment costs in each local area. The FY2025 file is the set of rents published during calendar 2024. It is the correct 2024-anchored rent measure, not a deviation at all.

**Why applying an exception to all 51 equally doesn't break the comparison.** The anchor-year rule exists to stop reference years drifting *between* states. If Maryland is measured in 2022 and Kentucky in 2026, the comparison between them is corrupted. If every state's retirement data is from October 2025, no state is advantaged over another. What is lost is the dimension's alignment to 2024 — a real cost, disclosed — not the fairness of the state-to-state comparison.

---

## 5. The five indicators

Two ways of turning a dollar figure into a 0–100 score are used, and it is worth understanding the main one first.

**Percentile ranking.** We line all 51 states up from lowest to highest and score each one by where it falls in the line. The lowest scores 0, the highest scores 100, and everyone else falls in between. A state scoring 74 beats about 74% of the others.

**Why ranking rather than stretching scores between the highest and lowest?** The alternative — sometimes called min-max normalization — would set the top state at 100, the bottom at 0, and place everyone else proportionally by dollar distance. That method is wrecked by outliers. If one state pays far more than the rest, it takes the 100 and squashes the other 50 into a narrow band near the bottom, where a $5,000 difference becomes a two-point difference. Ranking is immune to that: it uses order, not distance.

The cost is real and worth stating. **Percentile ranking measures order, not distance.** Two states $200 apart get scores as far apart as two states $20,000 apart would. A state scoring 60 is not "twice as good" as one scoring 30. It ranks higher. That is all.

### I1 — Pay level (weight 32%)

**What it measures:** what a state government actually pays its employees on average, adjusted for how expensive that state is to live in.

**Source:** BLS Occupational Employment and Wage Statistics Research Estimates, May 2024, industry code 999200 — "State Government, excluding Schools and Hospitals." Universities and hospitals are excluded because states differ enormously in whether they run them; including them would measure how a state is organized rather than what it pays.

**Scoring:** take the published average annual wage, divide by the state's cost-of-living index, percentile-rank the 51 results.

**Why the source changed mid-build.** The original plan used the Census Bureau's Annual Survey of Public Employment & Payroll (ASPEP) — a survey of what governments spend on payroll and how many people they employ. It was downloaded and inspected. **D.C. is not in it as a state government.** The Census classifies D.C. as a municipal government; the file contains 50 state-government records, not 51. Using ASPEP would have made I1 unmeasurable for D.C. — on the heaviest indicator — leaving D.C. with too little coverage to publish a score at all.

The OEWS research file has all 51, including D.C., with no suppressed cells and good reliability on every one. It was substituted. The consequence was accepted openly: the original plan computed pay as payroll divided by headcount over a fixed basket of seven government functions (corrections, highways, public welfare, and so on). The OEWS file publishes an average wage directly and cannot isolate those seven functions. **That basket was retired.** The exclusion of schools and hospitals matches what the basket was for; the named functions do not survive.

### I2 — Market position (weight 22%)

**What it measures:** how state government pay compares to what employers in that same state pay generally.

**Source:** BLS Quarterly Census of Employment and Wages (QCEW) — a near-complete count of wages drawn from unemployment-insurance records, not a survey. Private-sector average annual pay, 2024. Wisconsin: $63,799.

**Scoring:** divide I1's figure by this one, percentile-rank the ratio. Wisconsin's ratio is 1.166 — government pays about 17% above the private average — scoring 92.

**Why not compare matching jobs?** The obvious approach is to compare a state accountant to a private accountant. That was deliberately declined. Job titles that sound identical carry different duties, seniority, and education requirements across the two sectors, and BLS itself cautions against directly comparing state government and private-industry compensation without controlling for occupational mix. The old version made that comparison anyway, in 20 of 30 states, and in several of them the "private" comparator actually included government workers. It was one of the three findings that forced REBUILD.

What this indicator asks instead has an available answer: *in this state's labour market, how does government pay stack up?* That is the comparison a person actually faces.

One consequence to understand: a state with a very high-wage private economy scores low here even if it pays government workers well. **Washington, D.C. pays the fourth-highest government wages in the country and scores 2 out of 100 on this indicator**, because it sits against the highest private wages in the country.

Note this indicator is deliberately *not* cost-of-living adjusted. Both figures come from inside the same state, so cost of living is already on both sides. Adjusting would count it twice.

### I3 — Entry-level pay against rent (weight 20%)

**What it measures:** whether someone starting an entry-level state job can afford a one-bedroom apartment.

**Source:** BLS wages for the lowest-paid tenth of workers in three common entry-level government roles — eligibility interviewers, correctional officers, and tax examiners — against HUD's one-bedroom Fair Market Rent.

**Scoring:** a fixed bar, not a ranking. The standard affordability benchmark is that housing should cost no more than 30% of income. Wisconsin's population-weighted one-bedroom rent is $954.86/month, or $11,458 a year; at 30% that requires an income of $38,194. Wisconsin's cost-adjusted entry wage is $52,297. It clears the bar comfortably and scores 100 (capped).

**Why a fixed bar rather than a ranking?** "Can someone afford rent on this" is a yes-or-no question with a real answer that does not depend on other states. If every state failed, ranking would still hand a score of 100 to whichever failed least — rewarding a state for being least bad at something all of them are bad at. That would be misleading in a way the fixed bar cannot be.

### I4 — Retirement (weight 16%)

**What it measures:** three simple facts about the retirement benefit a new state employee gets.

**Source:** NASRA's Contributions Brief and its plan-type overview.

**Scoring:** points, not judgment.
- Social Security coverage: covered 40, partial 20, not covered 0.
- Plan type: defined benefit (a guaranteed pension) 40; hybrid 30; cash balance 30; choice 25; defined contribution (the employee carries the investment risk) 15.
- Employee contribution: ≤4% of salary earns 20 points, ≤7% earns 15, ≤10% earns 10, above that 5.

Wisconsin: covered (40) + defined benefit (40) + 6.95% contribution (15) = **95**.

**Why three facts rather than a judgment of pension quality?** Judging how good a pension is requires assumptions about vesting, cost-of-living adjustments, mortality, and investment returns — every one of them a choice, and every choice a place where a state could be favoured. The old version tried this and produced six different rubrics with pension ceilings from 25 to 40, in which Delaware (no automatic pension COLA) scored 90 and Kansas (also no COLA) scored 75. Three recorded facts can be checked by a reader. A quality judgment cannot.

### I5 — Real trajectory (weight 10%)

**What it measures:** whether state government pay kept up with inflation over five years.

**Source:** QCEW state-government average weekly wage for 2019 and 2024, adjusted using the Consumer Price Index (the standard federal measure of price change: 255.657 in 2019, 313.689 in 2024).

**Scoring:** Wisconsin's 2019 weekly wage of $1,170 is worth $1,435.58 in 2024 money. Actual 2024 wage: $1,522. That is real growth of 6.0%, percentile-ranked at 80.

The 2019 reference year is not an anchor violation — a five-year change requires two years by definition. This carries the lightest weight because a single five-year window can reflect one unusual budget cycle rather than a durable pattern.

---

## 6. What D1 does not measure

**Health insurance and paid leave are excluded.** Both are real parts of compensation. Both are missing for the same reason: no source publishes them for all 51 jurisdictions in a comparable form.

The best federal data on employer benefit costs is the BLS Employer Costs for Employee Compensation series. It reports **by multi-state region only** — no state breakout exists. The related MEPS-IC public-sector tables are census-division only. The one study that covers states individually, the Segal State Employee Health Benefits Study, **covers the 50 states and cannot support a Washington, D.C. value**, and sits behind a paywall.

The alternative was to gather 51 separate state HR websites. The old version did exactly that, and produced 51 numbers that looked comparable and were not — 67% of them undated.

So D1 measures pay and retirement. It does not measure total benefits. **A state with excellent health coverage and mediocre pay scores lower here than its full package deserves.** That is a disclosed gap, not an oversight.

---

## 7. The judgment calls

Decisions came up mid-collection. Each is recorded in [d1_source_registry.csv](d1-build/out/d1_source_registry.csv). What follows is each one, in the order it happened, and — most importantly — whether it was made before or after seeing which states it would affect.

**The standard.** A rule can be *corrected* when the fix follows from rules already set. A rule cannot be *changed* when the fix requires a new judgment made while looking at the results.

Why this distinction matters: changing rules after seeing who they help is exactly what broke the old version. Kansas, Maine, and Missouri each gained about 10 points from a multiplier no other state used. Nobody has to have intended that for it to be fatal — once a rule can move after the results are visible, no result can be trusted.

**Decision 1 — the source switch (I1).** ASPEP has no state-government record for D.C. Decided to substitute the OEWS research file for all 51. **Made before extraction, from a coverage test that named no state's score.** The trigger was a structural property of the file, not a look at anyone's number.

**Decision 4 — adding a plan-type source (I4).** The Contributions Brief has no plan-type field; it names a plan type in prose only when the plan is unusual. Under a strict source rule, every ordinary defined-benefit state would have been `COULDNT_CHECK` on plan type and I4 would have been nearly empty. A second NASRA document giving plan type for all 51 was added. **A standing rule was recorded with it:** a source not in the original plan may be proposed only if it is (a) the same publisher, (b) the same vintage, and (c) a primary source — and must always be flagged, never used silently. Everything else remains `COULDNT_CHECK`. This is a narrow patch for a gap in the plan, not permission to expand the source list.

**Decision 3 — rent weighting (I3).** A state has many local rent figures — Wisconsin has 72 rows, Mississippi 82. They must be combined into one. Decided: weight each row by population, using HUD's own `pop2022` field, which sits on all 4,680 rows at exactly the rent geography. The alternative was to join to Census county population estimates — declined because **9 county codes don't match on each side, and the mismatch is entirely Connecticut**: Census now uses 9 planning regions where HUD still uses 8 legacy counties. That join would have broken Connecticut. HUD's own field reaches all 1,605 sub-county town rows and has no join at all. Applied to every jurisdiction with no fallback. Disclosed in every I3 row: 2022 population weights are applied to a FY2025 rent index.

**Decision 5 — the cash-balance category (I4).** Cash-balance plans (where contributions earn an employer-guaranteed credit) fit none of the existing categories. Added at 30 points, equal to hybrid, because they pool investment risk with a guaranteed credit and sit structurally between a pension and a 401(k). **Added before any cash-balance jurisdiction was extracted and applied blind to all 51.** Four turned out to carry it: Kansas, Kentucky, Nebraska, and Texas. Texas was not among the three anticipated — its 2024 tier is cash balance for employees hired after 31 August 2022 — and it was scored under the same rule without adjustment. The 30 was never revisited after seeing its effect.

**Decision 6 — the first Social Security refinement.** The original rule mapped any wording of the form "covered, except X" to PARTIAL. That understated coverage where the exception fell on a class already excluded from the general-employee population. Restated: an exception affecting only already-excluded classes does not reduce coverage. **This follows from the scope rule already set — a correction, not a new judgment** — and was implemented as a mechanical classifier containing no state names, then re-run blind across all 51.

The re-run is why it matters. Five of six expected states moved (Kansas, Minnesota, New Hampshire, Pennsylvania, Rhode Island). Oregon correctly did not move — its exception is employer-elected and names no class. And **Kentucky moved the wrong way**, from PARTIAL to NOT_COVERED, because its exception names university members. That unpredicted move triggered a stop.

**Decision 8 — the second Social Security refinement.** Root cause of the Kentucky move: the exclusion list served two different purposes and the rule was reading both. Some entries name classes genuinely outside the general-employee population (public safety, police, fire, state patrol, judiciary, teachers). Others name classes who *are* general employees but whose separately-published rates must be kept out of the general rate — university members are one. The Social Security rule should inherit only the first kind. University members were dropped from its list.

An honest note was attached rather than a silent decision: corrections officers, sheriffs, law enforcement, custodial staff, and legislators are arguably first-kind entries but were not adjudicated, so they were **not** added. None of those words appears in any of the 51 raw source strings, so the ambiguity is moot for this build — and it is flagged for a future one rather than quietly resolved.

Re-run blind across all 51: **exactly one jurisdiction moved, Kentucky, back to PARTIAL, as predicted. No unpredicted moves.** The five from the first refinement were undisturbed and Oregon stayed put. That is what confirms the fix reached only as far as intended.

**Decision 7 — two contribution rates.** Oregon stands at 5.25%, excluding a contingent 0.75% component, consistent with how a risk-sharing component was already treated for Connecticut. Michigan stands at 0.0%, the rate for an employee who takes no action, consistent with how an opt-out-able default was already read for Georgia. **Changing either would break a precedent already applied to another state — the exact inconsistency this build exists to prevent.** Both alternative readings remain documented in the row notes.

---

## 8. How to read the data file

[d1_evidence.csv](d1-build/out/d1_evidence.csv) is a plain text file you can open in a spreadsheet. It has **255 rows: 51 jurisdictions × 5 indicators.** One row per measured value. Nothing else exists.

The columns that matter:

| Column | What it's for |
|---|---|
| `jurisdiction`, `indicator` | which cell of the 51 × 5 grid this is |
| `raw_value`, `raw_unit` | the number as the source publishes it, and what unit it's in |
| `reference_year` | the year the value refers to |
| `source_id`, `source_url`, `source_file` | which downloaded file it came from |
| `locator` | **where inside that file** — sheet and cell, or archive member, row, and column |
| `status` | `FOUND` / `CONFIRMED_ABSENT` / `COULDNT_CHECK` |
| `verification_method`, `verification_result` | how it was checked and whether it passed |
| `notes` | everything else, including every disclosure that applies to that value |

The `locator` column is what makes this checkable. It is not a citation; it is an address.

### A worked example: Wisconsin's pay level

Open the evidence file and find the row `Wisconsin, I1_PAY_LEVEL`. It says:

- `raw_value` = **74380**, `raw_unit` = USD_annual, `reference_year` = 2024
- `source_file` = `oes_research_2024_sec_99.xlsx`
- `locator` = `sheet 'state_industry_M2024'!M44210 (row 44210: AREA_TITLE='Wisconsin', NAICS=999200, O_GROUP=total, column A_MEAN)`

Open that file in `sources/`. Go to that sheet, row 44210. The row says Wisconsin, industry 999200 (State Government, excluding Schools and Hospitals), all occupations. Column M is `A_MEAN` — average annual wage. It reads **74380**. That is the entire chain.

Now the arithmetic, all of it in [score.py](d1-build/work/score.py):

1. **Adjust for cost of living.** Wisconsin's BEA price parity is 94.095 — things cost about 6% less than the national average. $74,380 ÷ 0.94095 = **$79,047.77** in national-average dollars.
2. **Rank it.** All 51 states get the same treatment. Wisconsin's adjusted figure places it 38th from the bottom of 51. Score = 37 ÷ 50 × 100 = **74.0**.

Compare Mississippi, the same two steps: $48,980 ÷ 0.86953 = $56,329 — lowest but one, score **2.0**. And Florida: $57,660 ÷ 1.03414 = $55,756 — lowest of all 51, score **0.0**. A score of 0 here does not mean "no data." It means last place. Missing data is never a zero; it is a blank.

Wisconsin's five scores are 74, 92, 100, 95, 80. Weighted at 32/22/20/16/10 percent, that gives **87.1** — first of 51.

### How the workbook is built from it

[d1_scores.xlsx](d1-build/out/d1_scores.xlsx) has six tabs: README, Evidence, Scores, Final, Flags, Coverage. Every one is generated from the evidence CSV by script. The Evidence tab *is* the CSV. The Scores tab is what `score.py` produces from it. The Final tab holds the weighted calculation with editable weights in the top row — change one and every score recalculates.

**No score exists anywhere that does not come from a row in the evidence file.** If a row's status is not `FOUND`, that indicator is excluded from the state's calculation and the remaining weights are rescaled. There is no hand-entry step at which a number could enter without a locator behind it.

*(One practical note: the Final tab uses live spreadsheet formulas, so it reads as blank to scripts until the file has been opened and saved in Excel. The Scores and Coverage tabs hold plain values and can be read by anything.)*

---

## 9. How the numbers were checked — and what that proves

Four checks were run.

**Every value was extracted twice, independently.** The file was re-opened, re-parsed, and the value re-read, with key fields re-asserted. **246 of 246 agreed. No disagreements.**

**Every value was checked against a plausible range.** Pay between $30,000 and $150,000; private wages $30,000–$130,000; rents $500–$3,500; contribution rates 0–20%. **All 246 passed.** The observed range for state-government pay runs from Mississippi at $48,980 to California at $95,570 — comfortably inside.

**Units were checked.** The old version had a live 100× hazard: Alaska recorded a price index as `1.017` while 26 states used `101.7`, into a formula that divides by 100. The new BEA file was checked at the source: the United States row reads exactly 100.000 and all 51 values fall between 86.937 and 110.720. That specific error is not present. Each row also records its unit explicitly, including where the unit sits outside the expected list — the retirement rate is recorded as `percent_of_salary` and not converted.

**A fabrication check, six parts.** Every `FOUND` row names a real file in `sources/`. Every locator is specific enough to re-find the value. No URL appears that isn't in the registry. Duplicate values across states were listed and explained — there are none in I1, I2, I3, or I5; the retirement rates that repeat (3.0% for Florida and Indiana, 6.0% for Alabama and Connecticut) are separately stated in the source for different plans. No value is computed from another value in the same indicator. **Zero rows carry the words estimated, approximate, assumed, proxy, derived, or TBD.** All six passed.

**Result: 246 of 255 values found and verified. Nine gaps, all in the retirement indicator** — Arkansas, California, D.C., Hawaii, Massachusetts, New York, Utah, Vermont, Washington. Each is an honest refusal. In every case the source does not publish a single contribution rate for a new hire; it gives a range varying by job class, or an escalating schedule. Working out a plausible number was possible in all nine. A gap was recorded instead.

### What this does not prove

**This proves the numbers are real. It does not prove the recipe is right.**

The weights — 32, 22, 20, 16, 10 — were chosen. They were not derived from anything. Nothing in this build tests whether these are the right five things to measure, or whether pay level deserves three times the weight of trajectory.

To find out how much that matters, the ranking was recomputed **2,000 times**, each time with all five weights randomly nudged by up to 25% (seed `20260804`, so it reproduces exactly). The findings, honestly:

**What holds.** Wisconsin never left the top three. Louisiana, Georgia and Florida never left the bottom three — Florida was 51st in all 2,000 runs. **22 of 51 jurisdictions never moved more than 3 positions.**

**What doesn't.** The mean rank range across all 51 was **6.6 positions**, and **29 of 51 had a range exceeding 5 positions**. The middle of the table is where the uncertainty lives. **Washington, D.C. ranged from 22nd to 39th** and moved more than 3 places in 36% of runs. New York ranged 35th to 48th. Massachusetts, 18th to 31st.

**Dropping an indicator entirely tells the same story.** Remove I1 and 39 of 51 states move more than 3 positions — Massachusetts falls 25 places, D.C. 23, California 21. That is the sensitivity test confirming what the 32% weight implies: I1 drives this dimension. Remove any of the other four and rank correlation with the baseline stays above 0.92.

**Equal weights (20% each) give a correlation of 0.929 with the published ranking, with 25 of 51 moving more than 3 places.** So the weight choice is not arbitrary in its effect — it moves half the table by a meaningful amount — but it does not reorder the picture.

**Tiers are more stable than ranks.** Four tiers hold their membership in 92.3% of runs on average; five tiers, 87.5%. This is the single most actionable finding: **read the tier as the result, and the exact rank as approximate.**

**The nine partially-measured jurisdictions are measurably less stable.** Their mean rank range is 9.9 positions against 5.9 for fully-measured states, and they move more than 3 places 13.6% of the time against 3.5%. When comparing a starred jurisdiction to an unstarred one, the comparison is weaker than the table's decimal places suggest.

---

## 10. Known limitations, and what a future version should fix

**Twenty-one states are tied at 100 on I3.** They genuinely clear the affordability bar, so this is the design working as intended — but an indicator carrying 20% of the dimension does no work at all in distinguishing among those 21. Their positions are effectively set by the other four. *Fix: a graduated scale above the affordability line, so the indicator can distinguish among states that all pass.*

**Nine jurisdictions are scored on 84% of the dimension.** The retirement source does not publish a single new-hire rate for them. Their scores are computed from the four available indicators and rescaled — better than scoring zero, but it means they are ranked against 42 states measured on a different basis, and they are demonstrably less stable. *Fix: find a retirement source that covers all 51 with a single rate. This is the largest single weakness here.*

**Retirement data is from late 2025, not 2024.** Uniform across all 51, so it does not distort comparisons between states — but it does mean the dimension is not entirely a 2024 measurement.

**Health insurance and leave are absent entirely.** *Fix: add them if a source emerges that covers all 51 comparably. This remains the largest gap between what D1 claims to measure and what it measures.*

**Scores show order, not distance.** Percentile ranks tell you who is ahead. They do not tell you by how much.

**The exclusion-list ambiguity is unresolved.** Whether corrections officers, sheriffs, law enforcement, custodial staff, and legislators count as outside the general-employee population was never adjudicated. It affects nothing in this build — none of those words appears in any of the 51 source strings — but it should be settled before the next one, in advance, rather than when a state's score depends on it.

**Publish tiers ahead of ranks.** The stability testing is unambiguous: the four-tier grouping holds up far better than individual positions. Reporting that leads with tiers and treats exact ranks as secondary would represent the underlying data more accurately than the ranked table does.

---

*All figures anchored to 2024 except as noted. Every value, locator, fingerprint, and decision is recorded in [d1_evidence.csv](d1-build/out/d1_evidence.csv) and [d1_source_registry.csv](d1-build/out/d1_source_registry.csv).*
