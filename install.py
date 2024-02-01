import os

import click

from config import get_resources_path


def run_install_r_data_science_tools(ctx):
    """Install data science tools, including the Tidyverse."""
    click.secho("🔧 Installing R Data Science tools...", fg="green", bold=True)
    click.secho("This may take a while.", fg="green")

    script = get_resources_path() + "/install/r-data-science.sh"
    os.system("sh " + script)

    click.secho("✅ Done.", fg="green")


def run_install_r_ohdsi_tools(ctx):
    """Install OHDSI tools."""
    click.secho("🔧 Installing OHDSI tools...", fg="green", bold=True)
    click.secho("This may take a while.", fg="green")

    script = get_resources_path() + "/install/r-data-science.sh"
    os.system("sh " + script)

    click.secho("✅ Done.", fg="green")
