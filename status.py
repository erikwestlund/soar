from config import get_config
from project import get_existing_projects, get_project_config
import click
import yaml


def show_config():
    config = get_config()
    click.secho("Your current configuration:\n", fg="green", bold=True)
    click.secho(yaml.dump(config), fg="white")


def run_show_status(ctx):
    show_config()
    show_projects()


def show_projects():
    project_ids = get_existing_projects()

    click.secho("\nProjects discovered:\n", fg="green", bold=True)

    for project_id in project_ids:

        click.secho(f"\nProject ID: {project_id}\n", fg="blue", bold=True)

        project_config = get_project_config(project_id)

        if project_config is None:
            click.secho("This project is empty.", fg="white")
            continue

        click.secho(yaml.dump(project_config), fg="white")
