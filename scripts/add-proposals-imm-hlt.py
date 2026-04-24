#!/usr/bin/env python3
"""Add MISSING/PROPOSED policy positions from the DB to immigration and healthcare pillar HTML files."""

import sqlite3
import sys
import os
sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.14/site-packages'))

from bs4 import BeautifulSoup, Tag

DB_PATH = 'data/policy_catalog.sqlite'
FILES = {
    'IMM': 'docs/pillars/immigration.html',
    'HLT': 'docs/pillars/healthcare.html',
}

# Maps DB family_code → fam-* id, handling non-obvious cases per-scope
FAMILY_MAP = {
    'IMM': {
        'CLM': 'fam-imm-clm',
    },
    'HLT': {
        'JUS': 'fam-jus-hlt',
    },
}


def fam_id_for(scope: str, family_code: str) -> str:
    """Return the expected fam-* id for a given scope + family_code."""
    override = FAMILY_MAP.get(scope, {}).get(family_code)
    if override:
        return override
    return f'fam-{family_code.lower()}'


def make_proposal_card(soup: BeautifulSoup, rule_id: str, canonical_statement: str, status: str) -> Tag:
    """Build a proposal card Tag."""
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

    rule_status = soup.new_tag('div', **{'class': 'rule-status'})
    rule_status.string = '🔵 Proposal — Under Review'

    title_p = soup.new_tag('p', **{'class': 'rule-title'})
    title_p.string = first_sentence

    stmt_p = soup.new_tag('p', **{'class': 'rule-stmt'})
    stmt_p.string = canonical_statement

    notes_p = soup.new_tag('p', **{'class': 'rule-notes'})
    notes_p.string = (
        f'Source: DB entry {rule_id}, status: {status}. '
        'Pending editorial review before promotion to core position.'
    )

    card.append(header)
    card.append(rule_status)
    card.append(title_p)
    card.append(stmt_p)
    card.append(notes_p)
    return card


def create_new_family(soup: BeautifulSoup, fam_id: str, family_code: str) -> Tag:
    """Create a new policy-family section."""
    section = soup.new_tag('div', **{'class': 'policy-family', 'id': fam_id})
    heading = soup.new_tag('h3')
    heading.string = family_code.title()
    grid = soup.new_tag('div', **{'class': 'rule-grid'})
    section.append(heading)
    section.append(grid)
    return section


def process_scope(scope: str, rows: list, html_path: str) -> dict:
    """Process one scope's rows and update the HTML file. Returns summary stats."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Collect all existing ids and all existing text (first 50 chars of text content) for dedup
    existing_ids = set(tag['id'] for tag in soup.find_all(id=True))
    existing_texts = set()
    for card in soup.find_all('div', class_='policy-card'):
        stmt = card.find('p', class_='rule-stmt')
        if stmt and stmt.string:
            existing_texts.add(stmt.string[:50].lower())
        # Also check all text content in the card
        full_text = card.get_text(' ', strip=True)
        if len(full_text) >= 50:
            existing_texts.add(full_text[:50].lower())

    pil_policy = soup.find(id='pil-policy')

    stats = {}  # fam_id → count added
    skipped_id = 0
    skipped_text = 0

    for rule_id, _scope, family_code, canonical_statement, status in rows:
        # Check ID dedup
        if rule_id in existing_ids:
            skipped_id += 1
            continue

        # Check text dedup (first 50 chars)
        text_key = canonical_statement[:50].lower()
        if text_key in existing_texts:
            skipped_text += 1
            continue

        fam_id = fam_id_for(scope, family_code)
        fam_div = soup.find(id=fam_id)

        if fam_div is None:
            # Create new family section inside pil-policy
            if pil_policy is None:
                print(f'  WARNING: no #pil-policy found in {html_path}, skipping {rule_id}')
                continue
            fam_div = create_new_family(soup, fam_id, family_code)
            pil_policy.append(fam_div)
            print(f'  Created new family section: {fam_id}')

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
    print(f'  DB rows: {len(rows)} | skipped (id dup): {skipped_id} | skipped (text dup): {skipped_text} | added: {total_added}')
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
        WHERE scope_code IN ('IMM', 'HLT') AND status IN ('MISSING', 'PROPOSED')
        ORDER BY scope_code, family_code, rule_id
    """)
    rows = c.fetchall()
    conn.close()

    imm_rows = [r for r in rows if r[1] == 'IMM']
    hlt_rows = [r for r in rows if r[1] == 'HLT']

    print(f'DB totals — IMM: {len(imm_rows)}, HLT: {len(hlt_rows)}, combined: {len(rows)}')

    process_scope('IMM', imm_rows, FILES['IMM'])
    process_scope('HLT', hlt_rows, FILES['HLT'])


if __name__ == '__main__':
    main()
