from __future__ import annotations

import re
from dataclasses import dataclass

# Heuristic signature lines (P0)
_SIG_RE = re.compile(
    r"^(\s*)("
    r"class\s+\w+"
    r"|def\s+\w+"
    r"|async\s+def\s+\w+"
    r"|function\s+\w+"
    r"|export\s+(?:async\s+)?function\s+\w+"
    r"|export\s+class\s+\w+"
    r"|export\s+(?:const|let|var)\s+\w+\s*="
    r"|func\s+(?:\([^)]*\)\s*)?\w+"
    r"|fn\s+\w+"
    r"|pub\s+(?:async\s+)?fn\s+\w+"
    r"|(?:public|private|protected|static|final|\s)+[\w<>\[\]]+\s+\w+\s*\("
    r"|interface\s+\w+"
    r"|type\s+\w+\s*="
    r"|struct\s+\w+"
    r"|enum\s+\w+"
    r")"
)

_IMPORT_RE = re.compile(
    r"^\s*(?:"
    r"import\s+(\S+)"
    r"|from\s+(\S+)\s+import"
    r"|#include\s+[<\"]([^>\"]+)"
    r"|use\s+([\w:]+)"
    r"|require\(['\"]([^'\"]+)['\"]\)"
    r")"
)

_NAME_RE = re.compile(
    r"(?:class|def|async\s+def|function|func|fn|interface|struct|enum|type)\s+"
    r"(?:\([^)]*\)\s*)?(\w+)"
    r"|export\s+(?:const|let|var)\s+(\w+)"
)


@dataclass
class SymbolSpan:
    name: str
    qualified: str
    kind: str
    start_line: int  # 1-based
    end_line: int  # inclusive
    signature: str
    indent: int


def _kind_from_sig(sig: str) -> str:
    s = sig.lstrip()
    if s.startswith("class ") or s.startswith("export class "):
        return "class"
    if "interface " in s[:20]:
        return "interface"
    if "struct " in s[:20]:
        return "struct"
    if "enum " in s[:20]:
        return "enum"
    if "def " in s or "function " in s or "func " in s or "fn " in s:
        return "function"
    return "symbol"


def _name_from_sig(sig: str) -> str | None:
    m = _NAME_RE.search(sig)
    if not m:
        return None
    return m.group(1) or m.group(2)


def extract_symbols(lines: list[str]) -> list[SymbolSpan]:
    """Extract top-level / nested signatures via indent heuristics."""
    raw: list[tuple[int, int, str, str]] = []  # indent, line_no, sig, name
    for i, line in enumerate(lines, start=1):
        if not _SIG_RE.match(line.rstrip("\n")):
            continue
        name = _name_from_sig(line)
        if not name:
            continue
        indent = len(line) - len(line.lstrip(" \t"))
        raw.append((indent, i, line.rstrip(), name))

    if not raw:
        return []

    symbols: list[SymbolSpan] = []
    stack: list[tuple[int, int, str]] = []  # indent, start_idx_in_symbols, name

    for idx, (indent, line_no, sig, name) in enumerate(raw):
        while stack and stack[-1][0] >= indent:
            prev_indent, sym_i, _ = stack.pop()
            # end at line before this signature
            end = line_no - 1
            symbols[sym_i] = SymbolSpan(
                name=symbols[sym_i].name,
                qualified=symbols[sym_i].qualified,
                kind=symbols[sym_i].kind,
                start_line=symbols[sym_i].start_line,
                end_line=max(symbols[sym_i].start_line, end),
                signature=symbols[sym_i].signature,
                indent=symbols[sym_i].indent,
            )

        parent_names = [n for _, _, n in stack]
        qualified = ".".join(parent_names + [name]) if parent_names else name
        kind = _kind_from_sig(sig)
        if parent_names and kind == "function":
            kind = "method"

        symbols.append(
            SymbolSpan(
                name=name,
                qualified=qualified,
                kind=kind,
                start_line=line_no,
                end_line=line_no,  # provisional
                signature=sig.strip(),
                indent=indent,
            )
        )
        stack.append((indent, len(symbols) - 1, name))

    # close remaining to EOF
    eof = len(lines)
    while stack:
        _, sym_i, _ = stack.pop()
        symbols[sym_i] = SymbolSpan(
            name=symbols[sym_i].name,
            qualified=symbols[sym_i].qualified,
            kind=symbols[sym_i].kind,
            start_line=symbols[sym_i].start_line,
            end_line=eof,
            signature=symbols[sym_i].signature,
            indent=symbols[sym_i].indent,
        )

    # Fix nested end_lines: sibling-aware already; for nested, end before next sibling
    # Recompute ends more carefully
    return _fix_end_lines(symbols, eof)


def _fix_end_lines(symbols: list[SymbolSpan], eof: int) -> list[SymbolSpan]:
    if not symbols:
        return symbols
    fixed: list[SymbolSpan] = []
    for i, sym in enumerate(symbols):
        end = eof
        for j in range(i + 1, len(symbols)):
            nxt = symbols[j]
            if nxt.indent <= sym.indent:
                end = nxt.start_line - 1
                break
            # still nested; continue
        else:
            end = eof
        fixed.append(
            SymbolSpan(
                name=sym.name,
                qualified=sym.qualified,
                kind=sym.kind,
                start_line=sym.start_line,
                end_line=max(sym.start_line, end),
                signature=sym.signature,
                indent=sym.indent,
            )
        )
    return fixed


def extract_imports(lines: list[str], limit: int = 20) -> list[str]:
    found: list[str] = []
    for line in lines[:200]:
        m = _IMPORT_RE.match(line)
        if not m:
            continue
        name = next(g for g in m.groups() if g)
        if name not in found:
            found.append(name)
        if len(found) >= limit:
            break
    return found


def format_outline(
    rel_path: str,
    lines: list[str],
    *,
    max_symbols: int = 80,
) -> str:
    imports = extract_imports(lines)
    symbols = extract_symbols(lines)
    out = [f"# {rel_path}  ({len(lines)} lines)"]
    if imports:
        out.append(f"imports: {', '.join(imports)}  ({len(imports)})")
    else:
        out.append("imports: (none detected)")
    out.append("")
    if not symbols:
        head = min(40, len(lines))
        out.append("[no signatures detected; showing file head — try mode=body]")
        for i in range(head):
            out.append(f"L{i + 1}  {lines[i].rstrip()}")
        return "\n".join(out)

    shown = symbols[:max_symbols]
    for sym in shown:
        pad = "  " * (sym.indent // 2 if sym.indent else 0)
        # prefer spaces-based display indent from nesting depth
        depth = sym.qualified.count(".")
        pad = "  " * depth
        out.append(f"L{sym.start_line}  {pad}{sym.signature}")
    if len(symbols) > max_symbols:
        out.append(f"[truncated: {len(symbols) - max_symbols} more symbols]")
    return "\n".join(out)


def find_symbol_span(lines: list[str], symbol: str) -> SymbolSpan | None:
    symbols = extract_symbols(lines)
    if not symbols:
        return None
    # exact qualified, then exact name, then suffix match
    for sym in symbols:
        if sym.qualified == symbol or sym.name == symbol:
            return sym
    for sym in symbols:
        if sym.qualified.endswith("." + symbol):
            return sym
    return None


def format_symbol_body(rel_path: str, lines: list[str], symbol: str) -> str:
    span = find_symbol_span(lines, symbol)
    if span is None:
        available = ", ".join(s.qualified for s in extract_symbols(lines)[:40]) or "(none)"
        return (
            f"ERROR: symbol '{symbol}' not found in {rel_path}\n"
            f"Available: {available}"
        )
    chunk = lines[span.start_line - 1 : span.end_line]
    numbered = [f"{span.start_line + i}|{line.rstrip()}" for i, line in enumerate(chunk)]
    header = (
        f"# {rel_path}  symbol={span.qualified}  "
        f"{span.kind}  L{span.start_line}-{span.end_line}"
    )
    return header + "\n" + "\n".join(numbered)
