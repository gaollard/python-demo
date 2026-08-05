from __future__ import annotations

from pathlib import Path

DEFAULT_IGNORE_DIRS = frozenset(
    {
        ".git",
        "node_modules",
        "dist",
        "build",
        ".venv",
        "venv",
        "__pycache__",
        ".idea",
        ".cursor",
        ".code-wiki",
        ".tox",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "target",
        "vendor",
    }
)

TEXT_EXTENSIONS = frozenset(
    {
        ".py",
        ".pyi",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".mjs",
        ".cjs",
        ".go",
        ".java",
        ".kt",
        ".rs",
        ".c",
        ".h",
        ".cpp",
        ".cc",
        ".hpp",
        ".cs",
        ".rb",
        ".php",
        ".swift",
        ".scala",
        ".sh",
        ".bash",
        ".zsh",
        ".md",
        ".txt",
        ".rst",
        ".json",
        ".yaml",
        ".yml",
        ".toml",
        ".ini",
        ".cfg",
        ".xml",
        ".html",
        ".css",
        ".scss",
        ".sql",
        ".graphql",
        ".proto",
        ".env",
        ".gitignore",
        ".dockerignore",
        "Dockerfile",
        "Makefile",
        ".vue",
        ".svelte",
    }
)


class PathEscapeError(ValueError):
    pass


def resolve_under_root(root: Path, relative: str | Path) -> Path:
    """Resolve path and ensure it stays inside root."""
    root = root.resolve()
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise PathEscapeError(f"path escapes workspace: {relative}") from exc
    return candidate


def is_ignored_name(name: str) -> bool:
    return name in DEFAULT_IGNORE_DIRS or name.startswith(".")


def should_skip_dir(path: Path) -> bool:
    return path.name in DEFAULT_IGNORE_DIRS


def is_probably_text_file(path: Path) -> bool:
    if path.name in {"Dockerfile", "Makefile", "Gemfile", "Procfile", "Jenkinsfile"}:
        return True
    if path.suffix.lower() in TEXT_EXTENSIONS:
        return True
    # extensionless small files: allow attempt
    return path.suffix == ""


def truncate(text: str, max_chars: int = 20_000, note: str = "[truncated]") -> str:
    if len(text) <= max_chars:
        return text
    return text[: max_chars - len(note) - 1] + "\n" + note


def truncate_lines(lines: list[str], max_lines: int, note: str = "[truncated]") -> list[str]:
    if len(lines) <= max_lines:
        return lines
    return lines[:max_lines] + [note]
