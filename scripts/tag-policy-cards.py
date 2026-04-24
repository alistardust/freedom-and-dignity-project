#!/usr/bin/env python3
"""
tag-policy-cards.py
=================
Normalize all policy-card IDs across every pillar HTML file.

Algorithm
---------
1. For each pillar HTML file, look up the canonical 3-letter scope code.
2. Walk every <div class="policy-family"> in document order.
3. Derive a scope-family prefix from the policy-family's id attribute:
     fam-eth          (COR pillar) → COR-ETH
     fam-inf-net      (INF pillar) → INF-NET   (INF is a known scope, strip it)
     fam-cor-mpy      (ANT pillar) → ANT-MPY   (COR is a known scope, strip it)
     fam-agr-sub      (ENV pillar) → ENV-AGR-SUB (AGR not a known scope, keep it)
     NO-ID family                  → {SCOPE}-GEN
4. Assign IDs globally per prefix within the pillar (so duplicate fam-ids
   in the same file share a counter: e.g. five fam-ovr divs in CHK give
   CHK-OVR-001 … CHK-OVR-NNN across all of them).
5. Orphaned policy-cards outside any policy-family div get {SCOPE}-GEN-NNN.
6. Write the modified HTML back using BeautifulSoup, preserving DOCTYPE.

All existing IDs are overwritten (full clean-slate renumbering per Ali's direction).

Usage
-----
    python3 scripts/tag-policy-cards.py [--dry-run] [pillar-slug ...]

    --dry-run   Print what would change without writing files.
    pillar-slug  If given, only process those pillar files.
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

from bs4 import BeautifulSoup

# ── Canonical scope code per pillar ──────────────────────────────────────────

PILLAR_SCOPE: dict[str, str] = {
    "administrative-state":          "ADM",
    "anti-corruption":               "COR",
    "antitrust-and-corporate-power": "ANT",
    "checks-and-balances":           "CHK",
    "consumer-rights":               "CON",
    "courts-and-judicial-system":    "JUD",
    "education":                     "EDU",
    "elections-and-representation":  "ELE",
    "environment-and-agriculture":   "ENV",
    "equal-justice-and-policing":    "JUS",
    "executive-power":               "EXP",
    "foreign-policy":                "FPL",
    "gun-policy":                    "GUN",
    "healthcare":                    "HLT",
    "housing":                       "HOU",
    "immigration":                   "IMM",
    "information-and-media":         "MED",
    "infrastructure-and-public-goods": "INF",
    "labor-and-workers-rights":      "LAB",
    "legislative-reform":            "LEG",
    "rights-and-civil-liberties":    "RGT",
    "science-technology-space":      "STS",
    "taxation-and-wealth":           "TAX",
    "technology-and-ai":             "TEC",
    "term-limits-and-fitness":       "TRM",
}

# All 25 canonical scope codes (used to detect old cross-scope prefixes in fam-* ids)
KNOWN_SCOPES: frozenset[str] = frozenset(PILLAR_SCOPE.values())

# Legacy scope codes that may appear as the first segment of a fam-* id
# and should be stripped in favour of the pillar's canonical scope.
LEGACY_SCOPES: frozenset[str] = frozenset({
    "ADM", "AGR", "CIV", "CON", "COR", "ECO", "EDU", "ELE", "ENV",
    "GOV", "GUN", "HLT", "HOU", "IMM", "INF", "JUD", "JUS", "LAB",
    "LEG", "MED", "OVR", "RGT", "STS", "SYS", "TAX", "TEC", "TRM",
})


# ── Helpers ───────────────────────────────────────────────────────────────────

def derive_prefix(fam_id: str, pillar_scope: str) -> str:
    """
    Derive the SCOPE-FAMILY prefix for a policy-family div.

    Examples (pillar scope in parens):
        fam-eth      (COR) → COR-ETH
        fam-inf-net  (INF) → INF-NET
        fam-cor-mpy  (ANT) → ANT-MPY
        fam-agr-sub  (ENV) → ENV-AGR-SUB
        NO-ID / ''   (any) → {pillar_scope}-GEN
    """
    if not fam_id or not fam_id.startswith("fam-"):
        return f"{pillar_scope}-GEN"

    rest = fam_id[4:]           # strip "fam-"
    parts = rest.upper().split("-")

    if len(parts) == 1:
        # Single-segment: just the family name, prepend pillar scope.
        return f"{pillar_scope}-{parts[0]}"

    # Multi-segment: if first segment is a known/legacy scope, strip it.
    if parts[0] in LEGACY_SCOPES or parts[0] in KNOWN_SCOPES:
        family = "-".join(parts[1:])
        return f"{pillar_scope}-{family}"

    # First segment is not a scope code; use the whole thing.
    return f"{pillar_scope}-{'-'.join(parts)}"


def tag_pillar(filepath: Path, dry_run: bool = False) -> dict:
    """Tag all policy-card divs in one pillar file. Returns a stats dict."""
    name = filepath.stem
    if name not in PILLAR_SCOPE:
        return {"skipped": True, "name": name}

    scope = PILLAR_SCOPE[name]
    original_html = filepath.read_text(encoding="utf-8")
    soup = BeautifulSoup(original_html, "html.parser")

    # Counter per prefix, shared across all divs with the same family id.
    counters: dict[str, int] = defaultdict(int)

    def next_id(prefix: str) -> str:
        counters[prefix] += 1
        return f"{prefix}-{counters[prefix]:03d}"

    changed = 0

    # ── Pass 1: cards inside policy-family divs ───────────────────────────
    for fam_div in soup.find_all("div", class_="policy-family"):
        fam_id = fam_div.get("id", "")
        prefix = derive_prefix(fam_id, scope)

        # find_all with recursive=True gets all nested cards too.
        for card in fam_div.find_all("div", class_="policy-card", recursive=True):
            new_id = next_id(prefix)
            if card.get("id") != new_id:
                card["id"] = new_id
                changed += 1

    # ── Pass 2: orphan policy-cards outside any policy-family div ──────────
    orphan_prefix = f"{scope}-GEN"
    for card in soup.find_all("div", class_="policy-card"):
        if not card.find_parent("div", class_="policy-family"):
            new_id = next_id(orphan_prefix)
            if card.get("id") != new_id:
                card["id"] = new_id
                changed += 1

    total_cards = sum(counters.values())

    if not dry_run and changed > 0:
        filepath.write_text(str(soup), encoding="utf-8")

    return {
        "name": name,
        "scope": scope,
        "total_cards": total_cards,
        "changed": changed,
        "families": dict(counters),
    }


# ── CLI ───────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print changes without writing files")
    parser.add_argument("pillars", nargs="*",
                        help="Pillar slugs to process (default: all)")
    args = parser.parse_args()

    pillars_dir = Path(__file__).parent.parent / "docs" / "pillars"
    if args.pillars:
        files = [pillars_dir / f"{slug}.html" for slug in args.pillars]
    else:
        files = sorted(pillars_dir.glob("*.html"))

    grand_total = 0
    grand_changed = 0

    for f in files:
        if not f.exists():
            print(f"  NOT FOUND: {f}", file=sys.stderr)
            continue
        result = tag_pillar(f, dry_run=args.dry_run)
        if result.get("skipped"):
            print(f"  SKIP  {result['name']} (no scope mapping)")
            continue

        marker = " [DRY RUN]" if args.dry_run else ""
        print(
            f"  {'✓' if result['changed'] else '·'}  {result['scope']}  "
            f"{result['name']}: {result['total_cards']} cards, "
            f"{result['changed']} updated{marker}"
        )
        grand_total += result["total_cards"]
        grand_changed += result["changed"]

    action = "Would update" if args.dry_run else "Updated"
    print(f"\nTotal: {grand_total} cards across all pillars, {action} {grand_changed} IDs.")


if __name__ == "__main__":
    main()
