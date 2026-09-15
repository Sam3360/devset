import json
import sys

import click


def _read_input(source):
    """Read JSON text from a file path or stdin ('-' or omitted)."""
    if source is None or source == "-":
        return sys.stdin.read()
    with open(source, "r", encoding="utf-8") as f:
        return f.read()


@click.group()
def json_group():
    """Work with JSON: pretty-print, minify, validate."""
    pass


@json_group.command("pretty")
@click.argument("source", required=False, type=click.Path(allow_dash=True))
@click.option("--indent", default=2, show_default=True, help="Indent width.")
@click.option("--sort-keys", is_flag=True, help="Sort object keys.")
def pretty(source, indent, sort_keys):
    """Pretty-print JSON from FILE or stdin."""
    try:
        data = json.loads(_read_input(source))
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")
    click.echo(json.dumps(data, indent=indent, sort_keys=sort_keys))


@json_group.command("minify")
@click.argument("source", required=False, type=click.Path(allow_dash=True))
def minify(source):
    """Minify JSON from FILE or stdin (removes all insignificant whitespace)."""
    try:
        data = json.loads(_read_input(source))
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")
    click.echo(json.dumps(data, separators=(",", ":")))


@json_group.command("validate")
@click.argument("source", required=False, type=click.Path(allow_dash=True))
def validate(source):
    """Validate JSON from FILE or stdin. Exits non-zero if invalid."""
    try:
        json.loads(_read_input(source))
    except json.JSONDecodeError as e:
        click.secho(f"Invalid JSON: {e}", fg="red")
        sys.exit(1)
    click.secho("Valid JSON", fg="green")


@json_group.command("path")
@click.argument("keypath")
@click.argument("source", required=False, type=click.Path(allow_dash=True))
def path_cmd(keypath, source):
    """Extract a value using dotted KEYPATH (e.g. 'a.b.0.c') from FILE or stdin."""
    try:
        data = json.loads(_read_input(source))
    except json.JSONDecodeError as e:
        raise click.ClickException(f"Invalid JSON: {e}")

    current = data
    for part in keypath.split("."):
        if isinstance(current, list):
            try:
                current = current[int(part)]
            except (ValueError, IndexError):
                raise click.ClickException(f"Bad list index: {part}")
        elif isinstance(current, dict):
            if part not in current:
                raise click.ClickException(f"Key not found: {part}")
            current = current[part]
        else:
            raise click.ClickException(f"Cannot descend into {type(current).__name__} with '{part}'")

    if isinstance(current, (dict, list)):
        click.echo(json.dumps(current, indent=2))
    else:
        click.echo(current)
