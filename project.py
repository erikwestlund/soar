from config import run_link_config, get_config, get_config_location, get_is_configured
import click
import yaml


def get_all_project_ids():
    config = get_config()
    return list(filter(lambda x: x != "default", list(config.keys())))


def project_exists(project_id):
    config = get_config()
    return project_id in config.keys()


def run_configure_project(ctx, project_id=None):
    """Configure your project."""

    if not get_is_configured():
        click.secho(
            "You must configure your settings before configuring a project.",
            fg="red",
            bold=True,
        )
        click.secho(
            "Run `soar configure` to configure your settings.", fg="red", bold=True
        )
        exit(1)

    if project_id and not project_exists(project_id):
        click.secho(
            f"The project ID {project_id} does not exist. Please create it first.",
            fg="red",
            bold=True,
        )
        exit(1)

    config = get_config()

    if project_id:
        click.secho(
            "Below you will be prompted to enter information about your project.",
            fg="green",
            bold=True,
        )
    else:
        click.secho(
            "Below you can update information about your project.",
            fg="green",
            bold=True,
        )

    click.secho(
        "Default values can be accepted when they are shown in brackets.",
        fg="white",
        bold=True,
    )
    click.secho(
        "If you do not know the value, you can leave it blank and enter it later.",
        fg="white",
        bold=True,
    )

    existing_project_ids = get_all_project_ids()

    if not project_id:
        click.secho(
            "Entering an existing project ID will allow you to update the settings.",
            fg="white",
        )

        default_project_id = (
            existing_project_ids[0] if existing_project_ids else "project_name"
        )

        project_id = click.prompt(
            'Give the project a string ID (e.g., "project_name")',
            type=str,
            default=default_project_id,
            show_default=bool(default_project_id),
        ).strip()

    project_data = config.get(project_id, {})
    provided_project_exists = bool(project_data)
    defaults = project_data.get("settings", {})

    default_name = defaults.get("name", "")
    name = click.prompt(
        'Give the project a name (e.g., "Project Name"',
        type=str,
        default=default_name,
        show_default=bool(default_name),
    ).strip()

    default_irb_number = defaults.get("irb_number", "") or ""
    irb_number = click.prompt(
        "Enter the IRB number (e.g.,  IRBXXXX) if you know it",
        type=str,
        default=default_irb_number,
        show_default=bool(default_irb_number),
    ).strip()

    default_db_driver = defaults.get("db_driver", "FreeTDS") or ""
    db_driver = click.prompt(
        "Enter the ODBC database driver",
        type=str,
        default=default_db_driver,
        show_default=bool(default_db_driver),
    ).strip()

    if db_driver == "FreeTDS":
        default_db_tds_version = defaults.get("db_tds_version", "8.0") or ""
        db_tds_version = click.prompt(
            "Enter the TDS version",
            type=str,
            default=default_db_tds_version,
            show_default=bool(default_db_tds_version),
        ).strip()

    default_db_server = defaults.get("db_server", "") or ""
    db_server = click.prompt(
        "Enter the database server (e.g., XXXX.jhu.edu)",
        type=str,
        default=default_db_server,
        show_default=bool(default_db_server),
    ).strip()

    default_db_port = defaults.get("db_port", 1433) or ""
    db_port = click.prompt(
        "Enter the database port",
        type=int,
        default=default_db_port,
        show_default=bool(default_db_port),
    )

    default_projection_name = defaults.get("projection_name", "") or ""
    projection_name = click.prompt(
        "Enter the projection database name",
        type=str,
        default=default_projection_name,
        show_default=bool(default_projection_name),
    ).strip()

    default_scratch_name = defaults.get("scratch_name", "") or ""
    scratch_name = click.prompt(
        "Enter the scratch database name",
        type=str,
        default=default_scratch_name,
        show_default=bool(default_scratch_name),
    ).strip()

    default_scratch_schema_name = defaults.get("scratch_schema_name", "dbo") or ""
    scratch_schema_name = click.prompt(
        "Enter the scratch schema name",
        type=str,
        default=default_scratch_schema_name,
        show_default=bool(default_scratch_schema_name),
    ).strip()

    default_safe_folder_name = defaults.get("safe_folder_name", "") or ""
    safe_folder_name = click.prompt(
        "Enter the SAFE Folder name",
        type=str,
        default=default_safe_folder_name,
        show_default=bool(default_safe_folder_name),
    ).strip()

    new_settings = {
        "id": project_id,
        "name": name,
        "irb_number": irb_number or None,
        "db_driver": db_driver or None,
        "db_server": db_server or None,
        "db_port": db_port or None,
        "projection_name": projection_name or None,
        "scratch_name": scratch_name or None,
        "scratch_schema_name": scratch_schema_name or None,
        "safe_folder_name": safe_folder_name or None,
    }

    if provided_project_exists:
        # Merge with any existing settings
        project_settings = defaults | new_settings
        config[project_id]["settings"] = project_settings
    else:
        config[project_id] = {"settings": new_settings}

    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)

    run_link_config()
