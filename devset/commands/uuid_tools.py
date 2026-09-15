import uuid

import click


@click.group()
def uuid_group():
    """Generate UUIDs."""
    pass


@uuid_group.command("gen")
@click.option("-n", "--count", default=1, show_default=True, help="How many to generate.")
@click.option("--version", "ver", type=click.Choice(["1", "4"]), default="4", show_default=True, help="UUID version.")
@click.option("--upper", is_flag=True, help="Output uppercase.")
@click.option("--no-dashes", is_flag=True, help="Strip dashes from output.")
def gen(count, ver, upper, no_dashes):
    """Generate one or more UUIDs."""
    for _ in range(count):
        value = str(uuid.uuid1()) if ver == "1" else str(uuid.uuid4())
        if no_dashes:
            value = value.replace("-", "")
        if upper:
            value = value.upper()
        click.echo(value)
