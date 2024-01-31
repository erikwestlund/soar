import click
from configure import get_config
from credentials import (
    get_password,
    unlock_keyring,
    keyring_is_locked,
    user_has_jhed_password,
    set_keyring_password,
)
import os


def run_mount_home(ctx):
    config = get_config()

    if not check_config(config):
        click.secho("Exiting", fg="red", bold=True)
        exit(1)

    jhed_password = get_password(config["credentials"]["jhed"]["username"])

    home_dir = config["settings"]["paths"]["home"]
    os.makedirs(home_dir, exist_ok=True)

    chown_string = f"sudo chown -R idies:idies {home_dir}"
    mount_string = f"sudo mount -t cifs {config['settings']['volumes']['user_home']} {home_dir} -o username={config['credentials']['jhed']['username']},workgroup=win,uid=idies,password={jhed_password}"

    os.system(chown_string)
    os.system(mount_string)

    click.secho(f"✅ Mounted Home directory to {home_dir}.", fg="green", bold=True)


def run_mount_safe(ctx):
    config = get_config()

    if not check_config(config):
        click.secho("Exiting", fg="red", bold=True)
        exit(1)

    jhed_password = get_password(config["credentials"]["jhed"]["username"])

    project_name = click.prompt(
        "Enter the name of the SAFE volume as it appears on the S drive (e.g., 'jhbc_camp')",
        type=str,
    )

    safe_dir = f"{config['settings']['paths']['workspace']}/{project_name}"
    os.makedirs(safe_dir, exist_ok=True)

    chown_string = f"sudo chown -R idies:idies {safe_dir}"
    mount_string = f"sudo mount -t cifs {config['settings']['volumes']['s_drive']}/{project_name} {safe_dir} -o username={config['credentials']['jhed']['username']},workgroup=win,uid=idies,password={jhed_password}"

    os.system(chown_string)
    os.system(mount_string)

    click.secho(f"✅ Mounted SAFE directory to {safe_dir}.", fg="green", bold=True)


def check_config(config):
    if not config["configured"]:
        click.secho(
            "Configuration not set. Run configure before proceeding.",
            fg="red",
            bold=True,
        )
        return False

    if not config["credentials"]["jhed"]["username"]:
        click.secho(
            "JHED username not set. Run configure before proceeding.",
            fg="red",
            bold=True,
        )
        return False

    if keyring_is_locked():
        unlock_keyring()
        click.secho("Unlocked the keyring.", fg="green")

    jhed_password_set = user_has_jhed_password(
        config["credentials"]["jhed"]["username"]
    )
    if not jhed_password_set:
        click.secho(
            "JHED password not set. Run configure before proceeding.",
            fg="red",
            bold=True,
        )
        return False

    return True
