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
import os


def run_enhance_shell(ctx):
    click.secho("Installing ZSH...")
    click.secho("Installing Oh My Zsh...")
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

    with open("resources/shell/.aliases", "r") as f:
        aliases = f.read()

    aliases = aliases.replace("{{PYTHONPATH}}", config["settings"]["paths"]["python"])
    aliases = aliases.replace("{{PIPPATH}}", config["settings"]["paths"]["pip"])
    aliases = aliases.replace("{{SOARPATH}}", get_soar_path(config))
    aliases = aliases.replace(
        "{{WORKSPACEPATH}}", config["settings"]["paths"]["workspace"]
    )
    aliases = aliases.replace("{{STORAGEPATH}}", get_user_storage_path(config))

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
