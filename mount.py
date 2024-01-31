import click
from configure import get_config

def run_mount_home(ctx):
    config = get_config()

    if not config["default"]["jhed_username"]:
        click.secho("JHED username not set. Run configure before proceeding.", fg="red", bold=True)


    click.echo("Implement the mount_home function here!")
