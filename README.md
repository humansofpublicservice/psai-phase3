# PSAI Phase 3: Academic Review, Evidence and Methodology

This repo holds the underlying evidence and methodology files behind the Public Service Appreciation Index's Phase 2 rebuild (Anushri's audit and reconstruction of Brian's original Phase 1 index). It exists to back up specific claims made in the review package below with a file you can open and check yourself.

## Start here

This repo is the evidence layer, not the narrative. Read these first:

- **[PSAI Review Dossier](https://claude.ai/code/artifact/5be43bdf-e6a6-4aa6-958a-89a78b605456)**: methodology, what changed between Phase 1 and Phase 2, open questions for reviewers.
- **[PSAI Results dashboard](https://claude.ai/code/artifact/585479b3-31b5-4e8a-b829-89537b5b4f37)**: the rebuilt composite and per-dimension scores for all 51 jurisdictions, with per-state provenance.

## What's in this repo

One folder per dimension. Each contains that dimension's methodology document, its scored evidence file, and the actual Claude Code agent definitions that collected the data, the same files the Dossier's per-dimension source citations point to.

| Folder | Weight | Contains |
|---|---|---|
| `d1-compensation/` | 30% | Methodology, 255-row evidence file with cell-level locators, source registry (every downloaded federal file, fingerprinted), the collection and audit agent definitions |
| `d2-workforce-health/` | 28% | Methodology, scored evidence file (turnover, vacancy, tenure per state) |
| `d3-public-perception/` | 22% | Rebuild methodology, scores, the polls dataset, and the poll-finder and sentiment-analyzer agent definitions |
| `d4-investment-in-people/` | 15% | Project rules (CLAUDE.md), scored evidence file, and the collector, fact-checker, and standardizer agent definitions |
| `d5-recognition-infrastructure/` | 5% | Methodology, 306-row evidence file (51 states times 6 indicators), and the collection and audit agent definitions |

## What's not here, on purpose

The raw downloaded government source files behind Dimension 1 (roughly 294 MB of BLS, HUD, and NASRA archives) aren't duplicated here. They're already fingerprinted (SHA256) and cited by exact URL in `d1-compensation/d1_source_registry.csv`, so there's no need to re-host them. Internal working notes from the review process also aren't included here, this repo is scoped to material a reviewer would actually want to open and verify.

## Provenance

Everything in this repo is copied, unmodified, from the Phase 2 project build (`PSAI_Index_Project_2026`). If you find a discrepancy between a file here and what the Dossier says about it, the file here is the source of truth, flag it.
