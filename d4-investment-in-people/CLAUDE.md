# PSAI — Dimension 4: Investment in People

Part of the Public Service Appreciation Index (PSAI), which measures how well
U.S. states value their public workforce across 51 jurisdictions (50 states +
Washington, D.C.). **This project covers only Dimension 4 — Investment in People,
weighted 15% of PSAI.**

Core question: Are the Dimension 4 scores accurate, consistent, and
methodologically sound across all 51 jurisdictions?

## The two scored metrics

Both metrics measure **commitment/infrastructure, not spending**. They are
proxies, not dollar figures. State this caveat plainly; never infer or impute
dollar amounts.

1. **CPM — professional development.** Whether the jurisdiction runs a program
   accredited by the National Certified Public Manager (CPM) Consortium.
2. **Digital States Survey — technology modernization.** The Center for Digital
   Government's biennial A–F grade for the jurisdiction.

## Scoring rules (0–100 scale)

**CPM points**
| Status | Points |
|---|---|
| No program | 0 |
| Program exists | 50 |
| Accredited + established | 100 |

**Digital States points**
| Grade | Pts | Grade | Pts |
|---|---|---|---|
| A  | 100 | C+ | 77 |
| A− | 92  | C  | 73 |
| B+ | 88  | C− | 70 |
| B  | 83  | D  | 60 |
| B− | 80  | F  | 0  |

**Composite**
- `dimension4_score = (cpm_points + digital_states_points) / 2`
- `psai_contribution = dimension4_score × 0.15`

Keep raw values (`cpm_status`, `digital_states_grade`) and standardized points
(`cpm_points`, `digital_states_points`) in **separate columns**. Never overwrite
raw data.

## Professional-development sub-metric (revised — supersedes CPM-only for PD)

The PD half of Dimension 4 is **no longer CPM-only**. It is a **cumulative,
PD-function-dominant** score. Revised results live in
**`data/dimension4_pd_revised.csv`** (documented in
`data/dimension4_pd_methodology.csv`); the original CPM-based files are retained
as the prior version.

**Rubric (`pd_points`, 0–100):**
- Base from `pd_function_count` (distinct official statewide PD functions):
  **3+ = 85 · 2 = 70 · 1 = 55 · none = 0**.
- Bonuses: **+12** if `cpm_status == "Accredited + established"` (explicit
  National CPM Consortium accreditation **only** — "Program exists" and "No
  program" earn no CPM credit); **+7** if a verified non-CPM certificate program
  exists that is **not already counted** as a function (no double-credit).
- `pd_points = min(100, base + bonuses)`.
- **CPM-only floor:** if `pd_function_count == 0` **and** CPM is
  "Accredited + established", floor `pd_points` at **20**.
- Composite: `dimension4_score = (pd_points + digital_states_points) / 2`;
  `psai_contribution = dimension4_score × 0.15`, full precision.

**Design choice:** statewide PD functions dominate (base up to 85); CPM
accreditation is credited modestly (+12, or a floor of 20 when it is the only PD
signal). A state can invest in PD outside the CPM Consortium and still score well.

**What counts as a PD function.** A dedicated official state central
training/learning division, a leadership academy, or a standing PD program —
confirmed on an **official state government primary source** (state `.gov`,
statute, or official agency page). Exclude generic HR/careers/benefits pages and
compliance-only training. Count each distinct function once.

**Fact-check + dates.** Count a function/certificate only when a primary source
**literally names it** (`verified=yes` only then; third-party/non-primary →
`no`; never infer). Record each source's **own publication/last-updated date**,
never the retrieval date; if none is shown, record **`undated`**.

**Limitation.** Counts depend on what official pages disclose and whether they
can be fetched; blocked (403) or vaguely-worded pages can under-count, yielding a
conservative 0 even where PD infrastructure likely exists.

## D.C. exception

The Digital States Survey grades the 50 states but **not** D.C. For D.C.:
- Find a substitute technology-modernization signal from an official D.C. source
  (e.g., D.C. Office of the CTO / OCTO).
- Log that source URL and date.
- Set `flag = "Substitute source"` for that row.
- **Never default D.C. to zero.**

## Budget / PD context data — collected but NOT scored

Separately collect budget signals per jurisdiction: percent of budget, bill
amendments, named PD programs, or other official evidence. Rules:
- Store in `data/dimension4_context.csv`, flagged **raw/unverified**.
- **Never merge into the scored index.**
- Do **not** infer or impute dollar figures. Record only what a source states.

## Output files (database-like spreadsheets)

### `data/dimension4.csv` — one row per jurisdiction
Columns:
`jurisdiction, cpm_status, cpm_points, digital_states_grade,
digital_states_points, dimension4_score, psai_contribution, source_cpm_url,
source_cpm_date, source_ds_url, source_ds_date, source_recency, flag, notes`

`source_recency` = the **year of the newest supporting source** for the row (see
**Recency standard**).

`flag` ∈ { `Verified (re-fetched)`, `Verified (corroborated)`,
`Substitute source`, `Unverified`, `Stale — needs refresh` }.  See **CPM source
rule** for how to choose between the two `Verified` variants and **Recency
standard** for `Stale`.

### `data/dimension4_context.csv` — budget/PD context (raw/unverified)
Columns:
`jurisdiction, signal_type, value, source_url, date_accessed, verified,
notes`  (`verified` ∈ { `yes`, `no` })

## Source logging (required for every value)

Every scored value must record: **source URL, date accessed, and a one-line
note** on what the source says.
- CPM values trace to the **CPM Consortium accreditation roster**.
- Digital States values trace to the **CDG Digital States Survey results**.

## CPM source rule (applies to every jurisdiction)

The CPM value must be backed by a **machine-fetchable authoritative source** —
the National CPM Consortium member list in **static HTML**, an **archived
(Wayback) snapshot**, or an **official PDF**. Choose the flag by what confirms it:

| Situation | `flag` |
|---|---|
| A machine-fetchable authoritative source confirms it | `Verified (re-fetched)` |
| Only a block-listed / JS-rendered page corroborates it | `Verified (corroborated)` |
| Nothing confirms it | `Unverified` |

Never delete the value — flag it.

**CPM point rule (explicit; apply uniformly to every jurisdiction).** Prior runs
applied this inconsistently — the following is the single standard:
- **100** — a **fetched, current (2022–2026)** source **explicitly states** the
  program is *accredited by the National CPM Consortium* (or "National CPM
  Consortium-accredited" / "accreditation from the National CPM Consortium").
- **50** — a program exists but the fetched source does **not** explicitly name
  the Consortium as accreditor. Non-qualifying phrasing: "nationally accredited"
  (no body named), "national CPM designation," "aligned with" / "affiliate of"
  the Consortium, or the Consortium appearing only as a link / logo / membership /
  related-resource.
- **0** — no CPM program found.

The score rests on the **current live program page**, not on ACE. ACE's listing
(review windows lapsed 2012) may set the flag but **cannot justify a 100** — it
fails the recency standard below.

## Recency standard (applies to every scored value)

Every scored value must be supported by a source dated **2022–2026**. Sources
older than 2022 (e.g., ACE records lapsed 2012) **do not count** as valid support.
- **Digital States:** the **2024** results are valid.
- **CPM:** the 100/50 score must rest on a **current live page (2022–2026)**. A
  page that states no recent/current status is treated as undated — re-fetch it;
  if no 2022–2026 source confirms accreditation, it **cannot score 100**.
- Record `source_recency` = the year of the newest supporting source per row.
- If a row's newest supporting source **predates 2022**, set
  `flag = Stale — needs refresh`. Never delete the value.

**CPM sourcing method (per jurisdiction).** The ACE National Guide only
machine-confirms **8 states** (Alabama, Arkansas, Kansas, Mississippi, Oklahoma,
Utah, Ohio, Wisconsin), and all of their ACE review windows lapsed by **2012**.
ACE is therefore *not* a full roster. Source CPM status **per jurisdiction from
each state's own official CPM program page** (a state `.gov` or the state
university that runs the program) — the **hybrid method**:
- `Verified (re-fetched)` — a live official program page was fetched and confirms
  an active, accredited program.
- `Verified (corroborated)` — only JS-rendered / blocked (403) / third-party
  pages corroborate it.
- `Unverified` — neither confirms it. (Keep the value; never delete it.)

**Validation tripwire.** Current Consortium/state sources show roughly **~40
jurisdictions** run an accredited CPM program. After collection, count the
jurisdictions confirmed with a CPM program. If the total falls **far outside
~40**, stop and flag it — it signals over- or under-counting. (The old ~22–24
figure came from ACE's outdated "22 states" line and is wrong; do not use it.)

## Precision rule

Store `psai_contribution` and all scores (`cpm_points`, `digital_states_points`,
`dimension4_score`) at **full precision**. Round to 2 decimals **only for display
or reporting**, never in the stored data.

## Non-negotiable rules

- Never overwrite raw data; raw and standardized points live in separate columns.
- Never merge context/budget data into the scored index.
- Never invent or impute dollar figures.
- Never default D.C. to zero — use a logged substitute source.
- Never delete an uncertain value — flag it (`Unverified`).
- CPM values require a machine-fetchable authoritative source; flag per the
  **CPM source rule**.
- Never round stored scores or `psai_contribution` — full precision in storage,
  2-decimal rounding only for display.
