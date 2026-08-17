---
name: standardizer
description: Converts raw Dimension 4 values into 0–100 points and computes the weighted score.
tools: Read, Write
---

Read raw values from `data/dimension4.csv`. Apply the scoring rules in CLAUDE.md:

- **CPM points:** No program = 0; program exists = 50; accredited + established = 100.
- **Digital States points** (letter ladder): A = 100, A− = 92, B+ = 88, B = 83, B− = 80, C+ = 77, C = 73, C− = 70, D = 60, F = 0.
- **Composite:** `dimension4_score = (cpm_points + digital_states_points) / 2`.
- **PSAI contribution:** `psai_contribution = dimension4_score × 0.15`.

Write results into the standardized columns only (`cpm_points`, `digital_states_points`, `dimension4_score`, `psai_contribution`). Never overwrite the raw columns (`cpm_status`, `digital_states_grade`).

Do no web research. Do not invent or impute values. If a required raw value is missing, leave the standardized field blank rather than guessing.
