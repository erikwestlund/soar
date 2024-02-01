import json
import os

import click
from jinja2 import Template

from config import (
    check_config,
    get_aliases_template_path,
    get_aliases_home_path,
    get_bashrc_path,
    get_config,
    get_rstudio_config_path,
    get_rstudio_keybindings_path,
    get_soar_path,
    get_soar_program_path,
    get_user_storage_path,
    get_zshrc_path,
)


def run_enhance_shell(ctx):
    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Enhancing your shell with Zsh and OhMyZsh...")
    install_script = get_soar_path("resources/shell/enhance.sh")
    os.system("sh resources/shell/install_zsh.sh")

    click.secho("Installing quick aliases...")
    run_install_aliases(ctx, install_bash=False, install_zsh=True)

    click.secho("Changing default RStudio shell to Zsh...")
    rstudio_options_path = f"{get_rstudio_config_path()}/rstudio-prefs.json"
    with open(rstudio_options_path, "r") as f:
        rstudio_config = f.read()

    rstudio_options = json.loads(rstudio_config)
    rstudio_options["posix_terminal_shell"] = "zsh"

    with open(rstudio_options_path, "w") as f:
        f.write(json.dumps(rstudio_options))

    click.secho(
        '✅ Done. Type "zsh" in the terminal to use the enhanced Zsh shell right now.',
        fg="green",
    )


def run_install_aliases(ctx, install_bash=True, install_zsh=True):
    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Installing quick aliases...")
    config = get_config()

    with open(get_aliases_template_path(), "r") as f:
        template = Template(f.read())

    aliases = template.render(
        python_path=config["settings"]["paths"]["python"],
        pip_path=config["settings"]["paths"]["pip"],
        soar_path=get_soar_program_path(),
        workspace_path=config["settings"]["paths"]["workspace"],
        storage_path=get_user_storage_path(),
    )

    # write to ~/.aliases
    aliases_location = get_aliases_home_path()
    with open(aliases_location, "w") as f:
        f.write(aliases)

    # load aliases by hand
    os.system(f"source {aliases_location}")

    # install to bash and zsh to make permanent
    source_string = f"source {aliases_location}"
    bashrc_path = get_bashrc_path()
    zshrc_path = get_zshrc_path()

    if install_bash:
        with open(bashrc_path, "a") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")

    if install_zsh:
        with open(zshrc_path, "a") as f:
            if source_string not in f.read():
                f.write(f"\n{source_string}")

    click.secho("✅ Done.", fg="green")


def run_install_rstudio_keybindings(ctx):

    if not check_config():
        click.secho("Exiting.", fg="red", bold=True)
        exit(1)

    click.secho("Installing enhanced RStudio keybindings...")
    config = get_config()
    rstudio_keybindings_path = get_rstudio_keybindings_path()
    os.system(f"cp resources/rstudio/editor_bindings.json {rstudio_keybindings_path}")
    click.secho("✅ Done.", fg="green")
