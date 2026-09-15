import subprocess
import sys
import venv
from pathlib import Path

import click

# Curated package profiles. Keep these focused - "essentials" should stay small
# and genuinely useful, not a dumping ground.
PROFILES = {
    "essentials": {
        "description": "Everyday must-haves for almost any Python project",
        "packages": [
            "requests",       # HTTP calls
            "python-dotenv",  # .env config loading
            "rich",           # pretty terminal output
            "click",          # CLI building
            "pytest",         # testing
            "black",          # formatting
            "ruff",           # linting
            "ipython",        # better REPL
        ],
    },
    "web": {
        "description": "Web / API development",
        "packages": [
            "fastapi",
            "uvicorn[standard]",
            "requests",
            "httpx",
            "python-dotenv",
            "pydantic",
        ],
    },
    "data": {
        "description": "Data analysis / data science",
        "packages": [
            "numpy",
            "pandas",
            "matplotlib",
            "jupyter",
            "openpyxl",
        ],
    },
    "testing": {
        "description": "Testing & quality tooling",
        "packages": [
            "pytest",
            "pytest-cov",
            "black",
            "ruff",
            "mypy",
        ],
    },
}


@click.group()
def setup_group():
    """Bootstrap a fully wired-up Python dev environment (venv + curated packages)."""
    pass


@setup_group.command("profiles")
def list_profiles():
    """List available setup profiles and what they install."""
    for name, info in PROFILES.items():
        click.secho(f"\n{name}", fg="cyan", bold=True)
        click.echo(f"  {info['description']}")
        click.echo(f"  packages: {', '.join(info['packages'])}")


@setup_group.command("init")
@click.option(
    "--profile", "-p",
    type=click.Choice(list(PROFILES.keys())),
    default="essentials",
    show_default=True,
    help="Which curated package set to install.",
)
@click.option(
    "--venv-name", "-v",
    default=".venv",
    show_default=True,
    help="Name/path of the virtualenv to create.",
)
@click.option(
    "--extra", "-e",
    multiple=True,
    help="Extra package(s) to install on top of the profile. Repeatable.",
)
@click.option(
    "--no-venv",
    is_flag=True,
    help="Skip venv creation and install into the current Python environment.",
)
@click.option(
    "--freeze/--no-freeze",
    default=True,
    show_default=True,
    help="Write a requirements.txt after installing.",
)
def init(profile, venv_name, extra, no_venv, freeze):
    """Create a venv and install a curated package profile into it.

    Example:

        devset setup init --profile web --extra sqlalchemy
    """
    packages = list(PROFILES[profile]["packages"]) + list(extra)
    cwd = Path.cwd()

    if no_venv:
        python_bin = sys.executable
        click.echo("Skipping venv creation, using current interpreter.")
    else:
        venv_path = cwd / venv_name
        if venv_path.exists():
            click.echo(f"Found existing venv at {venv_path}, reusing it.")
        else:
            click.echo(f"Creating virtualenv at {venv_path} ...")
            venv.EnvBuilder(with_pip=True).create(str(venv_path))

        if sys.platform == "win32":
            python_bin = str(venv_path / "Scripts" / "python.exe")
        else:
            python_bin = str(venv_path / "bin" / "python")

    click.echo(f"Installing profile '{profile}' ({len(packages)} packages)...")
    click.echo(f"  {', '.join(packages)}\n")

    result = subprocess.run(
        [python_bin, "-m", "pip", "install", "--upgrade", "pip", *packages],
    )
    if result.returncode != 0:
        raise click.ClickException("pip install failed - see output above.")

    if freeze:
        req_path = cwd / "requirements.txt"
        with open(req_path, "w") as f:
            subprocess.run([python_bin, "-m", "pip", "freeze"], stdout=f)
        click.secho(f"Wrote {req_path}", fg="green")

    click.secho("\nDone! Environment is ready.", fg="green", bold=True)
    if not no_venv:
        activate_hint = (
            f"{venv_name}\\Scripts\\activate" if sys.platform == "win32"
            else f"source {venv_name}/bin/activate"
        )
        click.echo(f"Activate it with: {activate_hint}")
