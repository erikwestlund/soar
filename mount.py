import os

import click

from config import check_config_with_password, get_config
from credentials import (
    get_password,
)


def run_mount_home(ctx):
    if not check_config_with_password():
        click.secho("Exiting.", fg="red", bold=True)
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
    if not check_config_with_password():
        click.secho("Exiting.", fg="red", bold=True)
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
