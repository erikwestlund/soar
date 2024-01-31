import click
from configure import set_config
from enhance import run_enhance_shell, run_install_rstudio_keybindings, run_install_aliases
from mount import run_mount_home
from status import get_status


@click.group()
@click.pass_context
def main(ctx):
    """Tooling to make CrunchR soar."""


@main.command()
@click.pass_context
@click.option(
    "--update",
    "-u",
    is_flag=True,
    show_default=True,
    help="Update all configuration items. Default is to update only empty values.",
)
def configure(ctx, update):
    """Configure your CrunchR container."""
    set_config(ctx, update)


@main.command()
@click.pass_context
def status(ctx):
    """Get the status of your CrunchR container."""
    get_status(ctx)


@main.group()
@click.pass_context
def mount(ctx):
    """Mount network volumes on your container."""


@mount.command("home")
@click.pass_context
def mount_home(ctx):
    """Mount your home directory to your container."""
    run_mount_home(ctx)


@mount.command("safe")
@click.pass_context
def mount_home(ctx):
    """Mount a SAFE directory to your container."""
    # run_mount_home(ctx)


@main.group()
@click.pass_context
def enhance(ctx):
    """Enhance your CrunchR container."""


@enhance.command("shell")
@click.pass_context
def enhance_shell(ctx):
    """Enhance your CrunchR shell."""
    run_enhance_shell(ctx)


@enhance.command("aliases")
@click.pass_context
def enhance_aliases(ctx):
    """Install useful shell aliases."""
    run_install_aliases(ctx)


@enhance.command("rstudio_keybindings")
@click.pass_context
def https_sync(ctx):
    """Install enhanced RStudio keybindings."""
    run_install_rstudio_keybindings(ctx)


if __name__ == "__main__":
    main(obj={})
