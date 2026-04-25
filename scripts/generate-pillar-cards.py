#!/usr/bin/env python3
"""
generate-pillar-cards.py — Phase 2 static site card generator.

Reads CANONICAL positions from policy_catalog_v2.sqlite and renders
missing cards into the correct <div class="rule-grid"> sections inside
the <section id="pil-policy"> of each pillar HTML file.

Does NOT overwrite existing cards — only appends positions whose v2 ID
is not already present as a policy-card div in the HTML.

Usage:
    python3 scripts/generate-pillar-cards.py --dry-run --all
    python3 scripts/generate-pillar-cards.py --dry-run --pillar healthcare
    python3 scripts/generate-pillar-cards.py --all
    python3 scripts/generate-pillar-cards.py --pillar healthcare
"""
from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from pathlib import Path
from typing import NamedTuple

from bs4 import BeautifulSoup, Tag

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
HTML_DIR = REPO_ROOT / "docs" / "pillars"
POLICY_SECTION_ID = "pil-policy"
V2_ID_RE = re.compile(r"^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$")


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


class PositionRow(NamedTuple):
    id: str
    domain: str
    subdomain: str
    seq: int
    short_title: str
    full_statement: str
    plain_language: str | None


# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------


def open_db(db_path: Path) -> sqlite3.Connection:
    """Open the SQLite DB read-only. Raises FileNotFoundError if missing."""
    if not db_path.exists():
        raise FileNotFoundError(f"Database not found: {db_path}")
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def load_positions(conn: sqlite3.Connection, domain: str) -> list[PositionRow]:
    """
    Load CANONICAL positions for domain, ordered by subdomain then seq.
    Falls back gracefully if the plain_language column does not exist yet.
    """
    try:
        rows = conn.execute(
            """
            SELECT id, domain, subdomain, seq, short_title, full_statement,
                   plain_language
            FROM positions
            WHERE domain = ? AND status = 'CANONICAL'
            ORDER BY subdomain, seq
            """,
            (domain,),
        ).fetchall()
        return [
            PositionRow(
                id=row["id"],
                domain=row["domain"],
                subdomain=row["subdomain"],
                seq=row["seq"],
                short_title=row["short_title"],
                full_statement=row["full_statement"],
                plain_language=row["plain_language"],
            )
            for row in rows
        ]
    except sqlite3.OperationalError:
        # plain_language column not yet added — treat as NULL
        rows = conn.execute(
            """
            SELECT id, domain, subdomain, seq, short_title, full_statement
            FROM positions
            WHERE domain = ? AND status = 'CANONICAL'
            ORDER BY subdomain, seq
            """,
            (domain,),
        ).fetchall()
        return [
            PositionRow(
                id=row["id"],
                domain=row["domain"],
                subdomain=row["subdomain"],
                seq=row["seq"],
                short_title=row["short_title"],
                full_statement=row["full_statement"],
                plain_language=None,
            )
            for row in rows
        ]


def load_all_domains(conn: sqlite3.Connection) -> list[tuple[str, str]]:
    """Return (domain_code, html_file) for all non-cross-domain pillar domains."""
    rows = conn.execute(
        """
        SELECT code, html_file FROM domains
        WHERE is_cross_domain = 0 AND html_file IS NOT NULL
        ORDER BY code
        """
    ).fetchall()
    return [(row["code"], row["html_file"]) for row in rows]


def lookup_domain_for_pillar(
    conn: sqlite3.Connection, pillar_id: str
) -> tuple[str, str]:
    """Return (domain_code, html_file) for a pillar_id slug. Raises on miss."""
    row = conn.execute(
        "SELECT code, html_file FROM domains WHERE pillar_id = ? AND is_cross_domain = 0",
        (pillar_id,),
    ).fetchone()
    if row is None:
        raise ValueError(
            f"No domain found for pillar_id '{pillar_id}'. "
            "Check the pillar_id value in the domains table."
        )
    return row["code"], row["html_file"]


# ---------------------------------------------------------------------------
# HTML analysis helpers
# ---------------------------------------------------------------------------


def get_html_card_ids(soup: BeautifulSoup) -> set[str]:
    """Return the set of v2-format card IDs already present in the HTML."""
    return {
        tag["id"]
        for tag in soup.find_all("div", class_="policy-card")
        if V2_ID_RE.match(str(tag.get("id", "")))
    }


def build_subdomain_grid_map(policy_section: Tag) -> dict[str, Tag]:
    """
    Map subdomain code → the first rule-grid inside pil-policy that already
    contains at least one v2 card with that subdomain.
    """
    mapping: dict[str, Tag] = {}
    for grid in policy_section.find_all("div", class_="rule-grid"):
        for card in grid.find_all("div", class_="policy-card"):
            card_id = str(card.get("id", ""))
            if V2_ID_RE.match(card_id):
                subdomain = card_id.split("-")[1]
                if subdomain not in mapping:
                    mapping[subdomain] = grid
    return mapping


# ---------------------------------------------------------------------------
# Card construction
# ---------------------------------------------------------------------------


def build_card_tag(soup: BeautifulSoup, pos: PositionRow) -> Tag:
    """
    Construct a <div class="policy-card"> Tag for the given position.

    Template (Phase 2 canonical form):
        <div class="policy-card" id="XXXX-XXXX-0000">
          <p class="rule-id"><code class="rule-id">XXXX-XXXX-0000</code></p>
          <p class="rule-plain">[plain_language or empty]</p>
          <p class="rule-title">[short_title]</p>
          <p class="rule-stmt">[full_statement]</p>
        </div>
    """
    card: Tag = soup.new_tag("div", **{"class": "policy-card", "id": pos.id})

    rule_id_p: Tag = soup.new_tag("p", **{"class": "rule-id"})
    code_el: Tag = soup.new_tag("code", **{"class": "rule-id"})
    code_el.string = pos.id
    rule_id_p.append(code_el)
    card.append(rule_id_p)

    rule_plain: Tag = soup.new_tag("p", **{"class": "rule-plain"})
    if pos.plain_language:
        rule_plain.string = pos.plain_language
    card.append(rule_plain)

    rule_title: Tag = soup.new_tag("p", **{"class": "rule-title"})
    rule_title.string = pos.short_title
    card.append(rule_title)

    rule_stmt: Tag = soup.new_tag("p", **{"class": "rule-stmt"})
    rule_stmt.string = pos.full_statement
    card.append(rule_stmt)

    return card


# ---------------------------------------------------------------------------
# Grid resolution
# ---------------------------------------------------------------------------


def find_or_create_grid(
    soup: BeautifulSoup,
    policy_section: Tag,
    subdomain: str,
    subdomain_grid_map: dict[str, Tag],
) -> Tag:
    """
    Return the rule-grid element for the given subdomain, creating a new
    family-header + rule-grid pair at the end of pil-policy if none exists.
    """
    if subdomain in subdomain_grid_map:
        return subdomain_grid_map[subdomain]

    # No existing grid for this subdomain — create one at the end of pil-policy
    fam_header: Tag = soup.new_tag("div", **{"class": "family-header"})
    fam_code_span: Tag = soup.new_tag("span", **{"class": "family-code"})
    fam_code_span.string = subdomain
    fam_title_span: Tag = soup.new_tag("span", **{"class": "family-title"})
    fam_title_span.string = subdomain
    fam_header.append(fam_code_span)
    fam_header.append(fam_title_span)

    grid: Tag = soup.new_tag("div", **{"class": "rule-grid"})

    policy_section.append(fam_header)
    policy_section.append(grid)

    subdomain_grid_map[subdomain] = grid
    return grid


# ---------------------------------------------------------------------------
# Core processing
# ---------------------------------------------------------------------------


def process_pillar(
    domain_code: str,
    html_file: str,
    conn: sqlite3.Connection,
    dry_run: bool,
) -> tuple[int, list[str]]:
    """
    Process one pillar HTML file. Returns (cards_added_count, messages).

    In dry_run mode no files are modified; messages describe what would change.
    """
    html_path = REPO_ROOT / "docs" / html_file
    if not html_path.exists():
        raise FileNotFoundError(f"HTML file not found: {html_path}")

    positions = load_positions(conn, domain_code)
    if not positions:
        return 0, []

    original_html = html_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(original_html, "html.parser")

    policy_section = soup.find("section", id=POLICY_SECTION_ID)
    if not isinstance(policy_section, Tag):
        raise ValueError(
            f"<section id='{POLICY_SECTION_ID}'> not found in {html_path.name}. "
            "Cannot determine where to insert cards."
        )

    existing_ids = get_html_card_ids(soup)
    subdomain_grid_map = build_subdomain_grid_map(policy_section)

    messages: list[str] = []
    cards_added = 0

    for pos in positions:
        if pos.id in existing_ids:
            continue  # Already present — idempotent

        grid = find_or_create_grid(soup, policy_section, pos.subdomain, subdomain_grid_map)
        card_tag = build_card_tag(soup, pos)
        messages.append(f"  + {pos.id} ({pos.subdomain})")
        cards_added += 1

        if not dry_run:
            grid.append(card_tag)
            existing_ids.add(pos.id)

    if not dry_run and cards_added > 0:
        html_path.write_text(str(soup), encoding="utf-8")

    return cards_added, messages


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Phase 2 card generator: renders missing DB positions into "
            "pillar HTML files without overwriting existing cards."
        ),
    )
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument(
        "--pillar",
        metavar="PILLAR_ID",
        help="Process a single pillar by its pillar_id slug (e.g. 'healthcare').",
    )
    target.add_argument(
        "--all",
        action="store_true",
        help="Process all pillar HTML files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would change without modifying any HTML files.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    try:
        conn = open_db(DB_PATH)
    except FileNotFoundError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        sys.exit(1)

    try:
        if args.all:
            domains = load_all_domains(conn)
        else:
            domain_code, html_file = lookup_domain_for_pillar(conn, args.pillar)
            domains = [(domain_code, html_file)]
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        conn.close()
        sys.exit(1)

    if args.dry_run:
        print("[DRY RUN] No files will be modified.\n")

    total_added = 0
    total_pillars_changed = 0

    for domain_code, html_file in domains:
        try:
            added, messages = process_pillar(domain_code, html_file, conn, args.dry_run)
        except (FileNotFoundError, ValueError) as exc:
            print(f"[ERROR] {domain_code}: {exc}", file=sys.stderr)
            conn.close()
            sys.exit(1)

        total_added += added
        if added > 0:
            total_pillars_changed += 1
            verb = "Would add" if args.dry_run else "Added"
            print(f"{verb} {added} card(s) to {html_file}:")
            for msg in messages:
                print(msg)

    conn.close()

    verb = "Would add" if args.dry_run else "Added"
    print(
        f"\n{verb} {total_added} card(s) across "
        f"{total_pillars_changed}/{len(domains)} pillar(s)."
    )


if __name__ == "__main__":
    main()
