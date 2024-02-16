import os
from pathlib import Path

import click
import rpy2.robjects.packages as rpackages
import yaml
from jinja2 import Template

from credentials import (
    get_password,
    keyring_is_locked,
    set_keyring_password,
    unlock_keyring,
    user_has_github_pat,
    user_has_jhed_password,
)

keyring = rpackages.importr("keyring")


def check_config(config=None, check_password=False):
    config = config if config else get_config()

    is_configured = get_is_configured()

    if not is_configured:
        click.secho(
            "Configuration not set. Run configure before proceeding.",
            fg="red",
            bold=True,
        )
        return False

    if not config["default"]["credentials"]["jhed"]["username"]:
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
            config["default"]["credentials"]["jhed"]["username"]
        )
        if not jhed_password_set:
            click.secho(
                "JHED password not set. Run configure before proceeding.",
                fg="red",
                bold=True,
            )
            return False

    return True


def check_config_with_password(config=None):
    config = config if config else get_config()
    return check_config(config, True)


def configure_ggplot_settings():
    pass


def configure_github_settings():
    config = get_config()
    changes_made = False

    if keyring_is_locked():
        unlock_keyring()

    click.secho("Blank answers will not be recorded.", fg="yellow")

    # Github Username
    new_github_username = config["default"]["credentials"]["github"][
        "username"
    ] = click.prompt(
        "Enter your GitHub username",
        default=config["default"]["credentials"]["github"]["username"] or "",
        show_default=True
        if config["default"]["credentials"]["github"]["username"]
        else False,
    ).strip()

    if new_github_username != "":
        config["default"]["credentials"]["github"]["username"] = new_github_username
        changes_made = True

    # Github Email
    new_github_email = config["default"]["credentials"]["github"][
        "email"
    ] = click.prompt(
        "Enter the email address associated with your GitHub username",
        default=config["default"]["credentials"]["github"]["email"] or "",
        show_default=True
        if config["default"]["credentials"]["github"]["email"]
        else False,
    ).strip()

    if new_github_email != "":
        config["default"]["credentials"]["github"]["email"] = new_github_email
        changes_made = True

    # Github core editor
    default_github_editor_number = (
        1
        if config["default"]["settings"]["github"]["core_editor"] == "nano"
        else 2
        if config["default"]["settings"]["github"]["core_editor"] == "vi"
        else 3
    )
    new_option = click.prompt(
        "Enter your preferred text editor for Git (1=nano, 2=vi, 3=emacs)",
        default=default_github_editor_number,
    )

    if new_option != default_github_editor_number:
        if new_option == 1:
            config["default"]["settings"]["github"]["core_editor"] = "nano"
        elif new_option == 2:
            config["default"]["settings"]["github"]["core_editor"] = "vi"
        elif new_option == 3:
            config["default"]["settings"]["github"]["core_editor"] = "emacs"
        else:
            config["default"]["settings"]["github"]["core_editor"] = "nano"

        changes_made = True

    # Github default branch
    new_default_branch = click.prompt(
        "Enter the default branch of your projects",
        default=config["default"]["settings"]["github"]["default_branch"] or "",
        show_default=True
        if config["default"]["settings"]["github"]["default_branch"]
        else False,
    ).strip()

    if new_default_branch != "":
        config["default"]["settings"]["github"]["default_branch"] = new_default_branch
        changes_made = True

    # Github Personal Access Token
    if not user_has_github_pat(config["default"]["credentials"]["github"]["username"]):
        click.secho(
            "To push and pull from JHU organization GitHub repositories, you will need a Personal Access Token (PAT).",
            fg="yellow",
        )
        click.secho(
            "This token will be securely stored in your keyring and used to authenticate with GitHub.",
            fg="yellow",
        )
        click.secho(
            "This PAT will need to be authorized by the relevant SSO organization (e.g., JH-inHealth, OHDSI-JHU.)",
            fg="yellow",
        )
        click.secho("Directions on how to do this are available here:", fg="yellow")
        click.secho(
            "https://docs.github.com/en/enterprise-cloud@latest/authentication/authenticating-with-saml-single-sign-on/authorizing-a-personal-access-token-for-use-with-saml-single-sign-on",
            fg="magenta",
        )

    new_github_pat = click.prompt(
        "Enter the GitHub Personal Access Token you will use for this container",
        hide_input=True,
        default="",
        show_default=False,
    ).strip()

    if new_github_pat != "":
        set_keyring_password(
            "github",
            config["default"]["credentials"]["github"]["username"],
            new_github_pat,
        )
        changes_made = True
        click.secho("Github Personal Authentication Token updated.", fg="green")

    if changes_made:
        generate_config_yaml(config)
        click.secho("✅  Configuration saved to config.yml.", fg="green")
    else:
        click.secho(
            "No changes made.",
            fg="yellow",
        )

    setup_config_files()


def configure_jhed_credentials():
    config = get_config()
    changes_made = False
    first_run = not get_is_configured()

    if first_run:
        click.secho(
            "\nLet's get started by configuring your JHED credentials.", fg="green"
        )

    if keyring_is_locked():
        unlock_keyring()

    click.secho("Blank answers will not be recorded.", fg="yellow")

    # Update JHED username
    jhed_username_default = (
        config["default"]["credentials"]["jhed"]["username"] or get_default_jhed()
    )

    new_jhed_username = (
        click.prompt(
            "Enter your JHED (without @jh.edu)",
            default=jhed_username_default or "",
            show_default=True if jhed_username_default else False,
        ).strip()
        or None
    )

    if new_jhed_username != "":
        config["default"]["credentials"]["jhed"]["username"] = new_jhed_username
        changes_made = True

    # Update JHED password in keyring
    if first_run:
        click.secho(
            "Your JHED password is required for mounting volumes and interacting with other JHU-related resources.",
            fg="yellow",
        )

    click.secho(
        "This password will be securely stored in the system keyring.", fg="yellow"
    )

    jhed_password = click.prompt(
        "Enter new JHED password", hide_input=True, default="", show_default=False
    ).strip()

    if jhed_password != "":
        set_keyring_password(
            "jhed",
            config["default"]["credentials"]["jhed"]["username"],
            jhed_password,
        )
        click.secho("Password updated.", fg="green")
        changes_made = True

    if changes_made:
        generate_config_yaml(config)
        with (get_soar_dir() / ".jhed_username").open("w") as f:
            f.write(config["default"]["credentials"]["jhed"]["username"])
        click.secho("✅  Configuration saved to config.yml.", fg="green")
    else:
        click.secho(
            "No changes made.",
            fg="yellow",
        )

    setup_config_files()


def generate_config_yaml(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)


def get_aliases_home_path():
    config = get_config()
    return f"{config['default']['settings']['paths']['home']}/.aliases"


def get_aliases_template_path():
    return f"{get_resources_path()}/shell/.aliases"


def get_bashrc_path():
    config = get_config()
    return f"{config['default']['settings']['paths']['home']}/.bashrc"


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

    if full_config["default"]["credentials"]["jhed"]["username"]:
        full_config["default"]["settings"]["paths"]["storage"] = get_user_storage_path(
            full_config
        )

    return full_config


def get_is_dev_env():
    return not os.path.exists("/home/idies")


def get_config_location(default=False):

    if not default:
        config_file = "config.yml"
    elif get_is_dev_env():
        config_file = "config.dev.default.yml"
    else:
        config_file = "config.default.yml"

    return (Path(__file__).parent / config_file).resolve()


def get_default_config():
    with open(get_default_config_location(), "r") as file:
        return yaml.load(file, Loader=yaml.FullLoader)


def get_default_config_location():
    return get_config_location(default=True)


def get_default_jhed():
    temp_jhed_username_path = (Path(__file__).parent / ".jhed_username").resolve()
    try:
        with open(temp_jhed_username_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return ""


def get_home_directory():
    config = get_config()
    return config["default"]["settings"]["paths"]["home"]


def get_is_configured():
    default_config = get_default_config()
    config = get_config()

    return default_config != config


def get_resources_path():
    return f"{get_soar_dir()}/resources"


def get_rstudio_config_path():
    config = get_config()
    return f"{config['default']['settings']['paths']['rstudio_config']}"


def get_rstudio_editor_keybindings_path():
    return f"{get_rstudio_keybindings_dir()}/editor_bindings.json"


def get_rstudio_keybindings_dir():
    return f"{get_rstudio_config_path()}/keybindings"


def get_rstudio_keybindings_path():
    return f"{get_rstudio_keybindings_dir()}/rstudio_bindings.json"


def get_soar_dir():
    return Path(__file__).parent.resolve()


def get_project_templates_library_dir():
    return f"{get_soar_dir()}/library"


def get_soar_path(path):
    return f"{get_soar_dir()}/{path}"


def get_soar_program_path():
    return get_soar_dir() / "/soar.py"


def get_soarrc_path():
    config = get_config()
    return f"{config['default']['settings']['paths']['home']}/.soarrc"


def get_user_storage_path(config=None):
    config = config if config else get_config()

    if not config["default"]["credentials"]["jhed"]["username"]:
        return config["default"]["settings"]["paths"]["storage_parent"]

    return (
        config["default"]["settings"]["paths"]["storage_parent"]
        + "/"
        + config["default"]["credentials"]["jhed"]["username"]
        + "/persistent"
    )


def get_workspace_dir():
    config = get_config()
    return f"{config['default']['settings']['paths']['workspace']}"


def get_zshrc_path():
    config = get_config()
    return f"{config['default']['settings']['paths']['home']}/.zshrc"


def install_soarrc():
    config = get_config()

    soarrc_template_path = get_resources_path() + "/shell/.soarrc"
    with open(soarrc_template_path, "r") as f:
        template = Template(f.read())

    soarrc = template.render(
        python_path=config["default"]["settings"]["paths"]["python"],
        pip_path=config["default"]["settings"]["paths"]["pip"],
        soar_dir=get_soar_dir(),
        soar_path=get_soar_program_path(),
        workspace_path=config["default"]["settings"]["paths"]["workspace"],
        storage_path=get_user_storage_path(),
    )

    # write to ~/.aliases
    soarrc_location = get_soarrc_path()

    if os.path.exists(soarrc_location):
        os.makedirs(os.path.dirname(soarrc_location), exist_ok=True)
        with open(soarrc_location, "w") as f:
            f.write(soarrc)

        # install to bash and zsh to make permanent
        source_string = f"source {soarrc_location}"
        bashrc_path = get_bashrc_path()
        zshrc_path = get_zshrc_path()

        with open(bashrc_path, "a+") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")

        with open(zshrc_path, "a+") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")
    else:
        click.secho(
            "⚠️  This looks like a non-Crunchr platform. Cannot write all config files because default config paths do not exist.",
            fg="yellow",
            bold=True,
        )


def run_link_config():
    config = get_config()
    new_location = get_workspace_dir() + "/config.yml"

    if os.path.exists(get_workspace_dir()):
        os.system(f"ln -s {get_config_location()} {new_location}")
    else:
        click.secho(
            "⚠️  This looks like a non-Crunchr platform. Cannot links config files because default config paths do not exist.",
            fg="yellow",
            bold=True,
        )


def run_refresh_config(ctx):
    config = get_config()
    click.secho("Refreshing your configuration...", fg="red", bold=True)

    refreshed_config = get_default_config() | config
    write_config(refreshed_config)

    click.secho("✅  Configuration refreshed.", fg="green", bold=True)

    setup_config_files()


def run_reset_keyring(ctx):
    config = get_config()
    click.secho("🔑 Resetting your keyring...", fg="red", bold=True)

    click.confirm("Are you sure you want to reset your keyring?", abort=True)

    os.system(
        f"rm -rf {config['default']['settings']['paths']['rstudio_keyring']}/system.keyring"
    )
    os.system(
        f"rm -rf {config['default']['settings']['paths']['rstudio_keyring']}/system.keyring.lck"
    )
    unlock_keyring()


def configure_keyring_password():
    click.secho(
        "The keyring is used to securely store credentials.", fg="yellow", bold=True
    )
    click.secho(
        "Enter a password to unlock your keying. This should be different from your JHED.",
        fg="yellow",
        bold=True,
    )

    unlock_keyring()


def run_select_config_options(ctx, option=None):
    if option:
        if option == "jhed":
            choice = "1"
        elif option == "github":
            choice = "2"
        elif option == "keyring":
            choice = "3"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    if not option:
        click.secho("🔧  Configure your Crunchr container.\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) JHED Credentials", fg="white")
        click.secho("(2) Github Settings", fg="white")
        click.secho("(3) Reset keyring", fg="white")
        click.secho("(4) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4"])
        )

    if choice == "1":
        configure_jhed_credentials()
    elif choice == "2":
        configure_github_settings()
    elif choice == "3":
        run_reset_keyring({})
    elif choice == "4":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(0)
    else:
        click.secho("Invalid option.", fg="red", bold=True)
        exit(1)


def setup_config_files():
    install_soarrc()
    run_link_config()


def write_config(config):
    with open(get_config_location(), "w") as file:
        yaml.dump(config, file)
