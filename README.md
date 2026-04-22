# American Renewal Project

> ⚠️ **Name Notice — Placeholder Name**
>
> It has come to our attention that the name "American Renewal Project" is already in use by an
> existing organization with which this project has **no affiliation, connection, or shared ideology**.
> The current name is a **placeholder** while a permanent name is selected. All references to
> "American Renewal Project" in this repository, website, and documentation should be understood
> as temporary. We apologize for any confusion.

This repository is now organized around the architecture described in the branch chats: a document-first policy platform with pillar docs, a cross-domain system-rules layer, strategy materials, and a structured catalog of tracked policy items.

## Repository layout

```text
/
├── overview/           Project framing and high-level structure
├── pillars/            Core policy-domain documents
├── strategy/           Roadmap and movement/communications planning
├── sources/chat-logs/  Downloaded branch chat transcripts used as source material
├── data/               Structured catalog database and notes
├── scripts/            Import and maintenance scripts
└── system_rules.md     Cross-domain rule architecture summary
```

## Current baseline

- `pillars/` is seeded from the latest reusable markdown in the legacy project snapshot.
- `sources/chat-logs/` contains the downloaded ChatGPT branch transcripts.
- `data/policy_catalog.sqlite` contains the first-pass structured catalog extracted from the chats:
  - 101 canonical numeric policy items
  - 1,095 canonical prefixed rule items
  - 138 canonical dedupe links
  - 888 contextual ID mentions from prose/summary sections
- The catalog is built from the formal IDs already present in the chat logs:
  - numeric policy backlog items such as `192`
  - canonical rule IDs such as `SYS-AI-007` or `HLT-COV-003`

## Canonical sources

The current first-pass import treats these as primary sources:

1. `sources/chat-logs/main-branch.txt`
2. `sources/chat-logs/brainstorm-branch.txt`
3. legacy markdown under `pillars/` for current document scaffolding

The `comparisons` and `AI-statement` branches are still useful context, but they do not currently contain the structured ID datasets.

Legacy pillar markdown in `pillars/` is useful scaffolding, but it should not be treated as the authoritative source for catalog completeness. The main and brainstorm chat logs plus the SQLite catalog are the authoritative audit trail.

## Rebuilding the catalog

Run:

```bash
scripts/import_policy_catalog.py
```

The importer:

- preserves all source occurrences
- picks canonical records deterministically, preferring the main branch and later occurrences within a source when the same ID appears more than once
- seeds named structured IDs that were identified in the chats but never formalized as pipe-delimited rows
- converts all current numeric checkpoint items to structured IDs through `record_links`
- preserves prose-only ID mentions in a separate table so provisional or superseded IDs are not lost

See `overview/current-state.md` for the current audit state and unresolved context-only IDs.
