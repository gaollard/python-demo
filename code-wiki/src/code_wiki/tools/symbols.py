from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from code_wiki.outline import extract_symbols
from code_wiki.safety import DEFAULT_IGNORE_DIRS, PathEscapeError, resolve_under_root, truncate
from code_wiki.tools.base import ToolSpec

DEF_MAX = 20
REF_MAX = 50
SCAN_EXTS = {
    ".py",
    ".pyi",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".go",
    ".java",
    ".rs",
    ".kt",
}


def _iter_source_files(root: Path, under: Path | None = None):
    start = under or root
    if start.is_file():
        yield start
        return
    for path in start.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in SCAN_EXTS:
            continue
        if any(part in DEFAULT_IGNORE_DIRS for part in path.parts):
            continue
        yield path


def find_definition(workspace: Path, args: dict[str, Any]) -> str:
    symbol = args.get("symbol")
    if not symbol:
        return "ERROR: symbol is required"
    simple = symbol.split(".")[-1]
    root = workspace.resolve()
    under = None
    if args.get("path"):
        try:
            under = resolve_under_root(workspace, args["path"])
        except PathEscapeError as e:
            return f"ERROR: {e}"

    hits: list[str] = []
    for fp in _iter_source_files(root, under):
        try:
            if fp.stat().st_size > 1_000_000:
                continue
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for sym in extract_symbols(lines):
            if sym.qualified == symbol or sym.name == simple or sym.qualified.endswith("." + simple):
                if symbol != simple and sym.name == simple and sym.qualified != symbol:
                    # when user asked qualified, prefer exact; still allow name match
                    pass
                rel = fp.relative_to(root).as_posix()
                hits.append(
                    f"- {rel}:{sym.start_line}-{sym.end_line}  {sym.kind}  "
                    f"{sym.qualified}  :: {sym.signature}"
                )
                if len(hits) >= DEF_MAX:
                    break
        if len(hits) >= DEF_MAX:
            break

    if not hits:
        return (
            f"DEFINITIONS (0) for '{symbol}'\n"
            "No heuristic definitions found. Fallback: use grep."
        )
    header = f"DEFINITIONS ({len(hits)}) backend=heuristic\n"
    return truncate(header + "\n".join(hits))


def find_references(workspace: Path, args: dict[str, Any]) -> str:
    symbol = args.get("symbol")
    if not symbol:
        return "ERROR: symbol is required"
    simple = symbol.split(".")[-1]
    include_decl = bool(args.get("include_declaration", False))
    root = workspace.resolve()
    under = None
    if args.get("path"):
        try:
            under = resolve_under_root(workspace, args["path"])
        except PathEscapeError as e:
            return f"ERROR: {e}"

    # word-boundary-ish match
    try:
        regex = re.compile(rf"\b{re.escape(simple)}\b")
    except re.error as e:
        return f"ERROR: {e}"

    refs: list[str] = []
    for fp in _iter_source_files(root, under):
        try:
            if fp.stat().st_size > 1_000_000:
                continue
            lines = fp.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        rel = fp.relative_to(root).as_posix()
        decl_lines = set()
        if not include_decl:
            for sym in extract_symbols(lines):
                if sym.name == simple:
                    decl_lines.add(sym.start_line)
        for i, line in enumerate(lines, start=1):
            if i in decl_lines:
                continue
            if regex.search(line):
                snippet = line.strip()
                if len(snippet) > 160:
                    snippet = snippet[:160] + "…"
                refs.append(f"- {rel}:{i}  {snippet}")
                if len(refs) >= REF_MAX:
                    break
        if len(refs) >= REF_MAX:
            break

    if not refs:
        return (
            f"REFERENCES (0) for '{symbol}' include_declaration={include_decl}\n"
            "No matches. Try grep or include_declaration=true."
        )
    header = (
        f"REFERENCES ({len(refs)}) for '{symbol}' "
        f"include_declaration={include_decl} backend=heuristic\n"
    )
    note = "\n[truncated]" if len(refs) >= REF_MAX else ""
    return truncate(header + "\n".join(refs) + note)


def symbol_tools() -> list[ToolSpec]:
    return [
        ToolSpec(
            name="find_definition",
            description=(
                "Find symbol definitions (heuristic scan). Prefer over blind grep when "
                "you know a function/class name."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "path": {"type": "string", "description": "Optional scope path"},
                },
                "required": ["symbol"],
            },
            handler=find_definition,
        ),
        ToolSpec(
            name="find_references",
            description=(
                "Find references to a symbol name (heuristic). "
                "Use after find_definition to see callers."
            ),
            parameters={
                "type": "object",
                "properties": {
                    "symbol": {"type": "string"},
                    "path": {"type": "string"},
                    "include_declaration": {"type": "boolean"},
                },
                "required": ["symbol"],
            },
            handler=find_references,
        ),
    ]
