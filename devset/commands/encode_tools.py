import base64
import sys
import urllib.parse

import click


def _read_text(text, source):
    if text is not None:
        return text
    if source is None or source == "-":
        return sys.stdin.read().rstrip("\n")
    with open(source, "r", encoding="utf-8") as f:
        return f.read().rstrip("\n")


@click.group()
def encode_group():
    """Encode/decode base64 and URL-encoded strings."""
    pass


@encode_group.command("encode")
@click.argument("text", required=False)
@click.option("--file", "source", type=click.Path(allow_dash=True), help="Read input from a file (or - for stdin).")
def b64_encode(text, source):
    """Base64-encode TEXT (or stdin/--file)."""
    data = _read_text(text, source)
    click.echo(base64.b64encode(data.encode("utf-8")).decode("ascii"))


@encode_group.command("decode")
@click.argument("text", required=False)
@click.option("--file", "source", type=click.Path(allow_dash=True), help="Read input from a file (or - for stdin).")
def b64_decode(text, source):
    """Base64-decode TEXT (or stdin/--file)."""
    data = _read_text(text, source)
    try:
        click.echo(base64.b64decode(data).decode("utf-8"))
    except Exception as e:
        raise click.ClickException(f"Could not decode: {e}")


@encode_group.command("urlencode")
@click.argument("text", required=False)
def url_encode(text):
    """URL-encode TEXT (or stdin)."""
    data = _read_text(text, None)
    click.echo(urllib.parse.quote(data))


@encode_group.command("urldecode")
@click.argument("text", required=False)
def url_decode(text):
    """URL-decode TEXT (or stdin)."""
    data = _read_text(text, None)
    click.echo(urllib.parse.unquote(data))
