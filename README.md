# PSAI Phase 3: Academic Review, Evidence and Methodology

This repo holds the underlying evidence and methodology files behind the Public Service Appreciation Index's Phase 2 rebuild (Anushri's audit and reconstruction of Brian's original Phase 1 index). It exists to back up specific claims made in the review package below with a file you can open and check yourself.

## Start here

This repo hosts the interactive review package itself, plus the evidence layer behind it. Read these first:

- **[PSAI Review Dossier](https://humansofpublicservice.github.io/psai-phase3/)**: methodology, what changed between Phase 1 and Phase 2, open questions for reviewers.
- **[PSAI Results dashboard](https://humansofpublicservice.github.io/psai-phase3/results.html)**: the rebuilt composite and per-dimension scores for all 51 jurisdictions, with per-state provenance.

## What's in this repo

`docs/` holds the two pages above, served via GitHub Pages. `composite/` holds the top-level composite scores file that combines the five dimensions. Everything else is one folder per dimension, each containing that dimension's methodology document, its scored evidence file, and the actual Claude Code agent definitions that collected the data, the same files the Dossier's per-dimension source citations point to.

| Folder | Weight | Contains |
|---|---|---|
| `d1-compensation/` | 30% | Methodology, 255-row evidence file with cell-level locators, source registry (every downloaded federal file, fingerprinted), the collection and audit agent definitions |
| `d2-workforce-health/` | 28% | Methodology, scored evidence file (turnover, vacancy, tenure per state) |
| `d3-public-perception/` | 22% | Rebuild methodology, scores, the polls dataset, and the poll-finder and sentiment-analyzer agent definitions |
| `d4-investment-in-people/` | 15% | Project rules (CLAUDE.md), scored evidence file, and the collector, fact-checker, and standardizer agent definitions |
| `d5-recognition-infrastructure/` | 5% | Methodology, 306-row evidence file (51 states times 6 indicators), and the collection and audit agent definitions |
| `composite/` | n/a | `PSAI_CompositeScores_Rebuilt.xlsx`, joining each dimension's own final score file by state name rather than row position (see the Dossier's Question 01 for why that distinction matters) |

## What's not here, on purpose

The raw downloaded government source files behind Dimension 1 (roughly 294 MB of BLS, HUD, and NASRA archives) aren't duplicated here. They're already fingerprinted (SHA256) and cited by exact URL in `d1-compensation/d1_source_registry.csv`, so there's no need to re-host them. Internal working notes from the review process also aren't included here, this repo is scoped to material a reviewer would actually want to open and verify.

## Provenance

The per-dimension evidence, methodology, and agent-definition files are copied, unmodified, from the Phase 2 project build (`PSAI_Index_Project_2026`). If you find a discrepancy between one of those files and what the Dossier says about it, the file here is the source of truth, flag it.

Two exceptions: `docs/` holds the Dossier and Dashboard themselves, the narrative and interactive layer, not raw evidence, and `composite/PSAI_CompositeScores_Rebuilt.xlsx` is a corrected rebuild of the Phase 2 project's original composite file, not a copy of it. The original had a data bug (dimension scores joined by row position instead of by state name); the corrected version and the reasoning behind it are described in the Dossier's Question 01.
