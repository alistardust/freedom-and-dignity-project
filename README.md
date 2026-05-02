# Freedom and Dignity Project

> ⚠️ **Name Notice — Placeholder Name**
>
> "Freedom and Dignity Project" is a working name derived from the repository slug while a permanent
> platform name is selected. It is **not a final name**. All references to it in this repository,
> website, and documentation are temporary and will be updated once a name is confirmed.

An active U.S. political platform in development, organized around 25 policy pillars and 5 foundations. The live site is at **https://alistardust.github.io/freedom-and-dignity-project/**.

## What's in this repository

```text
docs/               Website — served by GitHub Pages
  assets/           Shared CSS, JS, and images
  pillars/          25 pillar HTML pages
  compare/          Party comparison pages
policy/             All policy content
  catalog/          Policy catalog (SQLite), schema, ID docs, citation audit
  foundations/      Foundation values, framing, and platform-statement
    pillars/        Narrative markdown source (per-pillar prose, pre-generation)
  policyos/         PolicyOS system rules layer
  proposals/        Proposed foundational documents
    rights/         New Bill of Rights, Workers' Rights, Declaration of Indigenous Rights
scripts/            Import, generation, and maintenance scripts
tests/              Unit tests (Vitest) and E2E tests (Playwright/Firefox)
AGENTS.md           Codex CLI instruction file
system_rules.md     Cross-domain system rule architecture
```

## Current state

- **Pillars:** 25 active pillar pages across 5 foundations
- **Policy positions:** 3,810 canonical positions in `policy/catalog/policy_catalog_v2.sqlite`
- **Plain language:** All positions have plain-language summaries
- **Citations:** Inline APA citations across all pillar pages

For detailed status, see [`.github/current-state.md`](.github/current-state.md).

## Contributing

The best place to start is the **[Get Involved](https://alistardust.github.io/freedom-and-dignity-project/join.html)** page on the live site.

For technical contributors:
- Policy content lives in `docs/pillars/*.html` — each pillar page has a structured set of policy cards with `XXXX-XXXX-0000` IDs
- All factual claims require APA 7th edition citations — see `CODING_STANDARDS.md`
- All policy additions must follow the standards in `.github/copilot-instructions.md`
- Run `npm run test:unit` before committing; run `npm run test:e2e` after any HTML/JS/CSS change

For non-technical contributors, the Get Involved page has a link to the project Discord where policy review and rewriting work is coordinated.

## AI use

This platform was built with significant AI assistance to make institutional-scale work possible without institutional resources. Everything AI produced is a starting draft — the long-term goal is human review, rewriting, and progressive replacement of AI-generated content. See the [AI transparency page](https://alistardust.github.io/freedom-and-dignity-project/about-ai.html) for the full account.
