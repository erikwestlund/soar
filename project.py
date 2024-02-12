from config import (
    run_link_config,
    get_config,
    get_config_location,
    get_is_configured,
    get_soar_dir,
    get_workspace_dir,
)
from crunchr import confirm_crunchr_environment
import click
import yaml
import os


def check_project_exists(project_id):
    # Check if project.project_id.yml exists in projects folder
    return os.path.exists(f"projects/config.{project_id}.yml")


def configure_existing_project(project_id, project_type):
    configure_project(
        project_id=project_id, project_type=project_type, existing_project=True
    )


def configure_project(project_id, project_type=None, existing_project=False):
    # Construct basic project configuration
    if existing_project and not project_exists(project_id):
        click.secho(
            f"The project ID `{project_id}` does not exist. Please create it first.",
            fg="red",
            bold=True,
        )
        exit(1)
    elif existing_project and project_type and get_project_config(project_id).get(project_id).get(
            "type") != project_type:
        click.secho(
            f"The project ID `{project_id}` is not of type `{get_project_type_label(project_type)}`.",
            fg="red",
            bold=True,
        )
        exit(1)
    elif existing_project:
        retreived_project_config = get_project_config(project_id) or {}
        retreived_config = retreived_project_config.get(project_id, {})

        settings = retreived_config.get("settings", {})

        try:
            project_type = (
                retreived_config["type"]
                if retreived_config["type"] in get_valid_project_types()
                else "generic"
            )
        except:
            project_type = "generic"
    else:
        settings = {}
        project_type = (
            project_type if project_type in get_valid_project_types() else "generic"
        )

    if existing_project:
        click.secho(
            "\nDefault values can be accepted by hitting enter when they are shown in brackets.",
            fg="yellow",
            bold=True,
        )

    click.secho(
        "\nIf you do not know a value for a prompt, you can leave it blank and enter it later.\n",
        fg="yellow",
        bold=True,
    )

    settings = update_generic_project_settings(settings)

    if project_type == "pmap":
        settings = update_pmap_project_settings(settings)
    elif project_type == "ohdsi":
        settings = update_ohdsi_project_settings(settings)

    fully_structured_config = {
        project_id: {
            "type": project_type,
            "settings": settings,
        }
    }

    with open(f"projects/config.{project_id}.yml", "w") as file:
        yaml.dump(fully_structured_config, file)

    click.secho("\n✅  Project configured.\n", fg="green", bold=True)

    click.secho("Project config file saved to:", fg="yellow", bold=True)
    click.secho(f"{get_soar_dir()}/projects/config.{project_id}.yml\n", fg="white")
    copy_project_file(project_id)

    click.secho(
        "⚠️  This file should be copied to your project and placed in version control.\n",
        fg="white",
        bold=True,
    )
    click.secho(
        "To maintain different versions of configuration for a project, it is recommended \n"
        "to use either A) different branches in a version control system or B) maintaining \n"
        "separate config files and loading them as appropriate.\n",
        fg="white",
    )

    click.secho("Config output:\n", fg="yellow", bold=True)
    click.secho(yaml.dump(fully_structured_config, default_flow_style=False))


def copy_project_file(project_id):
    # confirm_crunchr_environment()

    soar_path = get_soar_project_config_path(project_id)
    workspace_path = f"{get_workspace_dir()}/config.{project_id}.yml"
    # os.system(f"cp {soar_path} {workspace_path}")

    click.secho(f"Project config file copied to:", fg="yellow", bold=True)
    click.secho(f"{workspace_path}\n", fg="white")


def get_existing_projects(project_type=None, update=False):
    # filter starts with config. and ends with .yml
    existing_projects = [
        x.split(".")[1]
        for x in os.listdir("projects")
        if x.startswith("config.") and x.endswith(".yml")
    ]

    if project_type:
        existing_projects = [
            x
            for x in existing_projects
            if get_project_config(x).get(x, {}).get("type", "") == project_type
        ]

    if update and project_type and not existing_projects:
        label = get_project_type_label(project_type)

        click.secho(
            f"No {label} projects have been configured. Please configure a new project.",
            fg="red",
            bold=True,
        )
        exit(1)

    return existing_projects


def get_project_config(project_id):
    # Load the project.project_id.yml file
    with open(f"projects/config.{project_id}.yml", "r") as file:
        loaded_yaml = yaml.safe_load(file)

        if loaded_yaml is None:
            return None
        else:
            return loaded_yaml


def get_soar_project_config_path(project_id):
    return f"{get_soar_dir()}/projects/config.{project_id}.yml"


def get_valid_project_types():
    return ["generic", "pmap", "ohdsi"]


def project_exists(project_id):
    return project_id in get_existing_projects()


def prompt_project_id():
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


def run_configure_existing_project(project_id=None, project_type=None):
    existing_projects = get_existing_projects(project_type, update=True)

    if project_id and not project_exists(project_id):
        click.secho(
            f"The project ID `{project_id}` does not exist. Please create it first.",
            fg="red",
            bold=True,
        )
        exit(1)

    if not existing_projects:
        click.secho(
            "No projects have been configured. Please create a new project.",
            fg="red",
            bold=True,
        )
        exit(1)

    if not project_id:
        click.secho(
            f"The following {get_project_type_label(project_type)} projects were found:"
            if project_type
            else "The following projects were found:",
            fg="green",
            bold=True,
        )

        for i, project_id in enumerate(existing_projects):
            click.secho(f"({i + 1}) {project_id}", fg="white")

        project_id_index = click.prompt(
            "Enter the project you would like to configure",
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

    configure_project(project_id=project_id, existing_project=True)


def get_project_type_label(project_type):
    if project_type == "generic":
        return "Generic"
    elif project_type == "pmap":
        return "PMAP"
    elif project_type == "ohdsi":
        return "OHDSI"
    else:
        return project_type


def run_configure_generic_project():
    project_id_data = prompt_project_id()
    configure_project(
        project_id=project_id_data["value"],
        project_type="generic",
        existing_project=project_id_data["already_exists"],
    )


def run_configure_pmap_project():
    project_id_data = prompt_project_id()
    configure_project(
        project_id=project_id_data["value"],
        project_type="pmap",
        existing_project=project_id_data["already_exists"],
    )


def run_configure_ohdsi_project():
    project_id_data = prompt_project_id()
    configure_project(
        project_id=project_id_data["value"],
        project_type="ohdsi",
        existing_project=project_id_data["already_exists"],
    )


def run_select_project_options(ctx, option=None):
    if option:
        if option == "generic":
            choice = "1"
        elif option == "pmap":
            choice = "2"
        elif option == "ohdsi":
            choice = "3"
        elif option == "existing":
            choice = "4"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    else:
        click.secho("🔬  Project Tools\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Configure a generic project", fg="white")
        click.secho("(2) Configure a PMAP project", fg="white")
        click.secho("(3) Configure an OHDSI project", fg="white")
        click.secho("(4) Configure an existing project", fg="white")
        click.secho("(5) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4", "5"])
        )

    if choice == "1":
        run_configure_generic_project()
    elif choice == "2":
        run_configure_pmap_project()
    elif choice == "3":
        run_configure_ohdsi_project()
    elif choice == "4":
        run_configure_existing_project()
    elif choice == "5":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(0)
    else:
        exit(0)


def update_after_prompt_database_driver(settings):
    default_db_driver = settings.get("db_driver", "FreeTDS") or ""
    new_db_driver = click.prompt(
        "Enter the ODBC database driver",
        type=str,
        default=default_db_driver,
        show_default=bool(default_db_driver),
    ).strip()

    return update_settings_with_value(settings, "db_driver", new_db_driver)


def update_after_prompt_db_port(settings):
    default_db_port = settings.get("db_port", "1433") or ""
    new_db_port = click.prompt(
        "Enter the database port",
        type=int,
        default=default_db_port,
        show_default=bool(default_db_port),
    )

    return update_settings_with_value(settings, "db_port", new_db_port)


def update_after_prompt_db_server(settings):
    default_db_server = settings.get("db_server", "") or ""
    new_db_server = click.prompt(
        "Enter the database server (e.g., dbserver.jhu.edu)",
        type=str,
        default=default_db_server,
        show_default=bool(default_db_server),
    ).strip()

    return update_settings_with_value(settings, "db_server", new_db_server)


def update_after_prompt_irb_number(settings):
    default_irb_number = settings.get("irb_number", "") or ""
    new_irb_number = click.prompt(
        "Enter the IRB number",
        type=str,
        default=default_irb_number,
        show_default=bool(default_irb_number),
    ).strip()

    return update_settings_with_value(settings, "irb_number", new_irb_number)


def update_after_prompt_project_name(settings):
    default_name = settings.get("name", "") or ""
    new_project_name = click.prompt(
        "Enter the name of the project",
        type=str,
        default=default_name,
        show_default=bool(default_name),
    ).strip()

    return update_settings_with_value(settings, "name", new_project_name)


def update_after_prompt_projection_name(settings):
    default_projection_name = settings.get("projection_name", "") or ""
    new_projection_name = click.prompt(
        "Enter the projection database name",
        type=str,
        default=default_projection_name,
        show_default=bool(default_projection_name),
    ).strip()

    return update_settings_with_value(settings, "projection_name", new_projection_name)


def update_after_prompt_omop_projection_name(settings):
    default_projection_name = settings.get("projection_name", "") or ""
    new_projection_name = click.prompt(
        "Enter the OMOP projection database name",
        type=str,
        default=default_projection_name,
        show_default=bool(default_projection_name),
    ).strip()

    return update_settings_with_value(settings, "projection_name", new_projection_name)


def update_after_prompt_safe_folder_name(settings):
    default_safe_folder_name = settings.get("safe_folder_name", "") or ""
    new_safe_folder_name = click.prompt(
        "Enter the SAFE folder name",
        type=str,
        default=default_safe_folder_name,
        show_default=bool(default_safe_folder_name),
    ).strip()

    return update_settings_with_value(
        settings, "safe_folder_name", new_safe_folder_name
    )


def update_after_prompt_scratch_db_name(settings):
    default_scratch_db_name = settings.get("scratch_db_name", "") or ""
    new_scratch_db_name = click.prompt(
        "Enter the scratch database name",
        type=str,
        default=default_scratch_db_name,
        show_default=bool(default_scratch_db_name),
    ).strip()

    return update_settings_with_value(settings, "scratch_db_name", new_scratch_db_name)


def update_after_prompt_omop_scratch_db_name(settings):
    default_scratch_db_name = settings.get("scratch_db_name", "") or ""
    new_scratch_db_name = click.prompt(
        "Enter the OMOP scratch database name",
        type=str,
        default=default_scratch_db_name,
        show_default=bool(default_scratch_db_name),
    ).strip()

    return update_settings_with_value(settings, "scratch_db_name", new_scratch_db_name)


def update_after_prompt_scratch_db_schema_name(settings):
    default_scratch_db_schema_name = settings.get("scratch_db_schema_name", "dbo") or ""
    new_scratch_db_schema_name = click.prompt(
        "Enter the scratch database schema name",
        type=str,
        default=default_scratch_db_schema_name,
        show_default=bool(default_scratch_db_schema_name),
    ).strip()

    return update_settings_with_value(
        settings, "scratch_db_schema_name", new_scratch_db_schema_name
    )


def update_after_prompt_free_tds_version(settings):
    default_free_tds_version = settings.get("free_tds_version", "8.0") or ""
    new_free_tds_version = click.prompt(
        "Enter the FreeTDS version",
        type=str,
        default=default_free_tds_version,
        show_default=bool(default_free_tds_version),
    ).strip()

    return update_settings_with_value(
        settings, "db_free_tds_version", new_free_tds_version
    )


def update_generic_project_settings(settings):
    settings = update_after_prompt_project_name(settings)

    return settings


def update_pmap_project_settings(settings):
    settings = update_after_prompt_irb_number(settings)
    settings = update_after_prompt_database_driver(settings)

    if settings["db_driver"] == "FreeTDS":
        settings = update_after_prompt_free_tds_version(settings)

    settings = update_after_prompt_db_server(settings)
    settings = update_after_prompt_db_port(settings)
    settings = update_after_prompt_projection_name(settings)
    settings = update_after_prompt_scratch_db_name(settings)
    settings = update_after_prompt_scratch_db_schema_name(settings)
    settings = update_after_prompt_safe_folder_name(settings)

    return settings


def update_ohdsi_project_settings(settings):
    settings = update_after_prompt_irb_number(settings)

    settings = update_after_prompt_db_server(settings)
    settings = update_after_prompt_db_port(settings)
    settings = update_after_prompt_omop_projection_name(settings)
    settings = update_after_prompt_omop_scratch_db_name(settings)
    settings = update_after_prompt_scratch_db_schema_name(settings)
    settings = update_after_prompt_safe_folder_name(settings)

    return settings


def update_settings_with_value(settings, key, value):
    settings[key] = value
    return settings


def validate_project_id(project_id):
    return project_id.isalnum()
