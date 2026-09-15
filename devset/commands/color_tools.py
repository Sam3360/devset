import click


@click.group()
def color_group():
    """Color format conversions (hex <-> rgb)."""
    pass


@color_group.command("hex2rgb")
@click.argument("hex_value")
def hex2rgb(hex_value):
    """Convert a HEX color (e.g. #ff8800) to RGB."""
    h = hex_value.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        raise click.ClickException("Expected a 3 or 6 digit hex color.")
    try:
        r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    except ValueError:
        raise click.ClickException("Invalid hex digits.")
    click.echo(f"rgb({r}, {g}, {b})")


@color_group.command("rgb2hex")
@click.argument("r", type=int)
@click.argument("g", type=int)
@click.argument("b", type=int)
def rgb2hex(r, g, b):
    """Convert R G B (0-255 each) to a HEX color."""
    for name, val in (("r", r), ("g", g), ("b", b)):
        if not 0 <= val <= 255:
            raise click.ClickException(f"{name}={val} out of range 0-255.")
    click.echo(f"#{r:02x}{g:02x}{b:02x}")
