#!/usr/bin/env python3
"""Add MISSING/PROPOSED policy positions from the DB to justice-related pillar HTML files.

Scopes handled:
    JUS → docs/pillars/equal-justice-and-policing.html
    JUD → docs/pillars/courts-and-judicial-system.html
    RGT → docs/pillars/rights-and-civil-liberties.html
    ELE → docs/pillars/elections-and-representation.html
"""

import sqlite3
import sys
import os
sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.14/site-packages'))

from bs4 import BeautifulSoup, Tag

DB_PATH = 'data/policy_catalog.sqlite'

FILES = {
    'JUS': 'docs/pillars/equal-justice-and-policing.html',
    'JUD': 'docs/pillars/courts-and-judicial-system.html',
    'RGT': 'docs/pillars/rights-and-civil-liberties.html',
    'ELE': 'docs/pillars/elections-and-representation.html',
}

# Human-readable titles for new families that need to be created.
NEW_FAMILY_TITLES = {
    'CAP': 'Capital Punishment',
    'MIL': 'Military & Weapons Restrictions',
    'CRB': 'Corrections & Rehabilitation',
    'PPR': 'Police Pay & Resources',
    'PPV': 'Police Procedures & Violence',
    'FIN': 'Campaign Finance',
    'PAR': 'Partisan Reform',
    'APT': 'Appointments',
}


def fam_id_for(scope: str, family_code: str) -> str:
    """Return the expected fam-* id for a given scope + family_code."""
    return f'fam-{family_code.lower()}'


def make_proposal_card(soup: BeautifulSoup, rule_id: str, canonical_statement: str, status: str) -> Tag:
    """Build a proposal card Tag matching the project's card schema."""
    # Short title: first sentence, capped at 120 chars
    first_sentence = canonical_statement.split('.')[0].strip()
    if len(first_sentence) > 120:
        first_sentence = first_sentence[:117] + '...'

    card = soup.new_tag('div', **{'class': 'policy-card proposal', 'id': rule_id})

    header = soup.new_tag('div', **{'class': 'rule-header'})
    code_tag = soup.new_tag('code', **{'class': 'rule-id'})
    code_tag.string = rule_id
    badge = soup.new_tag('span', **{'class': 'rule-badge'})
    badge.string = 'Proposal'
    header.append(code_tag)
    header.append(badge)

    rule_status_div = soup.new_tag('div', **{'class': 'rule-status'})
    rule_status_div.string = '🔵 Proposal — Under Review'

    title_p = soup.new_tag('p', **{'class': 'rule-title'})
    title_p.string = first_sentence

    stmt_p = soup.new_tag('p', **{'class': 'rule-stmt'})
    stmt_p.string = canonical_statement

    notes_p = soup.new_tag('p', **{'class': 'rule-notes'})
    notes_p.string = (
        f'Source: DB entry {rule_id}, status: {status}. '
        'Pending editorial review.'
    )

    card.append(header)
    card.append(rule_status_div)
    card.append(title_p)
    card.append(stmt_p)
    card.append(notes_p)
    return card


def create_new_family(soup: BeautifulSoup, fam_id: str, family_code: str) -> Tag:
    """Create a new policy-family section with family-header, matching existing structure."""
    section = soup.new_tag('div', **{'class': 'policy-family', 'id': fam_id})

    header_div = soup.new_tag('div', **{'class': 'family-header'})
    code_span = soup.new_tag('span', **{'class': 'family-code'})
    code_span.string = family_code.upper()
    title_span = soup.new_tag('span', **{'class': 'family-title'})
    title_span.string = NEW_FAMILY_TITLES.get(family_code.upper(), family_code.title())
    header_div.append(code_span)
    header_div.append(title_span)

    grid = soup.new_tag('div', **{'class': 'rule-grid'})
    section.append(header_div)
    section.append(grid)
    return section


def process_scope(scope: str, rows: list, html_path: str) -> dict:
    """Process one scope's rows and update the HTML file. Returns summary stats."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Collect existing ids for dedup
    existing_ids = set(tag['id'] for tag in soup.find_all(id=True))

    # Collect existing text snippets (first 60 chars of canonical_statement) for dedup
    existing_texts: set[str] = set()
    for card in soup.find_all('div', class_='policy-card'):
        stmt = card.find('p', class_='rule-stmt')
        if stmt and stmt.string:
            existing_texts.add(stmt.string[:60].lower())
        # Also index any title text already present
        title = card.find('p', class_='rule-title')
        if title and title.string:
            existing_texts.add(title.string[:60].lower())

    pil_policy = soup.find(id='pil-policy')

    stats: dict[str, int] = {}
    skipped_id = 0
    skipped_text = 0

    for rule_id, _scope, family_code, canonical_statement, status in rows:
        if rule_id in existing_ids:
            skipped_id += 1
            continue

        text_key = canonical_statement[:60].lower()
        if text_key in existing_texts:
            skipped_text += 1
            continue

        fam_id = fam_id_for(scope, family_code)
        fam_div = soup.find(id=fam_id)

        if fam_div is None:
            if pil_policy is None:
                print(f'  WARNING: no #pil-policy found in {html_path}, skipping {rule_id}')
                continue
            fam_div = create_new_family(soup, fam_id, family_code)
            pil_policy.append(fam_div)
            print(f'  Created new family section: #{fam_id} ({family_code})')

        rule_grid = fam_div.find('div', class_='rule-grid')
        if rule_grid is None:
            rule_grid = soup.new_tag('div', **{'class': 'rule-grid'})
            fam_div.append(rule_grid)

        card = make_proposal_card(soup, rule_id, canonical_statement, status)
        rule_grid.append(card)

        existing_ids.add(rule_id)
        existing_texts.add(text_key)
        stats[fam_id] = stats.get(fam_id, 0) + 1

    total_added = sum(stats.values())
    print(f'\n[{scope}] {html_path}')
    print(f'  DB rows: {len(rows)} | already present: {skipped_id} | text dup: {skipped_text} | new cards added: {total_added}')
    if stats:
        for fam, count in sorted(stats.items()):
            print(f'    {fam}: +{count}')

    if total_added > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    return stats


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT rule_id, scope_code, family_code, canonical_statement, status
        FROM policy_items
        WHERE scope_code IN ('JUS', 'JUD', 'RGT', 'ELE') AND status IN ('MISSING', 'PROPOSED')
        ORDER BY scope_code, family_code, rule_id
    """)
    rows = c.fetchall()
    conn.close()

    by_scope: dict[str, list] = {s: [] for s in FILES}
    for row in rows:
        scope = row[1]
        if scope in by_scope:
            by_scope[scope].append(row)

    print('=== add-proposals-justice.py ===')
    print(f'DB totals — ' + ', '.join(f'{s}: {len(by_scope[s])}' for s in FILES) + f' | total: {len(rows)}')

    total_new = 0
    for scope, scope_rows in by_scope.items():
        stats = process_scope(scope, scope_rows, FILES[scope])
        total_new += sum(stats.values())

    print(f'\n=== Done: {total_new} new proposal cards inserted across {len(FILES)} files ===')


if __name__ == '__main__':
    main()
