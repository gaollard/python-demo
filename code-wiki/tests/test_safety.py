from pathlib import Path

import pytest

from code_wiki.safety import PathEscapeError, resolve_under_root, truncate


def test_resolve_under_root_ok(tmp_path: Path):
    f = tmp_path / "a" / "b.txt"
    f.parent.mkdir()
    f.write_text("x")
    resolved = resolve_under_root(tmp_path, "a/b.txt")
    assert resolved == f.resolve()


def test_resolve_blocks_escape(tmp_path: Path):
    with pytest.raises(PathEscapeError):
        resolve_under_root(tmp_path, "../outside")


def test_truncate():
    assert truncate("hi", 100) == "hi"
    out = truncate("abcdef", 5)
    assert "truncat" in out or len(out) <= 5 + 20
