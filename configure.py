import click
import keyring
import os
import yaml


def set_credentials(self, refresh=False):

    # Set JHED if not set or refresh is True
    if refresh or not os.environ.get("user_jhed"):
        jhed_username = click.prompt("Enter your JHED (without @jh.edu)")
    else:
        jhed_username = os.environ.get("user_jhed")

    # Set JHED password if not set or refresh is True
    if refresh or keyring.get_password("jhed", jhed_username) is None:
        jhed_password = click.prompt("Enter your JHED password", hide_input=True)
    else:
        jhed_password = keyring.get_password("jhed", jhed_username)

    # Set GitHub username if not set or refresh is True
    if refresh or not os.environ.get("github_username"):
        github_username = click.prompt("Enter your GitHub username")
    else:
        github_username = os.environ.get("github_username")

    # Set GitHub email if not set or refresh is True
    if refresh or not os.environ.get("github_email"):
        github_email = click.prompt(
            "Enter the email address associated with your GitHub username"
        )
    else:
        github_email = os.environ.get("github_email")

    set_jhed_username(jhed_username)
    set_keyring_password(jhed_username, jhed_password)
    set_github_email(github_email)
    generate_config_yaml(jhed_username, github_username, github_email)


def set_jhed_username(jhed_username):
    os.environ["USER_JHED"] = jhed_username
    click.secho("Set your JHED username to " + jhed_username, fg="green")


def set_keyring_password(jhed_username, jhed_password):
    keyring.set_password("jhed", jhed_username, jhed_password)
    click.secho(
        "Stored your JHED password in the system credential manager", fg="green"
    )


def set_github_username(github_username):
    os.environ["GITHUB_USERNAME"] = github_username
    click.secho("Set your GitHub username to " + github_username, fg="green")


def set_github_email(github_email):
    os.environ["GITHUB_EMAIL"] = github_email
    click.secho("Set your GitHub email to " + github_email, fg="green")


def generate_config_yaml(jhed_username, github_username, github_email):
    config = {
        "default": {
            "user_jhed": jhed_username,
        },
        "github": {
            "username": github_username,
            "email": github_email,
            "core_editor": "nano",
            "default_branch": "main",
        },
        "my_pmap_db": {
            "irb_number": "IRBXXXXXXXX",
            "db_driver": "FreeTDS",
            "db_server": "my.database.address.jhu.edu",
            "db_port": 99999,
            "db_TDS_version": "8.0",
            "projection_name": "MY_PMAP_Projection",
            "scratch_name": "MY_PMAP_Scratch",
            "schema_name": "dbo",
            "safe_folder": "MY_PMAP_DB",
            "patient_id_name": "patient_id",
            "episode_id_name": "episode_id",
            "encounter_id_name": "encounter_id",
            "min_birth_year": 1890,
            "start_dt": "2020-03-01 00:00:01",
            "end_dt": "2025-05-01 00:00:01",
            "limit_by_start_end_dt": False,
            "min_age": 18,
            "limit_by_min_age": False,
            ## projection_metadata,
            "projection_metadata_table": "projection_status",  # Newer Projections,
            "projection_metadata_table_col": "table_name",  # projection_metadata,
            "projection_metadata_date_col": "end_dt",  # projection_metadata,
            "cohort_definition_table": "dbo.definition_table",
            "scratch_metadata_table": "scratch_metadata",
            # Report Information,
            "options_echo": False,
            "options_results": "asis",
            "options_message": False,
            "options_warnings": True,
            "options_knitr_na": "",
        },
    }
    with open("config.yml", "w") as file:
        yaml.dump(config, file)
    click.secho("Generated config.yml", fg="green")
