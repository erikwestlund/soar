import os
from pathlib import Path

import click
import rpy2.robjects.packages as rpackages
import yaml

from credentials import (
    get_password,
    keyring_is_locked,
    set_keyring_password,
    unlock_keyring,
    user_has_jhed_password,
    user_has_github_pat
)

keyring = rpackages.importr("keyring")


def check_config_with_password(config=None):
    config = config if config else get_config()
    return check_config(config, True)


def check_config(config=None, check_password=False):
    config = config if config else get_config()

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

    if check_password:
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


def generate_config_yaml(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)


def get_aliases_home_path():
    config = get_config()
    return f"{config['settings']['paths']['home']}/.aliases"


def get_aliases_template_path():
    return f"{get_resources_path()}/shell/.aliases"


def get_resources_path():
    return f"{get_soar_dir()}/resources"


def get_bashrc_path():
    config = get_config()
    return f"{config['settings']['paths']['home']}/.bashrc"


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


def get_config_location(default=False):
    return Path(__file__).parent / ("config.default.yml" if default else "config.yml")


def get_default_config():
    with open(get_default_config_location(), "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def get_default_config_location():
    return get_config_location(default=True)


def get_default_jhed():
    temp_jhed_username_path = Path(__file__).parent / ".jhed_username"
    try:
        with open(temp_jhed_username_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def get_rstudio_config_path():
    config = get_config()
    return f"{config['settings']['paths']['rstudio_config']}"


def get_rstudio_keybindings_dir():
    return f"{get_rstudio_config_path()}/keybindings"


def get_rstudio_editor_keybindings_path():
    return f"{get_rstudio_keybindings_dir()}/editor_bindings.json"


def get_rstudio_keybindings_path():
    return f"{get_rstudio_keybindings_dir()}/rstudio_bindings.json"


def get_soar_dir():
    return get_user_storage_path() + "/soar"


def get_soar_path(path):
    return f"{get_soar_dir()}/{path}"


def get_soar_program_path():
    return get_soar_dir() + "/soar.py"


def get_user_storage_path(config=None):
    config = config if config else get_config()

    if not config["credentials"]["jhed"]["username"]:
        return config["settings"]["paths"]["storage_parent"]

    return (
        config["settings"]["paths"]["storage_parent"]
        + "/"
        + config["credentials"]["jhed"]["username"]
        + "/persistent"
    )


def get_workspace_dir():
    config = get_config()
    return f"{config['settings']['paths']['workspace']}"


def get_zshrc_path():
    config = get_config()
    return f"{config['settings']['paths']['home']}/.zshrc"


def run_copy_config(ctx):
    config = get_config()
    new_location = get_workspace_dir() + "/config.yml"

    print(f"cp {get_soar_dir()}/config.yml {new_location}")
    os.system(f"cp {get_soar_dir()}/config.yml {new_location}")
    click.secho("✅ Configuration copied to:", fg="green", bold=True)
    click.secho(new_location, fg="yellow")


def run_refresh_config(ctx):
    config = get_config()
    click.secho("Refreshing your configuration...", fg="red", bold=True)

    refreshed_config = get_default_config() | config
    write_config(refreshed_config)

    click.secho("✅ Configuration refreshed.", fg="green", bold=True)



def run_reset_keyring(ctx):
    config = get_config()
    click.secho("🔑 Resetting your keyring...", fg="red", bold=True)
    os.system(f"rm -rf {config['settings']['paths']['rstudio_keyring']}/system.keyring")
    os.system(
        f"rm -rf {config['settings']['paths']['rstudio_keyring']}/system.keyring.lck"
    )
    click.secho("✅ Keyring reset.", fg="green", bold=True)
    click.secho(
        'Run "soar configure -u" to set your credentials again.', fg="green", bold=True
    )


def run_set_config(self, update=False):
    config = get_config()
    password_updated = False
    pat_updated = False
    changes_made = False

    first_run = not config["configured"]

    if first_run:
        click.secho("Welcome to CrunchR!", fg="green")
        click.secho("Let's get started by configuring your container.", fg="green")
    else:
        click.secho("Update Crunchr Configuration.", fg="green")

    click.secho("Note: To paste text into the RStudio terminal, right click and select paste.", fg="yellow")

    if keyring_is_locked():
        unlock_keyring()
        click.secho("Unlocked the keyring.", fg="green")

    if update:
        click.secho("Blank answers will not be recorded.", fg="yellow")

    # Set JHED if not set or update is True
    jhed_username_default = (
        config["credentials"]["jhed"]["username"] or get_default_jhed()
    )

    if first_run or update or not config["credentials"]["jhed"]["username"]:
        config["credentials"]["jhed"]["username"] = click.prompt(
            "Enter your JHED (without @jh.edu)",
            default=jhed_username_default or "",
            show_default=True if jhed_username_default else False
        ).strip()
        changes_made = True

    # Set JHED password if not set or update is True
    jhed_password_set = user_has_jhed_password(
        config["credentials"]["jhed"]["username"]
    )
    if first_run or update or not jhed_password_set:
        current_password = get_password("jhed", config["credentials"]["jhed"]["username"])
        click.secho("Your JHED password is required for mounting volumes and interacting with other JHU-related resources.", fg="yellow")
        click.secho("This password will be securely stored in the system keyring.", fg="yellow")
        jhed_password = click.prompt(
            "Enter your JHED password",
            hide_input=True,
            default="",
            show_default=False
        ).strip()

        if jhed_password != "":
            set_keyring_password(
                "jhed",
                config["credentials"]["jhed"]["username"],
                jhed_password
            )
            password_updated = True

    # Set GitHub username if not set or update is True
    if first_run or update or not config["credentials"]["github"]["username"]:
        config["credentials"]["github"]["username"] = click.prompt(
            "Enter your GitHub username",
            default=config["credentials"]["github"]["username"] or "",
            show_default=True if config["credentials"]["github"]["username"] else False
        ).strip()
        changes_made = True

    # Set GitHub email if not set or update is True
    if first_run or update or not config["credentials"]["github"]["email"]:
        config["credentials"]["github"]["email"] = click.prompt(
            "Enter the email address associated with your GitHub username",
            default=config["credentials"]["github"]["email"] or "",
            show_default=True if config["credentials"]["github"]["email"] else False
        ).strip()

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
            default=config["settings"]["github"]["default_branch"] or "",
            show_default=True if config["settings"]["github"]["default_branch"] else False
        ).strip()

        changes_made = True

    # Set Github Personal Access Token
    github_pat_set = user_has_github_pat(
        config["credentials"]["github"]["username"]
    )
    if first_run or update or not github_pat_set:
        current_pat = get_password("github", config["credentials"]["github"]["username"])

        click.secho("To push and pull from JHU organization GitHub repositories, you will need a Personal Access Token (PAT).", fg="yellow")
        click.secho("This token will be securely stored in your keyring and used to authenticate with GitHub.", fg="yellow")
        click.secho("This PAT will need to be authorized by the relevant SSO organization (e.g., JH-inHealth, OHDSI-JHU.)", fg="yellow")
        click.secho("Directions on how to do this are available here:", fg="yellow")
        click.secho("https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on", fg="magenta")
        github_pat = click.prompt(
            "Enter the GitHub Personal Access Token you will use for this container. ",
            hide_input=True,
            default="",
            show_default=False
        ).strip()

        if github_pat != "":
            set_keyring_password(
                "github",
                config["credentials"]["github"]["username"],
                github_pat
            )
            pat_updated = True

    config["configured"] = True

    generate_config_yaml(config)

    if password_updated:
        click.secho("Password updated.", fg="green")

    if pat_updated:
        click.secho("GitHub PAT updated.", fg="green")

    if changes_made:
        click.secho("✅ Configuration saved to config.yml.", fg="green")
    else:
        click.secho(
            "No changes made. To update your config, run configure with the -u flag.",
            fg="yellow",
        )


def write_config(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)
