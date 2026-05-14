#!/usr/bin/env python3
"""
add-proposals-econ.py
Add MISSING and PROPOSED policy positions from the database to economic pillar HTML files.
Skips items already present (by ID attribute or first-60-char statement match).
"""

import sys
import sqlite3
import re

sys.path.insert(0, '/home/alice/.local/lib/python3.14/site-packages')
from bs4 import BeautifulSoup, Tag

DB_PATH = 'data/policy_catalog.sqlite'

SCOPE_FILES = {
    'TAX': 'docs/policy/taxation-and-wealth.html',
    'CON': 'docs/policy/consumer-rights.html',
    'HOU': 'docs/policy/housing.html',
    'LAB': 'docs/policy/labor-and-workers-rights.html',
    'INF': 'docs/policy/infrastructure-and-public-goods.html',
}

FAMILY_NAME_MAP = {
    'ADM': 'Tax Administration',
    'AFD': 'Affordability Standards',
    'AI':  'AI and Automation Tax',
    'ALG': 'Algorithmic Pricing',
    'ANT': 'Antitrust and Market Competition',
    'AUT': 'Automation and Labor Displacement',
    'BEP': 'Base Erosion and Profit-Shifting',
    'BLD': 'Building and Construction Standards',
    'CAP': 'Capital and Investment Income',
    'CBA': 'Collective Bargaining',
    'CDR': 'Candidate Disclosure and Transparency',
    'CLM': 'Climate and Heat Protections',
    'CNS': 'Consumables and Supply Lock-in',
    'COE': 'Coercive Employer Practices',
    'CON': 'Consumer Rights',
    'COR': 'Corporate Taxation',
    'CRD': 'Credit Reporting',
    'DAT': 'Data Centers and Digital Infrastructure',
    'DBR': 'Data Brokers',
    'DED': 'Tax Deductions',
    'DMJ': 'Tax Equity and Democratic Majority Rule',
    'DOM': 'Domestic Workers',
    'DRK': 'Dark Patterns and Deceptive Interfaces',
    'ENF': 'Enforcement',
    'ENR': 'Energy Infrastructure',
    'ENV': 'Environmental Tax Policy',
    'EQJ': 'Environmental Justice in Infrastructure',
    'EQT': 'Equal Economic Opportunity',
    'EST': 'Estate and Inheritance Taxation',
    'EVI': 'Eviction Protections',
    'EXT': 'Financial Extraction Mechanisms',
    'FEE': 'Hidden and Junk Fees',
    'FIN': 'Mortgage and Financing',
    'FTR': 'Product Functionality',
    'FTT': 'Financial Transaction Tax',
    'GEN': 'General Consumer Protection',
    'GIG': 'Gig and Platform Workers',
    'GOV': 'Governance and Regulatory Integrity',
    'GRD': 'Electrical Grid',
    'HRS': 'Work Hours and Scheduling',
    'HVN': 'Tax Havens',
    'INC': 'Tax Incentives and Public Outcomes',
    'IND': 'Industrial and Manufacturing Policy',
    'INS': 'Insurance Protections',
    'INT': 'International Tax Coordination',
    'LAB': 'Labor Standards',
    'LBR': 'Infrastructure Labor Protections',
    'LND': 'Public Land for Housing',
    'LOP': 'Tax Loopholes',
    'LVT': 'Land Value Taxation',
    'NET': 'Internet and Broadband Infrastructure',
    'NCP': 'Non-Compete Agreements',
    'OWN': 'Ownership Rights',
    'PBN': 'Portable Benefits',
    'PLT': 'Algorithmic Management',
    'PRL': 'Prison Labor',
    'PUB': 'Public and Social Housing',
    'QLT': 'Product Quality Standards',
    'RAIL': 'Rail Infrastructure',
    'RET': 'Retirement Security',
    'SCH': 'Predictable Scheduling',
    'SMB': 'Small Business Support',
    'SUB': 'Subscription Practices',
    'SUR': 'Workplace Surveillance',
    'SYS': 'System-Level Policy',
    'TEN': 'Tenant Protections',
    'TRN': 'Transparency and Disclosure',
    'UNN': 'Union Formation',
    'WAR': 'Warranty Rights',
    'WAT': 'Water Infrastructure',
    'WRK': 'Work Week and Hours',
}


def target_scope_for(rule_id, scope, family):
    """Map ECO items to their canonical pillar scope."""
    if scope == 'ECO':
        return 'LAB' if family == 'LAB' else 'TAX'
    return scope


def short_title(stmt):
    """Extract a short title from the canonical statement (first sentence up to 100 chars)."""
    text = stmt.replace('&#x2014;', '—').replace('&#x2019;', "'")
    # Try to get the first sentence
    m = re.match(r'^([^.!?]{10,100}[.!?])', text)
    if m:
        return m.group(1).rstrip()
    # Fallback: truncate to 100 chars at a word boundary
    if len(text) <= 100:
        return text.rstrip('.')
    truncated = text[:100].rsplit(' ', 1)[0]
    return truncated + '…'


def find_family_div(pil_policy, scope, family_code):
    """Find an existing policy-family div whose id matches scope+family, or return None."""
    fam_lower = family_code.lower()
    scope_lower = scope.lower()

    # Try most specific first: fam-{scope}-{family}
    candidate = pil_policy.find('div', id=f'fam-{scope_lower}-{fam_lower}')
    if candidate:
        return candidate

    # Try fam-{family}
    candidate = pil_policy.find('div', id=f'fam-{fam_lower}')
    if candidate:
        return candidate

    # Try any fam-* ending with -{family}
    for div in pil_policy.find_all('div', class_='policy-family'):
        div_id = div.get('id', '')
        if div_id.endswith(f'-{fam_lower}'):
            return div

    return None


def create_family_div(soup, scope, family_code):
    """Create a new policy-family div with a rule-grid for the given family."""
    fam_lower = family_code.lower()
    scope_lower = scope.lower()
    fam_id = f'fam-{scope_lower}-{fam_lower}'
    family_name = FAMILY_NAME_MAP.get(family_code, f'{scope}-{family_code}')

    family_div = soup.new_tag('div', attrs={'class': 'policy-family', 'id': fam_id})

    header = soup.new_tag('div', attrs={'class': 'family-header'})
    code_span = soup.new_tag('span', attrs={'class': 'family-code'})
    code_span.string = scope
    title_span = soup.new_tag('span', attrs={'class': 'family-title'})
    title_span.string = f'{family_code} — {family_name}'
    count_span = soup.new_tag('span', attrs={'class': 'family-count'})
    count_span.string = '0/0 active'
    header.append(code_span)
    header.append(title_span)
    header.append(count_span)
    family_div.append(header)

    rule_grid = soup.new_tag('div', attrs={'class': 'rule-grid'})
    family_div.append(rule_grid)

    return family_div


def build_proposal_card(soup, rule_id, stmt, status):
    """Build a proposal card Tag from the given rule_id and statement."""
    card = soup.new_tag('div', attrs={'class': 'policy-card proposal', 'id': rule_id})

    header = soup.new_tag('div', attrs={'class': 'rule-header'})
    code_el = soup.new_tag('code', attrs={'class': 'rule-id'})
    code_el.string = rule_id
    badge = soup.new_tag('span', attrs={'class': 'rule-badge'})
    badge.string = 'Proposal'
    header.append(code_el)
    header.append(badge)
    card.append(header)

    status_div = soup.new_tag('div', attrs={'class': 'rule-status'})
    status_div.string = '🔵 Proposal — Under Review'
    card.append(status_div)

    title_p = soup.new_tag('p', attrs={'class': 'rule-title'})
    title_p.string = short_title(stmt)
    card.append(title_p)

    stmt_p = soup.new_tag('p', attrs={'class': 'rule-stmt'})
    # Preserve HTML entities in statement by parsing them back
    stmt_soup = BeautifulSoup(f'<p>{stmt}</p>', 'html.parser')
    stmt_p.string = stmt_soup.p.get_text()
    card.append(stmt_p)

    notes_p = soup.new_tag('p', attrs={'class': 'rule-notes'})
    notes_p.string = f'Source: DB entry {rule_id}, status: {status}. Pending editorial review.'
    card.append(notes_p)

    return card


def process_file(scope, html_path, items):
    """Process one pillar HTML file, adding new proposal cards."""
    with open(html_path, encoding='utf-8') as f:
        original_html = f.read()

    soup = BeautifulSoup(original_html, 'html.parser')
    pil_policy = soup.find(id='pil-policy')
    if not pil_policy:
        print(f'  ERROR: No #pil-policy section found in {html_path}')
        return 0, []

    existing_ids = {el.get('id') for el in soup.find_all(id=True)}

    added = []
    skipped = []

    for rule_id, db_scope, family_code, stmt, status in items:
        # Skip if already present by ID or by first 60 chars of statement
        if rule_id in existing_ids:
            skipped.append(rule_id)
            continue
        if stmt[:60] in original_html:
            skipped.append(rule_id)
            continue

        # Find or create the target family div
        family_div = find_family_div(pil_policy, scope, family_code)
        if family_div is None:
            family_div = create_family_div(soup, scope, family_code)
            pil_policy.append(family_div)

        rule_grid = family_div.find('div', class_='rule-grid')
        if rule_grid is None:
            rule_grid = soup.new_tag('div', attrs={'class': 'rule-grid'})
            family_div.append(rule_grid)

        card = build_proposal_card(soup, rule_id, stmt, status)
        rule_grid.append(card)
        added.append((rule_id, family_div.get('id')))

    if added:
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(str(soup))
        print(f'  Wrote {html_path}')

    return len(added), added, len(skipped)


def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT rule_id, scope_code, family_code, canonical_statement, status
        FROM policy_items
        WHERE scope_code IN ('TAX','LAB','HOU','CON','INF','ECO')
          AND status IN ('MISSING','PROPOSED')
        ORDER BY scope_code, rule_id
    """)
    db_items = c.fetchall()
    conn.close()

    # Group items by target scope
    by_scope = {s: [] for s in SCOPE_FILES}
    db_counts = {s: 0 for s in SCOPE_FILES}
    for row in db_items:
        rule_id, scope, family, stmt, status = row
        tgt = target_scope_for(rule_id, scope, family)
        if tgt in by_scope:
            by_scope[tgt].append(row)
            db_counts[tgt] += 1

    print('\n=== add-proposals-econ.py ===\n')
    total_added = 0
    for scope, html_path in SCOPE_FILES.items():
        items = by_scope[scope]
        print(f'[{scope}] {html_path}')
        print(f'  DB entries (MISSING+PROPOSED): {db_counts[scope]}')
        n_added, added_list, n_skipped = process_file(scope, html_path, items)
        print(f'  Already present (skipped):     {n_skipped}')
        print(f'  New cards added:               {n_added}')
        if added_list:
            for rule_id, fam_id in added_list:
                print(f'    + {rule_id}  →  #{fam_id}')
        total_added += n_added
        print()

    print(f'Total new proposal cards added: {total_added}')


if __name__ == '__main__':
    main()
