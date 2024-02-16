import click

from install import run_install_r_ohdsi_tools
from project import run_configure_existing_project


def run_select_ohdsi_options(ctx, option):
    if option:
        if option == "project":
            choice = "1"
        elif option == "existing":
            choice = "2"
        elif option == "install":
            choice = "3"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    else:
        click.secho("🏹  OHDSI Tools\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Configure a new OHDSI project", fg="white")
        click.secho("(2) Configure an existing OHDSI project", fg="white")
        click.secho("(3) Install OHDSI Tools & R Packages", fg="white")
        click.secho("(4) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4"])
        )

    if choice == "1":
        run_configure_existing_project(project_type="ohdsi")
    elif choice == "2":
        run_configure_existing_project(project_type="ohdsi")
    elif choice == "3":
        run_install_r_ohdsi_tools()
    elif choice == "4":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)
    else:
        exit(0)
