#!/usr/bin/env python3
"""Fix: insert rule-plain paragraphs into technology-and-ai.html from DB."""
import html
import re
import sqlite3
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
HTML_PATH = ROOT / "docs/pillars/technology-and-ai.html"
DB_PATH = ROOT / "policy/catalog/policy_catalog_v2.sqlite"


def get_all_tech_plain() -> list[tuple[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "SELECT id, plain_language FROM positions "
        "WHERE domain='TECH' AND plain_language IS NOT NULL AND plain_language != '' "
        "ORDER BY id"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def update_html(entries: list[tuple[str, str]]) -> tuple[int, list[str]]:
    """Insert rule-plain after rule-title using string find, not regex."""
    text = HTML_PATH.read_text(encoding="utf-8")
    inserted = 0
    warnings = []

    for pos_id, plain_text in entries:
        # Check if already present
        marker = f'id="{pos_id}"'
        card_start = text.find(marker)
        if card_start == -1:
            warnings.append(f"Card not found in HTML: {pos_id}")
            continue

        # Find the next closing </div> after card_start (end of whole policy-card div)
        # Instead just work from card_start forward to find rule-title then rule-stmt

        search_from = card_start

        # Find <p class="rule-plain"> already present in this card
        next_card = text.find('id="TECH-', card_start + len(marker))
        card_end = next_card if next_card != -1 else len(text)
        card_block = text[card_start:card_end]

        if 'class="rule-plain"' in card_block:
            # already done
            continue

        # Find rule-title closing </p> in the card block
        rt_close = card_block.find('</p>', card_block.find('class="rule-title"'))
        if rt_close == -1:
            warnings.append(f"rule-title not found in card: {pos_id}")
            continue

        # Absolute position of end of rule-title closing tag
        rt_close_abs = card_start + rt_close + len('</p>')

        escaped = html.escape(plain_text, quote=False)
        insertion = f'<p class="rule-plain">{escaped}</p>\n'

        text = text[:rt_close_abs] + '\n' + insertion + text[rt_close_abs:]
        inserted += 1

    HTML_PATH.write_text(text, encoding="utf-8")
    return inserted, warnings


def main():
    entries = get_all_tech_plain()
    print(f"Loaded {len(entries)} entries from DB")
    count, warnings = update_html(entries)
    print(f"Inserted {count} rule-plain paragraphs")
    if warnings:
        print(f"Warnings ({len(warnings)}):")
        for w in warnings:
            print(f"  {w}")
    else:
        print("No warnings.")


if __name__ == "__main__":
    main()
