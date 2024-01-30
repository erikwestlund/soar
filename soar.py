import click
from configure.configure import Configure
from enhance import run_enhance_shell, run_install_rstudio_keybindings
from status import get_status

@click.group()
@click.pass_context
def main(ctx):
    """Tooling to make CrunchR soar."""

@main.command()
@click.pass_context
def configure(ctx):
    """Configure your CrunchR container."""
    configure = Configure()
    configure.run()

@main.command()
@click.pass_context
def status(ctx):
    """Get the status of your CrunchR container."""
    get_status(ctx)

@main.group()
@click.pass_context
def enhance(ctx):
    """Enhance your CrunchR container."""

@enhance.command('shell')
@click.pass_context
def enhance_shell(ctx):
    """Enhance your CrunchR shell."""
    run_enhance_shell(ctx)

@enhance.command('rstudio_keybindings')
@click.pass_context
def https_sync(ctx):
    """Install enhanced RStudio keybindings."""
    run_install_rstudio_keybindings(ctx)

if __name__ == '__main__':
    main(obj={})
