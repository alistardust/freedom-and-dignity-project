# Copilot Instructions Reconciliation Request

Please audit and reconcile these Copilot instruction files:

- `~/.copilot/copilot-instructions.md`
- `.github/copilot-instructions.md`

## Goals

- Keep the global file focused on durable cross-project behavior.
- Keep the repo-local file focused on durable repo-specific behavior.
- Remove or relocate volatile facts such as hardcoded counts and changing inventories.
- Prefer short pointers to repo documentation over large embedded context blocks.
- Preserve rules about provenance, citations, source verification, documentation updates, and testing.
- Align approval language with the checked-in `AGENTS.md`.

## Approval language requirement

When approval is required, ask directly and wait for an unambiguous affirmative confirmation before acting.

Valid approval includes clear affirmative confirmations such as:
- `Yes`
- `Approve`
- `Approved`
- `Affirmative`
- `Confirmed`

The following do not count as approval:
- `Go ahead`
- `Go ahead and do this`
- `Proceed`
- `Sounds good`
- implied intent
- contextual inference
- language that could reasonably be interpreted in more than one way

If approval is required and has not been given, the assistant may prepare work, explain the next step, or show a proposed patch, but must not apply the change.

## Target structure

Global Copilot file:
- user preferences
- durable coding standards
- safety and security rules
- approval language

Repo-local Copilot file:
- short repo-specific behavior rules
- source-of-truth guidance
- provenance guidance
- citation and verification requirements
- documentation and testing expectations
- pointers to `overview/ai-repo-context.md` and `overview/current-state.md`

## Output requested

Please produce:
1. a proposed revised global Copilot instruction file
2. a proposed revised repo-local Copilot instruction file
3. a short explanation of what was removed, moved, or tightened and why
