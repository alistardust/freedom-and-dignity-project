#!/usr/bin/env python3
"""
Export GitHub Copilot CLI chat sessions to structured Markdown files.

Usage:
    python3 scripts/export-chat-logs.py                # export all sessions
    python3 scripts/export-chat-logs.py --project-only # only FDP project sessions
    python3 scripts/export-chat-logs.py --force        # re-export even if up to date

Output location:
    sources/chat-logs/copilot/YYYY-MM/YYYY-MM-DD-<summary>-<short-id>.md

Future S3 migration (when ready):
    aws s3 sync sources/chat-logs/copilot/ s3://your-bucket/copilot-chat-logs/ --storage-class STANDARD_IA
"""

import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SESSION_STATE_DIR = Path.home() / ".copilot" / "session-state"
REPO_ROOT = Path(__file__).parent.parent
OUTPUT_DIR = REPO_ROOT / "sources" / "chat-logs" / "copilot"


# Repositories that belong to this project (handles old username too)
PROJECT_REPOS = {
    "alistardust/freedom-and-dignity-project",
    "alistardust/american-renewal-project",
    "AXington/american-renewal-project",
}




def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:60].strip("-")


def fmt_ts(ts: str) -> str:
    """Format an ISO timestamp to a short readable string."""
    if not ts:
        return ""
    return ts[:16].replace("T", " ") + " UTC"


# ── Load session data ──────────────────────────────────────────────────────────

def load_workspace(session_dir: Path) -> dict:
    """Parse workspace.yaml into a flat dict."""
    ws_file = session_dir / "workspace.yaml"
    if not ws_file.exists():
        return {}
    meta = {}
    with open(ws_file, encoding="utf-8") as f:
        for line in f:
            if ":" in line and not line.startswith(" ") and not line.startswith("#"):
                key, _, value = line.partition(":")
                meta[key.strip()] = value.strip()
    return meta


def load_events(session_dir: Path) -> list:
    """Parse events.jsonl into a list of event dicts."""
    events_file = session_dir / "events.jsonl"
    if not events_file.exists():
        return []
    events = []
    with open(events_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    events.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return events


# ── Conversation reconstruction ────────────────────────────────────────────────

_SKIP_TOOLS = {"report_intent"}  # internal bookkeeping, not meaningful to readers


def _summarize_tool(name: str, args: dict) -> str:
    """Render a tool call as a compact human-readable string."""
    if name == "bash":
        cmd = args.get("command", "").replace("\n", " ").strip()
        desc = args.get("description", "")
        if desc:
            return f"`bash` — {desc}"
        return f"`bash` — {cmd[:100]}" + ("…" if len(cmd) > 100 else "")
    elif name == "view":
        path = args.get("path", "")
        r = args.get("view_range")
        return f"`view` {path}" + (f" lines {r[0]}–{r[1]}" if r else "")
    elif name == "edit":
        return f"`edit` {args.get('path', '')}"
    elif name == "create":
        return f"`create` {args.get('path', '')}"
    elif name == "grep":
        return f"`grep` pattern={args.get('pattern', '')!r}"
    elif name == "glob":
        return f"`glob` {args.get('pattern', '')}"
    elif name == "task":
        return f"`task` [{args.get('agent_type', '')}] {args.get('name', '')} — {args.get('description', '')}"
    elif name == "sql":
        return f"`sql` — {args.get('description', '')}"
    elif name == "ask_user":
        return f"`ask_user` — {args.get('question', '')[:80]}"
    elif name == "store_memory":
        return f"`store_memory` — {args.get('subject', '')}: {args.get('fact', '')[:60]}…"
    elif name in ("read_bash", "write_bash", "stop_bash"):
        shell_id = args.get("shellId", "")
        return f"`{name}` shell={shell_id}"
    elif name in ("read_agent", "write_agent", "list_agents"):
        agent_id = args.get("agent_id", "")
        return f"`{name}`" + (f" {agent_id[:8]}…" if agent_id else "")
    elif name.startswith("github-mcp-server"):
        method = args.get("method", name.split("-")[-1])
        return f"`github` {method}"
    else:
        return f"`{name}`"


def reconstruct_turns(events: list) -> list:
    """
    Reconstruct a list of turns from raw events.
    Each turn is:  {'role': 'user'|'assistant', 'content': str, 'tools': list, 'timestamp': str}
    """
    turns = []
    current_text_chunks = []
    current_tools = []
    in_turn = False

    for event in events:
        etype = event.get("type", "")
        data = event.get("data", {})
        ts = event.get("timestamp", "")

        if etype == "user.message":
            content = data.get("content", "")
            # Strip runtime-injected XML wrappers the CLI adds automatically
            content = re.sub(r"<current_datetime>[^<]*</current_datetime>\s*", "", content)
            content = re.sub(r"<reminder>.*?</reminder>\s*", "", content, flags=re.DOTALL)
            content = content.strip()
            if content:
                turns.append({"role": "user", "content": content, "tools": [], "timestamp": ts})

        elif etype == "assistant.turn_start":
            in_turn = True
            current_text_chunks = []
            current_tools = []

        elif etype == "assistant.message" and in_turn:
            chunk = data.get("content", "")
            if chunk:
                current_text_chunks.append(chunk)
            for req in data.get("toolRequests", []):
                name = req.get("name", "")
                if name and name not in _SKIP_TOOLS:
                    summary = _summarize_tool(name, req.get("arguments", {}))
                    if summary not in current_tools:
                        current_tools.append(summary)

        elif etype == "assistant.turn_end" and in_turn:
            in_turn = False
            text = "".join(current_text_chunks).strip()
            if text or current_tools:
                turns.append({
                    "role": "assistant",
                    "content": text,
                    "tools": list(current_tools),
                    "timestamp": ts,
                })

        elif etype == "system.notification":
            # Surface important system events (agent completions, etc.)
            msg = data.get("message", "").strip()
            if msg and "agent" in msg.lower():
                turns.append({
                    "role": "system",
                    "content": f"_System: {msg}_",
                    "tools": [],
                    "timestamp": ts,
                })

    return turns


# ── Markdown rendering ─────────────────────────────────────────────────────────

def format_markdown(meta: dict, turns: list, session_id: str) -> str:
    summary = meta.get("summary", "Untitled Session")
    created = meta.get("created_at", "")
    updated = meta.get("updated_at", "")
    repo = meta.get("repository", "")
    branch = meta.get("branch", "")

    lines = [
        f"# {summary}",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| **Session ID** | `{session_id}` |",
        f"| **Started** | {created} |",
        f"| **Last updated** | {updated} |",
    ]
    if repo:
        lines.append(f"| **Repository** | [{repo}](https://github.com/{repo}) |")
    if branch:
        lines.append(f"| **Branch** | `{branch}` |")

    user_count = sum(1 for t in turns if t["role"] == "user")
    lines.append(f"| **Turns** | {user_count} user messages |")
    lines += ["", "---", ""]

    for turn in turns:
        role = turn["role"]
        content = turn.get("content", "")
        tools = turn.get("tools", [])
        ts = fmt_ts(turn.get("timestamp", ""))

        if role == "user":
            lines.append("## 👤 Ali")
            if ts:
                lines.append(f"*{ts}*")
            lines.append("")
            lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")

        elif role == "assistant":
            lines.append("## 🤖 Sam")
            if ts:
                lines.append(f"*{ts}*")
            lines.append("")
            if tools:
                lines.append(
                    f"<details><summary>🔧 Tools used ({len(tools)})</summary>\n"
                )
                for t in tools:
                    lines.append(f"- {t}")
                lines.append("\n</details>\n")
            if content:
                lines.append(content)
            lines.append("")
            lines.append("---")
            lines.append("")

        elif role == "system":
            lines.append(f"> {content}")
            lines.append("")

    return "\n".join(lines)


# ── Output path ────────────────────────────────────────────────────────────────

def output_path_for(meta: dict, session_id: str) -> Path:
    created = meta.get("created_at", "")
    if created:
        dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
        date_str = dt.strftime("%Y-%m-%d")
        month_str = dt.strftime("%Y-%m")
    else:
        date_str = "unknown"
        month_str = "unknown"

    summary = meta.get("summary", "session")
    slug = slugify(summary)
    short_id = session_id[:8]
    filename = f"{date_str}-{slug}-{short_id}.md"
    return OUTPUT_DIR / month_str / filename


# ── Main ───────────────────────────────────────────────────────────────────────

def export_session(session_dir: Path, force: bool = False) -> tuple[str, Path | None]:
    """
    Export a single session.
    Returns (status, path) where status is 'exported', 'updated', 'skipped', or 'empty'.
    """
    session_id = session_dir.name
    meta = load_workspace(session_dir)
    events = load_events(session_dir)

    if not events:
        return ("empty", None)

    turns = reconstruct_turns(events)
    user_turns = [t for t in turns if t["role"] == "user"]
    if not user_turns:
        return ("empty", None)

    out_path = output_path_for(meta, session_id)
    is_new = not out_path.exists()

    if out_path.exists() and not force:
        # Re-export the active/current session (last modified recently); skip old ones
        session_mtime = (session_dir / "events.jsonl").stat().st_mtime
        file_mtime = out_path.stat().st_mtime
        if file_mtime >= session_mtime:
            return ("current", out_path)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    md = format_markdown(meta, turns, session_id)
    out_path.write_text(md, encoding="utf-8")
    return ("exported" if is_new else "updated", out_path)


def main():
    force = "--force" in sys.argv
    project_only = "--project-only" in sys.argv

    if not SESSION_STATE_DIR.exists():
        print(f"Session state directory not found: {SESSION_STATE_DIR}", file=sys.stderr)
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    sessions = sorted(SESSION_STATE_DIR.iterdir())
    counts = {"exported": 0, "updated": 0, "current": 0, "empty": 0, "filtered": 0}

    for session_dir in sessions:
        if not session_dir.is_dir():
            continue

        if project_only:
            meta = load_workspace(session_dir)
            repo = meta.get("repository", "")
            if repo not in PROJECT_REPOS:
                counts["filtered"] += 1
                continue

        status, out_path = export_session(session_dir, force=force)
        counts[status] = counts.get(status, 0) + 1
        if out_path and status in ("exported", "updated"):
            rel = out_path.relative_to(REPO_ROOT)
            print(f"  [{status.upper()}] {rel}")
        elif status == "current" and out_path:
            rel = out_path.relative_to(REPO_ROOT)
            print(f"  [OK]      {rel}")

    print(
        f"\nDone. {counts['exported']} new, {counts['updated']} updated, "
        f"{counts['current']} already current, {counts['empty']} skipped (no messages)"
        + (f", {counts['filtered']} filtered (non-project)" if project_only else "")
        + "."
    )
    print(f"Logs: {OUTPUT_DIR.relative_to(REPO_ROOT)}/")
    print()
    print("To sync to S3 when ready:")
    print(
        f"  aws s3 sync {OUTPUT_DIR.relative_to(REPO_ROOT)}/ "
        "s3://your-bucket/copilot-chat-logs/ --storage-class STANDARD_IA"
    )


if __name__ == "__main__":
    main()
