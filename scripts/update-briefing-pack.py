#!/usr/bin/env python3
"""
update-briefing-pack.py

Regenerates the dynamic sections of policy/briefing-pack.md:
  - "Last updated" date
  - Foundations & pillars table (from data.js)
  - Current state section (card count from DB, research file list)

Safe to run at any time. Only touches the sections it owns;
all editorial content (firm positions, values, theory of change,
open questions) is left untouched.

Usage:
    python3 scripts/update-briefing-pack.py

Run automatically via the pre-commit hook.
"""

import re
import sqlite3
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_JS   = REPO_ROOT / "docs" / "assets" / "js" / "data.js"
DB_PATH   = REPO_ROOT / "policy" / "catalog" / "policy_catalog_v2.sqlite"
RESEARCH  = REPO_ROOT / "policy" / "research"
PACK      = REPO_ROOT / "policy" / "briefing-pack.md"

# ── helpers ──────────────────────────────────────────────────────────────────

def parse_foundations(js: str) -> list[dict]:
    """Extract foundation objects (id, num, title) from data.js."""
    pattern = re.compile(
        r"\{\s*id:\s*'([^']+)',\s*num:\s*'([^']+)',\s*title:\s*'([^']+)'",
        re.MULTILINE,
    )
    return [{"id": m.group(1), "num": m.group(2), "title": m.group(3)}
            for m in pattern.finditer(js)]


def parse_pillars(js: str) -> list[dict]:
    """Extract pillar objects (id, title, foundation) from data.js.

    Handles escaped single quotes inside JS string values (e.g. "Workers\\'").
    """
    # JS single-quoted string: allow \' inside
    js_str = r"'((?:[^'\\]|\\.)*)'"
    pattern = re.compile(
        r"\{\s*id:\s*" + js_str + r",\s*title:\s*" + js_str + r",\s*foundation:\s*" + js_str,
        re.MULTILINE,
    )
    results = []
    for m in pattern.finditer(js):
        title = m.group(2).replace("\\'", "'")
        results.append({"id": m.group(1), "title": title, "foundation": m.group(3)})
    return results


def get_canonical_count() -> int:
    if not DB_PATH.exists():
        return 0
    conn = sqlite3.connect(DB_PATH)
    count = conn.execute(
        "SELECT COUNT(*) FROM positions WHERE status = 'CANONICAL'"
    ).fetchone()[0]
    conn.close()
    return count


def list_research_files() -> list[str]:
    """Return display names of top-level research markdown files."""
    if not RESEARCH.exists():
        return []
    return sorted(
        f.name for f in RESEARCH.iterdir()
        if f.is_file() and f.suffix == ".md"
    )


def build_table(foundations: list[dict], pillars: list[dict]) -> str:
    rows = ["| Foundation | Pillars |", "|---|---|"]
    for f in foundations:
        pillar_titles = [
            p["title"] for p in pillars if p["foundation"] == f["id"]
        ]
        row = f"| **{f['num']}. {f['title']}** | {', '.join(pillar_titles)} |"
        rows.append(row)
    return "\n".join(rows)


def build_current_state(card_count: int, research_files: list[str]) -> str:
    month = date.today().strftime("%B %Y")
    file_lines = "\n".join(f"  - `policy/research/{fn}`" for fn in research_files)
    return (
        f"- {len(list((REPO_ROOT / 'docs' / 'pillars').glob('*.html')))} live pillar pages"
        f" — all policy cards complete as of {month}\n"
        f"- {card_count:,} policy positions in the catalog\n"
        f"- Research documents (internal working documents, not on site):\n"
        f"{file_lines}"
    )


# ── section replacement ───────────────────────────────────────────────────────

def replace_section(text: str, start_marker: str, end_marker: str, new_body: str) -> str:
    """Replace everything between start_marker and end_marker (exclusive)."""
    pattern = re.compile(
        re.escape(start_marker) + r".*?" + re.escape(end_marker),
        re.DOTALL,
    )
    replacement = f"{start_marker}\n\n{new_body}\n\n{end_marker}"
    result, count = pattern.subn(replacement, text)
    if count == 0:
        raise ValueError(f"Could not find section bounded by {start_marker!r} … {end_marker!r}")
    return result


# ── main ─────────────────────────────────────────────────────────────────────

def main() -> None:
    js_text = DATA_JS.read_text(encoding="utf-8")
    foundations = parse_foundations(js_text)
    pillars     = parse_pillars(js_text)

    card_count     = get_canonical_count()
    research_files = list_research_files()

    content = PACK.read_text(encoding="utf-8")

    # 1. Update "Last updated" date
    month = date.today().strftime("%B %Y")
    content = re.sub(
        r"_Last updated: [^_]+_",
        f"_Last updated: {month}. Upload this file at the start of a brainstorming session._",
        content,
        count=1,
    )

    # 2. Rebuild foundations/pillars table
    new_table = build_table(foundations, pillars)
    content = replace_section(
        content,
        "## The 5 foundations and 25 pillars",
        "---\n\n## Voice and tone",
        new_table,
    )

    # 3. Rebuild current state section
    new_state = build_current_state(card_count, research_files)
    content = replace_section(
        content,
        "## Current state of the platform",
        "---\n\n## Open questions",
        new_state,
    )

    PACK.write_text(content, encoding="utf-8")
    print(f"✓ briefing-pack.md updated ({card_count:,} canonical positions, "
          f"{len(foundations)} foundations, {len(pillars)} pillars, "
          f"{len(research_files)} research files)")


if __name__ == "__main__":
    main()
