from configure import (
    get_config,
    get_soar_path,
    get_user_storage_path,
    get_aliases_path,
    get_bashrc_path,
    get_zshrc_path,
    get_rstudio_keybindings_path,
)
import click
from jinja2 import Template
import os


def run_enhance_shell(ctx):
    click.secho("Enhancing your shell with Zsh and OhMyZsh...")
    click.secho("Installing quick aliases...")
    click.secho("✅ Done.", fg="green")


def run_install_rstudio_keybindings(ctx):
    click.secho("Installing enhanced RStudio keybindings...")
    config = get_config()
    rstudio_keybindings_path = get_rstudio_keybindings_path(config)
    os.system(f"cp resources/rstudio/editor_bindings.json {rstudio_keybindings_path}")
    click.secho("✅ Done.", fg="green")


def run_install_aliases(ctx):
    click.secho("Installing quick aliases...")
    config = get_config()

    with open(f"resources/shell/.aliases", "r") as f:
        template = Template(f.read())

    aliases = template.render(
        python_path=config["settings"]["paths"]["python"],
        pip_path=config["settings"]["paths"]["pip"],
        soar_path=get_soar_path(config),
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

    with open(bashrc_path, "a") as f:
        if source_string not in f.read():
            f.write(f"\n{source_string}")

    with open(zshrc_path, "a") as f:
        if source_string not in f.read():
            f.write(f"\n{source_string}")

    click.secho("✅ Done.", fg="green")
