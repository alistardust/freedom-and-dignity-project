# AI Repo Context

This file contains shared repository context for AI assistants working in this repo.

## Purpose

Instruction files should stay short and stable. Put durable behavioral rules in:
- `AGENTS.md`
- `.github/copilot-instructions.md`

Put changing repository context in normal repo documentation like this file.

Changes to Copilot-specific instruction files should be made directly in `.github/copilot-instructions.md` and `~/.copilot/copilot-instructions.md`, keeping both in sync.

## Current project shape

This repository is a U.S. policy platform organized around:
- 5 foundations
- policy pillars under `pillars/`
- project-wide prose under `overview/`
- structured catalog data under `data/`
- source logs under `sources/`
- the current website under `docs/`

Do not hardcode counts from this file into instruction files. Verify current counts from the repo when they matter.

## Working order

When auditing or editing policy content, use this general order:
1. `overview/current-state.md`
2. `docs/pillars/`
3. `data/policy_catalog_v2.sqlite`
4. `sources/`
5. `pillars/`

## Source-of-truth guidance

The repo is in a pre-reconciliation state.

Until reconciliation is complete:
- site HTML and database content may both contain meaningful edits
- do not auto-resolve conflicts between HTML and database content
- treat divergences as review items
- preserve provenance

## Provenance guidance

- `data/policy_catalog_v2.sqlite` is the active structured catalog
- `data/policy_catalog.sqlite` is historical and may still be used for provenance, audit, and reconstruction tasks
- do not treat the legacy database as the canonical current source of policy positions
- preserve old-to-new ID relationships when reconciling records

## Maintenance requirements

When repository structure, workflow, source-of-truth rules, or other important project context changes, this file must be updated in the same change.

If a change affects repository behavior, developer workflow, build steps, architecture, testing expectations, documentation, or user-facing functionality, the relevant documentation must also be updated in the same change. This includes README files, overview documents, and other affected repo documentation.

## Testing requirements

All new code must receive tests appropriate to the change.

Before committing or pushing changes:
- relevant tests must be run
- newly added or updated tests must pass
- failing tests must be fixed or explicitly discussed with the user before proceeding
