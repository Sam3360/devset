from datetime import datetime, timezone

import click


@click.group()
def time_group():
    """Timestamp conversion utilities."""
    pass


@time_group.command("now")
@click.option("--utc", is_flag=True, help="Show UTC instead of local time.")
def now(utc):
    """Print the current time as unix timestamp and ISO 8601."""
    dt = datetime.now(timezone.utc) if utc else datetime.now()
    click.echo(f"unix:  {int(dt.timestamp())}")
    click.echo(f"iso:   {dt.isoformat()}")


@time_group.command("from-unix")
@click.argument("timestamp", type=float)
@click.option("--utc", is_flag=True, help="Show UTC instead of local time.")
def from_unix(timestamp, utc):
    """Convert a unix TIMESTAMP to a readable date."""
    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc if utc else None)
    click.echo(dt.isoformat())


@time_group.command("to-unix")
@click.argument("iso_string")
def to_unix(iso_string):
    """Convert an ISO 8601 date string to a unix timestamp."""
    try:
        dt = datetime.fromisoformat(iso_string)
    except ValueError as e:
        raise click.ClickException(f"Could not parse date: {e}")
    click.echo(int(dt.timestamp()))
