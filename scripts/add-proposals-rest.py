#!/usr/bin/env python3
"""
add-proposals-rest.py
=====================
Add MISSING and PROPOSED policy positions from the DB to the remaining
pillar HTML files that have not yet been processed.

Scopes covered:
  COR → anti-corruption.html
  ENV + AGR → environment-and-agriculture.html
  ADM → administrative-state.html
  GUN → gun-policy.html
  MED → information-and-media.html
  LEG → legislative-reform.html
  TRM → term-limits-and-fitness.html
  EDU → education.html
  FPL + OVR → foreign-policy.html
  CHK + SYS + GOV → checks-and-balances.html
  CIV → rights-and-civil-liberties.html
"""

import sqlite3
import sys
import os
sys.path.insert(0, os.path.expanduser('~/.local/lib/python3.14/site-packages'))

from bs4 import BeautifulSoup, Tag

DB_PATH = 'data/policy_catalog.sqlite'

# Scope code → HTML file (multiple scopes can target same file)
SCOPE_TO_FILE = {
    'COR': 'docs/policy/anti-corruption.html',
    'ENV': 'docs/policy/environment-and-agriculture.html',
    'AGR': 'docs/policy/environment-and-agriculture.html',
    'ADM': 'docs/policy/administrative-state.html',
    'GUN': 'docs/policy/gun-policy.html',
    'MED': 'docs/policy/information-and-media.html',
    'LEG': 'docs/policy/legislative-reform.html',
    'TRM': 'docs/policy/term-limits-and-fitness.html',
    'EDU': 'docs/policy/education.html',
    'FPL': 'docs/policy/foreign-policy.html',
    'OVR': 'docs/policy/foreign-policy.html',
    'CHK': 'docs/policy/checks-and-balances.html',
    'SYS': 'docs/policy/checks-and-balances.html',
    'GOV': 'docs/policy/checks-and-balances.html',
    'CIV': 'docs/policy/rights-and-civil-liberties.html',
}

# Per-scope family_code → fam-* id overrides for non-obvious cases.
# The default fallback logic tries:
#   1. fam-{family_code.lower()}
#   2. fam-{scope.lower()}-{family_code.lower()}
# Add overrides here when neither convention matches an existing id.
FAMILY_MAP_OVERRIDES: dict[str, dict[str, str]] = {
    # No overrides needed — fallback logic covers all known cases.
}

# Human-readable family names keyed by lowercase family_code (for new-family headers)
FAMILY_TITLES: dict[str, str] = {
    # COR families
    'agf': 'Anti-Graft and Financial Conflicts',
    'alg': 'Algorithmic and Tech Accountability',
    'ant': 'Anti-Corruption in Antitrust',
    'aud': 'Audit and Oversight',
    'cap': 'Regulatory Capture Prevention',
    'con': 'Contracting Integrity',
    'enf': 'Enforcement',
    'law': 'Law Enforcement Integrity',
    'mkt': 'Market and Competition Integrity',
    'mpy': 'Monopsony and Pricing Integrity',
    'nmd': 'Non-Monetary Disclosure',
    'peq': 'Political Equity',
    'pis': 'Public Interest Standards',
    'trn': 'Transparency',
    # ADM families
    'adj': 'Adjudication Rights',
    'agy': 'Agency Authority',
    'chv': 'Chevron Deference',
    'coo': 'Coordination',
    'fnd': 'Foundational Principles',
    'ind': 'Independence',
    'ovr': 'Oversight',
    'pub': 'Public Participation',
    'rgt': 'Rights Protection',
    'rul': 'Rulemaking',
    'sci': 'Scientific Integrity',
    'sys': 'Systemic Reform',
    'tns': 'Transparency',
    # ENV families
    'ai':  'AI and Environmental Policy',
    'bio': 'Biodiversity',
    'cli': 'Climate Policy',
    'cln': 'Clean Air and Water',
    'cor': 'Corporate Environmental Accountability',
    'cpx': 'Environmental Complexity',
    'des': 'Deforestation',
    'epr': 'Extended Producer Responsibility',
    'esc': 'Environmental Science',
    'ind': 'Industrial Standards',
    'inf': 'Infrastructure',
    'jus': 'Environmental Justice',
    'pkg': 'Packaging',
    'pks': 'Parks and Public Lands',
    'pls': 'Plastics',
    'pol': 'Pollution',
    'rec': 'Recycling',
    'reg': 'Regulation',
    'spc': 'Special Topics',
    'wst': 'Waste',
    'wtr': 'Water Policy',
    'urb': 'Urban Environment',
    # AGR families
    'reg': 'Agricultural Regulation',
    # GUN families (gun-prefixed ones already exist; new ones here)
    'amo': 'Ammunition',
    'lic': 'Licensing',
    'saf': 'Safe Storage',
    'stw': 'Statewide Standards',
    # MED families
    'dis': 'Disinformation',
    'lnj': 'Local News and Journalism',
    'plt': 'Platform Accountability',
    'prs': 'Press Freedom',
    'pub': 'Public Media',
    's230': 'Section 230 Reform',
    # LEG families
    'bba': 'Balanced Budget Amendment',
    'cap': 'Capitol Accountability',
    'com': 'Congressional Committee Reform',
    'dmj': 'Dismantling Judicial Override',
    'drf': 'Drafting Reform',
    'lob': 'Lobbying Reform',
    'pro': 'Procedural Reform',
    'rpl': 'Replacement Procedures',
    'sen': 'Senate Reform',
    'stk': 'Structural Reforms',
    # EDU families
    'bnd': 'Banning and Censorship',
    'chr': 'Charter Schools',
    'dis': 'Discipline',
    'fin': 'Financing',
    'lib': 'Civics and Civic Education',
    'rgt': 'Student Rights',
    'std': 'Standards',
    # OVR families (→ FPL file)
    'brn': 'International Norms and Rules-Based Order',
    'fed': 'Federal Authority in Foreign Affairs',
    'jur': 'Jurisdictional Limits',
    'sta': 'State and Local Foreign Policy',
    # SYS families (→ CHK file)
    'agn': 'Agency Oversight',
    'emg': 'Emergency Powers',
    'imp': 'Impeachment',
    'wpr': 'War Powers',
    # GOV families (→ CHK file)
    'acc': 'Government Accountability',
    'war': 'War and Force Authorization',
    # CIV families (→ RGT file)
    'vtl': 'Voting Rights and Civil Liberties',
    # TRM families
    'lim': 'Term Limits',
    'run': 'Runoff and Special Elections',
    'vac': 'Vacancy Rules',
}


def fam_id_for(scope: str, family_code: str, soup: BeautifulSoup) -> tuple[str, bool]:
    """Return (fam_id, already_exists) for a given scope + family_code.

    Tries in order:
    1. Per-scope override map
    2. fam-{family_code.lower()} — plain family id
    3. fam-{scope.lower()}-{family_code.lower()} — scope-prefixed family id
    Returns (candidate_id, True) if the id was found in the soup, else (candidate_id, False).
    """
    fc_lower = family_code.lower()
    sc_lower = scope.lower()

    # Check override first
    override = FAMILY_MAP_OVERRIDES.get(scope, {}).get(family_code)
    if override:
        exists = bool(soup.find(id=override))
        return override, exists

    # Try plain fam-{family_code}
    plain = f'fam-{fc_lower}'
    if soup.find(id=plain):
        return plain, True

    # Try scope-prefixed fam-{scope}-{family_code}
    scoped = f'fam-{sc_lower}-{fc_lower}'
    if soup.find(id=scoped):
        return scoped, True

    # Neither found — return the plain id as the new id to create
    return plain, False


def make_proposal_card(soup: BeautifulSoup, rule_id: str, canonical_statement: str, status: str) -> Tag:
    """Build a proposal card Tag."""
    # Short title: first sentence, truncated at 120 chars
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
    """Create a new policy-family section with an h3 and empty rule-grid."""
    fc_lower = family_code.lower()
    title = FAMILY_TITLES.get(fc_lower, family_code.title())

    section = soup.new_tag('div', **{'class': 'policy-family', 'id': fam_id})
    heading = soup.new_tag('h3')
    heading.string = title
    grid = soup.new_tag('div', **{'class': 'rule-grid'})
    section.append(heading)
    section.append(grid)
    return section


def process_file(html_path: str, rows: list[tuple]) -> dict:
    """Process all rows for a single HTML file. Returns summary stats."""
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'html.parser')

    # Pre-collect existing ids and statement snippets for dedup
    existing_ids: set[str] = {tag['id'] for tag in soup.find_all(id=True)}
    existing_stmt_snippets: set[str] = set()
    for card in soup.find_all('div', class_='policy-card'):
        stmt = card.find('p', class_='rule-stmt')
        if stmt and stmt.get_text():
            existing_stmt_snippets.add(stmt.get_text()[:60].lower().strip())
        # Also handle older cards that use rule-stmt as a string directly
        for p in card.find_all('p'):
            txt = p.get_text()
            if len(txt) > 20:
                existing_stmt_snippets.add(txt[:60].lower().strip())

    pil_policy = soup.find(id='pil-policy')

    stats = {
        'total': len(rows),
        'skipped_present': 0,
        'added': 0,
        'families_created': [],
        'families_appended': [],
    }

    # Group rows by family_code to batch-process per family
    from collections import defaultdict
    by_family: dict[str, list[tuple]] = defaultdict(list)
    for row in rows:
        rule_id, scope_code, family_code, canonical_statement, status = row
        by_family[family_code].append(row)

    for family_code, family_rows in by_family.items():
        fam_id, already_exists = fam_id_for(family_rows[0][1], family_code, soup)

        if already_exists:
            family_div = soup.find(id=fam_id)
        else:
            # Create new family section and append to pil-policy
            family_div = create_new_family(soup, fam_id, family_code)
            if pil_policy:
                # Find the closing wrap div or append directly to section
                wrap = pil_policy.find('div', class_='wrap', recursive=False)
                if wrap:
                    wrap.append(family_div)
                else:
                    pil_policy.append(family_div)
            else:
                soup.body.append(family_div)
            stats['families_created'].append(fam_id)

        grid = family_div.find('div', class_='rule-grid')
        if not grid:
            grid = soup.new_tag('div', **{'class': 'rule-grid'})
            family_div.append(grid)

        for row in family_rows:
            rule_id, scope_code, family_code, canonical_statement, status = row
            stmt_snippet = canonical_statement[:60].lower().strip()

            # Skip if already present by id or statement content
            if rule_id in existing_ids:
                stats['skipped_present'] += 1
                continue
            if stmt_snippet in existing_stmt_snippets:
                stats['skipped_present'] += 1
                continue

            card = make_proposal_card(soup, rule_id, canonical_statement, status)
            grid.append(card)
            existing_ids.add(rule_id)
            existing_stmt_snippets.add(stmt_snippet)
            stats['added'] += 1

            if fam_id not in stats['families_appended'] and fam_id not in stats['families_created']:
                stats['families_appended'].append(fam_id)

    if stats['added'] > 0:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))

    return stats


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT rule_id, scope_code, family_code, canonical_statement, status
        FROM policy_items
        WHERE scope_code IN (
            'COR','ENV','ADM','GUN','MED','LEG','TRM','EDU',
            'FPL','CHK','STS','OVR','SYS','GOV','CIV','AGR','EXP'
        )
        AND status IN ('MISSING', 'PROPOSED')
        ORDER BY scope_code, rule_id
    """)
    all_rows = c.fetchall()
    conn.close()

    # Group rows by target HTML file
    from collections import defaultdict
    by_file: dict[str, list[tuple]] = defaultdict(list)
    for row in all_rows:
        rule_id, scope_code, family_code, canonical_statement, status = row
        html_path = SCOPE_TO_FILE.get(scope_code)
        if html_path:
            by_file[html_path].append(row)
        else:
            print(f'  [WARN] No file mapping for scope {scope_code} (rule {rule_id})')

    grand_total = 0
    grand_added = 0
    grand_skipped = 0

    print('\n' + '=' * 70)
    print('add-proposals-rest.py — Results')
    print('=' * 70)

    for html_path, rows in sorted(by_file.items()):
        print(f'\n▶ {html_path}')
        print(f'  DB items for this file: {len(rows)}')

        # Group by scope for reporting
        scope_counts: dict[str, int] = defaultdict(int)
        for row in rows:
            scope_counts[row[1]] += 1
        for scope, cnt in sorted(scope_counts.items()):
            print(f'    {scope}: {cnt} items')

        stats = process_file(html_path, rows)

        print(f'  Already present (skipped): {stats["skipped_present"]}')
        print(f'  New cards added:           {stats["added"]}')
        if stats['families_created']:
            print(f'  New families created:      {", ".join(stats["families_created"])}')
        if stats['families_appended']:
            print(f'  Existing families updated: {", ".join(stats["families_appended"])}')

        grand_total += stats['total']
        grand_added += stats['added']
        grand_skipped += stats['skipped_present']

    print('\n' + '=' * 70)
    print(f'TOTAL — DB items scanned: {grand_total}')
    print(f'TOTAL — Already present:  {grand_skipped}')
    print(f'TOTAL — New cards added:  {grand_added}')
    print('=' * 70 + '\n')


if __name__ == '__main__':
    main()
