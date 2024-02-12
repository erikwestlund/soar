import os

import click

from config import check_config_with_password, get_config
from credentials import (
    get_password,
)
from crunchr import confirm_crunchr_environment


def run_mount_home(ctx):
    confirm_crunchr_environment()

    if not check_config_with_password():
        click.secho("Exiting.", fg="red", bold=True)
        exit(0)

    click.secho("Mounting Home directory. This may take a moment.")
    config = get_config()
    jhed_password = get_password(
        "jhed", config["default"]["credentials"]["jhed"]["username"]
    )

    home_dir = config["default"]["settings"]["paths"]["home_storage"]
    os.makedirs(home_dir, exist_ok=True)

    chown_string = f"sudo chown -R idies:idies {home_dir}"
    mount_string = f"sudo mount -t cifs {config['default']['settings']['volumes']['user_home']} {home_dir} -o username={config['default']['credentials']['jhed']['username']},workgroup=win,uid=idies,password={jhed_password}"

    os.system(chown_string)
    os.system(mount_string)

    click.secho(f"✅  Mounted Home directory to {home_dir}.", fg="green", bold=True)


def run_mount_safe(ctx):
    confirm_crunchr_environment()

    if not check_config_with_password():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    config = get_config()
    jhed_password = get_password(
        "jhed", config["default"]["credentials"]["jhed"]["username"]
    )

    project_name = click.prompt(
        "Enter the name of the SAFE volume as it appears on the S drive (e.g., 'jhbc_camp')",
        type=str,
    )

    click.secho("Mounting SAFE directory. This may take a moment.")
    safe_dir = f"{config['default']['settings']['paths']['workspace']}/{project_name}"
    os.makedirs(safe_dir, exist_ok=True)

    chown_string = f"sudo chown -R idies:idies {safe_dir}"
    mount_string = f"sudo mount -t cifs {config['default']['settings']['volumes']['s_drive']}/{project_name} {safe_dir} -o username={config['default']['credentials']['jhed']['username']},workgroup=win,uid=idies,password={jhed_password}"

    os.system(chown_string)
    os.system(mount_string)

    click.secho(f"✅  Mounted SAFE directory to {safe_dir}.", fg="green", bold=True)


def run_select_mount_options(ctx, option=None):
    if option:
        if option == "home":
            choice = "1"
        elif option == "safe":
            choice = "2"
        elif option == "both":
            choice = "3"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    else:
        click.secho("💾 Mount Storage.\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Mount Home directory", fg="white")
        click.secho("(2) Mount SAFE directory", fg="white")
        click.secho("(3) Mount both", fg="white")
        click.secho("(4) Cancel\n", fg="white")
        choice = click.prompt("Enter the number of your selection", type=str)

    if choice == "1":
        run_mount_home(ctx)
    elif choice == "2":
        run_mount_safe(ctx)
    elif choice == "3":
        run_mount_home(ctx)
        run_mount_safe(ctx)
    elif choice == "4":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(0)
    else:
        click.secho("Invalid option.", fg="red", bold=True)
        exit(1)
