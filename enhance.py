import click


def run_enhance_shell(ctx):
    click.secho("Installing ZSH...")
    click.secho("Installing Oh My Zsh...")
    click.secho("Installing quick aliases...")
    click.secho("Done.", fg="green")


def run_install_rstudio_keybindings(ctx):
    click.secho("Installing enhanced RStudio keybindings...")
    click.secho("Done.", fg="green")
