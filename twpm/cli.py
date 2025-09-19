import copy
import difflib
import enum
import json
import pathlib
import sys
from typing import Optional

import rich.console
import rich.json
import rich.syntax
import typer
from taskw_ng.warrior import TaskWarrior
from typing_extensions import Annotated

from twpm.__version__ import __version__

app = typer.Typer()
console = rich.console.Console()


def version_callback(value: bool = False) -> None:
    if value:
        typer.echo(f"twpm CLI Version: {__version__}", err=True)
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def cli(
    ctx: typer.Context,
    version: Annotated[  # pylint: disable=unused-argument
        Optional[bool],
        typer.Option(
            "--version",
            callback=version_callback,
            is_eager=True,
            help="Show the version and exit.",
        ),
    ] = None,
) -> None:
    """twpm - A CLI app for managing Taskwarrior plugins"""
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


@app.command()
def diagnostics() -> None:
    typer.echo(f"twpm {__version__}")
    typer.echo(f"task {TaskWarrior.get_version()}")


class HookType(enum.Enum):
    ON_ADD = "on-add"
    ON_MODIFY = "on-modify"


@app.command()
def install(
    hook_type: HookType = typer.Argument(..., help="Which hook type to install."),
    hooks_location: pathlib.Path = typer.Option(
        pathlib.Path.home() / ".task" / "hooks",
        "--hooks-location",
        "-l",
        help="Directory to install hooks into (default: $HOME/.task/hooks)",
        dir_okay=True,
        file_okay=False,
        writable=True,
    ),
) -> None:
    """
    Install a hook script.

    Example:
      twpm install on-add
      twpm install on-modify
    """
    typer.echo(f"Installing hook: {hook_type.value}")
    hooks_location.mkdir(parents=True, exist_ok=True)
    script_path = hooks_location / f"{hook_type.value}-twpm"

    script_contents = [
        "#!/usr/bin/env bash",
        f"exec {sys.executable} -m twpm {hook_type.value} -\n",
    ]

    # script_path.write_text(script_contents)
    script_path.write_text("\n".join(script_contents))
    script_path.chmod(0o755)
    typer.echo(f"Installed hook script at {script_path}")


@app.command("on-add")
def on_add(
    payload: str | None = typer.Argument(
        None,
        help="Task JSON payload. Omit to read from stdin, or pass '-' to force stdin.",
    )
) -> None:
    """
    Handle Taskwarrior on-add hook input.
    Reads a single argument from stdin.
    """
    # --- Read payload ---
    if payload is None or payload == "-":
        payload = sys.stdin.read().strip()

    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        console.print(f"[red]Error:[/red] input is not valid JSON:\n{payload}")
        raise typer.Exit(1) from exc

    # --- Show input JSON ---
    console.rule("[bold yellow]Input JSON")
    console.print(rich.json.JSON(payload))

    # --- Modify JSON (example: add a custom field) ---
    modified = copy.deepcopy(data)
    modified["tags"] = ["@home"]  # on-add hooks run here.

    # --- Show output JSON ---
    console.rule("[bold green]Output JSON")
    console.print(rich.json.JSON(json.dumps(modified)))

    # --- Show diff ---
    modified_str = json.dumps(modified, indent=2)
    payload_str = json.dumps(data, indent=2)
    diff = difflib.unified_diff(
        payload_str.splitlines(),
        modified_str.splitlines(),
        fromfile="input",
        tofile="output",
        lineterm="",
    )
    diff_text = "\n".join(diff)

    console.rule("[bold cyan]Diff")
    if diff_text.strip():
        console.print(rich.syntax.Syntax(diff_text, "diff", theme="monokai", word_wrap=True))
    else:
        console.print("[dim]No differences[/dim]")
