import click
from credentials import (
    user_has_jhed_password,
    keyring_is_locked,
    unlock_keyring,
    get_password,
    set_keyring_password,
)
import os
import rpy2.robjects.packages as rpackages
import yaml

keyring = rpackages.importr("keyring")


def set_config(self, update=False):
    config = get_config()
    password_updated = False
    changes_made = False

    first_run = not config["configured"]

    if first_run:
        click.secho("Welcome to CrunchR!", fg="green")
        click.secho("Let's get started by configuring your container.", fg="green")

    if keyring_is_locked():
        unlock_keyring()
        click.secho("Unlocked the keyring.", fg="green")

    if update:
        click.secho("Blank answers will not be recorded.", fg="yellow")

    # Set JHED if not set or update is True
    if first_run or update or not config["credentials"]["jhed"]["username"]:
        config["credentials"]["jhed"]["username"] = click.prompt(
            "Enter your JHED (without @jh.edu)",
            default=config["credentials"]["jhed"]["username"],
        )
        changes_made = True

    # Set JHED password if not set or update is True
    jhed_password_set = user_has_jhed_password(
        config["credentials"]["jhed"]["username"]
    )
    if first_run or update or not jhed_password_set:
        current_password = get_password(config["credentials"]["jhed"]["username"])

        jhed_password = click.prompt("Enter your JHED password", hide_input=True)

        if jhed_password != "":
            set_keyring_password(
                config["credentials"]["jhed"]["username"], jhed_password
            )
            password_updated = True

    # Set GitHub username if not set or update is True
    if first_run or update or not config["credentials"]["github"]["username"]:
        config["credentials"]["github"]["username"] = click.prompt(
            "Enter your GitHub username",
            default=config["credentials"]["github"]["username"],
        )
        changes_made = True

    # Set GitHub email if not set or update is True
    if first_run or update or not config["credentials"]["github"]["email"]:
        config["credentials"]["github"]["email"] = click.prompt(
            "Enter the email address associated with your GitHub username",
            default=config["credentials"]["github"]["email"],
        )

    # Set GitHub core editor if not set or update is True
    if first_run or update or not config["settings"]["github"]["core_editor"]:
        default_editor_number = (
            1
            if config["settings"]["github"]["core_editor"] == "nano"
            else 2
            if config["settings"]["github"]["core_editor"] == "vi"
            else 3
        )
        option = click.prompt(
            "Enter your preferred text editor for Git (1=nano, 2=vi, 3=emacs)",
            default=default_editor_number,
        )

        if option == 1:
            config["settings"]["github"]["core_editor"] = "nano"
        elif option == 2:
            config["settings"]["github"]["core_editor"] = "vi"
        elif option == 3:
            config["settings"]["github"]["core_editor"] = "emacs"
        else:
            config["settings"]["github"]["core_editor"] = "nano"

        changes_made = True

    # Set GitHub default branch
    if first_run or update or not config["settings"]["github"]["default_branch"]:
        config["settings"]["github"]["default_branch"] = click.prompt(
            "Enter the default branch of your projects.",
            default=config["settings"]["github"]["default_branch"],
        )

        changes_made = True

    config["configured"] = True

    generate_config_yaml(config)

    if password_updated:
        click.secho("Password updated.", fg="green")

    if changes_made:
        click.secho("✅ Configuration saved to config.yml.", fg="green")
    else:
        click.secho(
            "No changes made. To update your config, run configure with the -u flag.",
            fg="yellow",
        )


def get_config_location(default=False):
    return (
        get_user_storage_path(get_config())
        + "/"
        + ("config.default.yml" if default else "config.default.yml")
    )


def get_default_config_location():
    return get_config_location(default=True)


def generate_config_yaml(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)


def get_config():
    default_config = get_default_config()
    yaml_exists = os.path.exists(get_config_location())

    # If the file does not exist, write the default and return it
    if not yaml_exists:
        write_config(default_config)
        return default_config
    else:
        with open(get_config_location(), "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        # If the file is empty or not a dictionary, return default
        if not isinstance(config, dict):
            write_config(default_config)
            return default_config

    # Return compatible config with default values filled in
    full_config = default_config | config

    if full_config["credentials"]["jhed"]["username"]:
        full_config["settings"]["paths"]["storage"] = get_user_storage_path(full_config)

    return full_config


def get_default_config():
    with open(get_config_location(default=True), "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def write_config(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)


def get_user_storage_path(config):
    return (
        config["settings"]["paths"]["storage_parent"]
        + "/"
        + config["credentials"]["jhed"]["username"]
    )


def get_soar_path(config):
    return get_user_storage_path(config) + "/soar/soar.py"


def get_aliases_path(config):
    return f"{config['settings']['paths']['home']}/.aliases"


def get_bashrc_path(config):
    return f"{config['settings']['paths']['home']}/.bashrc"


def get_zshrc_path(config):
    return f"{config['settings']['paths']['home']}/.zshrc"


def get_rstudio_keybindings_path(config):
    return f"{config['settings']['paths']['home']}/.config/rstudio/keybindings/editor_bindings.json"
