import hashlib
import sys

import click

ALGOS = ["md5", "sha1", "sha256", "sha512"]


def _read_bytes(text, source):
    if text is not None:
        return text.encode("utf-8")
    if source is None or source == "-":
        return sys.stdin.buffer.read()
    with open(source, "rb") as f:
        return f.read()


@click.group()
def hash_group():
    """Compute hashes (md5, sha1, sha256, sha512) of text or files."""
    pass


def _make_hash_command(algo):
    @click.command(algo)
    @click.argument("text", required=False)
    @click.option("--file", "source", type=click.Path(allow_dash=True), help="Hash a file's contents instead.")
    def cmd(text, source):
        f"""Compute {algo} of TEXT (or stdin/--file)."""
        data = _read_bytes(text, source)
        digest = hashlib.new(algo, data).hexdigest()
        click.echo(digest)
    return cmd


for _algo in ALGOS:
    hash_group.add_command(_make_hash_command(_algo))


@hash_group.command("all")
@click.argument("text", required=False)
@click.option("--file", "source", type=click.Path(allow_dash=True), help="Hash a file's contents instead.")
def hash_all(text, source):
    """Compute every supported hash of TEXT (or stdin/--file) at once."""
    data = _read_bytes(text, source)
    for algo in ALGOS:
        digest = hashlib.new(algo, data).hexdigest()
        click.echo(f"{algo:8s} {digest}")
