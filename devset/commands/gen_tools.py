import secrets
import string

import click

LOREM_WORDS = (
    "lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod "
    "tempor incididunt ut labore et dolore magna aliqua ut enim ad minim "
    "veniam quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea "
    "commodo consequat duis aute irure dolor in reprehenderit voluptate "
    "velit esse cillum dolore eu fugiat nulla pariatur"
).split()


@click.group()
def gen_group():
    """Generators: passwords, lorem ipsum text."""
    pass


@gen_group.command("password")
@click.option("--length", "-l", default=16, show_default=True)
@click.option("--no-symbols", is_flag=True, help="Exclude symbols.")
@click.option("--no-digits", is_flag=True, help="Exclude digits.")
@click.option("-n", "--count", default=1, show_default=True, help="How many to generate.")
def password(length, no_symbols, no_digits, count):
    """Generate a cryptographically secure random password."""
    alphabet = string.ascii_letters
    if not no_digits:
        alphabet += string.digits
    if not no_symbols:
        alphabet += "!@#$%^&*()-_=+"

    for _ in range(count):
        click.echo("".join(secrets.choice(alphabet) for _ in range(length)))


@gen_group.command("lorem")
@click.option("--words", "-w", default=50, show_default=True, help="Number of words.")
@click.option("--paragraphs", "-p", default=1, show_default=True, help="Number of paragraphs.")
def lorem(words, paragraphs):
    """Generate lorem ipsum placeholder text."""
    import random

    for p in range(paragraphs):
        chosen = [random.choice(LOREM_WORDS) for _ in range(words)]
        chosen[0] = chosen[0].capitalize()
        sentence = " ".join(chosen) + "."
        click.echo(sentence)
        if p < paragraphs - 1:
            click.echo()
