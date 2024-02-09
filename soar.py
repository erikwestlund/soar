import click
import os

from config import (
    configure_github_settings,
    configure_jhed_credentials,
    configure_keyring_password,
    get_home_directory,
    get_is_configured,
    run_link_config,
    run_reset_keyring,
    run_select_config_options,
)
from enhance import (
    run_select_enhance_options,
)
from install import run_select_install_options
from logo import print_logo
from make import make_kerberos_auth
from mount import run_select_mount_options
from project import run_select_project_options
from status import run_show_status

if __name__ == "__main__":
    print_logo()
    if not get_is_configured():
        click.secho("Welcome to Crunchr!", fg="blue", bold=True)
        click.secho(
            "Let's get started by configuring your security credentials\n", fg="green"
        )
        configure_keyring_password()
        configure_jhed_credentials()

        click.secho("🎉 Initial configuration complete.", fg="blue", bold=True)

        if click.confirm(
            "Would you like to configure your GitHub credentials?", default=True
        ):
            configure_github_settings()
        else:
            click.secho(
                "Type `soar configure` to further configure your profile.", fg="blue"
            )

        click.secho("Type `soar` to see what else you can do.", fg="blue")

        exit(1)


@click.group()
@click.pass_context
def main(ctx):
    """Tooling to make Crunchr soar."""


@main.command()
@click.argument("option", required=False)
@click.pass_context
def configure(ctx, option=None):
    """
    Configure your Crunchr container

    Options:\n
     - jhed: Set your JHED credentials\n
     - github: Set your GitHub credentials\n
     - keyring: Set your keyring password
    """

    run_select_config_options(ctx, setting)


@main.command()
@click.pass_context
def reset_keyring(ctx):
    """Reset your keyring"""
    run_reset_keyring(ctx)


@main.command()
@click.argument("option", required=False)
@click.pass_context
def install(ctx, option=None):
    """
    Install useful packages and software

    Options:\n
     - r-data-tools: R data tools (e.g., Tidyverse, database connectors)\n
     - r-data-analysis: R data analysis packages (e.g., MLM, Bayes, MICE)\n
     - r-ohdsi: R OHDSI packages\n
     - r-data-suite: R tools and analysis packages\n
     - all: Install all\n
    """

    run_select_install_options(ctx, option)


@main.command()
@click.pass_context
def link_config(ctx):
    """Relink your configuration files"""
    run_link_config()
    click.secho("✅ Config relinked.", fg="green")


@main.command()
@click.argument("option", required=False)
@click.pass_context
def mount(ctx, option=None):
    """
    Mount network volumes on your container

    Mount options:\n
     - home: Mount your home directory to your container\n
     - safe: Mount a SAFE directory to your container\n
    """

    run_select_mount_options(ctx, option)


@main.command()
@click.argument("option", required=False)
@click.pass_context
def enhance(ctx, option=None):
    """
    Enhance your Crunchr container

    Options:\n
     - aliases: Install enhanced aliases only\n
     - rstudio-keybindings: Install enhanced keybindings\n
     - shell: Enhance your shell with Zsh and aliases\n
    """

    run_select_enhance_options(ctx, option)


@main.group()
@click.pass_context
def make(ctx):
    """Make files using templates (e.g., database config files)"""


@make.command("kerberos-auth")
@click.pass_context
def enhance_shell(ctx):
    """Create a kerberos auth template"""
    make_kerberos_auth(ctx)


@main.command()
@click.argument("option", required=False)
@click.pass_context
def project(ctx, option=None):
    """
    Project tools

    Options:\n
     - generic: Configure a generic project\n
     - pmap: Configure a PMAP project\n
     - existing: Configure an existing project\n
    """
    run_select_project_options(ctx, option)


@main.command()
@click.pass_context
def status(ctx):
    """Show details about your configuration and projects"""
    run_show_status(ctx)


if __name__ == "__main__":
    main(obj={})
