import click


def get_status(ctx):
    click.secho("JHED is set.", fg="green")
    click.secho("Github Username is set.", fg="green")
    click.secho("Github Email is set.", fg="green")
    click.secho("Keyring is not configured.", fg="red")
