from pathlib import Path

import click

DEFAULT_IGNORE = {".git", "__pycache__", "node_modules", ".venv", "venv", ".mypy_cache", ".pytest_cache"}


def _tree(path: Path, prefix: str, max_depth: int, depth: int, ignore: set):
    if depth > max_depth:
        return
    entries = [e for e in sorted(path.iterdir(), key=lambda p: (p.is_file(), p.name.lower())) if e.name not in ignore]
    for i, entry in enumerate(entries):
        last = i == len(entries) - 1
        connector = "└── " if last else "├── "
        click.echo(f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}")
        if entry.is_dir():
            extension = "    " if last else "│   "
            _tree(entry, prefix + extension, max_depth, depth + 1, ignore)


@click.group()
def fs_group():
    """Filesystem utilities."""
    pass


@fs_group.command("tree")
@click.argument("path", default=".", type=click.Path(exists=True, file_okay=False))
@click.option("--depth", "-d", default=3, show_default=True, help="Max depth to descend.")
@click.option("--all", "show_all", is_flag=True, help="Also show common ignored dirs (.git, node_modules, etc).")
def tree(path, depth, show_all):
    """Print a directory tree starting at PATH (defaults to cwd)."""
    root = Path(path)
    click.secho(f"{root.resolve().name or root.resolve()}/", fg="cyan", bold=True)
    ignore = set() if show_all else DEFAULT_IGNORE
    _tree(root, "", depth, 1, ignore)
