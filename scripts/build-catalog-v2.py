#!/usr/bin/env python3
"""
build-catalog-v2.py — Migrate Freedom and Dignity Project policy positions
from the v1 3-char/3-digit ID format to the v2 4-char/4-digit ID format.

Usage:
    python3 scripts/build-catalog-v2.py [--dry-run] [--output PATH] [--report PATH]
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path
from typing import NamedTuple

from bs4 import BeautifulSoup


# ---------------------------------------------------------------------------
# Constants / mappings
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
HTML_DIR = REPO_ROOT / "docs" / "pillars"
SOURCE_DB = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"

# Old 3-char domain → new 4-char domain code
DOMAIN_MAP: dict[str, str] = {
    "ADM": "ADMN",
    "AGR": "ENVR",
    # CIV = vital records access — unambiguously administrative state
    "CIV": "ADMN",
    "CON": "CNSR",
    "COR": "CRPT",
    # ECO = economic positions that live in specific pillar files; resolve per-card by HTML file
    "ECO": "_BY_FILE_",
    "EDU": "EDUC",
    "ELE": "ELEC",
    "ENV": "ENVR",
    "EWT": "ENVR",
    "EXE": "EXEC",
    "FPL": "FPOL",
    # GOV = governance positions split across checks-and-balances and executive-power; resolve per-card
    "GOV": "_BY_FILE_",
    "GUN": "GUNS",
    "HLT": "HLTH",
    "HOU": "HOUS",
    "IMM": "IMMG",
    "INF": "INFR",
    "JUD": "CORT",
    "JUS": "JUST",
    "LAB": "LABR",
    "LEG": "LEGL",
    "MED": "MDIA",
    # OVR = independent oversight boards — all in checks-and-balances
    "OVR": "CHKS",
    # PAT = patent/IP reform — all in technology-and-ai
    "PAT": "TECH",
    "RGT": "RGHT",
    # RPR = Right to Repair — all in consumer-rights (not reparations)
    "RPR": "CNSR",
    "STS": "SCIS",
    # SYS = systemic/structural reform — all in checks-and-balances
    "SYS": "CHKS",
    "TAX": "TAXN",
    "TEC": "TECH",
    "TRM": "TERM",
}

# Domain metadata: code → (name, pillar_id, html_file, is_cross_domain)
DOMAIN_META: dict[str, tuple[str, str | None, str | None, int]] = {
    "ADMN": ("administrative_state",          "administrative-state",             "pillars/administrative-state.html",          0),
    "ANTR": ("antitrust_and_corporate_power",  "antitrust-and-corporate-power",    "pillars/antitrust-and-corporate-power.html", 0),
    "CHKS": ("checks_and_balances",            "checks-and-balances",              "pillars/checks-and-balances.html",           0),
    "CNSR": ("consumer_rights",                "consumer-rights",                  "pillars/consumer-rights.html",               0),
    "CORT": ("courts_and_judicial_system",     "courts-and-judicial-system",       "pillars/courts-and-judicial-system.html",    0),
    "CRPT": ("anti_corruption",                "anti-corruption",                  "pillars/anti-corruption.html",               0),
    "EDUC": ("education",                      "education",                        "pillars/education.html",                     0),
    "ELEC": ("elections_and_representation",   "elections-and-representation",     "pillars/elections-and-representation.html",  0),
    "ENVR": ("environment_and_agriculture",    "environment-and-agriculture",      "pillars/environment-and-agriculture.html",   0),
    "EXEC": ("executive_power",                "executive-power",                  "pillars/executive-power.html",               0),
    "FPOL": ("foreign_policy",                 "foreign-policy",                   "pillars/foreign-policy.html",                0),
    "GUNS": ("gun_policy",                     "gun-policy",                       "pillars/gun-policy.html",                    0),
    "HLTH": ("healthcare",                     "healthcare",                       "pillars/healthcare.html",                    0),
    "HOUS": ("housing",                        "housing",                          "pillars/housing.html",                       0),
    "IMMG": ("immigration",                    "immigration",                      "pillars/immigration.html",                   0),
    "INFR": ("infrastructure_and_public_goods","infrastructure-and-public-goods",  "pillars/infrastructure-and-public-goods.html", 0),
    "JUST": ("equal_justice_and_policing",     "equal-justice-and-policing",       "pillars/equal-justice-and-policing.html",    0),
    "LABR": ("labor_and_workers_rights",       "labor-and-workers-rights",         "pillars/labor-and-workers-rights.html",      0),
    "LEGL": ("legislative_reform",             "legislative-reform",               "pillars/legislative-reform.html",            0),
    "MDIA": ("information_and_media",          "information-and-media",            "pillars/information-and-media.html",         0),
    "RGHT": ("rights_and_civil_liberties",     "rights-and-civil-liberties",       "pillars/rights-and-civil-liberties.html",    0),
    "SCIS": ("science_technology_space",       "science-technology-space",         "pillars/science-technology-space.html",      0),
    "TAXN": ("taxation_and_wealth",            "taxation-and-wealth",              "pillars/taxation-and-wealth.html",           0),
    "TECH": ("technology_and_ai",              "technology-and-ai",                "pillars/technology-and-ai.html",             0),
    "TERM": ("term_limits_and_fitness",        "term-limits-and-fitness",          "pillars/term-limits-and-fitness.html",       0),
    "XDOM": ("cross_domain",                   None,                               None,                                         1),
}

# Map from HTML filename stem → canonical domain code (for appearance tracking)
HTML_FILE_TO_DOMAIN: dict[str, str] = {
    "administrative-state":            "ADMN",
    "anti-corruption":                 "CRPT",
    "antitrust-and-corporate-power":   "ANTR",
    "checks-and-balances":             "CHKS",
    "consumer-rights":                 "CNSR",
    "courts-and-judicial-system":      "CORT",
    "education":                       "EDUC",
    "elections-and-representation":    "ELEC",
    "environment-and-agriculture":     "ENVR",
    "equal-justice-and-policing":      "JUST",
    "executive-power":                 "EXEC",
    "foreign-policy":                  "FPOL",
    "gun-policy":                      "GUNS",
    "healthcare":                      "HLTH",
    "housing":                         "HOUS",
    "immigration":                     "IMMG",
    "information-and-media":           "MDIA",
    "infrastructure-and-public-goods": "INFR",
    "labor-and-workers-rights":        "LABR",
    "legislative-reform":              "LEGL",
    "rights-and-civil-liberties":      "RGHT",
    "science-technology-space":        "SCIS",
    "taxation-and-wealth":             "TAXN",
    "technology-and-ai":               "TECH",
    "term-limits-and-fitness":         "TERM",
}

# Explicit 2-char subdomain expansions
SUBDOMAIN_2CHAR: dict[str, str] = {
    "AI": "AINL",
    "DB": "DBAS",
    "IG": "IGSP",
    "RX": "RXDG",
    "SS": "SSCI",
    "TR": "TRDE",
    "VP": "VPOF",
}

# Explicit 3-char subdomain expansions (all others get 'S' appended)
SUBDOMAIN_3CHAR: dict[str, str] = {
    "COV": "COVR",
    "ACC": "ACCS",
    "ENF": "ENFL",
    "SYS": "SYSR",
    "OVR": "OVRG",
    "RGT": "RGTS",
    "GOV": "GOVN",
    "ADM": "ADML",
    "GEN": "GENL",
    "INT": "INTL",
    "MED": "MEDA",
    "REG": "REGS",
    "NET": "NETS",
    "LAW": "LAWS",
    "CRT": "CRTS",
    "DAT": "DATA",
    "FIN": "FINC",
    "PUB": "PUBL",
    "PRV": "PRIV",
    "SEC": "SECU",
    "STD": "STDS",
    "SUP": "SUPR",
    "POL": "POLC",
    "AUD": "AUDT",
    "ALG": "ALGO",
    "ETH": "ETHL",
    "TRN": "TRAN",
    "BEN": "BENS",
    "CLM": "CLMS",
    "CIV": "CIVL",
    "TAX": "TAXS",
}

# 4-char subdomains: keep as-is
SUBDOMAIN_4CHAR_KEEP: set[str] = {"ANTI", "AUTO", "DEBT", "LIFE", "PRES", "RAIL"}

# Non-alpha subdomain codes: numeric or alphanumeric codes that must be
# remapped to all-letter 4-char codes to satisfy the CHECK constraint.
SUBDOMAIN_NONALPHA: dict[str, str] = {
    "25A":  "AMND",   # EXE: 25th Amendment presidential succession procedures
    "S230": "SECT",   # MED: Section 230 platform liability
}


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

class PositionRecord(NamedTuple):
    old_id: str
    short_title: str
    full_statement: str
    source: str          # 'db', 'html', or 'both'
    html_files: list[str]
    section_names: dict[str, str]    # html_file_stem → section_name
    display_orders: dict[str, int]   # html_file_stem → display_order
    original_status: str
    plain_language: str | None = None  # Phase 2: <p class="rule-plain">; NULL = data gap


# ---------------------------------------------------------------------------
# Subdomain expansion
# ---------------------------------------------------------------------------

def expand_subdomain(code: str) -> str:
    """Expand a v1 subdomain code to a 4-char v2 code (all uppercase letters)."""
    # Non-alpha codes take priority (e.g. "25A", "S230")
    if code in SUBDOMAIN_NONALPHA:
        return SUBDOMAIN_NONALPHA[code]
    if len(code) == 2:
        return SUBDOMAIN_2CHAR.get(code, code + "XS")
    if len(code) == 3:
        return SUBDOMAIN_3CHAR.get(code, code + "S")
    if len(code) == 4:
        return code  # already correct length
    # 5+ char: truncate to 4 (log-worthy)
    return code[:4]


def build_subdomain_name(old_code: str, new_code: str) -> str:
    """Generate a human-readable name for a subdomain."""
    return f"{old_code} (expanded to {new_code})"


# ---------------------------------------------------------------------------
# HTML parsing
# ---------------------------------------------------------------------------

def parse_html_cards(
    html_dir: Path,
) -> dict[str, PositionRecord]:
    """
    Parse all policy-card elements from pillar HTML files.

    Returns a dict keyed by the v1 rule-id string. Cards with duplicate
    IDs (same ID in multiple files) are merged into a single record with
    multiple html_files entries.
    """
    records: dict[str, PositionRecord] = {}

    for html_file in sorted(html_dir.glob("*.html")):
        file_stem = html_file.stem
        pillar_domain = HTML_FILE_TO_DOMAIN.get(file_stem)
        if pillar_domain is None:
            print(f"[WARN] Unknown HTML file (no domain mapping): {html_file.name}", file=sys.stderr)
            continue

        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")
        display_order = 0

        for card in soup.find_all(lambda tag: tag.name == "div" and "policy-card" in tag.get("class", [])):
            code_el = card.find("code", class_="rule-id")
            if not code_el:
                continue
            old_id = code_el.get_text(strip=True)

            if not re.match(r"^[A-Z]{3,4}-[A-Z0-9]+-[0-9]{3,4}[A-Z]?$", old_id):
                print(f"[WARN] Unparseable rule-id '{old_id}' in {html_file.name}", file=sys.stderr)
                continue

            title_el = card.find(["p", "h3"], class_="rule-title")
            title = title_el.get_text(strip=True) if title_el else ""

            plain_el = card.find("p", class_="rule-plain")
            plain_language: str | None = plain_el.get_text(strip=True) if plain_el else None
            if plain_language == "":
                plain_language = None

            # Determine section name from nearest ancestor section/family
            section_name = _get_section_name(card)

            display_order += 1

            if old_id in records:
                rec = records[old_id]
                updated = PositionRecord(
                    old_id=rec.old_id,
                    short_title=rec.short_title or title,
                    full_statement=rec.full_statement or title,
                    source="html" if rec.source == "html" else rec.source,
                    html_files=rec.html_files + [file_stem] if file_stem not in rec.html_files else rec.html_files,
                    section_names={**rec.section_names, file_stem: section_name},
                    display_orders={**rec.display_orders, file_stem: display_order},
                    original_status=rec.original_status,
                    plain_language=rec.plain_language or plain_language,
                )
                records[old_id] = updated
            else:
                records[old_id] = PositionRecord(
                    old_id=old_id,
                    short_title=title[:120],
                    full_statement=title,
                    source="html",
                    html_files=[file_stem],
                    section_names={file_stem: section_name},
                    display_orders={file_stem: display_order},
                    original_status="CANONICAL",
                    plain_language=plain_language,
                )

    return records


def _get_section_name(card_tag: BeautifulSoup) -> str:
    """Walk up the DOM to find the nearest meaningful section or family name."""
    parent = card_tag.parent
    while parent and parent.name not in ("body", "[document]", None):
        classes = parent.get("class") or []
        parent_id = parent.get("id") or ""
        if "policy-family" in classes and parent_id:
            return parent_id
        if parent.name == "section" and parent_id:
            return parent_id
        parent = parent.parent
    return ""


# ---------------------------------------------------------------------------
# DB parsing
# ---------------------------------------------------------------------------

def parse_db_items(source_db: Path) -> dict[str, PositionRecord]:
    """
    Read positions from the v2 SQLite database.

    Returns a dict keyed by position id (v2 format: XXXX-XXXX-0000).
    """
    records: dict[str, PositionRecord] = {}
    con = sqlite3.connect(source_db)
    con.row_factory = sqlite3.Row

    # The v2 DB may not exist yet on first run — fall back gracefully.
    try:
        try:
            rows = con.execute(
                "SELECT id, short_title, full_statement, plain_language, status FROM positions ORDER BY id"
            ).fetchall()
            for row in rows:
                pos_id: str = row["id"]
                records[pos_id] = PositionRecord(
                    old_id=pos_id,
                    short_title=row["short_title"] or "",
                    full_statement=row["full_statement"] or "",
                    source="db",
                    html_files=[],
                    section_names={},
                    display_orders={},
                    original_status=row["status"],
                    plain_language=row["plain_language"],
                )
        except sqlite3.OperationalError:
            # plain_language column not yet in DB — fall back without it
            rows = con.execute(
                "SELECT id, short_title, full_statement, status FROM positions ORDER BY id"
            ).fetchall()
            for row in rows:
                pos_id = row["id"]
                records[pos_id] = PositionRecord(
                    old_id=pos_id,
                    short_title=row["short_title"] or "",
                    full_statement=row["full_statement"] or "",
                    source="db",
                    html_files=[],
                    section_names={},
                    display_orders={},
                    original_status=row["status"],
                    plain_language=None,
                )
    except sqlite3.OperationalError:
        # First run — no v2 DB exists yet; source entirely from HTML
        pass

    con.close()
    return records


# ---------------------------------------------------------------------------
# Merging sources
# ---------------------------------------------------------------------------

def merge_sources(
    html_records: dict[str, PositionRecord],
    db_records: dict[str, PositionRecord],
) -> dict[str, PositionRecord]:
    """
    Merge HTML and DB records. DB wins for full_statement if present.
    HTML wins for html_files / section data.
    """
    merged: dict[str, PositionRecord] = {}
    all_ids = set(html_records) | set(db_records)

    for old_id in sorted(all_ids):
        in_html = old_id in html_records
        in_db = old_id in db_records

        if in_html and in_db:
            h = html_records[old_id]
            d = db_records[old_id]
            # DB plain_language wins if present; fall back to HTML
            plain = d.plain_language or h.plain_language
            merged[old_id] = PositionRecord(
                old_id=old_id,
                short_title=d.short_title or h.short_title,
                full_statement=d.full_statement,
                source="both",
                html_files=h.html_files,
                section_names=h.section_names,
                display_orders=h.display_orders,
                original_status=d.original_status,
                plain_language=plain,
            )
        elif in_html:
            merged[old_id] = html_records[old_id]
        else:
            merged[old_id] = db_records[old_id]

    return merged


# ---------------------------------------------------------------------------
# Domain force overrides
# ---------------------------------------------------------------------------

# Old antitrust-content subdomains that historically used "COR" domain code but
# belong in ANTR, not CRPT. Force is applied after DOMAIN_MAP resolution so that
# these positions land correctly even when the card appears in both HTML files
# (in which case html_files[0] order could otherwise misdirect them).
DOMAIN_FORCE_BY_OLD_SUB: dict[tuple[str, str], str] = {
    ("COR", "AGF"): "ANTR",  # agricultural market concentration
    ("COR", "ALG"): "ANTR",  # algorithmic price coordination
    ("COR", "ANT"): "ANTR",  # antitrust law strengthening
    ("COR", "CAP"): "ANTR",  # regulatory/competition-body capture
    ("COR", "CON"): "ANTR",  # concentration of economic power; govt duty to break up
    ("COR", "ENF"): "ANTR",  # antitrust/consumer-protection enforcement agencies
    ("COR", "MKT"): "ANTR",  # market structure and competition policy
    ("COR", "MPY"): "ANTR",  # labor market monopsony
    ("COR", "NMD"): "ANTR",  # media consolidation (antitrust angle)
    ("COR", "PEQ"): "ANTR",  # private equity / leveraged acquisition
    ("COR", "PIS"): "ANTR",  # essential-sector heightened competition obligations
    ("COR", "PLT"): "ANTR",  # dominant digital platform competition rules
    ("COR", "TRN"): "ANTR",  # dominant-firm transparency / disclosure
    # ("COR", "AUD") → stays CRPT: corporate audit/financial oversight standards
    # ("COR", "FIN") → stays CRPT: campaign finance reform
    # ("COR", "LAW") → stays CRPT: general corporate criminal liability
}

# Per-old-id domain force: a handful of ECO-domain cards that ended up in TAXN
# via _BY_FILE_ resolution but belong elsewhere.
OLD_ID_DOMAIN_FORCE: dict[str, str] = {
    "ECO-ANT-001": "ANTR",  # "Strengthen federal antitrust enforcement" — antitrust, not tax
    "ECO-ANT-003": "ANTR",  # "Algorithmic price coordination" — antitrust, not tax
    "ECO-ANT-002": "CNSR",  # "Require consumer goods to be durable/repairable" — consumer rights
}


# ---------------------------------------------------------------------------
# ID assignment
# ---------------------------------------------------------------------------

def assign_new_ids(
    merged: dict[str, PositionRecord],
    collision_log: list[str],
    review_log: list[tuple[str, str]],
) -> dict[str, str]:
    """
    Build a mapping old_id → new_id.

    Sequence numbers are assigned per (new_domain, new_subdomain), starting at 1.
    Lettered-suffix variants (e.g. HLT-AI-007A) get independent sequential IDs.
    """
    # Counter per (new_domain, new_subdomain)
    seq_counters: dict[tuple[str, str], int] = defaultdict(int)
    old_to_new: dict[str, str] = {}

    # Track subdomain-code collisions: (new_domain, new_sub) → set of original old_subs
    sub_origins: dict[tuple[str, str], set[str]] = defaultdict(set)

    for old_id in sorted(merged):
        parts = old_id.split("-")
        if len(parts) != 3:
            review_log.append((old_id, f"Unexpected ID format (not 3 parts): '{old_id}'"))
            continue

        old_dom, old_sub, old_seq_raw = parts

        # Pass v2-format IDs through unchanged — they are already in the target format
        # and do not need domain/subdomain mapping. Sequence is preserved as-is.
        if re.match(r"^[A-Z]{4}$", old_dom) and re.match(r"^[A-Z]{4}$", old_sub) and re.match(r"^\d{4}$", old_seq_raw):
            old_to_new[old_id] = old_id
            sub_origins[(old_dom, old_sub)].add(old_sub)
            continue

        # Strip trailing letter from sequence (e.g. "007A" → "007" + "A")
        seq_match = re.match(r"^(\d{3})([A-Z]?)$", old_seq_raw)
        if not seq_match:
            review_log.append((old_id, f"Unparseable sequence part: '{old_seq_raw}'"))
            continue

        new_dom = DOMAIN_MAP.get(old_dom)
        if new_dom is None:
            review_log.append((old_id, f"Unknown v1 domain code: '{old_dom}' — no mapping entry"))
            new_dom = "XDOM"
        elif new_dom == "_BY_FILE_":
            # Resolve domain from the HTML file the card lives in
            rec = merged.get(old_id)
            if rec and rec.html_files:
                file_dom = HTML_FILE_TO_DOMAIN.get(rec.html_files[0])
                if file_dom:
                    new_dom = file_dom
                else:
                    review_log.append((old_id, f"Domain '{old_dom}' marked _BY_FILE_ but html file '{rec.html_files[0]}' not in HTML_FILE_TO_DOMAIN — falling back to XDOM"))
                    new_dom = "XDOM"
            else:
                review_log.append((old_id, f"Domain '{old_dom}' marked _BY_FILE_ but no html_files on record — falling back to XDOM"))
                new_dom = "XDOM"

        # Apply per-old-id override first (most specific, highest priority)
        forced_by_id = OLD_ID_DOMAIN_FORCE.get(old_id)
        if forced_by_id:
            new_dom = forced_by_id

        # Apply subdomain-level force second (catches all COR antitrust subdomains
        # regardless of which HTML file the card appeared in first)
        elif (sub_force := DOMAIN_FORCE_BY_OLD_SUB.get((old_dom, old_sub))) is not None:
            new_dom = sub_force

        new_sub = expand_subdomain(old_sub)

        if len(new_sub) != 4:
            review_log.append((old_id, f"Subdomain expansion produced non-4-char code: '{old_sub}' → '{new_sub}'"))
            new_sub = (new_sub + "XXXX")[:4]

        if not new_sub.isalpha():
            review_log.append((old_id, f"Subdomain code contains non-alpha characters after expansion: '{old_sub}' → '{new_sub}' — mapped to MISC"))
            new_sub = "MISC"

        # Log subdomain origins for collision detection
        sub_origins[(new_dom, new_sub)].add(old_sub)

        key = (new_dom, new_sub)
        seq_counters[key] += 1
        seq_num = seq_counters[key]
        new_id = f"{new_dom}-{new_sub}-{seq_num:04d}"
        old_to_new[old_id] = new_id

    # Report collisions: same (domain, subdomain) pair receives multiple original subdomain codes
    for (new_dom, new_sub), old_subs in sorted(sub_origins.items()):
        if len(old_subs) > 1:
            collision_log.append(
                f"Subdomain collision in {new_dom}: {sorted(old_subs)} all expand to {new_sub}"
            )

    return old_to_new


# ---------------------------------------------------------------------------
# Database writing
# ---------------------------------------------------------------------------

def create_db(path: Path, schema_sql: str) -> sqlite3.Connection:
    """Drop and recreate the output database from the schema SQL."""
    if path.exists():
        path.unlink()
    con = sqlite3.connect(path)
    con.executescript(schema_sql)
    con.commit()
    return con


def populate_db(
    con: sqlite3.Connection,
    merged: dict[str, PositionRecord],
    old_to_new: dict[str, str],
    review_set: set[str],
) -> dict[str, int]:
    """
    Write all data to the v2 database.  Returns a dict of row counts.
    """
    counts: dict[str, int] = defaultdict(int)

    # ---- domains table ----
    for code, (name, pillar_id, html_file, is_xd) in DOMAIN_META.items():
        con.execute(
            "INSERT INTO domains(code, name, pillar_id, html_file, is_cross_domain) VALUES (?,?,?,?,?)",
            (code, name, pillar_id, html_file, is_xd),
        )
        counts["domains"] += 1

    # ---- subdomains table ----
    # Collect all (new_domain, new_sub, old_sub) triples from the mapping
    seen_subdomain_pairs: set[tuple[str, str]] = set()
    for old_id, new_id in old_to_new.items():
        parts_old = old_id.split("-")
        parts_new = new_id.split("-")
        old_sub = parts_old[1]
        new_dom = parts_new[0]
        new_sub = parts_new[1]
        pair = (new_sub, new_dom)
        if pair not in seen_subdomain_pairs:
            seen_subdomain_pairs.add(pair)
            sub_name = build_subdomain_name(old_sub, new_sub)
            con.execute(
                "INSERT INTO subdomains(code, domain, name) VALUES (?,?,?)",
                (new_sub, new_dom, sub_name),
            )
            counts["subdomains"] += 1

    # ---- positions + appearances + legacy_id_map ----
    # Build reverse map: new_id → old_id (for legacy map)
    # Also need to know if a position is cross-domain

    # Collect appearances keyed by new_id
    appearances: dict[str, list[tuple[str, str, int]]] = defaultdict(list)

    for old_id, rec in sorted(merged.items()):
        new_id = old_to_new.get(old_id)
        if new_id is None:
            print(f"[WARN] No new_id assigned for '{old_id}' — skipping", file=sys.stderr)
            continue

        new_dom = new_id.split("-")[0]
        new_sub = new_id.split("-")[1]
        seq = int(new_id.split("-")[2])

        is_xd = 1 if new_dom == "XDOM" else 0
        status = "REVIEW" if old_id in review_set else "CANONICAL"

        # Determine short_title fallback
        short_title = (rec.short_title or rec.full_statement[:120]).strip()[:120]
        if not short_title:
            short_title = old_id  # last resort
        full_statement = rec.full_statement.strip() if rec.full_statement.strip() else short_title

        try:
            con.execute(
                """INSERT INTO positions
                   (id, domain, subdomain, seq, short_title, full_statement,
                    plain_language, is_cross_domain, status)
                   VALUES (?,?,?,?,?,?,?,?,?)""",
                (new_id, new_dom, new_sub, seq, short_title, full_statement,
                 rec.plain_language, is_xd, status),
            )
            counts["positions"] += 1
        except sqlite3.IntegrityError as exc:
            print(f"[ERROR] Could not insert position {new_id} ({old_id}): {exc}", file=sys.stderr)
            continue

        # Legacy ID map
        con.execute(
            "INSERT INTO legacy_id_map(old_id, new_id, source) VALUES (?,?,?)",
            (old_id, new_id, rec.source),
        )
        counts["legacy_id_map"] += 1

        # Appearances — one per HTML file the card appeared in
        if rec.html_files:
            for file_stem in rec.html_files:
                pillar_dom = HTML_FILE_TO_DOMAIN.get(file_stem)
                if pillar_dom is None:
                    print(f"[WARN] Unknown file stem for appearance: {file_stem}", file=sys.stderr)
                    continue
                section = rec.section_names.get(file_stem, "")
                order = rec.display_orders.get(file_stem, 0)
                appearances[new_id].append((pillar_dom, section, order))
        else:
            # DB-only record: infer pillar domain from the new domain code
            if new_dom != "XDOM":
                appearances[new_id].append((new_dom, "", 0))
            else:
                # Cross-domain, DB only — no HTML file context
                appearances[new_id].append(("XDOM", "", 0))

    # Insert appearances, deduplicating on (position_id, pillar_domain)
    for new_id, app_list in sorted(appearances.items()):
        seen_app: set[str] = set()
        for pillar_dom, section, order in app_list:
            if pillar_dom in seen_app:
                continue
            seen_app.add(pillar_dom)
            try:
                con.execute(
                    """INSERT INTO position_pillar_appearances
                       (position_id, pillar_domain, section_name, display_order)
                       VALUES (?,?,?,?)""",
                    (new_id, pillar_dom, section, order),
                )
                counts["appearances"] += 1
            except sqlite3.IntegrityError as exc:
                print(f"[WARN] Duplicate appearance {new_id}/{pillar_dom}: {exc}", file=sys.stderr)

    con.commit()
    return dict(counts)


# ---------------------------------------------------------------------------
# Migration report
# ---------------------------------------------------------------------------

def write_report(
    report_path: Path,
    merged: dict[str, PositionRecord],
    old_to_new: dict[str, str],
    counts: dict[str, int],
    collision_log: list[str],
    review_log: list[tuple[str, str]],
) -> None:
    """Write the migration report markdown file."""
    lines: list[str] = []

    lines.append("# Freedom and Dignity Project — Policy Catalog v2 Migration Report\n")
    lines.append(f"Generated by `scripts/build-catalog-v2.py`\n")
    lines.append("")

    # --- Summary ---
    lines.append("## 1. Summary\n")
    source_counts: dict[str, int] = defaultdict(int)
    for rec in merged.values():
        source_counts[rec.source] += 1
    xdom_count = sum(
        1 for nid in old_to_new.values() if nid.startswith("XDOM-")
    )

    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Total v1 positions | {len(merged)} |")
    lines.append(f"| Source: HTML only | {source_counts.get('html', 0)} |")
    lines.append(f"| Source: DB only | {source_counts.get('db', 0)} |")
    lines.append(f"| Source: Both HTML + DB | {source_counts.get('both', 0)} |")
    lines.append(f"| Cross-domain (XDOM) | {xdom_count} |")
    lines.append(f"| Flagged REVIEW | {len(review_log)} |")
    lines.append(f"| Subdomain collisions | {len(collision_log)} |")
    lines.append(f"| v2 domains written | {counts.get('domains', 0)} |")
    lines.append(f"| v2 subdomains written | {counts.get('subdomains', 0)} |")
    lines.append(f"| v2 positions written | {counts.get('positions', 0)} |")
    lines.append(f"| v2 appearances written | {counts.get('appearances', 0)} |")
    lines.append(f"| legacy_id_map entries | {counts.get('legacy_id_map', 0)} |")
    lines.append("")

    # --- Domain mapping ---
    lines.append("## 2. Domain Code Mapping (v1 → v2)\n")
    lines.append("| v1 Code | v2 Code | Pillar |")
    lines.append("|---------|---------|--------|")
    for old, new in sorted(DOMAIN_MAP.items()):
        pillar = DOMAIN_META.get(new, ("?", None, None, 0))[0]
        lines.append(f"| {old} | {new} | {pillar} |")
    lines.append("")

    # --- Subdomain mapping (from actual data) ---
    lines.append("## 3. Subdomain Code Mapping (v1 → v2, all observed)\n")
    lines.append("| v1 Sub | v2 Sub | Rule Applied |")
    lines.append("|--------|--------|--------------|")
    seen_sub_pairs: set[tuple[str, str]] = set()
    for old_id in sorted(merged):
        parts = old_id.split("-")
        if len(parts) < 2:
            continue
        old_sub = parts[1]
        if old_sub in seen_sub_pairs:
            continue
        seen_sub_pairs.add(old_sub)  # type: ignore[arg-type]
        new_sub = expand_subdomain(old_sub)
        if len(old_sub) == 2:
            rule = "explicit 2-char expansion"
        elif len(old_sub) == 3 and old_sub in SUBDOMAIN_3CHAR:
            rule = "explicit 3-char expansion"
        elif len(old_sub) == 3:
            rule = "3-char + 'S' default"
        elif len(old_sub) == 4:
            rule = "4-char kept as-is"
        else:
            rule = "truncated to 4 chars"
        lines.append(f"| {old_sub} | {new_sub} | {rule} |")
    lines.append("")

    # --- REVIEW items ---
    lines.append("## 4. REVIEW-Flagged Items\n")
    if review_log:
        lines.append("| v1 ID | Reason |")
        lines.append("|-------|--------|")
        for old_id, reason in sorted(review_log):
            lines.append(f"| {old_id} | {reason} |")
    else:
        lines.append("_No items flagged for review._")
    lines.append("")

    # --- Subdomain collisions ---
    lines.append("## 5. Subdomain Collision Log\n")
    if collision_log:
        for entry in collision_log:
            lines.append(f"- {entry}")
    else:
        lines.append("_No subdomain collisions detected._")
    lines.append("")

    # --- Legacy ID sample ---
    lines.append("## 6. Legacy ID → New ID Mapping (first 20 + all REVIEW items)\n")
    lines.append("| v1 ID | v2 ID | Source |")
    lines.append("|-------|-------|--------|")
    review_ids = {old_id for old_id, _ in review_log}
    sample_count = 0
    for old_id in sorted(old_to_new):
        new_id = old_to_new[old_id]
        rec = merged.get(old_id)
        source = rec.source if rec else "?"
        if sample_count < 20 or old_id in review_ids:
            lines.append(f"| {old_id} | {new_id} | {source} |")
            sample_count += 1
    lines.append("")

    # --- Lettered suffix notes ---
    lines.append("## 7. Lettered Suffix Variants\n")
    lines.append("These v1 IDs had letter suffixes and were assigned independent sequential new IDs:\n")
    lines.append("| v1 ID | v2 ID |")
    lines.append("|-------|-------|")
    for old_id in sorted(old_to_new):
        if re.search(r"[A-Z]$", old_id.split("-")[-1]) and len(old_id.split("-")[-1]) == 4:
            lines.append(f"| {old_id} | {old_to_new[old_id]} |")
    lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[INFO] Migration report written to {report_path}", file=sys.stderr)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build policy_catalog_v2.sqlite from v1 sources.")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and map everything but do not write the output DB or report.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=REPO_ROOT / "data" / "policy_catalog_v2.sqlite",
        help="Output SQLite database path.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=REPO_ROOT / "data" / "migration-report.md",
        help="Output migration report path.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    print("[INFO] Reading HTML policy cards...", file=sys.stderr)
    html_records = parse_html_cards(HTML_DIR)
    print(f"[INFO]   {len(html_records)} unique IDs from HTML", file=sys.stderr)

    print("[INFO] Reading DB policy items...", file=sys.stderr)
    db_records = parse_db_items(SOURCE_DB)
    print(f"[INFO]   {len(db_records)} items from DB", file=sys.stderr)

    print("[INFO] Merging sources...", file=sys.stderr)
    merged = merge_sources(html_records, db_records)
    print(f"[INFO]   {len(merged)} total unique positions after merge", file=sys.stderr)

    collision_log: list[str] = []
    review_log: list[tuple[str, str]] = []

    print("[INFO] Assigning v2 IDs...", file=sys.stderr)
    old_to_new = assign_new_ids(merged, collision_log, review_log)
    print(f"[INFO]   {len(old_to_new)} IDs assigned", file=sys.stderr)
    print(f"[INFO]   {len(collision_log)} subdomain collisions detected", file=sys.stderr)
    print(f"[INFO]   {len(review_log)} items flagged for REVIEW", file=sys.stderr)

    review_set = {old_id for old_id, _ in review_log}

    if args.dry_run:
        print("\n[DRY RUN] No database or report written.", file=sys.stderr)
        # Print summary to stdout
        print(f"Dry-run complete.")
        print(f"  Total positions:    {len(merged)}")
        print(f"  IDs assigned:       {len(old_to_new)}")
        print(f"  REVIEW-flagged:     {len(review_log)}")
        print(f"  Collisions:         {len(collision_log)}")
        if collision_log:
            print("\nCollisions:")
            for c in collision_log:
                print(f"  {c}")
        if review_log:
            print("\nREVIEW items:")
            for old_id, reason in review_log[:20]:
                print(f"  {old_id}: {reason}")
        return

    schema_path = REPO_ROOT / "data" / "schema_v2.sql"
    schema_sql = schema_path.read_text(encoding="utf-8")

    print(f"[INFO] Creating output DB at {args.output}...", file=sys.stderr)
    con = create_db(args.output, schema_sql)

    print("[INFO] Populating tables...", file=sys.stderr)
    counts = populate_db(con, merged, old_to_new, review_set)
    con.close()

    print(f"[INFO] Writing migration report to {args.report}...", file=sys.stderr)
    write_report(args.report, merged, old_to_new, counts, collision_log, review_log)

    # Final summary to stdout
    print(f"\nMigration complete.")
    print(f"  Output DB:          {args.output}")
    print(f"  Report:             {args.report}")
    print(f"  Domains:            {counts.get('domains', 0)}")
    print(f"  Subdomains:         {counts.get('subdomains', 0)}")
    print(f"  Positions:          {counts.get('positions', 0)}")
    print(f"  Appearances:        {counts.get('appearances', 0)}")
    print(f"  Legacy map entries: {counts.get('legacy_id_map', 0)}")
    print(f"  REVIEW-flagged:     {len(review_log)}")
    print(f"  Collisions logged:  {len(collision_log)}")


if __name__ == "__main__":
    main()
