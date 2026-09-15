import subprocess

import click


def _run(args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return result.returncode, result.stdout.strip(), result.stderr.strip()


@click.group()
def git_group():
    """Small git quality-of-life helpers."""
    pass


@git_group.command("summary")
def summary():
    """Show a compact status/branch summary of the current repo."""
    code, branch, err = _run(["rev-parse", "--abbrev-ref", "HEAD"])
    if code != 0:
        raise click.ClickException(f"Not a git repo (or git not available): {err}")

    _, status, _ = _run(["status", "--porcelain"])
    _, ahead_behind, _ = _run(["rev-list", "--left-right", "--count", f"{branch}...origin/{branch}"])
    _, last_commit, _ = _run(["log", "-1", "--pretty=%h %s (%cr)"])

    click.secho(f"Branch: {branch}", fg="cyan", bold=True)
    if last_commit:
        click.echo(f"Last commit: {last_commit}")
    if ahead_behind:
        parts = ahead_behind.split()
        if len(parts) == 2:
            click.echo(f"Ahead/behind origin: +{parts[0]}/-{parts[1]}")

    if status:
        lines = status.splitlines()
        click.secho(f"Uncommitted changes: {len(lines)}", fg="yellow")
        for line in lines[:10]:
            click.echo(f"  {line}")
        if len(lines) > 10:
            click.echo(f"  ... and {len(lines) - 10} more")
    else:
        click.secho("Working tree clean", fg="green")


@git_group.command("merged-branches")
@click.option("--base", default="main", show_default=True, help="Base branch to compare against.")
def merged_branches(base):
    """List local branches already merged into BASE (safe to delete)."""
    code, out, err = _run(["branch", "--merged", base])
    if code != 0:
        raise click.ClickException(err)
    branches = [
        b.strip().lstrip("* ").strip()
        for b in out.splitlines()
        if b.strip().lstrip("* ").strip() not in (base, "")
    ]
    if not branches:
        click.echo("No merged branches to clean up.")
        return
    for b in branches:
        click.echo(b)


@git_group.command("clean-branches")
@click.option("--base", default="main", show_default=True, help="Base branch to compare against.")
@click.option("--yes", is_flag=True, help="Skip confirmation prompt.")
def clean_branches(base, yes):
    """Delete local branches already merged into BASE."""
    code, out, err = _run(["branch", "--merged", base])
    if code != 0:
        raise click.ClickException(err)
    branches = [
        b.strip().lstrip("* ").strip()
        for b in out.splitlines()
        if b.strip().lstrip("* ").strip() not in (base, "")
    ]
    if not branches:
        click.echo("Nothing to clean up.")
        return

    click.echo("Branches to delete:")
    for b in branches:
        click.echo(f"  {b}")

    if not yes and not click.confirm("Delete these branches?"):
        click.echo("Aborted.")
        return

    for b in branches:
        code, _, err = _run(["branch", "-d", b])
        if code == 0:
            click.secho(f"Deleted {b}", fg="green")
        else:
            click.secho(f"Could not delete {b}: {err}", fg="red")
