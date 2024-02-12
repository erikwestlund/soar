import json
import logging
import os

import click
from jinja2 import Template

from config import (
    check_config,
    get_aliases_template_path,
    get_aliases_home_path,
    get_bashrc_path,
    get_config,
    get_home_directory,
    get_resources_path,
    get_rstudio_config_path,
    get_rstudio_keybindings_dir,
    get_rstudio_keybindings_path,
    get_rstudio_editor_keybindings_path,
    get_soar_dir,
    get_soar_path,
    get_soar_program_path,
    get_user_storage_path,
    get_zshrc_path,
)

from crunchr import confirm_crunchr_environment


def run_enhance_shell():
    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Enhancing your shell with Zsh and OhMyZsh...")
    install_script = get_soar_path("resources/shell/enhance.sh")
    os.system("sh " + install_script)

    click.secho("Installing quick aliases...")
    run_install_aliases(install_bash=False, install_zsh=True)

    click.secho("Changing default RStudio shell to Zsh...")
    rstudio_options_path = f"{get_rstudio_config_path()}/rstudio-prefs.json"
    with open(rstudio_options_path, "r") as f:
        rstudio_config = f.read()

    rstudio_options = json.loads(rstudio_config)
    rstudio_options["posix_terminal_shell"] = "zsh"

    with open(rstudio_options_path, "w") as f:
        f.write(json.dumps(rstudio_options))

    click.secho(
        '✅  Done. Type "zsh" in the terminal to use the enhanced Zsh shell right now.',
        fg="green",
    )


def run_install_aliases(install_bash=True, install_zsh=True):
    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Installing quick aliases...")
    config = get_config()

    with open(get_aliases_template_path(), "r") as f:
        template = Template(f.read())

    aliases = template.render(
        python_path=config["default"]["settings"]["paths"]["python"],
        pip_path=config["default"]["settings"]["paths"]["pip"],
        soar_dir=get_soar_dir(),
        soar_path=get_soar_program_path(),
        workspace_path=config["default"]["settings"]["paths"]["workspace"],
        storage_path=get_user_storage_path(),
    )

    # write to ~/.aliases
    aliases_location = get_aliases_home_path()
    os.makedirs(os.path.dirname(aliases_location), exist_ok=True)
    with open(aliases_location, "w") as f:
        f.write(aliases)

    # load aliases by hand
    os.system(f"source {aliases_location}")

    # install to bash and zsh to make permanent
    source_string = f"source {aliases_location}"
    bashrc_path = get_bashrc_path()
    zshrc_path = get_zshrc_path()

    if install_bash:
        with open(bashrc_path, "a+") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")

    if install_zsh:
        with open(zshrc_path, "a+") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")

    click.secho("✅  Done.", fg="green")


def run_install_rstudio_keybindings():
    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Installing enhanced RStudio keybindings...")
    config = get_config()

    rstudio_editor_keybindings_template_path = (
        get_resources_path() + "/rstudio/editor_bindings.json"
    )
    rstudio_keybindings_template_path = (
        get_resources_path() + "/rstudio/rstudio_bindings.json"
    )

    rstudio_editor_keybindings_system_path = get_rstudio_editor_keybindings_path()
    rstudio_keybindings_system_path = get_rstudio_keybindings_path()

    os.makedirs(get_rstudio_keybindings_dir(), exist_ok=True)
    os.system(
        f"cp {rstudio_editor_keybindings_template_path} {rstudio_editor_keybindings_system_path}"
    )
    os.system(
        f"cp {rstudio_keybindings_template_path} {rstudio_keybindings_system_path}"
    )

    click.secho("✅  Done.", fg="green")
    click.secho(
        '🚨 To make the keybindings take effect, click "Session -> Terminate R" in RStudio.',
        bold=True,
        fg="red",
        bg="white",
    )
    click.secho("Save your work before terminating.", bold=True, fg="red", bg="white")


def run_select_enhance_options(ctx, option=None):
    if option:
        if option == "aliases":
            choice = "1"
        elif option == "rstudio-keybindings":
            choice = "2"
        elif option == "shell":
            choice = "3"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)

    else:
        click.secho("🚀 Enhance your Crunchr container.\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Add enhanced shell aliases", fg="white")
        click.secho("(2) Install enhanced RStudio keybindings", fg="white")
        click.secho(
            "(3) Enhance your shell environment with Zsh and aliases", fg="white"
        )
        click.secho("(4) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4"])
        )

    if choice == "4":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)

    confirm_crunchr_environment()

    if choice == "1":
        run_install_aliases()
    elif choice == "2":
        run_install_rstudio_keybindings()
    elif choice == "3":
        run_enhance_shell()
    else:
        click.secho("Invalid option.", fg="red", bold=True)
        exit(1)
