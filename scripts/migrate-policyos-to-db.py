#!/usr/bin/env python3
"""migrate-policyos-to-db.py

Populates four PolicyOS tables in policy_catalog_v2.sqlite from the three
locked markdown sources and the inheritance matrix CSV. Idempotent.

Run from repo root:
  python3 scripts/migrate-policyos-to-db.py

Then run the generation script:
  python3 scripts/generate-policyos.py
"""
import csv
import re
import sqlite3
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DB_PATH      = REPO / "policy/catalog/policy_catalog_v2.sqlite"
DATA_JS      = REPO / "docs/assets/js/data.js"
RULES_MD     = REPO / "policy/policyos/policyos_1_0_rules_proposal.md"
AUTHORING_MD = REPO / "policy/policyos/policyos_authoring_os_v1.md"
VALUES_MD    = REPO / "policy/policyos/policyos_platform_values_v1.md"
MATRIX_CSV   = REPO / "policy/policyos/policyos_1_0_inheritance_matrix.csv"

# ── Static canonical metadata (locked) ─────────────────────────────

LAYERS = [
    ("values",     "Platform Values",    "The moral and political anchor for all rules.",                              1),
    ("principles", "System Principles",  "Cross-platform design rules governing how policy must work.",               2),
    ("authoring",  "Authoring OS",       "How policy must be written, tested, scoped, enforced, and maintained.",     3),
]

# (code, layer_id, label, anchor_id, summary, sort_order)
FAMILIES = [
    ("KERN", "principles", "Core Kernel",                    "plos-kern", "Universal rules that apply to every pillar.",                                                              1),
    ("GEOG", "principles", "Geography & Access",             "plos-geog", "Rights and services may not vary by geography in ways that create unequal classes of people.",            2),
    ("FEDR", "principles", "Federalism & Anti-Centralization","plos-fedr","Power must be distributed to prevent single-point failure and abuse.",                                    3),
    ("REGD", "principles", "Regulatory Design",              "plos-regd", "Regulation must protect the public interest and resist capture by the regulated.",                        4),
    ("ENFA", "principles", "Enforcement Architecture",       "plos-enfa", "Enforcement must be designed, not assumed; penalties must be proportionate and actionable.",             5),
    ("AIGV", "principles", "AI Governance",                  "plos-aigv", "AI and algorithmic systems require transparency, accountability, and human oversight.",                  6),
    ("ECOL", "principles", "Ecological Habitability",        "plos-ecol", "Policy must not degrade the ecological conditions for human survival and flourishing.",                  7),
    ("THRV", "principles", "Material Security",              "plos-thrv", "Policy must actively secure the material preconditions for a dignified life.",                           8),
    ("DEMO", "principles", "Democratic Participation",       "plos-demo", "Policy must protect and expand the practical capacity for civic participation.",                         9),
    ("PRIV", "principles", "Privacy & Surveillance",         "plos-priv", "Policy must protect persons against surveillance, data exploitation, and coercive monitoring.",         10),
    ("ECON", "principles", "Economic Domination",            "plos-econ", "Policy must prevent and correct dangerous concentrations of private economic power.",                   11),
    ("NORM", "authoring",  "Normative Alignment",            "paos-norm", "Rules must be grounded in and aligned with the platform's core values.",                               12),
    ("AUTH", "authoring",  "Rule Construction",              "paos-auth", "Rules must be structurally complete, precise, and enforceable.",                                        13),
    ("TEST", "authoring",  "Validation & Adversarial Review","paos-test", "Rules must be reviewed for gaps, loopholes, edge cases, and abuse paths before adoption.",             14),
    ("ENFC", "authoring",  "Enforcement Design",             "paos-enfc", "Rules must specify enforcement actors, triggers, escalation, and remedies.",                           15),
    ("PLAC", "authoring",  "Scope & Placement",              "paos-plac", "Rules must be placed at the correct scope level -- not too broad, not too narrow.",                    16),
    ("MAINT","authoring",  "Maintenance & Revision",         "paos-maint","Rules must have review cadences and mechanisms for revision, deprecation, and replacement.",           17),
]

# ── DB setup ────────────────────────────────────────────────────────

DDL = """
CREATE TABLE IF NOT EXISTS policyos_layers (
    id         TEXT PRIMARY KEY,
    label      TEXT NOT NULL,
    summary    TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS policyos_families (
    code       TEXT PRIMARY KEY,
    layer_id   TEXT NOT NULL REFERENCES policyos_layers(id),
    label      TEXT NOT NULL,
    anchor_id  TEXT NOT NULL,
    summary    TEXT NOT NULL,
    sort_order INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS policyos_rules (
    id           TEXT PRIMARY KEY,
    family_code  TEXT REFERENCES policyos_families(code),
    layer_id     TEXT REFERENCES policyos_layers(id),
    sort_order   INTEGER NOT NULL,
    rule_text    TEXT NOT NULL,
    value_name   TEXT,
    rule_subtype TEXT
);

CREATE TABLE IF NOT EXISTS policyos_pillar_overlays (
    pillar_slug  TEXT NOT NULL,
    family_code  TEXT NOT NULL REFERENCES policyos_families(code),
    overlay_type TEXT NOT NULL,
    notes        TEXT,
    PRIMARY KEY (pillar_slug, family_code)
);
"""

# ── Parsing ─────────────────────────────────────────────────────────

def parse_system_principles(path: Path) -> list[tuple]:
    """Parse PLOS-*-NNNN rules from policyos_1_0_rules_proposal.md.

    Returns list of (id, family_code, layer_id, sort_order, rule_text).
    layer_id is None for System Principles rules (family_code is set instead).
    """
    text = path.read_text(encoding="utf-8")
    family_block_re = re.compile(r'^### `([A-Z]+)`', re.MULTILINE)
    positions = [(m.start(), m.group(1)) for m in family_block_re.finditer(text)]
    rows: list[tuple] = []
    rule_re = re.compile(
        r'^\d+\.\s+`(PLOS-[A-Z]+-\d{4})`\n(.*?)(?=^\d+\.\s+`PLOS-|^###|\Z)',
        re.MULTILINE | re.DOTALL
    )
    for i, (start, family_code) in enumerate(positions):
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        block = text[start:end]
        for m in rule_re.finditer(block):
            rule_id    = m.group(1)
            rule_text  = m.group(2).strip()
            sort_order = int(rule_id.split("-")[-1])
            rows.append((rule_id, family_code, None, sort_order, rule_text))
    return rows


def parse_authoring_os(path: Path) -> list[tuple]:
    """Parse PAOS-*-NNNN rules from policyos_authoring_os_v1.md.

    Returns list of (id, family_code, layer_id, sort_order, rule_text).
    layer_id is None for Authoring OS rules (family_code is set instead).
    """
    text = path.read_text(encoding="utf-8")
    rule_re = re.compile(r'^- `(PAOS-([A-Z]+)-(\d{4}))` (.+)$', re.MULTILINE)
    rows: list[tuple] = []
    for m in rule_re.finditer(text):
        rule_id     = m.group(1)
        family_code = m.group(2)
        sort_order  = int(m.group(3))
        rule_text   = m.group(4).strip()
        rows.append((rule_id, family_code, None, sort_order, rule_text))
    return rows


def parse_platform_values(path: Path) -> list[tuple]:
    """Parse floor/duty pairs from policyos_platform_values_v1.md.

    Returns list of (id, family_code, layer_id, sort_order, rule_text, value_name, rule_subtype).
    family_code is None for Platform Values rows; layer_id is 'values'.
    """
    text = path.read_text(encoding="utf-8")
    section_re = re.compile(
        r'^### (\d+)\. (.+?)\n(.*?)(?=^### \d+\.|\Z)',
        re.MULTILINE | re.DOTALL
    )
    floor_re = re.compile(r'Policy-writing floor:\n(.*?)(?=\n\nPolicy-writing duty:)', re.DOTALL)
    duty_re  = re.compile(r'Policy-writing duty:\n(.*?)(?=\n\n|\Z)', re.DOTALL)
    rows: list[tuple] = []
    for m in section_re.finditer(text):
        n          = int(m.group(1))
        value_name = m.group(2).strip()
        body       = m.group(3)
        floor_m    = floor_re.search(body)
        duty_m     = duty_re.search(body)
        if floor_m:
            rows.append((
                f"VAL-{n:04d}-FLOOR", None, "values",
                n * 10 - 1, floor_m.group(1).strip(),
                value_name, "floor"
            ))
        if duty_m:
            rows.append((
                f"VAL-{n:04d}-DUTY", None, "values",
                n * 10, duty_m.group(1).strip(),
                value_name, "duty"
            ))
    return rows


def parse_pillar_overlays(path: Path) -> list[tuple]:
    """Parse pillar_slug, family_code, overlay_type rows from CSV.

    Returns list of (pillar_slug, family_code, overlay_type).
    """
    rows: list[tuple] = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row["pillar_slug"].strip()
            for fam in row["mandatory_families"].split("|"):
                fam = fam.strip()
                if fam:
                    rows.append((slug, fam, "mandatory"))
            for fam in row["conditional_families"].split("|"):
                fam = fam.strip()
                if fam:
                    rows.append((slug, fam, "conditional"))
    return rows


# ── Sentinel init ────────────────────────────────────────────────────

SENTINEL_BLOCK = """
// %%POLICYOS-FAMILIES-BEGIN%%
siteData.policyosFamilies = [];
// %%POLICYOS-FAMILIES-END%%
// %%POLICYOS-OVERLAYS-BEGIN%%
siteData.policyosOverlays = {};
// %%POLICYOS-OVERLAYS-END%%
"""

def init_sentinels(data_js: Path) -> None:
    """Append sentinel comment blocks to data.js if not already present."""
    src = data_js.read_text(encoding="utf-8")
    if "%%POLICYOS-FAMILIES-BEGIN%%" in src:
        print("Sentinels already present in data.js -- skipping.")
        return
    anchor = "window.siteData = siteData;"
    if anchor not in src:
        print(f"ERROR: anchor '{anchor}' not found in {data_js}", file=sys.stderr)
        sys.exit(1)
    updated = src.replace(anchor, anchor + SENTINEL_BLOCK, 1)
    data_js.write_text(updated, encoding="utf-8")
    print(f"Sentinel blocks appended to {data_js}.")


# ── Main ─────────────────────────────────────────────────────────────

def main() -> None:
    con = sqlite3.connect(DB_PATH)
    con.execute("PRAGMA foreign_keys = ON")
    cur = con.cursor()

    cur.executescript(DDL)

    cur.executemany(
        "INSERT OR REPLACE INTO policyos_layers VALUES (?,?,?,?)",
        LAYERS
    )

    cur.executemany(
        "INSERT OR REPLACE INTO policyos_families VALUES (?,?,?,?,?,?)",
        FAMILIES
    )

    sp_rows = parse_system_principles(RULES_MD)
    cur.executemany(
        "INSERT OR REPLACE INTO policyos_rules(id,family_code,layer_id,sort_order,rule_text) VALUES (?,?,?,?,?)",
        sp_rows
    )
    print(f"System Principles: {len(sp_rows)} rules inserted.")

    ao_rows = parse_authoring_os(AUTHORING_MD)
    cur.executemany(
        "INSERT OR REPLACE INTO policyos_rules(id,family_code,layer_id,sort_order,rule_text) VALUES (?,?,?,?,?)",
        ao_rows
    )
    print(f"Authoring OS: {len(ao_rows)} rules inserted.")

    pv_rows = parse_platform_values(VALUES_MD)
    cur.executemany(
        "INSERT OR REPLACE INTO policyos_rules(id,family_code,layer_id,sort_order,rule_text,value_name,rule_subtype) VALUES (?,?,?,?,?,?,?)",
        pv_rows
    )
    print(f"Platform Values: {len(pv_rows)} floor/duty rows inserted.")

    valid_codes = {r[0] for r in cur.execute("SELECT code FROM policyos_families").fetchall()}
    overlay_rows = parse_pillar_overlays(MATRIX_CSV)
    bad = [(s, f) for s, f, _ in overlay_rows if f not in valid_codes]
    if bad:
        print(f"ERROR: unknown family codes in overlay CSV: {bad}", file=sys.stderr)
        con.rollback()
        sys.exit(1)
    cur.executemany(
        "INSERT OR REPLACE INTO policyos_pillar_overlays(pillar_slug,family_code,overlay_type) VALUES (?,?,?)",
        overlay_rows
    )
    print(f"Pillar overlays: {len(overlay_rows)} rows inserted.")

    con.commit()
    con.close()
    print("DB migration complete.")

    init_sentinels(DATA_JS)


if __name__ == "__main__":
    main()
