# The Foundations

## The Bigger Frame

This project is, at its core, a rights framework.

The Bill of Rights tradition told government what it could *not* do to you: freedom of speech, freedom from unreasonable search, and due process. Essential, still unfinished.

Franklin Roosevelt proposed an economic rights framework: a job, a living wage, a decent home, healthcare, education, and protection from want and fear. He called them the conditions of true freedom. They remain unfinished.

This project completes that work — and extends it into a century Roosevelt could not have imagined: a world of algorithmic control, mass digital surveillance, climate collapse, and rights under assault from both state power and private concentration.

The foundations are not just policy themes. They are **rights categories**:

- **Accountable Power** — the right to a government that answers to law
- **Clean Democracy** — the right to a government that answers to people
- **Equal Justice** — the right to equal treatment under that law
- **Real Freedom** — the right to live without coercion, surveillance, or weapons of war
- **Freedom to Thrive** — the right to the material conditions that make freedom real

---

This project is organized in layered sources.

**Foundations** are the core values — the moral and political commitments that define what this project believes. They are written to be public-facing, accessible, and resonant. They explain *why* the work matters before getting into *what* must change.

**Pillars** are policy domains where those values get translated into concrete rules, institutional design, and enforceable requirements. Each pillar belongs to a foundation, with limited shared cases. Pillar source markdown lives as a subdirectory of its foundation directory (e.g., `accountable_power/executive_power/`).

Reading the foundations is the right way to understand the project. They are the "why." The pillars are the "how."

---

| Foundation | Core Belief | Pillars |
|---|---|---|
| [Accountable Power](accountable_power/values.md) | No actor, whether president, judge, agency, or party, is above the law or beyond accountability. | Executive Power, Checks & Balances, Term Limits & Fitness, Courts & Judicial System, Administrative State, Legislative Reform |
| [Clean Democracy](clean_democracy/values.md) | Government must answer to people, not to money, corporations, or concentrated private power. | Elections & Representation, Anti-Corruption, Antitrust & Corporate Power, Information & Media |
| [Equal Justice](equal_justice/values.md) | The law must apply equally to everyone, and justice must be fair, humane, and consistent regardless of wealth, race, or status. | Equal Justice & Policing, Immigration, Rights & Civil Liberties, Foreign Policy |
| [Real Freedom](real_freedom/values.md) | Rights must be explicit, enforceable, and protected — including privacy, bodily autonomy, digital rights, and the right to safety from weapons of war. | Gun Policy, Technology & AI, Consumer Rights, Rights & Civil Liberties* |
| [Freedom to Thrive](freedom_to_thrive/values.md) | Real freedom requires material security. Healthcare, economic opportunity, a clean environment, and a fair wage are not luxuries — they are the conditions of a free life. | Healthcare, Taxation & Wealth, Environment & Agriculture, Education, Labor & Workers' Rights, Housing, Infrastructure & Public Goods, Science, Technology & Space |

---

## Directory structure

Each foundation directory contains:
- `values.md` — the foundation's moral and political commitments
- `pillars.md` — index of pillar descriptions with links
- A subdirectory per pillar (e.g., `accountable_power/executive_power/`)

Each pillar subdirectory contains:
- `overview.md` — public-facing narrative: why this area matters and what the platform stands for
- `policy.md` — detailed policy positions by family; source for rule cards in `docs/pillars/<slug>.html`

---

*Note: Rights & Civil Liberties is shared between Equal Justice (primary) and Real Freedom. Its markdown source lives at `equal_justice/rights_and_civil_liberties/`. Real Freedom references it by relative path.*
