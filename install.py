import os

import click

from config import get_resources_path
from crunchr import confirm_crunchr_environment


def run_install_r_data_science_tools():
    """Install data science tools, including the Tidyverse."""
    click.secho("🔧 Installing R Data Science Tools...", fg="green", bold=True)
    click.secho("This may take a while.", fg="green")

    script = get_resources_path() + "/install/r-data-science.sh"
    os.system("/bin/sh " + script)

    click.secho("✅ Done.", fg="green")


def run_install_r_data_analysis_tools():
    """Install data science tools, including the Tidyverse."""
    click.secho("🔧 Installing R Data Analysis Tools...", fg="green", bold=True)
    click.secho("This may take a while.", fg="green")

    script = get_resources_path() + "/install/r-data-analysis.sh"
    os.system("/bin/sh " + script)

    click.secho("✅ Done.", fg="green")


def run_install_r_ohdsi_tools():
    """Install OHDSI tools."""
    click.secho("🔧 Installing OHDSI Tools...", fg="green", bold=True)
    click.secho("This may take a while.", fg="green")

    script = get_resources_path() + "/install/r-ohdsi.sh"
    os.system("/bin/sh " + script)

    click.secho("✅ Done.", fg="green")


def run_select_install_options(ctx, option=None):
    if option:
        if option == "r-data-tools":
            choice = "1"
        elif option == "r-data-analysis":
            choice = "2"
        elif option == "r-data-suite":
            choice = "4"
        elif option == "r-ohdsi":
            choice = "3"
        elif option == "all":
            choice = "5"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    if not option:
        click.secho("🛠️ Install Software & Packages.\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho(
            "(1) R data tools (e.g., Tidyverse, database connectors)", fg="white"
        )
        click.secho(
            "(2) R data analysis packages (e.g., multilevel modeling, Bayesian analysis tools including Stan, multiple imputation)",
            fg="white",
        )
        click.secho("(3) OHDSI tools", fg="white")
        click.secho("(4) Both 1 & 2", fg="white")
        click.secho("(5) All (1-3)", fg="white")
        click.secho("(6) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4"])
        )

    if choice == "6":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)

    confirm_crunchr_environment()

    if choice == "1":
        run_install_r_data_science_tools()
    elif choice == "2":
        run_install_r_data_analysis_tools()
    elif choice == "3":
        run_install_r_ohdsi_tools()
    elif choice == "4":
        run_install_r_data_science_tools()
        run_install_r_data_analysis_tools()
    elif choice == "5":
        run_install_r_data_science_tools()
        run_install_r_data_analysis_tools()
        run_install_r_ohdsi_tools()
    else:
        click.secho("Invalid option.", fg="red", bold=True)
        exit(1)
