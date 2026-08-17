# Dimension 2 (Workforce Health) — Recalculation Methodology

**Status:** Finalized for scoring (rulings applied 2026-07). Stability sub-metric is turnover-only (no state publishes retention); source tiers include `official_via_secondary` (medium confidence); median-tenure and dead-link values are excluded; count-derived vacancy grand-totals kept at low confidence; contradictory single-source values resolved to the more conservative figure.

## 1. Design principle

The dimension answers one question: **whether states can attract and retain talented people in public service roles.** It measures workforce health.

The prior D2 needs a revamp: it required three metrics (retention, vacancy, tenure) for all 51 jurisdictions when only ~24 states publish them, and a framework demanding universal coverage of unpublished data forces estimation and inference by construction — which led to fabricated data (see the Arizona audit finding). This method removes that pressure: **a state is scored only on what can be verified about it, never on an imputed or estimated value.** Where data does not exist, that absence is measured (transparency) rather than filled.

Capacity/size metrics (FTE trajectory, per-capita staffing) were considered and **dropped**: workforce size reflects budget and population, not how the existing workforce is treated, and is out of scope for this dimension.

---

## 2. Tier structure and weighting

| Tier | Measures | Weight | Coverage |
|---|---|---|---|
| **C — Reported workforce metrics** | Retention/turnover, vacancy, tenure | **65%** | Published data only |
| **B — Workforce transparency** | Whether the state publishes workforce data at all | **35%** | All 51, verifiable |

Tier C is weighted above Tier B by intent: reported outcomes are the most direct treatment signal. Tier B carries meaningful weight because for many states it is the only verifiable signal, and because whether a state measures its workforce is itself a stewardship signal.

### Tier C internal weighting (of the 65%)

| Sub-metric | Weight within C | Rationale |
|---|---|---|
| Workforce turnover | 50% | Most direct behavioral signal; most widely published |
| Vacancy rate | 30% | Ability to fill and hold positions |
| Tenure | 20% | Thinnest data; least widely published |

A state with some but not all three sub-metrics has its available sub-metrics rescaled to the full 65%.

**Workforce stability is measured by turnover only.** Retention was originally allowed as an alternative form, but collection across all 51 jurisdictions found that **0 states publish a retention rate** as their stability figure — every state that publishes stability publishes turnover (separations ÷ headcount). The sub-metric is therefore **turnover only**. The value is still recorded **exactly as published, in its native form — no `100 − x` conversion under any circumstance** (a conversion is an inference, which §1 forbids; this was the single most common defect in the pre-existing SoSI files).

- A `turnover_definition` field records what the published turnover figure actually measures: `voluntary_only` / `total_separation` / `includes_retirements` / `new_hire_only` / `unclear`. These are **not interchangeable** — a voluntary-resignation-only rate and a total-separation-including-retirements rate measure different things — and the definition travels into the comparison and the report (see §9).
- Where turnover is published **with a voluntary/involuntary/retirement breakout**, the voluntary figure may be used as the scored figure (it best reflects whether people choose to stay), recorded as `voluntary_only` — but only when that breakout is published, never derived.

Normalization of this sub-metric is a single nationwide ranking — see §9.

---

## 3. Higher education — excluded

**Public higher-education staff are excluded from all turnover and vacancy values.** State-government figures frequently bundle university employees, who are a large share of state headcount and follow academic-calendar dynamics unrelated to general workforce stewardship. Where a state report offers both a general-workforce figure and an all-inclusive figure, the agent uses the **general-workforce (non-higher-ed)** figure. This preference is applied identically to all 51 jurisdictions. Where a report bundles higher ed inseparably, the value is tagged `INCLUDES_HIGHER_ED` and flagged as a comparability limitation rather than silently used.

---

## 4. Value hierarchy (the agent uses the first tier that applies)

1. **Official state report — in-folder.** HOPS files, traceable to the state's own agency, HR/personnel division, civil service board, or state auditor. `confidence = high`. (In practice **0 of 51** states had a genuine official report in-folder — every in-folder file was an LLM-generated SoSI narrative whose numbers were rejected as conversions/composites/estimates.)
2. **Official state report — recovered via web.** Same standard, located online (see §5). `source_type = official_recovered`, `confidence = high`, flagged for human spot-check.
3. **Official data relayed via a secondary source.** An official agency figure that is only reachable through a news outlet or a third-party analysis of official open data (not a self-published agency document). `source_type = official_via_secondary`, `confidence = medium` — below a directly-recovered official document, above a third-party proxy, because the underlying figure is the state's own but its exact provenance/scope is one step removed.
4. **Third-party proxy (Reason Foundation).** Used **only** when no official report exists in tiers 1–3. `source_type = third_party_proxy`, `confidence = low`, source URL recorded. Source: https://reason.org/commentary/alaska-retaining-public-workers-better-than-most-states/
5. **No value.** No official report and no proxy figure → `NOT_PUBLISHED` → Category 3 (§7) → Tier C weight redistributes to Tier B. **No estimation, ever.**

`confidence` therefore takes three values: `high` (directly-recovered official document), `medium` (official-via-secondary), `low` (third-party proxy; count-derived vacancy per §8; official-but-subset scope, e.g. a new-hire-only turnover figure).

---

## 5. Web-recovery procedure

Discipline is identical to the D3 fact-check rule: **find the state's published figure, or record that none exists. Never construct, estimate, or substitute.**

**Permitted:** search for an official state workforce/HR report (dept. of administration/management, HR/personnel division, civil service board, state auditor); a real published figure **for state government employees**; record value, direct URL, year, publishing agency → tier 2 / Category 1.

**If Reason cites an underlying state report:** the agent pulls and cites that **underlying official report** (promoting the state to tier 2), rather than citing Reason. Reason is the fallback, not the preferred citation when the official one is one click away.

---

## 6. Third-party proxy rules (Reason Foundation)

The proxy is permitted at tier 3, but the following guardrails always apply — they govern *how it is recorded*, not *whether it is used*:

- **Verbatim only.** The agent transcribes the figure Reason **states**. It does not derive, adjust, recompute, average, or reconcile it. If Reason only implies a value, that is not a stated value → `NOT_PUBLISHED`.
- **`scope_flag` runs.** If Reason's figure is non-statewide, it is recorded with its actual scope (e.g. `single_agency_subset`), not laundered into a statewide number. The tag travels into the final comparison.
- **`population_match` runs.** The figure must concern state-government employees. (Example: Reason's Alaska figure is an agency subset obtained privately from the executive branch — usable under this rule as the only figure available, but tagged `scope = single_agency_subset`, `confidence = low`, never treated as equal to a clean statewide figure.)
- **Internal inconsistency — general rule (applies to any source, not just Reason).** Where a single source states two contradictory values for one figure (e.g. Reason gives Alaska both 18% and 17.5%), use the **more conservative (worse-performing) figure** — for turnover and vacancy, the *higher* number; for tenure, the *lower* — and flag the discrepancy in Notes with both values. This is a deliberate conservatism rule, **not** a rounding choice, and must not be justified as one. (Alaska turnover is therefore scored at **18%**, not 17.5%.)
- **Coverage expectation.** Reason's usable cross-state numbers are mostly states that already publish (they resolve to tier 1–2 anyway). Genuine non-publishers usually have no Reason figure either, so this fallback fills few gaps; most true non-publishers still land in Category 3.

---

## 7. The three-way publication sort

- **Category 1 — Published (official, in-folder or recovered), or third-party proxy available.** Scored on Tier C + Tier B. Proxy-based values carry `THIRD_PARTY_PROXY` + `confidence = low`.
- **Category 2 — Recovered official report.** Sub-case of Category 1, flagged for spot-check.
- **Category 3 — No official report and no proxy.** After a genuine search, nothing exists. Tier C weight **redistributes to Tier B**; non-reporting counts against the state. Justified because the search confirms the data does not exist rather than assuming it.

---

## 8. Mandatory checks on every value (any source)

- **`population_match`** — does the source measure state government employees? Catches the Arizona education substitution (school-district teachers), which passes every other check.
- **`scope_flag`** — `statewide_all_agencies` / `executive_branch_only` / `single_agency` / `single_agency_subset` / `classified_only` / `unclear`.
- **`composite_metric`** — constructed weighted averages (as Arizona's vacancy figure was) are decomposed; each component's provenance recorded separately.
- **Estimation-language trigger** — "I estimated," "I assumed," "in the absence of state-specific data" auto-sets `INFERRED` / `NOT_PUBLISHED` and quotes the phrase.
- **`source_year`** — underlying data year, not file date. Window **2022–2026**; `STALE` if earlier, `OUT_OF_RANGE` if later or impossible.
- **`higher_ed_status`** — `excluded` (preferred) / `INCLUDES_HIGHER_ED` (flagged limitation).
- **Median-tenure exclusion.** A **median** length of service is not an average and must **not** be used as a proxy for mean tenure — the two are not interchangeable and the framework's tenure axis is a mean. If a state's *only* tenure figure is a median, tenure is set to `NOT_PUBLISHED`; the median value and its URL are preserved in Notes for reference, never converted or adjusted. (Where a state publishes both a mean and a median, the mean is used.)
- **Dead-link exclusion.** A value whose source link is dead (returns 404 / no longer resolves) is **excluded** and set to `NOT_PUBLISHED`, because it can no longer be verified; the value and dead URL are preserved in Notes. (A `403`/access-block where the document still exists and was verified via an archive/mirror is *not* a dead link and is kept, flagged.)
- **Count-derived vacancy (kept, low confidence).** A vacancy rate that is not printed verbatim but is a **single grand-total division** (total vacant ÷ total positions) taken from an official vacancy-purpose document is kept, at `confidence = low`, with a Notes annotation that the rate was computed from published counts. A verbatim **printed** statewide vacancy rate is kept at full confidence. A **constructed cross-sector composite** (a weighted average the agent or the SoSI file built) is never a published rate → `NOT_PUBLISHED`.

---

## 9. Normalization

**Replace `100 − x` with percentile rank across the jurisdictions that have a value**, per sub-metric. The prior inversion compressed all states into ~85–98, barely discriminating; percentile rank uses the full 0–100 scale. **Turnover and vacancy percentiles are inverted so lower turnover / lower vacancy = higher score; tenure ranks direct (higher = better).** All three axes thus read "higher score = healthier workforce." Only states with a published value for a sub-metric enter that sub-metric's ranking; a state with no value for a sub-metric simply does not receive that sub-score (its Tier C internal weights rescale to what it has, §2).

**Workforce turnover — a single nationwide ranking.** Because 0 of 51 states publish retention (§2), there is no retention pool and no two-pool split. All published **turnover** values are percentile-ranked together in **one nationwide ranking**, inverted so lower turnover = higher score.

**Required disclosure in the final report (definitional heterogeneity).** The turnover values ranked together are **not one measurement**: they span `voluntary_only`, `total_separation`, `includes_retirements`, `new_hire_only`, and `unclear` (the proxy figures). Percentile rank makes them *scale*-comparable, not *definitionally* comparable — a voluntary-resignation-only rate ranked against a total-separation-including-retirements rate is comparing different things. The report must (a) state that states do not publish retention, so this is a turnover ranking, and (b) give the per-state `turnover_definition` breakdown and flag the heterogeneity **prominently** as the central comparability limitation of the stability sub-metric.

**Caveat normalization cannot fix:** percentile rank makes values *scale*-comparable, not *definitionally* comparable. A state's executive-branch-only FY2023 turnover and another's all-agencies 2024 turnover become percentiles on the same axis but remain different measurements. The `turnover_definition`, `scope_flag`, `source_year`, `population_match`, and `higher_ed_status` tags travel with each value into the comparison; material mismatches are surfaced, not silently ranked. Medium-confidence (official-via-secondary), low-confidence (proxy / count-derived / subset-scope) values are marked as such in the output, and the report states how much of the final scoring rests on each confidence tier.

---

## 10. Output files

The agent produces **two CSV files**, both organized as labeled tables.

### 10.1 `dimension2_scores.csv` — one row per jurisdiction (51 rows)

Every gathered metric is fact-checked before entry per §5 and §8 to reduce the risk of fabricated data; the source URL is recorded for each metric so every value is traceable, and a Notes column captures any anomaly.

| Column | Contents |
|---|---|
| `jurisdiction` | State or "Washington, D.C." |
| `stability_value` | Workforce **turnover** figure as published, in native form, never converted (`NOT_PUBLISHED` if none) |
| `turnover_definition` | `voluntary_only` / `total_separation` / `includes_retirements` / `new_hire_only` / `unclear` — what the published turnover figure measures (§2). Replaces the former `stability_metric_type`; retention is no longer a value because no state publishes it. |
| `stability_url` | Direct source URL for that value |
| `stability_source_type` | `official_in_folder` / `official_recovered` / `official_via_secondary` / `third_party_proxy` / `not_published` — for this metric |
| `stability_confidence` | `high` / `medium` / `low` — for this metric |
| `stability_scope_flag` | Per §8 — for this metric |
| `stability_source_year` | Per §8 — for this metric |
| `stability_higher_ed_status` | `excluded` / `INCLUDES_HIGHER_ED` — for this metric |
| `stability_fact_check_result` | Outcome of §5/§8 verification for this metric |
| `vacancy_value` | Vacancy rate as published (`NOT_PUBLISHED` if none) |
| `vacancy_url` | Direct source URL |
| `vacancy_source_type` | `official_in_folder` / `official_recovered` / `official_via_secondary` / `third_party_proxy` / `not_published` |
| `vacancy_confidence` | `high` / `medium` / `low` (count-derived grand-total = low) |
| `vacancy_scope_flag` | Per §8 |
| `vacancy_source_year` | Per §8 |
| `vacancy_higher_ed_status` | `excluded` / `INCLUDES_HIGHER_ED` |
| `vacancy_fact_check_result` | Outcome of §5/§8 verification |
| `tenure_value` | Average tenure as published (`NOT_PUBLISHED` if none) |
| `tenure_url` | Direct source URL |
| `tenure_source_type` | `official_in_folder` / `official_recovered` / `official_via_secondary` / `third_party_proxy` / `not_published` |
| `tenure_confidence` | `high` / `medium` / `low` (median-only = `NOT_PUBLISHED`, see §8) |
| `tenure_scope_flag` | Per §8 |
| `tenure_source_year` | Per §8 |
| `tenure_higher_ed_status` | `excluded` / `INCLUDES_HIGHER_ED` |
| `tenure_fact_check_result` | Outcome of §5/§8 verification |
| `workforce_transparency` | Tier B result — whether the state publishes workforce data, and which metrics (per §2/§7) |
| `stability_score` | Percentile-rank score — single nationwide turnover ranking, inverted (lower turnover = higher score) (§9) |
| `vacancy_score` | Percentile-rank score |
| `tenure_score` | Percentile-rank score |
| `transparency_score` | Tier B score |
| `dimension2_score` | **Final D2 score** — Tier C (65%, internally 50/30/20) + Tier B (35%), with Tier C weight redistributed to B for Category 3 states (§7) |
| `Notes` | Any anomaly that doesn't fit a structured column: internal source inconsistency (e.g. two conflicting Reason values), composite decomposition detail, estimation-language quotes, or cross-metric comparability caveats |

**Per-metric tagging.** Source type, confidence, scope, year, higher-ed status, and fact-check result are recorded **separately for each of the three metrics**, because a state's three metrics routinely differ on all of them (e.g. a state may have high-confidence official tenure but a low-confidence proxy stability figure from a different year and scope). Row-level tags would force one metric's tags to stand in for all three and push the rest into free-text Notes, where Phase 3 scoring cannot read them. Per-metric columns let the scope-mismatch and confidence checks in Phase 3 run automatically. Notes is reserved only for anomalies that have no structured column.

The three sub-metrics each carry their own value **and** URL column so no number is ever recorded without its source. Fact-check every metric before it enters the table — an unverified value is marked as such in its `*_fact_check_result`, never entered as if confirmed.

### 10.2 `dimension2_documentation.csv` — the data dictionary

A separate CSV defining the score file, one row per column:

| Column | Contents |
|---|---|
| `column_name` | The column being defined |
| `definition` | What the value is |
| `collection_or_calculation` | How it was collected (which source tier, §4) or calculated (normalization/weighting, §9/§2) |
| `possible_values` | Allowed entries / flags for that column |

The documentation CSV also carries a header block (or a leading `methodology_overview` row) summarizing the D2 methodology: the attract-and-retain question, the Tier C (65%) / Tier B (35%) structure, the official → recovered → proxy → no-value hierarchy, higher-ed exclusion, percentile-rank normalization, and the no-estimation rule.

---

## 11. Open decisions requiring your sign-off

1. **Category 2/proxy spot-check rate.** Recovered official reports and third-party proxy values carry the highest error risk (population/scope mistakes enter here). Recommend 100% human review of both, given there are at most ~27. Confirm.
2. **Tier weights.** C 65 / B 35 confirmed.

---

## 12. What this method does and does not deliver

**Does:** scores every state only on published data (official or, at lowest confidence, a named third-party figure) — no estimates enter any value; measures data absence instead of imputing it; recovers real data missing from the folder; excludes higher ed for comparability; carries scope/year/population/higher-ed tags into the comparison; uses a normalization that actually discriminates.

**Does not:** make definitionally different measurements identical (flags them); treat proxy values as equal to official ones (tags and down-weights confidence); fully escape the coverage/relevance tension (resolves it by measuring absence — a documented choice); judge whether a staffing level is "right" (out of scope).

**Settled inputs:** higher ed excluded from turnover/vacancy; 65/35 C-over-B split; Tier C internal 50 (turnover) / 30 (vacancy) / 20 (tenure) rescaled to available sub-metrics; stability = **turnover only** (0/51 publish retention); source hierarchy official-in-folder → official-recovered → **official-via-secondary (medium)** → Reason proxy (low) → no-value; median-tenure and dead-link values excluded to `NOT_PUBLISHED`; count-derived vacancy grand-totals kept at low confidence; contradictory single-source values → more conservative figure; no estimation under any circumstance.
