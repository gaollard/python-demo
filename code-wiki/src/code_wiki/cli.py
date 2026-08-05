from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console

from code_wiki import __version__
from code_wiki.agent import run_agent
from code_wiki.config import Settings

console = Console(stderr=True)


def main(
    workspace: Path = typer.Argument(..., help="Path to the code workspace"),
    question: str = typer.Argument(..., help="Natural-language question"),
    max_steps: Optional[int] = typer.Option(
        None, "--max-steps", help="Max tool-calling rounds"
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print step banners and extra debug traces"
    ),
    version: bool = typer.Option(False, "--version", help="Show version and exit"),
) -> None:
    """Code Wiki — analyze a workspace with an LLM agent."""
    if version:
        typer.echo(__version__)
        raise typer.Exit(0)

    ws = workspace.expanduser().resolve()
    if not ws.exists() or not ws.is_dir():
        console.print(f"[red]ERROR:[/red] workspace not found: {ws}")
        raise typer.Exit(1)

    settings = Settings.from_env()
    try:
        answer = run_agent(
            ws,
            question,
            settings=settings,
            verbose=verbose,
            max_steps=max_steps,
            log=lambda m: console.print(m),
        )
    except RuntimeError as e:
        console.print(f"[red]ERROR:[/red] {e}")
        raise typer.Exit(2) from e
    except Exception as e:  # noqa: BLE001
        console.print(f"[red]ERROR:[/red] {type(e).__name__}: {e}")
        raise typer.Exit(2) from e

    sys.stdout.write(answer + "\n")


def app() -> None:
    typer.run(main)


if __name__ == "__main__":
    app()
