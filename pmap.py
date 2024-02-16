import click

from make import generate_dbi_for_pmap_project
from project import run_configure_existing_project, run_configure_pmap_project


def run_select_pmap_options(ctx, option):
    if option:
        if option == "project":
            choice = "1"
        elif option == "existing":
            choice = "2"
        elif option == "dbi-connect":
            choice = "3"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    else:
        click.secho("🧬  PMAP Tools\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Configure a new PMAP project", fg="white")
        click.secho("(2) Configure an existing PMAP project", fg="white")
        click.secho("(3) Create a DBI connection file for an existing PMAP project", fg="white")
        click.secho("(4) Cancel\n", fg="white")
        choice = click.prompt("Enter your choice", type=click.Choice(["1", "2", "3", "4"]))

    if choice == "1":
        run_configure_pmap_project()
    elif choice == "2":
        run_configure_existing_project(project_type="pmap")
    elif choice == "3":
        generate_dbi_for_pmap_project()
    elif choice == "4":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)
    else:
        exit(0)
