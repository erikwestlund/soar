import click
from config import run_copy_config, run_refresh_config, run_reset_keyring, run_set_config
from enhance import (
    run_enhance_shell,
    run_install_rstudio_keybindings,
    run_install_aliases,
)
from install import run_install_r_data_science_tools, run_install_r_ohdsi_tools
from make import make_kerberos_auth
from mount import run_mount_home, run_mount_safe
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
@click.option(
    "--refresh",
    "-r",
    is_flag=True,
    show_default=True,
    help="Refresh config to ensure it has all default values.",
)
def configure(ctx, update, refresh=False):
    """Configure your CrunchR container."""
    if(refresh):
        run_refresh_config(ctx)
    else:
        run_set_config(ctx, update)


@main.command()
@click.pass_context
def status(ctx):
    """Get the status of your CrunchR container."""
    get_status(ctx)


@main.command()
@click.pass_context
def reset_keyring(ctx):
    """Reset your keyring."""
    run_reset_keyring(ctx)


@main.group()
@click.pass_context
def install(ctx):
    """Install useful packages and software."""


@install.command("r-data-science")
@click.pass_context
def install_r_data_science(ctx):
    """Install R Data Science tools such as the Tidyverse and connection utilities."""
    run_install_r_data_science_tools(ctx)


@install.command("r-ohdsi")
@click.pass_context
def install_r_ohdsi_tools(ctx):
    """Install R OHDSI tools."""
    run_install_r_ohdsi_tools(ctx)


@main.group()
@click.pass_context
def mount(ctx):
    """Mount network volumes on your container."""


@main.group()
@click.pass_context
def copy(ctx):
    """Copy files to useful locations."""


@copy.command("config")
@click.pass_context
def copy_config(ctx):
    """Copies your config.yml to your home directory."""
    run_copy_config()


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
    run_mount_safe(ctx)


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


@enhance.command("rstudio-keybindings")
@click.pass_context
def https_sync(ctx):
    """Install enhanced RStudio keybindings."""
    run_install_rstudio_keybindings(ctx)


@main.group()
@click.pass_context
def make(ctx):
    """Make files using templates for various tasks, such as authorization to databases."""


@make.command("kerberos-auth")
@click.pass_context
def enhance_shell(ctx):
    """Create a kerberos auth template."""
    make_kerberos_auth(ctx)


if __name__ == "__main__":
    main(obj={})
