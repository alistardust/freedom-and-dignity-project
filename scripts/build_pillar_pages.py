#!/usr/bin/env python3
"""
Generate full-content pillar pages from pillars/*/overview.md and policy.md sources.
Outputs to docs/pillars/{slug}.html.
"""
import os
import re
import sys
import textwrap

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Foundation metadata
FOUNDATIONS = {
    'accountable-power': {
        'num': 'I', 'title': 'Accountable Power', 'color': '#bf0a30', 'id': 'accountable-power'
    },
    'clean-democracy': {
        'num': 'II', 'title': 'Clean Democracy', 'color': '#2471a3', 'id': 'clean-democracy'
    },
    'equal-justice': {
        'num': 'III', 'title': 'Equal Justice', 'color': '#1e8449', 'id': 'equal-justice'
    },
    'real-freedom': {
        'num': 'IV', 'title': 'Real Freedom', 'color': '#7d3c98', 'id': 'real-freedom'
    },
    'freedom-to-thrive': {
        'num': 'V', 'title': 'Freedom to Thrive', 'color': '#c9952a', 'id': 'freedom-to-thrive'
    },
}

# Pillar HTML slug → (source dir slug, title, foundation key, summary)
PILLARS = [
    ('executive-power',           'executive_power',              'Executive Power',              'accountable-power'),
    ('checks-and-balances',       'checks_and_balances',          'Checks & Balances',            'accountable-power'),
    ('term-limits-and-fitness',   'term_limits_and_fitness',      'Term Limits & Fitness',        'accountable-power'),
    ('courts-and-judicial-system','courts_and_judicial_system',   'Courts & Judicial System',     'accountable-power'),
    ('administrative-state',      'administrative_state',         'Administrative State',         'accountable-power'),
    ('elections-and-representation','elections_and_representation','Elections & Representation',  'clean-democracy'),
    ('anti-corruption',           'anti_corruption',              'Anti-Corruption',              'clean-democracy'),
    ('antitrust-and-corporate-power','antitrust_and_corporate_power','Antitrust & Corporate Power','clean-democracy'),
    ('information-and-media',     'information_and_media',        'Information & Media',          'clean-democracy'),
    ('equal-justice-and-policing','equal_justice_and_policing',   'Equal Justice & Policing',     'equal-justice'),
    ('immigration',               'immigration',                  'Immigration',                  'equal-justice'),
    ('rights-and-civil-liberties','rights_and_civil_liberties',   'Rights & Civil Liberties',     'equal-justice'),
    ('gun-policy',                'gun_policy',                   'Gun Policy',                   'real-freedom'),
    ('technology-and-ai',         'technology_and_ai',            'Technology & AI',              'real-freedom'),
    ('healthcare',                'healthcare',                   'Healthcare',                   'freedom-to-thrive'),
    ('taxation-and-wealth',       'taxation_and_wealth',          'Taxation & Wealth',            'freedom-to-thrive'),
    ('environment-and-agriculture','environment_and_agriculture', 'Environment & Agriculture',    'freedom-to-thrive'),
    ('education',                 'education',                    'Education',                    'freedom-to-thrive'),
    ('labor-and-workers-rights',  'labor_and_workers_rights',     "Labor & Workers' Rights",      'freedom-to-thrive'),
    ('housing',                   'housing',                      'Housing',                      'freedom-to-thrive'),
    ('consumer-rights',           'consumer_rights',              'Consumer Rights',              'real-freedom'),
    ('legislative-reform',        'legislative_reform',           'Legislative Reform',           'accountable-power'),
]

STATUS_BADGE = {
    'INCLUDED': ('status-included', 'Included'),
    'UPDATED':  ('status-updated',  'Updated'),
    'PARTIAL':  ('status-partial',  'Partial'),
    'MISSING':  ('status-missing',  'Proposed'),
    'PROPOSED': ('status-missing',  'Proposed'),
}


# ─── Markdown helpers ────────────────────────────────────────────────────────

def md_inline(text):
    """Convert inline markdown: **bold**, *italic*, [text](url), `code`."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    text = re.sub(r'\*(.+?)\*',     r'<em>\1</em>', text)
    text = re.sub(r'`(.+?)`',       r'<code>\1</code>', text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2" target="_blank" rel="noopener">\1</a>', text)
    return text


def md_blocks(text):
    """Convert markdown body text to HTML block elements."""
    lines = text.split('\n')
    html = []
    in_ul = False
    in_ol = False
    buf = []

    def flush_para():
        nonlocal buf
        if buf:
            joined = ' '.join(l.strip() for l in buf if l.strip())
            if joined:
                html.append(f'<p>{md_inline(joined)}</p>')
            buf = []

    def close_list():
        nonlocal in_ul, in_ol
        if in_ul:
            html.append('</ul>')
            in_ul = False
        if in_ol:
            html.append('</ol>')
            in_ol = False

    for line in lines:
        # H4
        if line.startswith('#### '):
            flush_para(); close_list()
            html.append(f'<h4>{md_inline(line[5:].strip())}</h4>')
        # H3
        elif line.startswith('### '):
            flush_para(); close_list()
            html.append(f'<h3>{md_inline(line[4:].strip())}</h3>')
        # H2
        elif line.startswith('## '):
            flush_para(); close_list()
            html.append(f'<h2>{md_inline(line[3:].strip())}</h2>')
        # unordered list
        elif re.match(r'^[-*] ', line):
            flush_para()
            if not in_ul:
                close_list()
                html.append('<ul>')
                in_ul = True
            html.append(f'<li>{md_inline(line[2:].strip())}</li>')
        # ordered list
        elif re.match(r'^\d+\. ', line):
            flush_para()
            if not in_ol:
                close_list()
                html.append('<ol>')
                in_ol = True
            html.append(f'<li>{md_inline(re.sub(r"^\d+\. ", "", line).strip())}</li>')
        # blank line
        elif not line.strip():
            flush_para()
            close_list()
        else:
            buf.append(line)

    flush_para()
    close_list()
    return '\n'.join(html)


# ─── Overview parser ─────────────────────────────────────────────────────────

def parse_overview(path):
    """
    Parse overview.md into a dict of section_name -> markdown text.
    Top-level (##) sections are keys; content including ### sub-sections is preserved.
    """
    if not os.path.exists(path):
        return {}

    with open(path, encoding='utf-8') as f:
        content = f.read()

    sections = {}
    current = None
    buf = []

    for line in content.split('\n'):
        if line.startswith('## '):
            if current is not None:
                sections[current] = '\n'.join(buf).strip()
            current = line[3:].strip()
            buf = []
        elif line.startswith('# '):
            pass  # title line
        else:
            buf.append(line)

    if current:
        sections[current] = '\n'.join(buf).strip()

    return sections


# ─── Policy parser ───────────────────────────────────────────────────────────

def parse_policy(path):
    """
    Returns list of families: [{code, title, rules:[{id, title, status, statement, notes}]}]
    """
    if not os.path.exists(path):
        return []

    with open(path, encoding='utf-8') as f:
        lines = f.readlines()

    families = []
    current_family = None
    current_rule = None

    def save_rule():
        nonlocal current_rule
        if current_rule and current_family:
            current_family['rules'].append(current_rule)
            current_rule = None

    def save_family():
        nonlocal current_family
        save_rule()
        if current_family:
            families.append(current_family)
            current_family = None

    for line in lines:
        line_stripped = line.rstrip('\n')

        # Family heading: ## CODE — Title
        fam_match = re.match(r'^## ([A-Z0-9]+)\s*[—–-]+\s*(.+)$', line_stripped)
        if fam_match:
            save_family()
            current_family = {'code': fam_match.group(1), 'title': fam_match.group(2).strip(), 'rules': []}
            continue

        # Also catch ## CODE (no dash/title)
        fam_plain = re.match(r'^## ([A-Z0-9]+)\s*$', line_stripped)
        if fam_plain:
            save_family()
            current_family = {'code': fam_plain.group(1), 'title': fam_plain.group(1), 'rules': []}
            continue

        # Rule heading: ### SCOPE-FAM-NNN — Title  OR  ### SCOPE-FAM-NNN
        rule_match = re.match(r'^### ([A-Z]+-[A-Z0-9]+-\d+[A-Z]?)\s*[—–-]*\s*(.*)?$', line_stripped)
        if rule_match:
            save_rule()
            if current_family is None:
                current_family = {'code': 'MISC', 'title': 'Miscellaneous', 'rules': []}
            current_rule = {
                'id': rule_match.group(1),
                'title': rule_match.group(2).strip() if rule_match.group(2) else '',
                'status': 'MISSING',
                'statement': '',
                'notes': '',
            }
            continue

        if current_rule is None:
            continue

        # Status
        st = re.match(r'^\*\*Status:\*\*\s*(.+)$', line_stripped)
        if st:
            current_rule['status'] = st.group(1).strip().upper()
            continue

        # Statement
        stmt = re.match(r'^\*\*Statement:\*\*\s*(.+)$', line_stripped)
        if stmt:
            current_rule['statement'] = stmt.group(1).strip()
            continue

        # Notes (may span multiple lines — just grab first)
        notes = re.match(r'^\*\*Notes?:\*\*\s*(.*)?$', line_stripped)
        if notes:
            current_rule['notes'] = notes.group(1).strip()
            continue

        # Multi-line notes continuation
        if current_rule.get('notes') and line_stripped and not line_stripped.startswith('**') and not line_stripped.startswith('#'):
            if not line_stripped.startswith('---'):
                current_rule['notes'] += ' ' + line_stripped.strip()

    save_family()
    return families


# ─── HTML building blocks ─────────────────────────────────────────────────────

def rule_card(rule):
    status_key = rule['status'].split()[0] if rule['status'] else 'MISSING'
    cls, label = STATUS_BADGE.get(status_key, ('status-missing', status_key))
    title_text = rule['title'] or rule['statement'][:80] if rule['statement'] else rule['id']
    notes_html = f'<p class="rule-notes">{md_inline(rule["notes"])}</p>' if rule['notes'] else ''
    stmt = rule['statement'] or ''
    return f'''\
<div class="rule-card {cls}">
  <div class="rule-header">
    <code class="rule-id">{rule["id"]}</code>
    <span class="rule-badge">{label}</span>
  </div>
  <p class="rule-title">{md_inline(title_text)}</p>
  {f'<p class="rule-stmt">{md_inline(stmt)}</p>' if stmt and stmt != title_text else ''}
  {notes_html}
</div>'''


def family_section(fam):
    rule_count = len(fam['rules'])
    included = sum(1 for r in fam['rules'] if r['status'] in ('INCLUDED', 'UPDATED'))
    cards = '\n'.join(rule_card(r) for r in fam['rules'])
    return f'''\
<div class="policy-family" id="fam-{fam["code"].lower()}">
  <div class="family-header">
    <span class="family-code">{fam["code"]}</span>
    <span class="family-title">{fam["title"]}</span>
    <span class="family-count">{included}/{rule_count} active</span>
  </div>
  <div class="rule-grid">
    {cards}
  </div>
</div>'''


NAV_HTML = '''\
<nav class="site-nav">
  <div class="nav-inner">
    <a href="../index.html" class="nav-brand">
      <img src="../assets/img/logo.svg" alt="Freedom and Dignity Project" width="36" height="36">
      <span class="nav-wordmark">Freedom and Dignity<span>Project</span></span>
    </a>
    <button class="nav-hamburger" aria-label="Menu">☰</button>
    <ul class="nav-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="index.html">Pillars</a></li>
      <li><a href="../compare/index.html">Compare</a></li>
    </ul>
  </div>
</nav>'''

FOOTER_HTML = '''\
<footer class="site-footer">
  <div class="wrap">
    <span class="footer-brand">Freedom and Dignity Project</span>
    <ul class="footer-links">
      <li><a href="../index.html">Home</a></li>
      <li><a href="../foundations.html">Foundations</a></li>
      <li><a href="index.html">Pillars</a></li>
      <li><a href="../compare/index.html">Compare</a></li>
    </ul>
    <span class="footer-note">A Third Bill of Rights for the 21st Century. · <a href="../about-ai.html" style="color:inherit;opacity:.7">On the Use of AI</a></span>
  </div>
</footer>'''

PILLAR_CSS = '''\
<style>
/* ── Pillar page styles ─────────────────────────────────────── */
.pil-snav {
  position: sticky; top: 63px; z-index: 150;
  background: var(--navy); border-bottom: 2px solid rgba(255,255,255,.12);
  overflow-x: auto; white-space: nowrap;
}
.pil-snav ul { display:flex; gap:0; list-style:none; margin:0; padding:0; }
.pil-snav a {
  display:block; padding:.55rem 1.1rem; font-family:'Oswald',sans-serif;
  font-size:.78rem; letter-spacing:.06em; text-transform:uppercase;
  color:rgba(255,255,255,.62); text-decoration:none; transition:color .15s;
}
.pil-snav a:hover, .pil-snav a.active { color:#fff; }
.pil-snav a.active { border-bottom:2px solid var(--accent-color,#fff); }

/* ── Section layouts ────────────────────────────────────────── */
.pil-intro { display:grid; grid-template-columns:1fr 1fr; gap:2rem; }
@media(max-width:700px){ .pil-intro { grid-template-columns:1fr; } }

.pil-intro h2 { font-size:1.1rem; text-transform:uppercase; letter-spacing:.08em; margin-bottom:.6rem; }
.pil-intro p, .pil-intro li { font-size:1rem; line-height:1.75; }

.problem-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(300px,1fr)); gap:1.25rem; margin-top:1rem; }
.problem-card {
  background:#fff; border-radius:6px; padding:1.2rem 1.4rem;
  border-left:4px solid var(--accent-color,#0a2240);
  box-shadow:0 1px 4px rgba(0,0,0,.07);
}
.problem-card h3 { font-size:1rem; margin:0 0 .4rem; color:var(--navy); }
.problem-card p  { font-size:.92rem; line-height:1.65; margin:0; color:#333; }

.reform-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(260px,1fr)); gap:1rem; margin-top:1rem; }
.reform-card {
  background:var(--navy); color:#fff; border-radius:6px;
  padding:1.1rem 1.3rem; border-top:3px solid var(--accent-color,#c9952a);
}
.reform-card h3 { font-size:.95rem; margin:0 0 .4rem; color:var(--accent-color,#fff); text-transform:uppercase; letter-spacing:.04em; }
.reform-card p  { font-size:.88rem; line-height:1.6; margin:0; color:rgba(255,255,255,.8); }

/* ── Policy rules ───────────────────────────────────────────── */
.policy-family { margin-bottom:2.5rem; }
.family-header {
  display:flex; align-items:baseline; gap:.8rem; margin-bottom:1rem;
  padding-bottom:.5rem; border-bottom:2px solid var(--accent-color,#0a2240);
}
.family-code {
  font-family:'Oswald',sans-serif; font-size:1.1rem;
  color:var(--accent-color,#0a2240); min-width:3rem;
}
.family-title { font-size:1rem; font-weight:600; color:var(--ink); }
.family-count { margin-left:auto; font-size:.8rem; color:#888; white-space:nowrap; }

.rule-grid {
  display:grid; grid-template-columns:repeat(auto-fill,minmax(280px,1fr)); gap:.75rem;
}
.rule-card {
  border-radius:5px; padding:.9rem 1rem;
  background:#fff; border:1px solid #e0d8c8;
  font-size:.88rem; line-height:1.55;
}
.rule-card.status-included { border-left:4px solid #1e8449; }
.rule-card.status-updated  { border-left:4px solid #2471a3; }
.rule-card.status-partial  { border-left:4px solid #c9952a; }
.rule-card.status-missing  { border-left:4px solid #ccc; opacity:.72; }

.rule-header { display:flex; align-items:center; gap:.5rem; margin-bottom:.35rem; }
.rule-id { font-size:.72rem; color:#888; letter-spacing:.03em; }
.rule-badge {
  font-size:.68rem; font-weight:700; text-transform:uppercase; letter-spacing:.06em;
  padding:.12em .45em; border-radius:3px;
}
.status-included .rule-badge { background:#d4edda; color:#155724; }
.status-updated  .rule-badge { background:#cce5ff; color:#004085; }
.status-partial  .rule-badge { background:#fff3cd; color:#856404; }
.status-missing  .rule-badge { background:#f0f0f0; color:#666; }

.rule-title { font-weight:600; margin:.2rem 0 .2rem; color:var(--ink); }
.rule-stmt  { font-size:.85rem; color:#444; margin:.15rem 0 0; }
.rule-notes { font-size:.8rem; color:#666; font-style:italic; margin:.25rem 0 0; }

/* ── Research section ───────────────────────────────────────── */
.research-body h3 { font-size:1.05rem; color:var(--accent-color,#0a2240); margin:1.5rem 0 .4rem; }
.research-body p  { line-height:1.8; font-size:.97rem; }

/* ── Related pillars ────────────────────────────────────────── */
.related-grid { display:grid; grid-template-columns:repeat(auto-fill,minmax(200px,1fr)); gap:.85rem; margin-top:1rem; }
.related-card {
  background:var(--navy); color:#fff; border-radius:6px; padding:1rem;
  text-decoration:none; transition:opacity .15s;
}
.related-card:hover { opacity:.82; }
.related-card strong { display:block; font-size:.95rem; margin-bottom:.3rem; }
.related-card span   { font-size:.8rem; color:rgba(255,255,255,.65); }

/* ── Summary stats bar ──────────────────────────────────────── */
.stats-bar {
  display:flex; flex-wrap:wrap; gap:1.5rem; margin:1.2rem 0;
  padding:1rem 1.2rem; background:#fff; border-radius:6px;
  border:1px solid #e0d8c8;
}
.stat-item { text-align:center; }
.stat-num { display:block; font-family:'Oswald',sans-serif; font-size:2rem; color:var(--accent-color,#0a2240); }
.stat-label { font-size:.78rem; text-transform:uppercase; letter-spacing:.06em; color:#888; }

/* ── Design logic accordion ─────────────────────────────────── */
details.design-logic { margin-top:1rem; }
details.design-logic summary {
  cursor:pointer; font-weight:700; padding:.6rem .8rem;
  background:rgba(0,0,0,.06); border-radius:4px; user-select:none;
}
details.design-logic[open] summary { border-radius:4px 4px 0 0; }
details.design-logic .design-body { padding:.8rem 1rem; background:#fff; border:1px solid #e0d8c8; border-top:none; border-radius:0 0 4px 4px; }
details.design-logic .design-body p { font-size:.93rem; line-height:1.75; }
details.design-logic .design-body ul { padding-left:1.3rem; }
details.design-logic .design-body li { font-size:.93rem; line-height:1.65; margin-bottom:.3rem; }
</style>'''


def build_snav_links(has_problem, has_reform, has_research, has_related, family_count):
    links = [('<a href="#pil-intro">Overview</a>', True),
             ('<a href="#pil-problem">The Problem</a>', has_problem),
             ('<a href="#pil-reform">Reform Areas</a>', has_reform),
             ('<a href="#pil-policy">Policy Rules</a>', family_count > 0),
             ('<a href="#pil-research">Research</a>', has_research),
             ('<a href="#pil-related">Related</a>', has_related)]
    items = ''.join(f'<li>{a}</li>' for a, show in links if show)
    return f'<nav class="pil-snav" id="pil-snav"><ul>{items}</ul></nav>'


def render_problem_section(text):
    """Parse Problem It Solves: h3 sub-sections become cards."""
    if not text:
        return ''
    # Split into sub-sections
    parts = re.split(r'\n### ', text)
    if len(parts) <= 1:
        return f'<div class="wrap">{md_blocks(text)}</div>'

    cards = ''
    intro = parts[0].strip()
    for part in parts[1:]:
        first_nl = part.find('\n')
        title = part[:first_nl].strip() if first_nl > 0 else part.strip()
        body  = part[first_nl:].strip() if first_nl > 0 else ''
        cards += f'<div class="problem-card"><h3>{md_inline(title)}</h3><p>{md_inline(body.split(chr(10))[0][:300])}</p></div>\n'

    intro_html = f'<p style="font-size:1.05rem;line-height:1.8;margin-bottom:1.2rem">{md_inline(intro)}</p>' if intro else ''
    return f'<div class="wrap">{intro_html}<div class="problem-grid">{cards}</div></div>'


def render_reform_section(text):
    """Parse Key Reform Areas: bullet items or ### sub-sections become cards."""
    if not text:
        return ''
    cards = ''
    # Try ### sub-sections first
    parts = re.split(r'\n###\s+', text)
    if len(parts) > 1:
        intro = parts[0].strip()
        for part in parts[1:]:
            first_nl = part.find('\n')
            title = part[:first_nl].strip() if first_nl > 0 else part.strip()
            body  = part[first_nl:].strip() if first_nl > 0 else ''
            # Extract first sentence/line of body
            body_first = re.sub(r'\n.*', '', body, flags=re.DOTALL)[:280]
            cards += f'<div class="reform-card"><h3>{md_inline(title)}</h3><p>{md_inline(body_first)}</p></div>\n'
        intro_html = f'<p style="margin-bottom:1rem">{md_inline(intro)}</p>' if intro else ''
        return f'<div class="wrap">{intro_html}<div class="reform-grid">{cards}</div></div>'
    # Fall back: bullet list
    lines = text.split('\n')
    for line in lines:
        m = re.match(r'^[-*] \*\*(.+?)\*\*[:\s]*(.*)', line)
        if m:
            cards += f'<div class="reform-card"><h3>{md_inline(m.group(1))}</h3><p>{md_inline(m.group(2)[:240])}</p></div>\n'
        elif re.match(r'^[-*] ', line) and not cards:
            cards += f'<div class="reform-card"><h3>{md_inline(line[2:].strip()[:100])}</h3><p></p></div>\n'
    if cards:
        return f'<div class="wrap"><div class="reform-grid">{cards}</div></div>'
    return f'<div class="wrap">{md_blocks(text)}</div>'


def render_related_pillars(text):
    """Parse Related Pillars section into linked cards."""
    if not text:
        return ''
    cards = ''
    for line in text.split('\n'):
        m = re.match(r'^[-*] \*\*(.+?)\*\*[:\s]*(.*)', line)
        if m:
            pillar_title = m.group(1).strip()
            desc = m.group(2).strip()[:120]
            # Build a slug from the title
            slug = re.sub(r'[^a-z0-9]+', '-', pillar_title.lower()).strip('-')
            cards += f'<a href="{slug}.html" class="related-card"><strong>{pillar_title}</strong><span>{desc}</span></a>\n'
    if cards:
        return f'<div class="wrap"><div class="related-grid">{cards}</div></div>'
    return f'<div class="wrap">{md_blocks(text)}</div>'


def compute_stats(families):
    total = sum(len(f['rules']) for f in families)
    included = sum(1 for f in families for r in f['rules'] if r['status'] in ('INCLUDED', 'UPDATED'))
    partial  = sum(1 for f in families for r in f['rules'] if r['status'] == 'PARTIAL')
    proposed = total - included - partial
    return total, included, partial, proposed


def generate_page(slug, src_slug, title, foundation_key):
    fnd = FOUNDATIONS[foundation_key]
    color = fnd['color']

    src_dir = os.path.join(REPO, 'pillars', src_slug)
    overview_path = os.path.join(src_dir, 'overview.md')
    policy_path   = os.path.join(src_dir, 'policy.md')

    sections = parse_overview(overview_path)
    families = parse_policy(policy_path)

    purpose    = sections.get('Purpose', '')
    principle  = sections.get('Core Principle', '')
    problem    = sections.get('The Problem It Solves', '')
    design     = sections.get('Design Logic', '')
    reform     = sections.get('Key Reform Areas', '')
    research   = sections.get('Research & Context', '')
    related_md = sections.get('Related Pillars', '')

    total, included, partial, proposed = compute_stats(families)

    # ── Hero ──────────────────────────────────────────────────────────────────
    fnd_link = f'../foundations.html#{foundation_key}'
    hero = f'''\
<div class="page-hero compact" style="border-bottom:4px solid {color}">
  <div class="hero-eyebrow">
    <a href="{fnd_link}" style="color:rgba(255,255,255,.6);text-decoration:none">
      Foundation {fnd["num"]}: {fnd["title"]}
    </a>
  </div>
  <h1 class="hero-title" style="font-size:clamp(1.8rem,5vw,2.8rem)">{title}</h1>
  <div class="hero-divider"><span>★ ★ ★</span></div>
  {f'<p class="hero-statement" style="font-size:1rem;max-width:680px;margin:0 auto">{md_inline(purpose[:220])}</p>' if purpose else ''}
</div>'''

    # ── Sticky snav ───────────────────────────────────────────────────────────
    snav = build_snav_links(
        bool(problem), bool(reform), bool(research), bool(related_md), len(families)
    ).replace('var(--accent-color,#fff)', color)
    snav = snav  # accent handled via CSS var below

    # ── Stats bar ──────────────────────────────────────────────────────────────
    stats_bar = ''
    if total > 0:
        stats_bar = f'''\
<div class="stats-bar">
  <div class="stat-item"><span class="stat-num">{total}</span><span class="stat-label">Total Rules</span></div>
  <div class="stat-item"><span class="stat-num" style="color:#1e8449">{included}</span><span class="stat-label">Active</span></div>
  <div class="stat-item"><span class="stat-num" style="color:#c9952a">{partial}</span><span class="stat-label">Partial</span></div>
  <div class="stat-item"><span class="stat-num" style="color:#888">{proposed}</span><span class="stat-label">Proposed</span></div>
</div>'''

    # ── Intro section (purpose + principle) ───────────────────────────────────
    purpose_html   = md_blocks(purpose) if purpose else ''
    principle_html = md_blocks(principle) if principle else ''

    intro_section = f'''\
<section class="bg-parchment ruled" id="pil-intro">
<div class="wrap">
  {stats_bar}
  <div class="pil-intro">
    <div>
      <h2 style="color:{color};font-family:\'Oswald\',sans-serif;text-transform:uppercase;letter-spacing:.06em">Purpose</h2>
      {purpose_html}
    </div>
    <div>
      <h2 style="color:{color};font-family:\'Oswald\',sans-serif;text-transform:uppercase;letter-spacing:.06em">Core Principle</h2>
      {principle_html}
    </div>
  </div>
</div>
</section>'''

    # ── Problem section ────────────────────────────────────────────────────────
    problem_section = ''
    if problem:
        problem_inner = render_problem_section(problem)
        problem_section = f'''\
<section class="bg-dark on-dark ruled" id="pil-problem">
<div class="wrap" style="margin-bottom:0">
  <h2 style="color:{color}">The Problem It Solves</h2>
</div>
{problem_inner}
</section>'''

    # ── Reform areas ──────────────────────────────────────────────────────────
    reform_section = ''
    if reform:
        reform_inner = render_reform_section(reform)
        reform_section = f'''\
<section class="bg-cream ruled" id="pil-reform">
<div class="wrap" style="margin-bottom:0">
  <h2 style="color:{color}">Key Reform Areas</h2>
</div>
{reform_inner}
</section>'''

    # ── Design logic accordion ─────────────────────────────────────────────────
    design_section = ''
    if design:
        design_html = md_blocks(design)
        design_section = f'''\
<section class="bg-parchment ruled">
<div class="wrap">
  <details class="design-logic">
    <summary>Design Logic — How These Rules Work Together</summary>
    <div class="design-body">{design_html}</div>
  </details>
</div>
</section>'''

    # ── Policy rules section ───────────────────────────────────────────────────
    policy_section = ''
    if families:
        fam_html = '\n'.join(family_section(f) for f in families)
        policy_section = f'''\
<section class="bg-cream ruled" id="pil-policy">
<div class="wrap">
  <h2 style="color:{color}">Full Policy Platform</h2>
  <p style="font-size:.95rem;color:#555;margin-bottom:1.5rem">
    Every rule in this pillar, organized by policy area.
    <strong style="color:#1e8449">Active</strong> rules are current platform commitments.
    <strong style="color:#c9952a">Partial</strong> rules are in development.
    <strong style="color:#888">Proposed</strong> rules are planned for future inclusion.
  </p>
  {fam_html}
</div>
</section>'''

    # ── Research section ───────────────────────────────────────────────────────
    research_section = ''
    if research:
        research_html = md_blocks(research)
        research_section = f'''\
<section class="bg-dark on-dark ruled" id="pil-research">
<div class="wrap">
  <h2 style="color:{color}">Research & Context</h2>
  <div class="research-body" style="color:rgba(255,255,255,.85)">{research_html}</div>
</div>
</section>'''

    # ── Related pillars ────────────────────────────────────────────────────────
    related_section = ''
    if related_md:
        related_inner = render_related_pillars(related_md)
        related_section = f'''\
<section class="bg-parchment ruled" id="pil-related">
<div class="wrap" style="margin-bottom:0">
  <h2 style="color:{color}">Related Pillars</h2>
  <p style="font-size:.92rem;color:#666;margin-bottom:.5rem">These pillars intersect with and reinforce this one.</p>
</div>
{related_inner}
<div class="wrap" style="margin-top:2rem;display:flex;gap:1rem;flex-wrap:wrap">
  <a href="{fnd_link}" class="btn-primary" style="background:{color}">← Foundation {fnd["num"]}: {fnd["title"]}</a>
  <a href="index.html" class="btn-primary" style="background:var(--navy)">All Pillars</a>
</div>
</section>'''
    else:
        related_section = f'''\
<section class="bg-parchment ruled">
<div class="wrap">
  <div style="display:flex;gap:1rem;flex-wrap:wrap">
    <a href="{fnd_link}" class="btn-primary" style="background:{color}">← Foundation {fnd["num"]}: {fnd["title"]}</a>
    <a href="index.html" class="btn-primary" style="background:var(--navy)">All Pillars</a>
  </div>
</div>
</section>'''

    # ── Scroll-spy JS ──────────────────────────────────────────────────────────
    scrollspy_js = '''\
<script>
(function(){
  var nav = document.getElementById('pil-snav');
  if(!nav) return;
  var links = nav.querySelectorAll('a[href^="#"]');
  var sections = Array.from(links).map(function(a){
    return document.querySelector(a.getAttribute('href'));
  }).filter(Boolean);
  function onScroll(){
    var y = window.scrollY + 120;
    var active = sections[0];
    sections.forEach(function(s){ if(s.offsetTop <= y) active = s; });
    links.forEach(function(a){
      a.classList.toggle('active', a.getAttribute('href') === '#'+active.id);
    });
  }
  window.addEventListener('scroll', onScroll, {passive:true});
  onScroll();
})();
</script>'''

    # ── Full page ──────────────────────────────────────────────────────────────
    page = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Freedom and Dignity Project</title>
<link rel="stylesheet" href="../assets/css/style.css">
<link rel="icon" type="image/svg+xml" href="../assets/img/logo.svg">
{PILLAR_CSS.replace("var(--accent-color,#0a2240)", color).replace("var(--accent-color,#fff)", color).replace("var(--accent-color,#c9952a)", color)}
<style>:root {{ --accent-color: {color}; }}</style>
</head>
<body>
{NAV_HTML}
{hero}
{snav}
{intro_section}
{problem_section}
{reform_section}
{design_section}
{policy_section}
{research_section}
{related_section}
{FOOTER_HTML}
<script src="../assets/js/data.js"></script>
<script src="../assets/js/app.js"></script>
{scrollspy_js}
</body>
</html>'''

    return page


def main():
    out_dir = os.path.join(REPO, 'docs', 'pillars')
    os.makedirs(out_dir, exist_ok=True)

    targets = sys.argv[1:] if sys.argv[1:] else None  # optional: specific slugs

    for slug, src_slug, title, foundation_key in PILLARS:
        if targets and slug not in targets:
            continue
        src_dir = os.path.join(REPO, 'pillars', src_slug)
        if not os.path.isdir(src_dir):
            print(f'  SKIP {slug} — source dir not found: {src_dir}')
            continue

        print(f'  Building {slug}...', end=' ')
        html = generate_page(slug, src_slug, title, foundation_key)
        out_path = os.path.join(out_dir, f'{slug}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        # Count lines as a sanity check
        line_count = html.count('\n')
        print(f'{line_count} lines')

    print('Done.')


if __name__ == '__main__':
    main()
