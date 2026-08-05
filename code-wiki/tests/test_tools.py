from pathlib import Path

from code_wiki.outline import extract_symbols, format_outline
from code_wiki.tools.filesystem import list_dir, read_file
from code_wiki.tools.grep import grep_code
from code_wiki.tools.symbols import find_definition


def test_outline_and_symbol(tmp_path: Path):
    src = tmp_path / "svc.py"
    src.write_text(
        "import os\n\n"
        "class AuthService:\n"
        "    def login(self, u: str) -> str:\n"
        "        return u\n"
        "\n"
        "def helper():\n"
        "    pass\n"
    )
    lines = src.read_text().splitlines()
    symbols = extract_symbols(lines)
    names = {s.qualified for s in symbols}
    assert "AuthService" in names
    assert "AuthService.login" in names or "login" in {s.name for s in symbols}

    outline = format_outline("svc.py", lines)
    assert "AuthService" in outline

    body = read_file(tmp_path, {"path": "svc.py", "mode": "symbol", "symbol": "login"})
    assert "def login" in body


def test_list_dir_and_grep(tmp_path: Path):
    (tmp_path / "pkg").mkdir()
    (tmp_path / "pkg" / "a.py").write_text("def foo():\n    return 1\n")
    listing = list_dir(tmp_path, {"path": "."})
    assert "pkg/" in listing

    hits = grep_code(tmp_path, {"pattern": "def foo", "glob": "*.py"})
    assert "foo" in hits


def test_find_definition(tmp_path: Path):
    (tmp_path / "m.py").write_text("def pay_invoice():\n    return 0\n")
    out = find_definition(tmp_path, {"symbol": "pay_invoice"})
    assert "pay_invoice" in out
    assert "DEFINITIONS" in out
