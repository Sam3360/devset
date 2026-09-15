import click

from devset import __version__
from devset.commands.json_tools import json_group
from devset.commands.encode_tools import encode_group
from devset.commands.hash_tools import hash_group
from devset.commands.uuid_tools import uuid_group
from devset.commands.git_tools import git_group
from devset.commands.text_tools import text_group
from devset.commands.time_tools import time_group
from devset.commands.gen_tools import gen_group
from devset.commands.net_tools import net_group
from devset.commands.color_tools import color_group
from devset.commands.fs_tools import fs_group
from devset.commands.setup_tools import setup_group


@click.group()
@click.version_option(version=__version__, prog_name="devset")
def main():
    """devset - a Swiss-army-knife CLI with the everyday tools every dev needs.

    Run `devset COMMAND --help` for details on any tool group.
    """
    pass


main.add_command(json_group, name="json")
main.add_command(encode_group, name="b64")
main.add_command(hash_group, name="hash")
main.add_command(uuid_group, name="uuid")
main.add_command(git_group, name="git")
main.add_command(text_group, name="text")
main.add_command(time_group, name="time")
main.add_command(gen_group, name="gen")
main.add_command(net_group, name="net")
main.add_command(color_group, name="color")
main.add_command(fs_group, name="fs")
main.add_command(setup_group, name="setup")


if __name__ == "__main__":
    main()
