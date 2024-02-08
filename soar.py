import click
from config import (
    get_is_configured,
    run_link_config,
    run_refresh_config,
    run_reset_keyring,
    run_select_options,
    run_set_config,
    configure_keyring_password,
    configure_jhed_credentials,
)

from enhance import (
    run_enhance_shell,
    run_install_rstudio_keybindings,
    run_install_aliases,
)
from install import (
    run_install_r_data_science_tools,
    run_install_r_data_analysis_tools,
    run_install_r_ohdsi_tools,
)
from logo import print_logo
from make import make_kerberos_auth
from mount import run_mount_home, run_mount_safe
from project import run_configure_project
from status import get_status


if __name__ == "__main__":
    print_logo()
    if not get_is_configured():
        click.secho("Welcome to Crunchr!", fg="blue", bold=True)
        click.secho(
            "Let's get started by configuring your security credentials.\n", fg="green"
        )
        configure_keyring_password()
        configure_jhed_credentials()

        click.secho("🎉 Initial configuration complete.", fg="blue", bold=True)
        click.secho(
            "Type `soar configure` to further configure your profile.",
            fg="blue",
            bold=True,
        )
        click.secho("Type `soar` to see what else you can do.", fg="blue", bold=True)

        exit(1)


@click.group()
@click.pass_context
def main(ctx):
    """Tooling to make CrunchR soar."""


@main.command()
@click.argument("setting", required=False)
@click.pass_context
def configure(ctx, setting=None):
    """
    Configure your CrunchR container.

    Setting options:\n
     - jhed: Set your JHED credentials.\n
     - github: Set your GitHub credentials.\n
     - ggplot: Set your ggplot2 settings.\n
     - keyring: Set your keyring password.
    """

    run_select_options(ctx, setting)


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
    """R data science tools: Tidyverse, database utilities, etc."""
    run_install_r_data_science_tools(ctx)


@install.command("r-data-analysis")
@click.pass_context
def install_r_data_science(ctx):
    """R data analysis tools: multilevel modeling,  Bayesian analysis, etc."""
    run_install_r_data_analysis_tools(ctx)


@install.command("r-ohdsi")
@click.pass_context
def install_r_ohdsi_tools(ctx):
    """R OHDSI tools."""
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
    run_link_config()


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
    """Make files using templates (e.g., database config files)."""


@make.command("kerberos-auth")
@click.pass_context
def enhance_shell(ctx):
    """Create a kerberos auth template."""
    make_kerberos_auth(ctx)


@main.group()
@click.pass_context
def project(ctx):
    """Project tools (e.g., configuring database credentials)."""


@project.command("configure")
@click.argument("project_id", required=False)
@click.pass_context
def configure_project(ctx, project_id):
    """Configure your project."""

    run_configure_project(ctx, project_id)


if __name__ == "__main__":
    main(obj={})
