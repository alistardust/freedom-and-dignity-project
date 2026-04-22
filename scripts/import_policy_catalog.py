#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


NUMERIC_SOURCE_PRIORITY = {
    "main-branch.txt": 1,
    "brainstorm-branch.txt": 2,
    "brainstorm-branch1part2.txt": 2,
    "comparisons-branch.txt": 3,
    "AI-statement-branch.txt": 4,
}

# Fetched directly from ChatGPT API — higher fidelity than copy-paste exports.
# These live under sources/chatgpt-fetched/ and use the same priority tiers.
FETCHED_SOURCE_PRIORITY = {
    "political_project_main.txt": 1,
    "branch_branch_political_project_main.txt": 1,
    "political_project_brainstorm.txt": 2,
    "branch_political_project_brainstorm.txt": 2,
    "political_project_comparisons.txt": 3,
}

NUMERIC_ROW_MIN_FIELDS = 4
RULE_ID_RE = re.compile(r"^[A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?$")
PROSE_RULE_ID_RE = re.compile(r"^([A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?)\s{1,2}(.+)$")
MIGRATION_ROW_RE = re.compile(
    r"^\|\s*(\d+)\s*\|\s*([A-Z]{2,}(?:-[A-Z0-9]+)+-\d{3}[A-Z]?)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*([A-Z]+)\s*\|\s*([^|]*)\|\s*$"
)
MANUAL_RULE_SEEDS = {
    "ECO-TAX-001": {
        "scope_code": "ECO",
        "family_code": "TAX",
        "statement": "Anti-wealth hoarding",
        "status": "PARTIAL",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21098,
    },
    "ADM-CHV-001": {
        "scope_code": "ADM",
        "family_code": "CHV",
        "statement": "Restore Chevron deference",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21099,
    },
    "ADM-AGY-001": {
        "scope_code": "ADM",
        "family_code": "AGY",
        "statement": "Congress explicitly empowered to create agencies",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21100,
    },
    "HLT-TRL-001": {
        "scope_code": "HLT",
        "family_code": "TRL",
        "statement": "Approvals and trials for new treatments funded and streamlined",
        "status": "MISSING",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 21157,
    },
    # ── Gun Policy (GUN scope) ─────────────────────────────────────────────────
    # Items 115–124 from main chat log; never received structured IDs upstream.
    # Additional rules (ACQ-002, TRN-001–003, RFL-001) sourced from brainstorm
    # log line 6385 (original detailed policy description).
    "GUN-REG-001": {
        "scope_code": "GUN",
        "family_code": "REG",
        "statement": "Amend the Constitution to explicitly affirm government authority to regulate firearms and weaponry",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17896,
    },
    "GUN-BAN-001": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Ban private ownership of weapons of war including automatic weapons and semi-automatic military analogues designed to evade regulation",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17912,
    },
    "GUN-BAN-002": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Definition of weapons of war must be evasion-resistant and cover both automatic weapons and demilitarized semi-automatic civilian versions",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-BAN-003": {
        "scope_code": "GUN",
        "family_code": "BAN",
        "statement": "Ban high-capacity ammunition magazines above a defined threshold",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-ACQ-001": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Require background checks for all firearm acquisitions",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17900,
    },
    "GUN-ACQ-002": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Background check requirement applies to all transfers including private sales and gun shows",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-ACQ-003": {
        "scope_code": "GUN",
        "family_code": "ACQ",
        "statement": "Background check databases must be comprehensive, interoperable, and up to date",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-001": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require safety training as a condition of firearm ownership",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-002": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require de-escalation training as a condition of firearm ownership",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-TRN-003": {
        "scope_code": "GUN",
        "family_code": "TRN",
        "statement": "Require secure storage of firearms; safe storage law as federal minimum standard",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-MHE-001": {
        "scope_code": "GUN",
        "family_code": "MHE",
        "statement": "Mental health evaluations for gun ownership must be narrowly tailored to dangerousness, not diagnosis category",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17904,
    },
    "GUN-MHE-002": {
        "scope_code": "GUN",
        "family_code": "MHE",
        "statement": "Prohibit blanket exclusion from firearm ownership based solely on a mental health diagnosis",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17908,
    },
    "GUN-RFL-001": {
        "scope_code": "GUN",
        "family_code": "RFL",
        "statement": "Establish federal minimum standards for red flag / extreme risk protection orders with due process protections",
        "status": "PROPOSED",
        "source_name": "branch_political_project_brainstorm.txt",
        "line_number": 6385,
    },
    "GUN-MIL-001": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Define 'well regulated militia' in enforceable constitutional and statutory terms",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17916,
    },
    "GUN-MIL-002": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Ban private armies and mercenary groups",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17920,
    },
    "GUN-MIL-003": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Require militias to maintain membership records, financial transparency, audits, insurance, and disclosed chain of command",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17924,
    },
    "GUN-MIL-004": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Federal and state governments must have oversight authority over militia training materials and requirements",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17928,
    },
    "GUN-MIL-005": {
        "scope_code": "GUN",
        "family_code": "MIL",
        "statement": "Provide mechanisms for regulated militias to train for disaster relief and search and rescue alongside first responders",
        "status": "PROPOSED",
        "source_name": "branch_branch_political_project_main.txt",
        "line_number": 17932,
    },
}
MANUAL_POLICY_ITEM_TO_RULE_ID = {
    192: "TRM-LIM-001",
    193: "TRM-LIM-002",
    194: "TRM-LIM-003",
    195: "TRM-RUN-001",
    196: "TRM-RUN-002",
    197: "TRM-VAC-001",
    198: "TRM-VAC-002",
    199: "TRM-VAC-003",
    200: "COR-ETH-002",
    201: "COR-ETH-003",
    202: "COR-ETH-004",
    203: "COR-ETH-005",
    204: "COR-ETH-006",
    205: "COR-ETH-007",
    206: "COR-ETH-008",
    207: "COR-ETH-009",
    208: "COR-ETH-010",
    209: "COR-ETH-010",
    210: "HLT-MHC-001",
    211: "HLT-STD-002",
    212: "HLT-STD-001",
    213: "HLT-TRL-001",
    214: "HLT-TRL-001",
    215: "HLT-PHR-001",
    216: "HLT-PHR-002",
    217: "HLT-SUP-001",
    218: "HLT-SUP-002",
    219: "HLT-SUP-003",
    220: "HLT-SUP-004",
    221: "HLT-PHR-003",
    222: "HLT-EMS-001",
    223: "HLT-EMS-002",
    224: "HLT-ACC-001",
    225: "HLT-ACC-002",
    226: "HLT-ACC-003",
    227: "HLT-STD-005",
    228: "HLT-STD-008",
    229: "HLT-STD-006",
    230: "HLT-STD-007",
    231: "HLT-STD-008",
    232: "HLT-STD-001",
    233: "HLT-STD-009",
    234: "HLT-STD-008",
    235: "HLT-STD-011",
    236: "HLT-STD-008",
    237: "HLT-STD-005",
    238: "HLT-STD-007",
    239: "HLT-STD-010",
    240: "HLT-STD-008",
    241: "HLT-STD-009",
    242: "HLT-STD-001",
    243: "HLT-STD-009",
    244: "HLT-STD-010",
    245: "HLT-STD-011",
    246: "HLT-STD-002",
    247: "SYS-GEO-001",
    248: "SYS-GEO-002",
    249: "SYS-GEO-003",
    250: "SYS-GEO-004",
    251: "SYS-GEO-005",
    252: "HLT-TEL-001",
    253: "HLT-TEL-002",
    254: "SYS-GEO-002",
    255: "SYS-GEO-001",
    256: "SYS-GEO-002",
    257: "SYS-GEO-003",
    258: "SYS-GEO-004",
    259: "SYS-GEO-005",
    260: "SYS-GEO-003",
    261: "SYS-FED-001",
    262: "SYS-FED-002",
    263: "SYS-FED-003",
    264: "SYS-FED-004",
    265: "SYS-FED-005",
    266: "SYS-FED-004",
    267: "MED-PRS-001",
    268: "MED-PRS-002",
    269: "MED-PRS-003",
    270: "MED-PRS-004",
    271: "COR-WHB-001",
    272: "MED-PRS-005",
    273: "MED-PRS-006",
    274: "MED-PRS-007",
    275: "MED-PRS-008",
    276: "COR-WHB-001",
    277: "MED-PRS-009",
    278: "JUS-DRG-001",
    279: "JUS-DRG-002",
    280: "HLT-STD-012",
    281: "JUS-DRG-003",
    282: "JUS-DRG-004",
    283: "HLT-STD-013",
    284: "JUS-DRG-005",
    285: "HLT-REB-001",
    286: "HLT-REB-002",
    287: "HLT-REB-003",
    288: "HLT-REB-004",
    289: "HLT-REB-005",
    290: "HLT-REB-006",
    291: "HLT-REB-007",
    292: "RGT-BOD-001",
}


@dataclass(frozen=True)
class SourceFile:
    name: str
    path: Path
    priority: int


@dataclass
class PolicyOccurrence:
    item_id: int
    source_name: str
    line_number: int
    statement: str
    status: str
    target: str
    notes: str
    raw_line: str


@dataclass
class RuleOccurrence:
    rule_id: str
    source_name: str
    line_number: int
    scope_code: str
    family_code: str
    statement: str
    status: str
    raw_line: str


@dataclass
class RecordLinkOccurrence:
    source_record_type: str
    source_record_id: str
    target_record_type: str
    target_record_id: str
    relationship_type: str
    source_name: str
    line_number: int
    label: str
    status: str
    target_file: str
    notes: str
    raw_line: str


@dataclass
class ProseRuleMention:
    rule_id: str
    source_name: str
    line_number: int
    description: str
    raw_line: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Import structured policy items and rule IDs from branch chat logs."
    )
    parser.add_argument(
        "--repo-root",
        default=Path(__file__).resolve().parents[1],
        type=Path,
        help="Repository root. Defaults to the current script's repo.",
    )
    parser.add_argument(
        "--db",
        default=None,
        type=Path,
        help="Path to the SQLite database. Defaults to <repo>/data/policy_catalog.sqlite.",
    )
    return parser.parse_args()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def get_source_files(chat_dir: Path) -> list[SourceFile]:
    files: list[SourceFile] = []
    for name, priority in NUMERIC_SOURCE_PRIORITY.items():
        path = chat_dir / name
        if path.exists():
            files.append(SourceFile(name=name, path=path, priority=priority))
    fetched_dir = chat_dir.parent  # chatgpt-fetched files are now directly under sources/
    for name, priority in FETCHED_SOURCE_PRIORITY.items():
        path = fetched_dir / name
        if path.exists():
            files.append(SourceFile(name=name, path=path, priority=priority))
    return files


def parse_numeric_occurrences(source: SourceFile) -> list[PolicyOccurrence]:
    occurrences: list[PolicyOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("\t")
        if len(parts) < NUMERIC_ROW_MIN_FIELDS or not parts[0].isdigit():
            continue

        parts += [""] * (5 - len(parts))
        item_id, statement, status, target = parts[:4]
        notes = parts[4] if len(parts) > 4 else ""
        occurrences.append(
            PolicyOccurrence(
                item_id=int(item_id),
                source_name=source.name,
                line_number=line_number,
                statement=statement.strip(),
                status=status.strip(),
                target=target.strip(),
                notes=notes.strip(),
                raw_line=line,
            )
        )
    return occurrences


def parse_rule_occurrences(source: SourceFile) -> list[RuleOccurrence]:
    occurrences: list[RuleOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        parts = line.split("|")
        if len(parts) != 5:
            continue
        rule_id, scope_code, family_code, statement, status = (part.strip() for part in parts)
        if not RULE_ID_RE.match(rule_id):
            continue
        occurrences.append(
            RuleOccurrence(
                rule_id=rule_id,
                source_name=source.name,
                line_number=line_number,
                scope_code=scope_code,
                family_code=family_code,
                statement=statement,
                status=status,
                raw_line=line,
            )
        )
    return occurrences


def parse_record_link_occurrences(source: SourceFile) -> list[RecordLinkOccurrence]:
    occurrences: list[RecordLinkOccurrence] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        match = MIGRATION_ROW_RE.match(line)
        if not match:
            continue
        old_id, new_id, label, target_file, status, notes = (part.strip() for part in match.groups())
        occurrences.append(
            RecordLinkOccurrence(
                source_record_type="policy_item",
                source_record_id=old_id,
                target_record_type="rule_item",
                target_record_id=new_id,
                relationship_type="migrated_to",
                source_name=source.name,
                line_number=line_number,
                label=label,
                status=status,
                target_file=target_file,
                notes=notes,
                raw_line=line,
            )
        )
    return occurrences


def parse_prose_rule_mentions(source: SourceFile) -> list[ProseRuleMention]:
    mentions: list[ProseRuleMention] = []
    for line_number, line in enumerate(source.path.read_text(encoding="utf-8").splitlines(), 1):
        stripped = line.strip()
        if not stripped or "|" in stripped:
            continue
        match = PROSE_RULE_ID_RE.match(stripped)
        if not match:
            continue
        rule_id, description = match.groups()
        mentions.append(
            ProseRuleMention(
                rule_id=rule_id,
                source_name=source.name,
                line_number=line_number,
                description=description.strip(),
                raw_line=line,
            )
        )
    return mentions


def create_schema(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        PRAGMA foreign_keys = ON;

        CREATE TABLE IF NOT EXISTS source_files (
            id INTEGER PRIMARY KEY,
            source_name TEXT NOT NULL UNIQUE,
            relative_path TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            source_priority INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policy_items (
            item_id INTEGER PRIMARY KEY,
            canonical_statement TEXT NOT NULL,
            status TEXT NOT NULL,
            target TEXT NOT NULL,
            notes TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS policy_item_occurrences (
            id INTEGER PRIMARY KEY,
            item_id INTEGER NOT NULL REFERENCES policy_items(item_id) ON DELETE CASCADE,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            statement TEXT NOT NULL,
            status TEXT NOT NULL,
            target TEXT NOT NULL,
            notes TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(item_id, source_id, line_number, raw_line)
        );

        CREATE TABLE IF NOT EXISTS rule_items (
            rule_id TEXT PRIMARY KEY,
            scope_code TEXT NOT NULL,
            family_code TEXT NOT NULL,
            canonical_statement TEXT NOT NULL,
            status TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL
        );

        CREATE TABLE IF NOT EXISTS rule_occurrences (
            id INTEGER PRIMARY KEY,
            rule_id TEXT NOT NULL REFERENCES rule_items(rule_id) ON DELETE CASCADE,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            scope_code TEXT NOT NULL,
            family_code TEXT NOT NULL,
            statement TEXT NOT NULL,
            status TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(rule_id, source_id, line_number, raw_line)
        );

        CREATE TABLE IF NOT EXISTS record_links (
            id INTEGER PRIMARY KEY,
            source_record_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            target_record_type TEXT NOT NULL,
            target_record_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            canonical_label TEXT NOT NULL,
            status TEXT NOT NULL,
            target_file TEXT NOT NULL,
            notes TEXT NOT NULL,
            canonical_source_id INTEGER NOT NULL REFERENCES source_files(id),
            canonical_line_number INTEGER NOT NULL,
            occurrence_count INTEGER NOT NULL,
            source_count INTEGER NOT NULL,
            UNIQUE (source_record_type, source_record_id, target_record_type, target_record_id, relationship_type)
        );

        CREATE TABLE IF NOT EXISTS record_link_occurrences (
            id INTEGER PRIMARY KEY,
            source_record_type TEXT NOT NULL,
            source_record_id TEXT NOT NULL,
            target_record_type TEXT NOT NULL,
            target_record_id TEXT NOT NULL,
            relationship_type TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            label TEXT NOT NULL,
            status TEXT NOT NULL,
            target_file TEXT NOT NULL,
            notes TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                raw_line
            )
        );

        CREATE TABLE IF NOT EXISTS prose_rule_mentions (
            id INTEGER PRIMARY KEY,
            rule_id TEXT NOT NULL,
            source_id INTEGER NOT NULL REFERENCES source_files(id) ON DELETE CASCADE,
            line_number INTEGER NOT NULL,
            description TEXT NOT NULL,
            raw_line TEXT NOT NULL,
            UNIQUE(rule_id, source_id, line_number, raw_line)
        );

        DROP VIEW IF EXISTS catalog_entries;
        CREATE VIEW catalog_entries AS
        SELECT
            'policy_item' AS record_type,
            CAST(item_id AS TEXT) AS record_id,
            NULL AS scope_code,
            NULL AS family_code,
            canonical_statement AS statement,
            status,
            target,
            notes,
            occurrence_count,
            source_count
        FROM policy_items
        UNION ALL
        SELECT
            'rule_item' AS record_type,
            rule_id AS record_id,
            scope_code,
            family_code,
            canonical_statement AS statement,
            status,
            NULL AS target,
            NULL AS notes,
            occurrence_count,
            source_count
        FROM rule_items;

        DROP VIEW IF EXISTS deduped_catalog_entries;
        CREATE VIEW deduped_catalog_entries AS
        SELECT
            ce.record_type,
            ce.record_id,
            ce.scope_code,
            ce.family_code,
            ce.statement,
            ce.status,
            ce.target,
            ce.notes,
            ce.occurrence_count,
            ce.source_count
        FROM catalog_entries ce
        WHERE NOT (
            ce.record_type = 'policy_item'
            AND EXISTS (
                SELECT 1
                FROM record_links rl
                WHERE rl.relationship_type = 'migrated_to'
                  AND rl.source_record_type = 'policy_item'
                  AND rl.target_record_type = 'rule_item'
                  AND rl.source_record_id = ce.record_id
            )
        );

        DROP VIEW IF EXISTS unresolved_prose_rule_mentions;
        CREATE VIEW unresolved_prose_rule_mentions AS
        SELECT
            prm.rule_id,
            sf.source_name,
            prm.line_number,
            prm.description,
            prm.raw_line
        FROM prose_rule_mentions prm
        JOIN source_files sf ON sf.id = prm.source_id
        WHERE NOT EXISTS (
            SELECT 1
            FROM rule_items ri
            WHERE ri.rule_id = prm.rule_id
        );

        CREATE INDEX IF NOT EXISTS idx_policy_items_status ON policy_items(status);
        CREATE INDEX IF NOT EXISTS idx_policy_items_target ON policy_items(target);
        CREATE INDEX IF NOT EXISTS idx_policy_occurrences_source ON policy_item_occurrences(source_id, item_id);
        CREATE INDEX IF NOT EXISTS idx_rule_items_scope_family ON rule_items(scope_code, family_code);
        CREATE INDEX IF NOT EXISTS idx_rule_items_status ON rule_items(status);
        CREATE INDEX IF NOT EXISTS idx_rule_occurrences_source ON rule_occurrences(source_id, rule_id);
        CREATE INDEX IF NOT EXISTS idx_record_links_source ON record_links(source_record_type, source_record_id);
        CREATE INDEX IF NOT EXISTS idx_record_links_target ON record_links(target_record_type, target_record_id);
        CREATE INDEX IF NOT EXISTS idx_record_link_occurrences_source ON record_link_occurrences(source_id, source_record_id);
        CREATE INDEX IF NOT EXISTS idx_prose_rule_mentions_rule_id ON prose_rule_mentions(rule_id);
        """
    )


def reset_import_tables(conn: sqlite3.Connection) -> None:
    conn.executescript(
        """
        DELETE FROM prose_rule_mentions;
        DELETE FROM record_link_occurrences;
        DELETE FROM record_links;
        DELETE FROM rule_occurrences;
        DELETE FROM rule_items;
        DELETE FROM policy_item_occurrences;
        DELETE FROM policy_items;
        DELETE FROM source_files;
        """
    )


def insert_source_files(conn: sqlite3.Connection, repo_root: Path, sources: Iterable[SourceFile]) -> dict[str, int]:
    source_ids: dict[str, int] = {}
    for source in sources:
        text = source.path.read_text(encoding="utf-8")
        cursor = conn.execute(
            """
            INSERT INTO source_files (source_name, relative_path, sha256, source_priority)
            VALUES (?, ?, ?, ?)
            """,
            (
                source.name,
                str(source.path.relative_to(repo_root)),
                sha256_text(text),
                source.priority,
            ),
        )
        source_ids[source.name] = int(cursor.lastrowid)
    return source_ids


def choose_policy_canonical(occurrences: list[PolicyOccurrence], source_priority: dict[str, int]) -> PolicyOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.statement)),
    )[0]


def choose_rule_canonical(occurrences: list[RuleOccurrence], source_priority: dict[str, int]) -> RuleOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.statement)),
    )[0]


def choose_record_link_canonical(
    occurrences: list[RecordLinkOccurrence], source_priority: dict[str, int]
) -> RecordLinkOccurrence:
    return sorted(
        occurrences,
        key=lambda occ: (source_priority[occ.source_name], -occ.line_number, -len(occ.label)),
    )[0]


def import_policy_items(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[PolicyOccurrence],
) -> None:
    grouped: dict[int, list[PolicyOccurrence]] = {}
    for occurrence in occurrences:
        grouped.setdefault(occurrence.item_id, []).append(occurrence)

    for item_id, item_occurrences in sorted(grouped.items()):
        canonical = choose_policy_canonical(item_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO policy_items (
                item_id,
                canonical_statement,
                status,
                target,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                item_id,
                canonical.statement,
                canonical.status,
                canonical.target,
                canonical.notes,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(item_occurrences),
                len({occ.source_name for occ in item_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO policy_item_occurrences (
                item_id,
                source_id,
                line_number,
                statement,
                status,
                target,
                notes,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    item_id,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.statement,
                    occ.status,
                    occ.target,
                    occ.notes,
                    occ.raw_line,
                )
                for occ in item_occurrences
            ],
        )


def import_rule_items(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[RuleOccurrence],
) -> None:
    grouped: dict[str, list[RuleOccurrence]] = {}
    for occurrence in occurrences:
        grouped.setdefault(occurrence.rule_id, []).append(occurrence)

    for rule_id, rule_occurrences in sorted(grouped.items()):
        canonical = choose_rule_canonical(rule_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO rule_items (
                rule_id,
                scope_code,
                family_code,
                canonical_statement,
                status,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rule_id,
                canonical.scope_code,
                canonical.family_code,
                canonical.statement,
                canonical.status,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(rule_occurrences),
                len({occ.source_name for occ in rule_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO rule_occurrences (
                rule_id,
                source_id,
                line_number,
                scope_code,
                family_code,
                statement,
                status,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    rule_id,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.scope_code,
                    occ.family_code,
                    occ.statement,
                    occ.status,
                    occ.raw_line,
                )
                for occ in rule_occurrences
            ],
        )


def import_record_links(
    conn: sqlite3.Connection,
    source_ids: dict[str, int],
    source_priority: dict[str, int],
    occurrences: list[RecordLinkOccurrence],
) -> None:
    grouped: dict[tuple[str, str, str, str, str], list[RecordLinkOccurrence]] = {}
    for occurrence in occurrences:
        key = (
            occurrence.source_record_type,
            occurrence.source_record_id,
            occurrence.target_record_type,
            occurrence.target_record_id,
            occurrence.relationship_type,
        )
        grouped.setdefault(key, []).append(occurrence)

    for key, link_occurrences in sorted(grouped.items()):
        canonical = choose_record_link_canonical(link_occurrences, source_priority)
        conn.execute(
            """
            INSERT INTO record_links (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                canonical_label,
                status,
                target_file,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                canonical.source_record_type,
                canonical.source_record_id,
                canonical.target_record_type,
                canonical.target_record_id,
                canonical.relationship_type,
                canonical.label,
                canonical.status,
                canonical.target_file,
                canonical.notes,
                source_ids[canonical.source_name],
                canonical.line_number,
                len(link_occurrences),
                len({occ.source_name for occ in link_occurrences}),
            ),
        )
        conn.executemany(
            """
            INSERT INTO record_link_occurrences (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                label,
                status,
                target_file,
                notes,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (
                    occ.source_record_type,
                    occ.source_record_id,
                    occ.target_record_type,
                    occ.target_record_id,
                    occ.relationship_type,
                    source_ids[occ.source_name],
                    occ.line_number,
                    occ.label,
                    occ.status,
                    occ.target_file,
                    occ.notes,
                    occ.raw_line,
                )
                for occ in link_occurrences
            ],
        )


def import_prose_rule_mentions(
    conn: sqlite3.Connection, source_ids: dict[str, int], mentions: list[ProseRuleMention]
) -> None:
    conn.executemany(
        """
        INSERT INTO prose_rule_mentions (
            rule_id,
            source_id,
            line_number,
            description,
            raw_line
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                mention.rule_id,
                source_ids[mention.source_name],
                mention.line_number,
                mention.description,
                mention.raw_line,
            )
            for mention in mentions
        ],
    )


def get_line_from_source(source: SourceFile, line_number: int) -> str:
    lines = source.path.read_text(encoding="utf-8").splitlines()
    if line_number < 1 or line_number > len(lines):
        return ""
    return lines[line_number - 1]


def insert_manual_rule_seeds(
    conn: sqlite3.Connection, sources: dict[str, SourceFile], source_ids: dict[str, int]
) -> None:
    for rule_id, seed in MANUAL_RULE_SEEDS.items():
        exists = conn.execute("SELECT 1 FROM rule_items WHERE rule_id = ?", (rule_id,)).fetchone()
        if exists:
            continue
        source = sources[seed["source_name"]]
        raw_line = get_line_from_source(source, seed["line_number"])
        conn.execute(
            """
            INSERT INTO rule_items (
                rule_id,
                scope_code,
                family_code,
                canonical_statement,
                status,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, 1, 1)
            """,
            (
                rule_id,
                seed["scope_code"],
                seed["family_code"],
                seed["statement"],
                seed["status"],
                source_ids[seed["source_name"]],
                seed["line_number"],
            ),
        )
        conn.execute(
            """
            INSERT INTO rule_occurrences (
                rule_id,
                source_id,
                line_number,
                scope_code,
                family_code,
                statement,
                status,
                raw_line
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                rule_id,
                source_ids[seed["source_name"]],
                seed["line_number"],
                seed["scope_code"],
                seed["family_code"],
                seed["statement"],
                seed["status"],
                raw_line,
            ),
        )


def apply_manual_policy_item_links(conn: sqlite3.Connection) -> None:
    current_ids = tuple(str(item_id) for item_id in MANUAL_POLICY_ITEM_TO_RULE_ID)
    placeholders = ", ".join("?" for _ in current_ids)
    conn.execute(
        f"""
        DELETE FROM record_link_occurrences
        WHERE source_record_type = 'policy_item'
          AND relationship_type = 'migrated_to'
          AND source_record_id IN ({placeholders})
        """,
        current_ids,
    )
    conn.execute(
        f"""
        DELETE FROM record_links
        WHERE source_record_type = 'policy_item'
          AND relationship_type = 'migrated_to'
          AND source_record_id IN ({placeholders})
        """,
        current_ids,
    )

    for item_id, target_rule_id in MANUAL_POLICY_ITEM_TO_RULE_ID.items():
        policy_row = conn.execute(
            """
            SELECT
                p.canonical_statement,
                p.canonical_source_id,
                p.canonical_line_number,
                p.status,
                COALESCE(pio.raw_line, '')
            FROM policy_items p
            LEFT JOIN policy_item_occurrences pio
              ON pio.item_id = p.item_id
             AND pio.source_id = p.canonical_source_id
             AND pio.line_number = p.canonical_line_number
            WHERE p.item_id = ?
            """,
            (item_id,),
        ).fetchone()
        rule_row = conn.execute(
            """
            SELECT canonical_statement, status
            FROM rule_items
            WHERE rule_id = ?
            """,
            (target_rule_id,),
        ).fetchone()
        if not policy_row or not rule_row:
            continue

        policy_statement, source_id, line_number, _policy_status, raw_line = policy_row
        rule_statement, rule_status = rule_row
        notes = "Context-based conversion to the later structured ID corpus."
        conn.execute(
            """
            INSERT INTO record_links (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                canonical_label,
                status,
                target_file,
                notes,
                canonical_source_id,
                canonical_line_number,
                occurrence_count,
                source_count
            )
            VALUES ('policy_item', ?, 'rule_item', ?, 'migrated_to', ?, ?, '', ?, ?, ?, 1, 1)
            """,
            (
                str(item_id),
                target_rule_id,
                rule_statement,
                rule_status,
                notes,
                source_id,
                line_number,
            ),
        )
        conn.execute(
            """
            INSERT INTO record_link_occurrences (
                source_record_type,
                source_record_id,
                target_record_type,
                target_record_id,
                relationship_type,
                source_id,
                line_number,
                label,
                status,
                target_file,
                notes,
                raw_line
            )
            VALUES ('policy_item', ?, 'rule_item', ?, 'migrated_to', ?, ?, ?, ?, '', ?, ?)
            """,
            (
                str(item_id),
                target_rule_id,
                source_id,
                line_number,
                rule_statement,
                rule_status,
                notes,
                raw_line,
            ),
        )


def main() -> None:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    db_path = (args.db or (repo_root / "data" / "policy_catalog.sqlite")).resolve()
    chat_dir = repo_root / "sources" / "chat-logs"
    sources = get_source_files(chat_dir)
    source_lookup = {source.name: source for source in sources}

    if not sources:
        raise SystemExit(f"No chat logs found under {chat_dir}")

    all_source_priority = {**NUMERIC_SOURCE_PRIORITY, **FETCHED_SOURCE_PRIORITY}

    all_policy_occurrences: list[PolicyOccurrence] = []
    all_rule_occurrences: list[RuleOccurrence] = []
    all_record_link_occurrences: list[RecordLinkOccurrence] = []
    all_prose_rule_mentions: list[ProseRuleMention] = []
    for source in sources:
        all_policy_occurrences.extend(parse_numeric_occurrences(source))
        all_rule_occurrences.extend(parse_rule_occurrences(source))
        all_record_link_occurrences.extend(parse_record_link_occurrences(source))
        all_prose_rule_mentions.extend(parse_prose_rule_mentions(source))

    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        create_schema(conn)
        reset_import_tables(conn)
        source_ids = insert_source_files(conn, repo_root, sources)
        import_policy_items(conn, source_ids, all_source_priority, all_policy_occurrences)
        import_rule_items(conn, source_ids, all_source_priority, all_rule_occurrences)
        insert_manual_rule_seeds(conn, source_lookup, source_ids)
        import_record_links(conn, source_ids, all_source_priority, all_record_link_occurrences)
        apply_manual_policy_item_links(conn)
        import_prose_rule_mentions(conn, source_ids, all_prose_rule_mentions)
        conn.commit()

        policy_count = conn.execute("SELECT COUNT(*) FROM policy_items").fetchone()[0]
        policy_occurrence_count = conn.execute("SELECT COUNT(*) FROM policy_item_occurrences").fetchone()[0]
        rule_count = conn.execute("SELECT COUNT(*) FROM rule_items").fetchone()[0]
        rule_occurrence_count = conn.execute("SELECT COUNT(*) FROM rule_occurrences").fetchone()[0]
        record_link_count = conn.execute("SELECT COUNT(*) FROM record_links").fetchone()[0]
        record_link_occurrence_count = conn.execute("SELECT COUNT(*) FROM record_link_occurrences").fetchone()[0]
        prose_rule_mention_count = conn.execute("SELECT COUNT(*) FROM prose_rule_mentions").fetchone()[0]

    print(f"Imported {policy_count} canonical policy items from {policy_occurrence_count} occurrences.")
    print(f"Imported {rule_count} canonical rule items from {rule_occurrence_count} occurrences.")
    print(
        f"Imported {record_link_count} canonical dedupe links from {record_link_occurrence_count} occurrences."
    )
    print(f"Imported {prose_rule_mention_count} contextual ID mentions.")
    print(f"Database written to {db_path}")


if __name__ == "__main__":
    main()
