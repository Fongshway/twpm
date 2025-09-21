import pytest
from typer.testing import CliRunner

from twpm.__version__ import __version__
from twpm.cli import app


@pytest.fixture
def cli_runner() -> CliRunner:
    return CliRunner()


def test_cli_version_flag(cli_runner):
    result = cli_runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stderr


def test_diagnostics_command(cli_runner):
    result = cli_runner.invoke(app, ["diagnostics"])
    assert result.exit_code == 0


@pytest.mark.parametrize("hook_type", ["on-add", "on-modify"])
def test_install_command(hook_type, cli_runner, tmp_path):
    result = cli_runner.invoke(
        app,
        [
            "install",
            hook_type,
            "--hooks-location",
            str(tmp_path),
        ],
    )

    # Should succeed
    assert result.exit_code == 0

    hook_file = tmp_path / f"{hook_type}-twpm"
    assert hook_file.exists()
    assert hook_file.is_file()
