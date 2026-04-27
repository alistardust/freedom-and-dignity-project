# Policy ID Schema — v2 Format

> **Status:** Active. This document supersedes all prior ID format descriptions.
> The v2 format was introduced during the Phase 1 → Phase 2 catalog migration.

---

## §1 ID Format

### Regex

```
^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$
```

### Structure

```
HLTH-COVR-0001
│    │    │
│    │    └── Sequence number (0001–9999), zero-padded, scoped per domain + subdomain
│    └──────── Subdomain code (exactly 4 uppercase letters)
└───────────── Domain code (exactly 4 uppercase letters)
```

### Examples

| v2 ID | Domain | Subdomain | Meaning |
|-------|--------|-----------|---------|
| `HLTH-COVR-0001` | Healthcare | Coverage | Universal coverage for citizens |
| `EDUC-STDS-0003` | Education | Standards | Academic standards policy |
| `XDOM-GOVN-0001` | Cross-domain | Governance | Cross-pillar governance rule |
| `TECH-AINL-0007` | Technology & AI | Artificial intelligence | AI liability framework |
| `EXEC-AMND-0001` | Executive Power | 25th Amendment | Presidential succession |

### Terminology

- **Domain** — the policy pillar that owns this position (4-char uppercase)
- **Subdomain** — the policy family or topic within the pillar (4-char uppercase)
- **Sequence** — monotonically increasing integer within each (domain, subdomain) pair, starting at `0001`
- **Position** — a single canonical policy stance, identified uniquely by its ID

### Format invariants

1. All three segments are always present and separated by hyphens.
2. The domain and subdomain segments contain **only uppercase ASCII letters** (A–Z).
3. The sequence segment contains **exactly 4 decimal digits**, zero-padded.
4. IDs are case-sensitive; lowercase variants are invalid.
5. Sequences are stable once assigned — a position's ID never changes unless explicitly deprecated and superseded.

---

## §2 Domain Codes

There are **25 canonical domain codes**, one per policy pillar. The `XDOM` domain is defined in the schema but holds zero migrated positions — it is reserved for future positions that genuinely cannot be attributed to any single pillar after review. Every current position belongs to exactly one pillar domain.

| Code | Pillar Name | `data.js` ID | HTML File |
|------|------------|--------------|-----------|
| `ADMN` | Administrative State | `administrative-state` | `pillars/administrative-state.html` |
| `ANTR` | Antitrust & Corporate Power | `antitrust-and-corporate-power` | `pillars/antitrust-and-corporate-power.html` |
| `CHKS` | Checks & Balances | `checks-and-balances` | `pillars/checks-and-balances.html` |
| `CNSR` | Consumer Rights | `consumer-rights` | `pillars/consumer-rights.html` |
| `CORT` | Courts & Judicial System | `courts-and-judicial-system` | `pillars/courts-and-judicial-system.html` |
| `CRPT` | Anti-Corruption | `anti-corruption` | `pillars/anti-corruption.html` |
| `EDUC` | Education | `education` | `pillars/education.html` |
| `ELEC` | Elections & Representation | `elections-and-representation` | `pillars/elections-and-representation.html` |
| `ENVR` | Environment & Agriculture | `environment-and-agriculture` | `pillars/environment-and-agriculture.html` |
| `EXEC` | Executive Power | `executive-power` | `pillars/executive-power.html` |
| `FPOL` | Foreign Policy | `foreign-policy` | `pillars/foreign-policy.html` |
| `GUNS` | Gun Policy | `gun-policy` | `pillars/gun-policy.html` |
| `HLTH` | Healthcare | `healthcare` | `pillars/healthcare.html` |
| `HOUS` | Housing | `housing` | `pillars/housing.html` |
| `IMMG` | Immigration | `immigration` | `pillars/immigration.html` |
| `INFR` | Infrastructure & Public Goods | `infrastructure-and-public-goods` | `pillars/infrastructure-and-public-goods.html` |
| `JUST` | Equal Justice & Policing | `equal-justice-and-policing` | `pillars/equal-justice-and-policing.html` |
| `LABR` | Labor & Workers' Rights | `labor-and-workers-rights` | `pillars/labor-and-workers-rights.html` |
| `LEGL` | Legislative Reform | `legislative-reform` | `pillars/legislative-reform.html` |
| `MDIA` | Information & Media | `information-and-media` | `pillars/information-and-media.html` |
| `RGHT` | Rights & Civil Liberties | `rights-and-civil-liberties` | `pillars/rights-and-civil-liberties.html` |
| `SCIS` | Science, Technology & Space | `science-technology-space` | `pillars/science-technology-space.html` |
| `TAXN` | Taxation & Wealth | `taxation-and-wealth` | `pillars/taxation-and-wealth.html` |
| `TECH` | Technology & AI | `technology-and-ai` | `pillars/technology-and-ai.html` |
| `TERM` | Term Limits & Fitness | `term-limits-and-fitness` | `pillars/term-limits-and-fitness.html` |
| `XDOM` | Cross-Domain | _(reserved — no current positions)_ | _(none — not a pillar)_ |

> **Note:** `ANTR` (Antitrust & Corporate Power) and `SCIS` (Science, Technology & Space) are registered pillar domains with HTML pages but currently have **zero policy positions** in the catalog. Content for these pillars needs to be authored.

### v1 → v2 domain code mapping

The v2 format consolidates 32 v1 HTML domain codes into 25 canonical pillar codes. Every position was assigned to its correct single pillar — no content was collapsed into `XDOM`. For codes that were ambiguous (appearing in multiple pillar files), the position was assigned to the domain of the HTML file it lives in.

| v1 Code | v2 Code | Decision |
|---------|---------|----------|
| `ADM` | `ADMN` | Direct rename |
| `AGR` | `ENVR` | Agriculture is part of the environment/agriculture pillar |
| `CIV` | `ADMN` | Vital records access — unambiguously administrative state |
| `CON` | `CNSR` | Consumer rights rename |
| `COR` | `CRPT` | Anti-corruption rename |
| `ECO` | _(by file)_ | Each card assigned to its HTML-file pillar (`TAXN` or `LABR`) |
| `EDU` | `EDUC` | Direct rename |
| `ELE` | `ELEC` | Elections rename |
| `ENV` | `ENVR` | Direct rename |
| `EWT` | `ENVR` | Extended producer responsibility / lifecycle — part of environment |
| `EXE` | `EXEC` | Executive power rename |
| `FPL` | `FPOL` | Foreign policy rename |
| `GOV` | _(by file)_ | Each card assigned to its HTML-file pillar (`CHKS` or `EXEC`) |
| `GUN` | `GUNS` | Direct rename |
| `HLT` | `HLTH` | Healthcare rename |
| `HOU` | `HOUS` | Housing rename |
| `IMM` | `IMMG` | Immigration rename |
| `INF` | `INFR` | Infrastructure rename |
| `JUD` | `CORT` | Courts/judicial rename |
| `JUS` | `JUST` | Equal justice rename |
| `LAB` | `LABR` | Labor rename |
| `LEG` | `LEGL` | Legislative reform rename |
| `MED` | `MDIA` | Information/media rename |
| `OVR` | `CHKS` | Independent oversight boards — all in checks-and-balances |
| `PAT` | `TECH` | Patent/IP reform — all cards are in technology-and-ai pillar |
| `RGT` | `RGHT` | Rights rename |
| `RPR` | `CNSR` | **Right to Repair** (not reparations) — all cards in consumer-rights |
| `STS` | `SCIS` | Science/Technology/Space rename |
| `SYS` | `CHKS` | Systemic/structural reform — all cards in checks-and-balances |
| `TAX` | `TAXN` | Taxation rename |
| `TEC` | `TECH` | Technology/AI rename |
| `TRM` | `TERM` | Term limits rename |

---

## §3 Subdomain Codes

Subdomain codes are exactly 4 uppercase letters, scoped to their parent domain. The same 4-char code may appear in multiple domains if the conceptual family is analogous (e.g. `REGS` for "Regulations" in both `ADMN` and `ENVR`). The `subdomains` table stores the canonical name for each `(code, domain)` pair.

### Expansion rules (v1 → v2)

| v1 Length | Rule | Example |
|-----------|------|---------|
| 2 chars | Explicit expansion map (see below) | `AI` → `AINL` |
| 3 chars | Explicit map if listed; otherwise append `S` | `COV` → `COVR`; `AGY` → `AGYS` |
| 4 chars | Kept as-is | `ANTI` → `ANTI` |
| Non-alpha | Explicit semantic remap | `25A` → `AMND`; `S230` → `SECT` |

### 2-char explicit expansions

| v1 | v2 | Meaning |
|----|----|---------|
| `AI` | `AINL` | Artificial intelligence |
| `DB` | `DBAS` | Database / data systems |
| `IG` | `IGSP` | Inspector General / special oversight |
| `RX` | `RXDG` | Prescription drugs |
| `SS` | `SSCI` | Social Security / civil status |
| `TR` | `TRDE` | Trade |
| `VP` | `VPOF` | Vice President / office |

### 3-char explicit expansions

| v1 | v2 | Meaning |
|----|----|---------|
| `ACC` | `ACCS` | Access |
| `ADM` | `ADML` | Administration |
| `ALG` | `ALGO` | Algorithm |
| `AUD` | `AUDT` | Audit |
| `BEN` | `BENS` | Benefits |
| `CIV` | `CIVL` | Civil |
| `CLM` | `CLMS` | Claims |
| `COV` | `COVR` | Coverage |
| `CRT` | `CRTS` | Courts |
| `DAT` | `DATA` | Data |
| `ENF` | `ENFL` | Enforcement |
| `ETH` | `ETHL` | Ethics |
| `FIN` | `FINC` | Finance |
| `GEN` | `GENL` | General |
| `GOV` | `GOVN` | Governance |
| `INT` | `INTL` | International |
| `LAW` | `LAWS` | Law |
| `MED` | `MEDA` | Media |
| `NET` | `NETS` | Network |
| `OVR` | `OVRG` | Oversight |
| `POL` | `POLC` | Police / policy |
| `PRV` | `PRIV` | Privacy |
| `PUB` | `PUBL` | Public |
| `REG` | `REGS` | Regulation |
| `RGT` | `RGTS` | Rights |
| `SEC` | `SECU` | Security |
| `STD` | `STDS` | Standards |
| `SUP` | `SUPR` | Supreme / support |
| `SYS` | `SYSR` | Systems / reform |
| `TAX` | `TAXS` | Taxes (subdomain of `TAXN`) |
| `TRN` | `TRAN` | Transition |

### Non-alpha remaps

These v1 subdomain codes contained digits and were remapped to all-letter codes:

| v1 | v2 | Domain | Meaning |
|----|----|--------|---------|
| `25A` | `AMND` | `EXEC` | 25th Amendment (presidential succession) |
| `S230` | `SECT` | `MDIA` | Section 230 (platform liability) |

### Querying subdomains

```sql
-- All subdomains for the healthcare pillar
SELECT code, name FROM subdomains WHERE domain = 'HLTH' ORDER BY code;

-- All positions in the AI subdomain of healthcare
SELECT id, short_title FROM positions WHERE domain = 'HLTH' AND subdomain = 'AINL' ORDER BY seq;
```

---

## §4 Cross-Domain Positions

`XDOM` is a **reserved domain** for policy positions that genuinely span multiple pillars and cannot be correctly attributed to any single one. As of the v2 migration, **no positions carry the `XDOM` domain** — every migrated position was assigned to its correct single pillar after careful review.

### When to use XDOM

Use `XDOM` only when a position:
- Is substantively inseparable from 2 or more pillar areas (not merely *related* to them), **and**
- Would require meaningful distortion to file under any single pillar

A position appearing in multiple pillar HTML files is not automatically cross-domain. In most cases the correct fix is to pick the primary pillar and add a cross-reference, not to use `XDOM`.

### The `position_pillar_appearances` table

Every position has at least one row in `position_pillar_appearances` indicating which pillar it belongs to. A future `XDOM` position that genuinely appears in multiple pillars would have one row per pillar.

```sql
-- All positions that appear in 2 or more pillars
SELECT p.id, p.short_title, COUNT(a.pillar_domain) AS pillar_count
FROM positions p
JOIN position_pillar_appearances a ON p.id = a.position_id
GROUP BY p.id
HAVING pillar_count > 1
ORDER BY pillar_count DESC;
```

### Authoring an XDOM position (future use)

1. Insert the position into `positions` with `domain = 'XDOM'` and `is_cross_domain = 1`.
2. Insert one row into `position_pillar_appearances` for each pillar it belongs to.
3. Insert one row into `subdomains` for `(new_sub_code, 'XDOM')` if the subdomain is new.
4. Do **not** create duplicate positions in the individual pillar domains.

---

## §5 Status Values

Every position carries one of four status values:

| Status | Meaning |
|--------|---------|
| `CANONICAL` | Adopted, active policy position — the default for all migrated records |
| `PROPOSED` | Under consideration; not yet adopted |
| `DEPRECATED` | Superseded or withdrawn; retained for provenance only |
| `REVIEW` | Flagged during migration for human review — may have ambiguous domain mapping, unparseable ID, or other anomaly |

### Lifecycle

```
PROPOSED → CANONICAL → DEPRECATED
                ↑
           REVIEW (during migration only)
```

Positions set to `REVIEW` during migration should be examined and moved to `CANONICAL`, `PROPOSED`, or `DEPRECATED` before Phase 2 goes live.

---

## §6 Legacy ID Cross-Reference

Every v1 ID is tracked in the `legacy_id_map` table.

```sql
-- Look up the new ID for a known v1 ID
SELECT new_id, source, notes FROM legacy_id_map WHERE old_id = 'HLT-COV-001';

-- Find all v2 IDs that came from a specific v1 subdomain family
SELECT l.old_id, l.new_id, p.short_title
FROM legacy_id_map l
JOIN positions p ON l.new_id = p.id
WHERE l.old_id LIKE 'HLT-AI-%'
ORDER BY l.old_id;
```

### Source field values

| Value | Meaning |
|-------|---------|
| `db` | The v1 ID existed only in `policy_catalog.sqlite` |
| `html` | The v1 ID existed only in `docs/pillars/*.html` |
| `both` | The v1 ID existed in both the DB and the HTML |

### Lettered suffix variants

Eight v1 IDs carried letter suffixes to denote sub-positions of a parent rule (e.g. `HLT-AI-007A` through `HLT-AI-007G`). Each variant was treated as an independent canonical position and assigned its own sequential v2 ID. The parent-child relationship is preserved only in the `legacy_id_map` via the old-ID ordering.

| v1 ID | v2 ID |
|-------|-------|
| `HLT-AI-007A` | `HLTH-AINL-0008` |
| `HLT-AI-007B` | `HLTH-AINL-0009` |
| `HLT-AI-007C` | `HLTH-AINL-0010` |
| `HLT-AI-007D` | `HLTH-AINL-0011` |
| `HLT-AI-007E` | `HLTH-AINL-0012` |
| `HLT-AI-007F` | `HLTH-AINL-0013` |
| `HLT-AI-007G` | `HLTH-AINL-0014` |
| `TEC-MIL-005A` | `TECH-MILS-0006` |

---

## §7 Migration Notes

### What changed

| Area | v1 | v2 |
|------|----|----|
| Domain code length | 3 chars | 4 chars |
| Subdomain code length | 2–5 chars (mixed) | Exactly 4 chars |
| Sequence length | 3 digits (`001`) | 4 digits (`0001`) |
| Number of canonical domains | 32 HTML codes | 26 codes (25 pillars + XDOM) |
| Non-alpha subdomains | Present (`25A`, `S230`) | Remapped to all-letter codes |
| Cross-domain tracking | Not formalized | `position_pillar_appearances` table |
| Multi-source provenance | Not tracked | `legacy_id_map.source` field |

### Why

The v1 format grew organically: domain and subdomain codes were assigned ad hoc as new pillars were introduced, resulting in inconsistent lengths, digit-containing codes that broke regex validation, and multiple domain codes pointing at the same pillar. The v2 format enforces a uniform structure that can be validated with a single regex, accommodates up to 9,999 positions per subdomain (vs. 999 in v1), and formalizes cross-domain positions.

### When

The migration was performed during the Phase 1 → Phase 2 transition of the Freedom and Dignity Project policy platform. The source data was:

- `data/policy_catalog.sqlite` — 1,554 v1 positions
- `docs/pillars/*.html` — 2,935 policy cards (2,759 unique IDs)
- Total after merge and deduplication: **2,783 canonical positions**

### Idempotency

`scripts/build-catalog-v2.py` is idempotent: re-running it drops and recreates `data/policy_catalog_v2.sqlite`. The output DB is generated, not hand-edited. All content changes must be made to the source data (`policy_catalog.sqlite` or the pillar HTML), then the v2 DB regenerated.

### Lookup during transition

While both v1 and v2 IDs are in use (Phase 1), use `legacy_id_map` to translate:

```sql
-- Translate any v1 ID to v2
SELECT new_id FROM legacy_id_map WHERE old_id = ?;

-- Reverse lookup: find the v1 ID(s) for a v2 position
SELECT old_id, source FROM legacy_id_map WHERE new_id = ?;
```

After Phase 2 is complete and all HTML is regenerated from the DB, the v1 IDs will be retired. The `legacy_id_map` table will be retained permanently for provenance.
