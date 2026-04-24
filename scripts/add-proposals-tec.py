#!/usr/bin/env python3
"""
add-proposals-tec.py
====================
Insert MISSING/PROPOSED TEC policy positions from the database into
docs/pillars/technology-and-ai.html as proposal cards.

Only adds cards whose rule_id is not already present as an id= attribute
in the HTML. Preserves all existing content exactly.
"""

import sys
import sqlite3
import re
import os

sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.14/site-packages'))
from bs4 import BeautifulSoup, Tag

HTML_PATH = 'docs/pillars/technology-and-ai.html'
DB_PATH = 'data/policy_catalog.sqlite'

# Map family_code → existing fam-* id in HTML (lower-case)
# Built from grep output; tec-prefixed families use the tec- prefix
FAMILY_MAP = {
    'AGE': 'fam-age',
    'AI':  'fam-ai',
    'ALG': 'fam-alg',
    'AUD': 'fam-aud',
    'AUT': 'fam-aut',
    'BIO': 'fam-bio',
    'DAT': 'fam-dat',
    'EDU': 'fam-edu',
    'ENV': 'fam-env',
    'FIN': 'fam-fin',
    'GOV': 'fam-gov',
    'HAR': 'fam-tec-har',
    'IMM': 'fam-imm',
    'INT': 'fam-int',
    'JUD': 'fam-jud',
    'LAB': 'fam-lab',
    'MHC': 'fam-mhc',
    'MIL': 'fam-mil',
    'MKT': 'fam-tec-mkt',
    'OVR': 'fam-ovr',
    'PRV': 'fam-prv',
    'PUB': 'fam-tec-pub',
    'SUR': 'fam-sur',
    'SYN': 'fam-syn',
    # families that need new sections are absent from this map intentionally
}

# Human-readable names for new family sections we must create
NEW_FAMILY_NAMES = {
    'CHD': ('fam-chd',  'Child Safety & AI'),
    'DEM': ('fam-dem',  'Democratic Integrity'),
    'INF': ('fam-inf',  'Critical Infrastructure'),
    'MED': ('fam-med',  'Media Recommender Systems'),
    'SCI': ('fam-sci',  'Scientific Integrity'),
}


def first_sentence(text: str) -> str:
    """Return the first sentence (up to 120 chars) as a short title."""
    m = re.match(r'^(.+?[.!?])\s', text)
    if m and len(m.group(1)) <= 160:
        return m.group(1)
    # Fall back to first 120 chars + ellipsis
    if len(text) <= 120:
        return text
    cut = text[:120].rsplit(' ', 1)[0]
    return cut + '…'


def make_proposal_card(soup: BeautifulSoup, rule_id: str, stmt: str, status: str) -> Tag:
    """Build a proposal card Tag."""
    card = soup.new_tag('div', attrs={'class': 'policy-card proposal', 'id': rule_id})

    header = soup.new_tag('div', attrs={'class': 'rule-header'})
    code_tag = soup.new_tag('code', attrs={'class': 'rule-id'})
    code_tag.string = rule_id
    badge = soup.new_tag('span', attrs={'class': 'rule-badge'})
    badge.string = 'Proposal'
    header.append(code_tag)
    header.append(badge)
    card.append(header)

    status_div = soup.new_tag('div', attrs={'class': 'rule-status'})
    status_div.string = '🔵 Proposal — Under Review'
    card.append(status_div)

    title_p = soup.new_tag('p', attrs={'class': 'rule-title'})
    title_p.string = first_sentence(stmt)
    card.append(title_p)

    stmt_p = soup.new_tag('p', attrs={'class': 'rule-stmt'})
    stmt_p.string = stmt
    card.append(stmt_p)

    notes_p = soup.new_tag('p', attrs={'class': 'rule-notes'})
    notes_p.string = (
        f'Source: DB entry {rule_id}, status: {status}. '
        'Pending editorial review before promotion to core position.'
    )
    card.append(notes_p)

    return card


def make_new_family_section(soup: BeautifulSoup, fam_id: str, fam_name: str) -> Tag:
    """Build a new policy-family section with an empty rule-grid."""
    section = soup.new_tag('div', attrs={'class': 'policy-family', 'id': fam_id})
    h3 = soup.new_tag('h3')
    h3.string = fam_name
    grid = soup.new_tag('div', attrs={'class': 'rule-grid'})
    section.append(h3)
    section.append(grid)
    return section


def main():
    # --- Load DB rows ---
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        SELECT rule_id, family_code, canonical_statement, status
        FROM policy_items
        WHERE scope_code = 'TEC' AND status IN ('MISSING', 'PROPOSED')
        ORDER BY rule_id
    """)
    db_rows = cur.fetchall()
    conn.close()

    # --- Load HTML ---
    with open(HTML_PATH, 'r', encoding='utf-8') as f:
        raw_html = f.read()

    soup = BeautifulSoup(raw_html, 'html.parser')

    # Build set of IDs already present in HTML
    existing_ids = {tag['id'] for tag in soup.find_all(id=True)}

    # Filter to rows genuinely absent from HTML
    missing_rows = [r for r in db_rows if r[0] not in existing_ids]

    if not missing_rows:
        print('Nothing to add — all DB positions are already present in the HTML.')
        return

    print(f'DB MISSING/PROPOSED TEC entries: {len(db_rows)}')
    print(f'Already in HTML:                  {len(db_rows) - len(missing_rows)}')
    print(f'To be added:                      {len(missing_rows)}')
    print()

    # Find the #pil-policy section (for appending new families)
    policy_section = soup.find(id='pil-policy')
    if not policy_section:
        print('ERROR: Could not find #pil-policy section.', file=sys.stderr)
        sys.exit(1)

    # Track counts per family
    family_counts: dict[str, int] = {}

    for rule_id, fam_code, stmt, status in missing_rows:
        fam_id = FAMILY_MAP.get(fam_code)
        if fam_id is None:
            # Need a new family section
            if fam_code in NEW_FAMILY_NAMES:
                fam_id, fam_name = NEW_FAMILY_NAMES[fam_code]
            else:
                fam_id = f'fam-{fam_code.lower()}'
                fam_name = fam_code.title()

        # Find or create the family div
        fam_div = soup.find(id=fam_id)
        if fam_div is None:
            # Create new section and append to policy_section
            fam_name = NEW_FAMILY_NAMES.get(fam_code, (fam_id, fam_code.title()))[1]
            fam_div = make_new_family_section(soup, fam_id, fam_name)
            policy_section.append(fam_div)
            print(f'  Created new family section: #{fam_id} ({fam_name})')

        # Find rule-grid inside family
        rule_grid = fam_div.find(class_='rule-grid')
        if rule_grid is None:
            rule_grid = soup.new_tag('div', attrs={'class': 'rule-grid'})
            fam_div.append(rule_grid)

        # Build and append the proposal card
        card = make_proposal_card(soup, rule_id, stmt, status)
        rule_grid.append(card)

        family_counts[fam_code] = family_counts.get(fam_code, 0) + 1
        print(f'  + {rule_id}  ({fam_code})')

    # --- Write output ---
    # BeautifulSoup strips the DOCTYPE; preserve it manually
    doctype_match = re.match(r'(<!DOCTYPE[^>]*>)', raw_html, re.IGNORECASE)
    doctype = doctype_match.group(1) + '\n' if doctype_match else ''

    output = doctype + str(soup)
    with open(HTML_PATH, 'w', encoding='utf-8') as f:
        f.write(output)

    print()
    print('Summary by family:')
    for fam, count in sorted(family_counts.items()):
        print(f'  {fam}: {count} card(s) added')
    print()
    print(f'Total cards added: {sum(family_counts.values())}')
    print(f'HTML written to: {HTML_PATH}')


if __name__ == '__main__':
    main()
