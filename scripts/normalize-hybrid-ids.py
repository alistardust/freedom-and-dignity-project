#!/usr/bin/env python3
"""
normalize-hybrid-ids.py

Fixes policy-card IDs in pillar HTML files that use a "hybrid" format:
valid 4-digit sequences but non-conforming domain (3-char) or subdomain
(3-char, 5-char, or containing digits) that prevent them from being
parsed as canonical v2 IDs by build-catalog-v2.py.

Writes corrected IDs directly to the HTML files and prints a report.
Run build-catalog-v2.py afterward to pick up the normalized cards.

Usage:
    python3 scripts/normalize-hybrid-ids.py [--dry-run]
"""

from __future__ import annotations

import argparse
import re
import sqlite3
import sys
from collections import defaultdict
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PILLARS_DIR = REPO_ROOT / "docs" / "pillars"
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"

# Mapping: (old_domain, old_subdomain) → (new_domain, new_subdomain)
PREFIX_FIXES: dict[tuple[str, str], tuple[str, str]] = {
    # --- 3-char domain → 4-char domain ---
    ("ADM", "DPA"):  ("ADMN", "DPAS"),
    ("ADM", "LCAL"): ("ADMN", "LCAL"),
    ("ADM", "MDRG"): ("ADMN", "MDRG"),
    ("ADM", "SDST"): ("ADMN", "SDST"),
    ("ADM", "TANF"): ("ADMN", "TANF"),
    ("ADM", "UNEM"): ("ADMN", "UNEM"),
    ("AGR", "CHKN"): ("ENVR", "CHKN"),
    ("AGR", "CORN"): ("ENVR", "CORN"),
    ("ENV", "COAL"): ("ENVR", "COAL"),
    ("ENV", "COFF"): ("ENVR", "COFF"),
    ("ENV", "FRCK"): ("ENVR", "FRCK"),
    ("ENV", "NGAS"): ("ENVR", "NGAS"),
    ("ENV", "OILG"): ("ENVR", "OILG"),
    ("ENV", "PLST"): ("ENVR", "PLST"),
    ("ENV", "RFNY"): ("ENVR", "RFNY"),
    ("GUN", "EXCL"): ("GUNS", "EXCL"),
    ("GUN", "RSCH"): ("GUNS", "RSCH"),
    ("GUN", "SAFE"): ("GUNS", "SAFE"),
    ("GUN", "TRAF"): ("GUNS", "TRAF"),
    ("INF", "UTIL"): ("INFR", "UTIL"),
    ("LEG", "ETHX"): ("LEGL", "ETHX"),
    ("LEG", "FILB"): ("LEGL", "FILB"),
    ("LEG", "LBBY"): ("LEGL", "LBBY"),
    # --- 4-char domain, 5-char subdomain → truncate to 4 ---
    ("CNSR", "TMSHR"): ("CNSR", "TMSH"),   # Timeshare
    ("CRPT", "CNSLT"): ("CRPT", "CNSL"),   # Consulting/lobbying
    ("EDUC", "VCHRS"): ("EDUC", "VCHR"),   # School vouchers
    ("ENVR", "PLTRY"): ("ENVR", "PLTR"),   # Poultry industry
    ("JUST", "SLTRY"): ("JUST", "SLTR"),   # Solitary confinement
    # --- 4-char domain, 3-char subdomain → add S suffix ---
    ("ENVR", "GND"):  ("ENVR", "GNDS"),    # Green New Deal
    ("HOUS", "HOA"):  ("HOUS", "HOAS"),    # Homeowners associations (merges into HOAS)
    ("HOUS", "MHP"):  ("HOUS", "MHPS"),    # Mobile home parks
    ("INFR", "TOD"):  ("INFR", "TODS"),    # Transit-oriented development
    ("JUST", "CAF"):  ("JUST", "CAFS"),    # Civil asset forfeiture
    ("JUST", "SRO"):  ("JUST", "SROS"),    # School resource officers
    ("LABR", "GIG"):  ("LABR", "GIGS"),    # Gig economy (merges into GIGS)
    # --- Special cases: non-alpha or ambiguous subdomains ---
    ("EDUC", "K12"):  ("EDUC", "SCHL"),    # K-12 → schooling
    ("TECH", "S230"): ("TECH", "PLAT"),    # Section 230 → platform liability
}

# v2 ID regex
V2_RE = re.compile(r"^[A-Z]{4}-[A-Z]{4}-[0-9]{4}$")
# Pattern to find hybrid IDs inside id= and <code> text:
# Captures: domain-sub-seq where domain or sub length ≠ 4, or sub contains digit
HYBRID_RE = re.compile(r"\b([A-Z]{3,5}-[A-Z0-9]{2,5}-[0-9]{4})\b")


def get_max_sequences(db_path: Path) -> dict[tuple[str, str], int]:
    """Return the current max sequence number per (domain, subdomain) in the DB."""
    seq_map: dict[tuple[str, str], int] = defaultdict(int)
    if not db_path.exists():
        return seq_map
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("SELECT id FROM positions")
    for (pid,) in cur.fetchall():
        if V2_RE.match(pid):
            dom, sub, seq = pid.split("-")
            seq_map[(dom, sub)] = max(seq_map[(dom, sub)], int(seq))
    conn.close()
    return seq_map


def build_replacement_map(
    hybrid_ids: list[str],
    db_seq_map: dict[tuple[str, str], int],
) -> dict[str, str]:
    """
    Build a mapping from each old hybrid ID to its canonical v2 ID.

    Sequence numbers are assigned in the order IDs are encountered.
    For target families already in the DB, new sequences continue
    from max_existing + 1.
    """
    # Track next available sequence per target (domain, sub)
    next_seq: dict[tuple[str, str], int] = {}
    for (dom, sub), max_seq in db_seq_map.items():
        next_seq[(dom, sub)] = max_seq + 1

    old_to_new: dict[str, str] = {}

    for old_id in sorted(set(hybrid_ids)):
        if V2_RE.match(old_id):
            continue  # Already canonical
        parts = old_id.split("-")
        if len(parts) != 3:
            print(f"[SKIP] Unexpected format: {old_id}", file=sys.stderr)
            continue
        old_dom, old_sub, old_seq = parts
        fix = PREFIX_FIXES.get((old_dom, old_sub))
        if fix is None:
            print(f"[WARN] No mapping for ({old_dom}, {old_sub}) — skipping {old_id}", file=sys.stderr)
            continue
        new_dom, new_sub = fix
        target = (new_dom, new_sub)
        # Assign next sequence for this target family
        if target not in next_seq:
            next_seq[target] = 1
        new_id = f"{new_dom}-{new_sub}-{next_seq[target]:04d}"
        next_seq[target] += 1
        old_to_new[old_id] = new_id

    return old_to_new


def find_hybrid_ids_in_file(html: str) -> list[str]:
    """Return all hybrid IDs found in an HTML file, in document order."""
    return [m for m in HYBRID_RE.findall(html) if not V2_RE.match(m)]


def apply_replacements(html: str, replacement_map: dict[str, str]) -> tuple[str, list[tuple[str, str]]]:
    """Replace all occurrences of old IDs with new IDs. Returns (new_html, changes)."""
    changes: list[tuple[str, str]] = []

    def replacer(m: re.Match) -> str:
        old = m.group(1)
        new = replacement_map.get(old)
        if new:
            changes.append((old, new))
            return new
        return old

    new_html = HYBRID_RE.sub(replacer, html)
    return new_html, changes


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize hybrid policy-card IDs in pillar HTML files.")
    parser.add_argument("--dry-run", action="store_true", help="Print changes without writing files.")
    args = parser.parse_args()

    print("[INFO] Loading current DB sequence numbers...")
    db_seq_map = get_max_sequences(DB_PATH)

    # Collect all hybrid IDs across all pillar HTML files
    all_hybrid: list[str] = []
    file_hybrids: dict[Path, list[str]] = {}
    for html_file in sorted(PILLARS_DIR.glob("*.html")):
        html = html_file.read_text(encoding="utf-8")
        hybrids = find_hybrid_ids_in_file(html)
        if hybrids:
            file_hybrids[html_file] = hybrids
            all_hybrid.extend(hybrids)

    if not all_hybrid:
        print("[INFO] No hybrid IDs found. Nothing to do.")
        return

    unique_hybrid = sorted(set(all_hybrid))
    print(f"[INFO] Found {len(unique_hybrid)} unique hybrid IDs across {len(file_hybrids)} files.")

    # Build replacement map (sequenced globally so IDs are unique)
    replacement_map = build_replacement_map(unique_hybrid, db_seq_map)

    if not replacement_map:
        print("[WARN] Replacement map is empty — check PREFIX_FIXES for missing entries.")
        return

    # Apply to each file
    total_replacements = 0
    for html_file, _ in sorted(file_hybrids.items()):
        html = html_file.read_text(encoding="utf-8")
        new_html, changes = apply_replacements(html, replacement_map)
        if not changes:
            continue
        unique_changes = sorted(set(changes))
        print(f"\n[FILE] {html_file.name} — {len(unique_changes)} unique ID(s) renamed:")
        for old, new in unique_changes:
            count = sum(1 for o, _ in changes if o == old)
            print(f"  {old}  →  {new}  ({count} occurrence{'s' if count > 1 else ''})")
        total_replacements += len(unique_changes)
        if not args.dry_run:
            html_file.write_text(new_html, encoding="utf-8")

    print(f"\n[SUMMARY] {total_replacements} unique ID pairs renamed across {len(file_hybrids)} files.")
    if args.dry_run:
        print("[DRY RUN] No files were modified.")
    else:
        print("[INFO] Files updated. Run scripts/build-catalog-v2.py to rebuild the DB.")

    # Print full mapping for the report
    print("\n[MAPPING] Complete old → new ID table:")
    print(f"{'Old ID':<30} {'New ID'}")
    print("-" * 60)
    for old, new in sorted(replacement_map.items()):
        print(f"{old:<30} {new}")


if __name__ == "__main__":
    main()
