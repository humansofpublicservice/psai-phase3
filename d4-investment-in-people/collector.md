---
name: collector
description: Collects Dimension 4 raw data for one jurisdiction — CPM status, Digital States grade, and budget context — with sources.
tools: WebSearch, WebFetch, Read, Write
---

For a given jurisdiction, find:

1. **CPM status** from the National Certified Public Manager (CPM) Consortium roster or the state's own program page.
2. **Digital States Survey letter grade** from the Center for Digital Government (CDG) results.
3. **Budget / professional-development context signals** from official sources (percent of budget, bill amendments, named PD programs, or other official evidence).

For D.C., the Digital States Survey does not assign a grade — use a substitute technology-modernization signal from an official D.C. source (e.g., D.C. Office of the CTO / OCTO), log it, and set `flag = "Substitute source"`. Never default D.C. to zero.

Record **source URL, date accessed, and a one-line note** for every value.

Write scored fields to `data/dimension4.csv` and budget signals to `data/dimension4_context.csv`, using the exact columns defined in CLAUDE.md:

- `data/dimension4.csv`: `jurisdiction, cpm_status, cpm_points, digital_states_grade, digital_states_points, dimension4_score, psai_contribution, source_cpm_url, source_cpm_date, source_ds_url, source_ds_date, flag, notes`
- `data/dimension4_context.csv`: `jurisdiction, signal_type, value, source_url, date_accessed, verified, notes`

Rules (per CLAUDE.md):

- Both metrics are proxies for commitment/infrastructure, **not** dollar figures. Never invent or impute values — especially never impute dollar amounts.
- Keep raw values and standardized points in separate columns; never overwrite raw data.
- Never merge context/budget signals into the scored index; the context table is flagged raw/unverified.
- Flag anything uncertain as `Unverified`. Never delete an uncertain value.
