import os

import click
from jinja2 import Template

from config import (
    get_aliases_path,
    get_bashrc_path,
    get_config,
    get_rstudio_keybindings_path,
    get_soar_path,
    get_soar_program_path,
    get_user_storage_path,
    get_zshrc_path,
)


def run_enhance_shell(ctx):
    click.secho("Enhancing your shell with Zsh and OhMyZsh...")
    install_script = get_soar_path(get_config(), "resources/shell/install_zsh.sh")
    os.system("sh resources/shell/install_zsh.sh")
    click.secho("Installing quick aliases...")
    click.secho("✅ Done.", fg="green")


def run_install_aliases(ctx, install_bash=True, install_zsh=True):
    click.secho("Installing quick aliases...")
    config = get_config()

    with open(f"resources/shell/.aliases", "r") as f:
        template = Template(f.read())

    aliases = template.render(
        python_path=config["settings"]["paths"]["python"],
        pip_path=config["settings"]["paths"]["pip"],
        soar_path=get_soar_program_path(config),
        workspace_path=config["settings"]["paths"]["workspace"],
        storage_path=get_user_storage_path(config),
    )

    # write to ~/.aliases
    aliases_location = get_aliases_path(config)
    with open(aliases_location, "w") as f:
        f.write(aliases)

    # load aliases by hand
    os.system(f"source {aliases_location}")

    # install to bash and zsh to make permanent
    source_string = f"source {aliases_location}"
    bashrc_path = get_bashrc_path(config)
    zshrc_path = get_zshrc_path(config)

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
    click.secho("Installing enhanced RStudio keybindings...")
    config = get_config()
    rstudio_keybindings_path = get_rstudio_keybindings_path(config)
    os.system(f"cp resources/rstudio/editor_bindings.json {rstudio_keybindings_path}")
    click.secho("✅ Done.", fg="green")
