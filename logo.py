import click


def print_logo():
    """Print the Crunchr logo."""
    click.secho("")
    click.secho("   _____                    ", fg="blue")
    click.secho("  / ___/ ____   ____ _ _____", fg="blue")
    click.secho("  \__ \ / __ \ / __ `// ___/", fg="blue")
    click.secho(" ___/ // /_/ // /_/ // /    ", fg="blue")
    click.secho("/____/ \____/ \__,_//_/     ", fg="blue")
    click.secho("\n")
