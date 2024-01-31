import click
from credentials import (
    user_has_jhed_password,
    keyring_is_locked,
    unlock_keyring,
    get_password,
)
import os
import rpy2.robjects.packages as rpackages
import yaml

keyring = rpackages.importr("keyring")


def set_config(self, update=False):
    config = get_config()
    password_updated = False

    if keyring_is_locked():
        unlock_keyring()
        click.secho("Unlocked the keyring.", fg="green")

    if update:
        click.secho("Blank answers will not be recorded.", fg="yellow")

    # Set JHED if not set or update is True
    if update or not config["default"]["jhed_username"]:
        config["default"]["jhed_username"] = click.prompt(
            "Enter your JHED (without @jh.edu)",
            default=config["default"]["jhed_username"],
        )

    # Set JHED password if not set or update is True
    jhed_password_set = user_has_jhed_password(config["default"]["jhed_username"])
    if update or not jhed_password_set:
        current_password = get_password(config["default"]["jhed_username"])

        jhed_password = click.prompt("Enter your JHED password", hide_input=True)

        if jhed_password != "":
            set_keyring_password(config["default"]["jhed_username"], jhed_password)
            password_updated = True

    # Set GitHub username if not set or update is True
    if update or not config["github"]["username"]:
        config["github"]["username"] = click.prompt(
            "Enter your GitHub username", default=config["github"]["username"]
        )

    # Set GitHub email if not set or update is True
    if update or not config["github"]["email"]:
        config["github"]["email"] = click.prompt(
            "Enter the email address associated with your GitHub username",
            default=config["github"]["email"],
        )

    # Set GitHub core editor if not set or update is True
    if update or not config["github"]["core_editor"]:
        default_editor_number = (
            1
            if config["github"]["core_editor"] == "nano"
            else 2
            if config["github"]["core_editor"] == "vi"
            else 3
        )
        option = click.prompt(
            "Enter your preferred text editor for Git (1=nano, 2=vi, 3=emacs)",
            default=default_editor_number,
        )

        if option == 1:
            config["github"]["core_editor"] = "nano"
        elif option == 2:
            config["github"]["core_editor"] = "vi"
        elif option == 3:
            config["github"]["core_editor"] = "emacs"
        else:
            config["github"]["core_editor"] = "nano"

    generate_config_yaml(config)

    if password_updated:
        click.secho("Password updated.", fg="green")

    click.secho("Configuration saved to config.yml.", fg="green")


def set_keyring_password(jhed_username, jhed_password):
    keyring.key_set_with_value("jhed", jhed_username, jhed_password)


def generate_config_yaml(config):
    with open("config.yml", "w") as file:
        yaml.dump(config, file)


def get_config():
    default_config = get_default_config()
    yaml_exists = os.path.exists("config.yml")

    # If the file does not exist, write the default and return it
    if not yaml_exists:
        write_config(default_config)
        return make_compatible(default_config)
    else:
        with open("config.yml", "r") as file:
            config = yaml.load(file, Loader=yaml.FullLoader)

        # If the file is empty or not a dictionary, return default
        if not isinstance(config, dict):
            write_config(default_config)
            return make_compatible(default_config)

    # Return compatible config with default values filled in
    return make_compatible(default_config | config)


def get_default_config():
    return {
        "default": {
            "user_jhed": None,
        },
        "github": {
            "username": None,
            "email": None,
            "core_editor": "nano",
            "default_branch": "main",
        },
    }


def write_config(config):
    with open("config.yml", "w") as file:
        yaml.dump(make_compatible(config), file)


def make_compatible(config):
    config["default"]["user_jhed"] = config["default"]["jhed_username"]

    return config
