import project
import click


def db_port(default="1433"):
    return click.prompt(
        "Enter the database port",
        type=int,
        default=default,
        show_default=bool(default),
    )


def db_server(default=""):
    return click.prompt(
        "Enter the database server (e.g., dbserver.jhu.edu)",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def existing_project(project_type=None):
    existing_projects = project.get_existing_projects(project_type=project_type)

    click.secho(
        f"The following {project.get_project_type_label(project_type)} projects were found:"
        if project_type
        else "The following projects were found:",
        fg="blue",
        bold=True,
    )

    for i, project_id in enumerate(existing_projects):
        click.secho(f"({i + 1}) {project_id}", fg="white")

    project_id_index = click.prompt(
        "\nSelect a project",
        type=click.Choice([str(i + 1) for i in range(len(existing_projects))]),
        show_choices=False,
    )

    try:
        project_id = existing_projects[int(project_id_index) - 1]
    except:
        click.secho(
            f"Invalid project ID.",
            fg="red",
            bold=True,
        )
        exit(1)

    return project_id


def free_tds_version(default="8.0"):
    return click.prompt(
        "Enter the FreeTDS version",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def irb_number(default=""):
    return click.prompt(
        "Enter the IRB number",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def odbc_db_driver(default="FreeTDS"):
    return click.prompt(
        "Enter the ODBC database driver",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def omop_projection_db_name(default=""):
    return click.prompt(
        "Enter the OMOP projection database name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def driver_version(default=""):
    return click.prompt(
        "Enter the ODBC driver version",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def omop_scratch_db_name(default=""):
    return click.prompt(
        "Enter the OMOP scratch database name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def project_id():
    valid = False
    while not valid:
        project_id = click.prompt(
            "Enter a project ID. It should be an alphanumeric string without spaces (e.g., 'project_name')",
            type=str,
        ).strip()

        if not project_id.replace("_", "").isalnum():
            click.secho(
                "The project ID should be an alphanumeric string without spaces.",
                fg="red",
                bold=True,
            )

            valid = False

        elif project_exists(project_id):
            click.secho(
                f"The project ID `{project_id}` already exists.",
                fg="red",
                bold=True,
            )

            valid = click.confirm("Do you want to configure the existing project?")

            if valid:
                return {
                    "already_exists": True,
                    "value": project_id,
                }

        else:
            return {
                "already_exists": False,
                "value": project_id,
            }


def project_name(default=""):
    return click.prompt(
        "Enter the name of the project",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def projection_db_name(default=""):
    return click.prompt(
        "Enter the projection database name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def safe_folder_name(default=""):
    return click.prompt(
        "Enter the SAFE folder name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def scratch_db_name(default=""):
    return click.prompt(
        "Enter the scratch database name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()


def scratch_db_schema_name(default=""):
    return click.prompt(
        "Enter the scratch database schema name",
        type=str,
        default=default,
        show_default=bool(default),
    ).strip()
