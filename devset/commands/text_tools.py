import re
import sys

import click


def _read(text):
    if text is not None:
        return text
    return sys.stdin.read().rstrip("\n")


@click.group()
def text_group():
    """Text case conversion, slugify, and regex testing."""
    pass


@text_group.command("slug")
@click.argument("text", required=False)
def slug(text):
    """Convert TEXT (or stdin) into a URL-friendly slug."""
    data = _read(text).lower().strip()
    data = re.sub(r"[^a-z0-9]+", "-", data).strip("-")
    click.echo(data)


@text_group.command("case")
@click.argument("style", type=click.Choice(["upper", "lower", "snake", "kebab", "camel", "pascal", "title"]))
@click.argument("text", required=False)
def case(style, text):
    """Convert TEXT (or stdin) to STYLE case."""
    data = _read(text)
    words = re.split(r"[\s_\-]+|(?<=[a-z0-9])(?=[A-Z])", data)
    words = [w for w in words if w]

    if style == "upper":
        result = data.upper()
    elif style == "lower":
        result = data.lower()
    elif style == "snake":
        result = "_".join(w.lower() for w in words)
    elif style == "kebab":
        result = "-".join(w.lower() for w in words)
    elif style == "camel":
        result = words[0].lower() + "".join(w.capitalize() for w in words[1:]) if words else ""
    elif style == "pascal":
        result = "".join(w.capitalize() for w in words)
    elif style == "title":
        result = " ".join(w.capitalize() for w in words)
    click.echo(result)


@text_group.command("regex")
@click.argument("pattern")
@click.argument("text", required=False)
@click.option("--flags", default="", help="Regex flags: i (ignorecase), m (multiline), s (dotall).")
def regex(pattern, text, flags):
    """Test PATTERN against TEXT (or stdin) and print all matches."""
    data = _read(text)
    py_flags = 0
    if "i" in flags:
        py_flags |= re.IGNORECASE
    if "m" in flags:
        py_flags |= re.MULTILINE
    if "s" in flags:
        py_flags |= re.DOTALL

    try:
        matches = list(re.finditer(pattern, data, py_flags))
    except re.error as e:
        raise click.ClickException(f"Bad regex: {e}")

    if not matches:
        click.secho("No matches.", fg="yellow")
        return

    for i, m in enumerate(matches, 1):
        click.echo(f"{i}: {m.group(0)!r}  (span {m.span()})")
        if m.groups():
            for gi, g in enumerate(m.groups(), 1):
                click.echo(f"     group {gi}: {g!r}")


@text_group.command("count")
@click.argument("text", required=False)
def count(text):
    """Count characters, words, and lines in TEXT (or stdin)."""
    data = _read(text)
    click.echo(f"chars: {len(data)}")
    click.echo(f"words: {len(data.split())}")
    click.echo(f"lines: {len(data.splitlines()) or (1 if data else 0)}")
