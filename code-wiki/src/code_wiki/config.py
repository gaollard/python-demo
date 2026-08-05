from __future__ import annotations

import os
from dataclasses import dataclass


def _env_int(name: str, default: int) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return int(raw)


def _env_bool(name: str, default: bool) -> bool:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_DEFAULT_MODEL = "deepseek-v4-flash"


@dataclass(frozen=True)
class Settings:
    api_key: str
    base_url: str | None
    model: str
    max_steps: int
    tool_max_workers: int
    tool_timeout: float
    git_enabled: bool
    git_log_max: int
    symbol_backend: str  # auto | heuristic | off (P0: heuristic/off)

    @classmethod
    def from_env(cls) -> Settings:
        api_key = (
            os.environ.get("CODE_WIKI_API_KEY")
            or os.environ.get("DEEPSEEK_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or ""
        )
        base_url = os.environ.get("CODE_WIKI_BASE_URL") or DEEPSEEK_BASE_URL
        return cls(
            api_key=api_key,
            base_url=base_url,
            model=os.environ.get("CODE_WIKI_MODEL", DEEPSEEK_DEFAULT_MODEL),
            max_steps=_env_int("CODE_WIKI_MAX_STEPS", 20),
            tool_max_workers=_env_int("CODE_WIKI_TOOL_MAX_WORKERS", 8),
            tool_timeout=float(os.environ.get("CODE_WIKI_TOOL_TIMEOUT", "30")),
            git_enabled=_env_bool("CODE_WIKI_GIT_ENABLED", True),
            git_log_max=_env_int("CODE_WIKI_GIT_LOG_MAX", 30),
            symbol_backend=os.environ.get("CODE_WIKI_SYMBOL_BACKEND", "heuristic"),
        )
