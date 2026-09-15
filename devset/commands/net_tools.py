import socket
import time

import click


@click.group()
def net_group():
    """Small network utilities: port checks, basic HTTP requests."""
    pass


@net_group.command("port")
@click.argument("host")
@click.argument("port", type=int)
@click.option("--timeout", default=3.0, show_default=True, help="Timeout in seconds.")
def check_port(host, port, timeout):
    """Check whether HOST:PORT is open (TCP connect test)."""
    start = time.time()
    try:
        with socket.create_connection((host, port), timeout=timeout):
            elapsed = (time.time() - start) * 1000
            click.secho(f"{host}:{port} is OPEN ({elapsed:.0f}ms)", fg="green")
    except (socket.timeout, ConnectionRefusedError, OSError) as e:
        click.secho(f"{host}:{port} is CLOSED/unreachable ({e})", fg="red")


@net_group.command("get")
@click.argument("url")
@click.option("--headers", is_flag=True, help="Show response headers.")
def http_get(url, headers):
    """Make a simple GET request and print status + body."""
    import requests

    resp = requests.get(url, timeout=10)
    click.secho(f"{resp.status_code} {resp.reason}", fg="green" if resp.ok else "red")
    if headers:
        for k, v in resp.headers.items():
            click.echo(f"  {k}: {v}")
    click.echo()
    click.echo(resp.text[:5000])
