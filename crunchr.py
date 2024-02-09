import click
import os
from config import get_home_directory


def confirm_crunchr_environment():
    if not os.path.exists(get_home_directory()):
        click.secho(
            "This command must be run from a Crunchr container.", fg="red", bold=True
        )
        exit(1)
