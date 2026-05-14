# Freedom and Dignity Project

> ⚠️ **Name Notice — Placeholder Name**
>
> "Freedom and Dignity Project" is a working name derived from the repository slug while a permanent
> platform name is selected. It is **not a final name**. All references to it in this repository,
> website, and documentation are temporary and will be updated once a name is confirmed.

An active U.S. political platform in development, organized around policy foundations. The live site is at **https://alistardust.github.io/freedom-and-dignity-project/**.

## What's in this repository

```text
docs/               Website — served by GitHub Pages
  assets/           Shared CSS, JS, and images
  policy/           Policy area HTML pages
  compare/          Party comparison pages
policy/             All policy content
  briefing-pack.md  Condensed project context for AI brainstorming sessions
  catalog/          Policy catalog (SQLite), schema, ID docs, citation audit
  foundations/      Foundation values, framing, and platform-statement
    pillars/        Narrative markdown source (per-policy-area prose, pre-generation)
  policyos/         PolicyOS system rules layer
  proposals/        Proposed foundational documents
    rights/         New Bill of Rights, Workers' Rights, Declaration of Indigenous Rights
  research/         Background research documents (constitutional review, senate reform, per-policy-area)
scripts/            Import, generation, and maintenance scripts
tests/              Unit tests (Vitest) and E2E tests (Playwright/Firefox)
AGENTS.md           Codex CLI instruction file
system_rules.md     Cross-domain system rule architecture
```

## Current state

- **Policy areas:** Active policy area pages across the project foundations — see [`.github/current-state.md`](.github/current-state.md) for the current registry.
- **Plain language:** All positions have plain-language summaries
- **Citations:** Inline APA citations across all policy area pages
- **Policy card audit:** Complete — all cards are now in included status

For detailed status, see [`.github/current-state.md`](.github/current-state.md).

## Research

Foundational research documents live in `policy/research/`:

- `us-constitution-adversarial-review.md` — structural failures, loopholes, and exploitation vectors in the U.S. Constitution (incl. *Trump v. United States*, 2024)
- `new-bill-of-rights-adversarial-review.md` — per-amendment adversarial analysis of the project's proposed New Bill of Rights
- `senate-reform-research.md` — malapportionment data, filibuster history, reform proposals, and comparative democracy analysis
- `research/` — per-policy-area background research used to draft policy cards

## Contributing

The best place to start is the **[Get Involved](https://alistardust.github.io/freedom-and-dignity-project/get-involved.html)** page on the live site.

For technical contributors:
- Policy content lives in `docs/policy/*.html` — each policy area page has a structured set of policy cards with `XXXX-XXXX-0000` IDs
- All factual claims require citations that follow `CODING_STANDARDS.md`
- All policy additions must follow the standards in `.github/copilot-instructions.md`
- Run `npm run test:unit` before committing; run `npm run test:e2e` after any HTML/JS/CSS change

**Scripts:**

| Command | What it does |
|---|---|
| `npm run test:unit` | Vitest unit tests — run before every commit |
| `npm run test:e2e` | Playwright E2E tests — run after HTML/JS/CSS changes |
| `npm run serve` | Serve `docs/` locally at port 5500 |
| `npm run briefing-pack` | Regenerate `policy/briefing-pack.md` dynamic sections manually |
| `python3 scripts/update-briefing-pack.py` | Same as above — also runs automatically via pre-commit hook |
| `python3 scripts/migrate-policyos-to-db.py` | Initial setup: parse PolicyOS markdown + CSV into DB tables; init data.js sentinels |
| `python3 scripts/generate-policyos.py` | Regenerate `docs/policyos.html` and fill `data.js` PolicyOS sentinels from DB |

Git hooks are stored in `.githooks/` (tracked) and activated by the `prepare` npm script. Running `npm install` once after cloning is enough to set them up.

For non-technical contributors, the Get Involved page has a link to the project Discord where policy review and rewriting work is coordinated.

## AI use

This platform was built with significant AI assistance to make institutional-scale work possible without institutional resources. Everything AI produced is a starting draft — the long-term goal is human review, rewriting, and progressive replacement of AI-generated content. See the [AI transparency page](https://alistardust.github.io/freedom-and-dignity-project/about-ai.html) for the full account.
