#!/usr/bin/env python3
"""scripts/reconcile-catalog.py

Three-way audit: HTML policy cards <-> DB policy_items <-> pillars/ markdown.

Produces data/reconciliation-report.md — READ-ONLY REPORT, no modifications to
HTML or DB. Ali must review and sign off before any Phase 2 migration begins.

Conflict resolution rules (to be applied during Phase 2, NOT here):
  - HTML has it, DB doesn't    → HTML wins; DB must be backfilled
  - DB has it, HTML doesn't    → Add as proposal card to HTML
  - Both have it, text diverges → FLAG for human review
"""

from __future__ import annotations

import re
import sqlite3
from collections import defaultdict
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:
    raise SystemExit("BeautifulSoup4 is required: pip install beautifulsoup4")

REPO_ROOT = Path(__file__).parent.parent
DB_PATH = REPO_ROOT / "data" / "policy_catalog_v2.sqlite"
PILLARS_HTML_DIR = REPO_ROOT / "docs" / "pillars"
PILLARS_MD_DIR = REPO_ROOT / "pillars"
REPORT_PATH = REPO_ROOT / "data" / "reconciliation-report.md"


# ── HTML extraction ───────────────────────────────────────────────────────────


def extract_html_cards() -> list[dict]:
    """Extract all policy cards from all pillar HTML files."""
    cards: list[dict] = []

    for html_file in sorted(PILLARS_HTML_DIR.glob("*.html")):
        if html_file.name == "index.html":
            continue
        soup = BeautifulSoup(html_file.read_text(encoding="utf-8"), "html.parser")

        for card in soup.find_all(
            "div",
            class_=lambda c: c and "policy-card" in c.split() if c else False,
        ):
            div_id = card.get("id", "")
            code_el = card.find(
                "code",
                class_=lambda x: x and "rule-id" in x.split() if x else False,
            )
            rule_id_code = code_el.get_text(strip=True) if code_el else ""
            title_el = card.find(
                "p",
                class_=lambda x: x and "rule-title" in x.split() if x else False,
            )
            title = title_el.get_text(strip=True) if title_el else ""
            classes = card.get("class", [])
            is_proposal = "proposal" in classes

            # Canonical ID: code element is authoritative; div id is a fragment anchor
            canonical_id = rule_id_code or div_id

            # ID validity check: v2 format XXXX-XXXX-0000
            valid_id_pattern = re.compile(r"^[A-Z]{4}-[A-Z]{4}-\d{4}$")
            id_is_valid = bool(canonical_id and valid_id_pattern.match(canonical_id))

            cards.append(
                {
                    "source_file": html_file.name,
                    "div_id": div_id,
                    "rule_id_code": rule_id_code,
                    "canonical_id": canonical_id,
                    "title": title,
                    "is_proposal": is_proposal,
                    "classes": " ".join(classes),
                    "id_mismatch": (
                        div_id != rule_id_code
                        and bool(div_id)
                        and bool(rule_id_code)
                    ),
                    "id_is_valid": id_is_valid,
                }
            )

    return cards


# ── DB extraction ─────────────────────────────────────────────────────────────


def extract_db_items() -> dict[str, dict]:
    """Extract all positions from v2 DB, keyed by id."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    items = {
        row["id"]: {
            "rule_id": row["id"],
            "canonical_statement": row["short_title"],
            "full_statement": row["full_statement"],
            "status": row["status"],
            "domain": row["domain"],
        }
        for row in conn.execute(
            "SELECT id, short_title, full_statement, status, domain FROM positions ORDER BY id"
        )
    }
    conn.close()
    return items


# ── Markdown extraction ───────────────────────────────────────────────────────


def extract_markdown_ids() -> dict[str, list[str]]:
    """Find policy IDs mentioned in pillars/ markdown files."""
    id_pattern = re.compile(r"\b([A-Z]{4}-[A-Z]{4}-\d{4})\b")
    md_ids: dict[str, list[str]] = {}

    for md_file in sorted(PILLARS_MD_DIR.rglob("*.md")):
        text = md_file.read_text(encoding="utf-8")
        found = id_pattern.findall(text)
        if found:
            md_ids[str(md_file.relative_to(REPO_ROOT))] = list(set(found))

    return md_ids


# ── Classification ────────────────────────────────────────────────────────────


def _title_similarity(a: str, b: str) -> bool:
    """Return True if two titles appear to describe the same position."""
    a_norm = re.sub(r"[^a-z0-9 ]", "", a.lower()).strip()
    b_norm = re.sub(r"[^a-z0-9 ]", "", b.lower()).strip()
    if a_norm == b_norm:
        return True
    # Check first 20 chars match after normalization
    if len(a_norm) >= 20 and len(b_norm) >= 20:
        return a_norm[:20] == b_norm[:20]
    # Check if one is a substring of the other
    shorter, longer = (a_norm, b_norm) if len(a_norm) <= len(b_norm) else (b_norm, a_norm)
    return shorter in longer or longer in shorter


def classify(
    html_cards: list[dict],
    db_items: dict[str, dict],
) -> dict:
    """Cross-reference HTML cards against DB items."""
    # Group HTML cards by canonical_id
    html_by_id: dict[str, list[dict]] = defaultdict(list)
    for card in html_cards:
        cid = card["canonical_id"]
        if cid:
            html_by_id[cid].append(card)

    html_id_set = set(html_by_id.keys())
    db_id_set = set(db_items.keys())

    both = html_id_set & db_id_set
    html_only = html_id_set - db_id_set
    db_only = db_id_set - html_id_set

    # Divergence check: in both sets but title/statement differ significantly
    diverge: list[dict] = []
    for cid in sorted(both):
        html_title = html_by_id[cid][0]["title"]
        db_stmt = db_items[cid]["canonical_statement"]
        if not _title_similarity(html_title, db_stmt):
            diverge.append(
                {
                    "id": cid,
                    "html_title": html_title,
                    "db_statement": db_stmt,
                    "source_file": html_by_id[cid][0]["source_file"],
                }
            )

    # No-ID cards
    no_id_cards = [c for c in html_cards if not c["canonical_id"]]

    # ID mismatches (div id ≠ code element id)
    id_mismatches = [c for c in html_cards if c["id_mismatch"]]

    # Duplicate IDs in HTML
    duplicate_ids = {cid: cards for cid, cards in html_by_id.items() if len(cards) > 1}

    # Invalid ID format
    invalid_id_cards = [c for c in html_cards if c["canonical_id"] and not c["id_is_valid"]]

    return {
        "html_by_id": html_by_id,
        "html_id_set": html_id_set,
        "db_id_set": db_id_set,
        "both": both,
        "html_only": html_only,
        "db_only": db_only,
        "diverge": diverge,
        "no_id_cards": no_id_cards,
        "id_mismatches": id_mismatches,
        "duplicate_ids": duplicate_ids,
        "invalid_id_cards": invalid_id_cards,
    }


# ── Report generation ─────────────────────────────────────────────────────────


def _scope_summary(ids: set[str]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for pid in ids:
        scope = pid.split("-")[0] if "-" in pid else "???"
        counts[scope] += 1
    return dict(sorted(counts.items()))


def generate_report(
    html_cards: list[dict],
    db_items: dict[str, dict],
    md_ids: dict[str, list[str]],
    results: dict,
) -> str:
    lines: list[str] = []
    a = lines.append

    a("# Policy Catalog Reconciliation Report")
    a("")
    a("> **READ-ONLY REPORT** — No HTML or DB changes were made.")
    a("> Phase 2 migration may begin only after Ali signs off on this report.")
    a("")
    a("---")
    a("")
    a("## Summary")
    a("")
    a(f"| Item | Count |")
    a(f"|------|-------|")
    a(f"| HTML policy cards (total) | {len(html_cards):,} |")
    a(f"| HTML cards with valid ID | {sum(1 for c in html_cards if c['id_is_valid']):,} |")
    a(f"| HTML cards with NO ID | {len(results['no_id_cards']):,} |")
    a(f"| HTML cards: div id ≠ code element id | {len(results['id_mismatches']):,} |")
    a(f"| HTML cards: invalid ID format | {len(results['invalid_id_cards']):,} |")
    a(f"| DB policy_items (total) | {len(db_items):,} |")
    a(f"| **Confirmed match** (in both HTML & DB) | **{len(results['both']):,}** |")
    a(f"| Text divergence (same ID, different text) | {len(results['diverge']):,} |")
    a(f"| **HTML-only** (on site, not in DB) | **{len(results['html_only']):,}** |")
    a(f"| **DB-only** (in DB, not on site) | **{len(results['db_only']):,}** |")
    a(f"| Duplicate IDs in HTML | {len(results['duplicate_ids']):,} |")
    a("")
    a("---")
    a("")

    # ── HTML-only ──────────────────────────────────────────────────────────────
    a("## HTML-only cards (on site, not in DB)")
    a("")
    a("These cards exist in the HTML but have no matching `rule_id` in `policy_items`.")
    a("Per Phase 2 conflict rules: **HTML wins — DB must be backfilled.**")
    a("")

    html_only_sorted = sorted(results["html_only"])
    scope_counts = _scope_summary(results["html_only"])
    a("**By scope:**")
    for scope, count in scope_counts.items():
        a(f"- `{scope}`: {count}")
    a("")
    a(f"**Total: {len(html_only_sorted)}**")
    a("")
    a("<details>")
    a("<summary>Full list</summary>")
    a("")
    a("| ID | Title | File |")
    a("|----|-------|------|")
    for pid in html_only_sorted:
        cards = results["html_by_id"][pid]
        title = cards[0]["title"][:70]
        src = cards[0]["source_file"]
        a(f"| `{pid}` | {title} | {src} |")
    a("")
    a("</details>")
    a("")
    a("---")
    a("")

    # ── DB-only ────────────────────────────────────────────────────────────────
    a("## DB-only items (in DB, not on site)")
    a("")
    a("These items are in `policy_items` but have no matching ID on the site.")
    a("Per Phase 2 conflict rules: **Add as proposal card to HTML.**")
    a("")
    a("> ⚠️ NOTE: DB `status = 'MISSING'` does NOT reliably indicate the item is absent")
    a("> from the site. Many HTML cards were added after the DB was built from source logs.")
    a("> This list reflects IDs genuinely absent from HTML, not the DB status field.")
    a("")

    db_only_sorted = sorted(results["db_only"])
    scope_counts_db = _scope_summary(results["db_only"])
    a("**By scope:**")
    for scope, count in scope_counts_db.items():
        a(f"- `{scope}`: {count}")
    a("")
    a(f"**Total: {len(db_only_sorted)}**")
    a("")
    a("<details>")
    a("<summary>Full list</summary>")
    a("")
    a("| ID | Statement | DB Status |")
    a("|----|-----------|-----------|")
    for pid in db_only_sorted:
        item = db_items[pid]
        stmt = item["canonical_statement"][:70]
        status = item["status"]
        a(f"| `{pid}` | {stmt} | {status} |")
    a("")
    a("</details>")
    a("")
    a("---")
    a("")

    # ── Divergence ─────────────────────────────────────────────────────────────
    a("## Text divergences (same ID, different text)")
    a("")
    a("These items are in both HTML and DB, but the text appears to differ.")
    a("**These require human review — do not auto-resolve.**")
    a("")
    if results["diverge"]:
        a(f"**Total: {len(results['diverge'])}**")
        a("")
        a("| ID | HTML title | DB statement | File |")
        a("|----|-----------|--------------|------|")
        for item in sorted(results["diverge"], key=lambda x: x["id"]):
            html_t = item["html_title"][:55]
            db_s = item["db_statement"][:55]
            a(f"| `{item['id']}` | {html_t} | {db_s} | {item['source_file']} |")
    else:
        a("✅ No text divergences detected.")
    a("")
    a("---")
    a("")

    # ── ID mismatches ──────────────────────────────────────────────────────────
    a("## ID mismatches (div `id` attribute ≠ `<code class=\"rule-id\">` element)")
    a("")
    a("The `<code class=\"rule-id\">` is the authoritative policy ID.")
    a("The `id=` attribute on the div is the HTML fragment anchor and should match.")
    a("These are data integrity issues to fix before Phase 2.")
    a("")
    if results["id_mismatches"]:
        a(f"**Total: {len(results['id_mismatches'])}**")
        a("")
        a("<details>")
        a("<summary>Full list (grouped by file)</summary>")
        a("")
        by_file: dict[str, list[dict]] = defaultdict(list)
        for c in results["id_mismatches"]:
            by_file[c["source_file"]].append(c)
        for fname in sorted(by_file.keys()):
            a(f"### {fname} ({len(by_file[fname])} mismatches)")
            a("")
            a("| div id | rule-id code | Title |")
            a("|--------|-------------|-------|")
            for c in by_file[fname]:
                a(f"| `{c['div_id']}` | `{c['rule_id_code']}` | {c['title'][:50]} |")
            a("")
        a("</details>")
    else:
        a("✅ No ID mismatches detected.")
    a("")
    a("---")
    a("")

    # ── No-ID cards ────────────────────────────────────────────────────────────
    a("## Cards with no ID")
    a("")
    if results["no_id_cards"]:
        a(f"**Total: {len(results['no_id_cards'])}**")
        a("")
        a("| File | Title |")
        a("|------|-------|")
        for c in results["no_id_cards"]:
            a(f"| {c['source_file']} | {c['title'][:60]} |")
    else:
        a("✅ All cards have IDs.")
    a("")
    a("---")
    a("")

    # ── Duplicate IDs ──────────────────────────────────────────────────────────
    a("## Duplicate IDs in HTML")
    a("")
    if results["duplicate_ids"]:
        a(f"**{len(results['duplicate_ids'])} IDs appear on more than one card.**")
        a("")
        a("| ID | Files |")
        a("|----|-------|")
        for pid, cards in sorted(results["duplicate_ids"].items()):
            files = ", ".join(set(c["source_file"] for c in cards))
            a(f"| `{pid}` | {files} |")
    else:
        a("✅ No duplicate IDs found.")
    a("")
    a("---")
    a("")

    # ── Markdown cross-reference ──────────────────────────────────────────────
    a("## Markdown cross-reference")
    a("")
    a("Policy IDs mentioned in `pillars/` markdown sources.")
    a("")
    if md_ids:
        all_md_ids: set[str] = set()
        for file_ids in md_ids.values():
            all_md_ids.update(file_ids)

        md_not_in_html = all_md_ids - results["html_id_set"]
        md_not_in_db = all_md_ids - results["db_id_set"]

        a(f"- Markdown files with policy IDs: {len(md_ids)}")
        a(f"- Unique IDs mentioned in markdown: {len(all_md_ids)}")
        a(f"- Markdown IDs not found in HTML: {len(md_not_in_html)}")
        a(f"- Markdown IDs not found in DB: {len(md_not_in_db)}")
    else:
        a("No policy IDs found in `pillars/` markdown files.")
    a("")
    a("---")
    a("")

    # ── Action items ──────────────────────────────────────────────────────────
    a("## Required actions before Phase 2")
    a("")
    a("1. **Fix ID mismatches**: Update all div `id` attributes to match their `<code class=\"rule-id\">` value")
    a(f"   ({len(results['id_mismatches'])} mismatches across all pillar files)")
    a("2. **Assign IDs to untagged cards**: {len(results['no_id_cards'])} cards have no ID — run `scripts/tag-policy-cards.py`")
    a("3. **Review divergences**: {len(results['diverge'])} items have mismatched text between HTML and DB — human decision required")
    a("4. **Backfill HTML-only items**: {len(results['html_only'])} HTML cards must be added to DB before DB becomes canonical")
    a("5. **Add DB-only items to HTML**: {len(results['db_only'])} DB items must appear as proposal cards in the correct pillar pages")
    a("")
    a("Ali must sign off on this report before Phase 2 migration begins.")
    a("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> None:
    print("Extracting HTML cards...")
    html_cards = extract_html_cards()
    print(f"  {len(html_cards):,} cards extracted from HTML")

    print("Extracting DB items...")
    db_items = extract_db_items()
    print(f"  {len(db_items):,} items extracted from DB")

    print("Extracting markdown IDs...")
    md_ids = extract_markdown_ids()
    id_count = sum(len(v) for v in md_ids.values())
    print(f"  {id_count:,} IDs found across {len(md_ids)} markdown files")

    print("Classifying...")
    results = classify(html_cards, db_items)

    print(f"  Confirmed match: {len(results['both']):,}")
    print(f"  HTML-only:       {len(results['html_only']):,}")
    print(f"  DB-only:         {len(results['db_only']):,}")
    print(f"  Text diverges:   {len(results['diverge']):,}")
    print(f"  ID mismatches:   {len(results['id_mismatches']):,}")
    print(f"  No-ID cards:     {len(results['no_id_cards']):,}")

    print("Generating report...")
    report = generate_report(html_cards, db_items, md_ids, results)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(f"  Report written to: {REPORT_PATH}")
    print("")
    print("Done. Review data/reconciliation-report.md before proceeding to Phase 2.")


if __name__ == "__main__":
    main()
