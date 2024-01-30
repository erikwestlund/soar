import click

class Configure:
    def __init__(self):
        pass

    def run(self):
        click.clear()
        jhed = click.prompt("Enter your JHED (without @jh.edu)")
        github_username = click.prompt("Enter your GitHub username")
        github_email = click.prompt("Enter the email address associated with your GitHub username")
        click.echo("Set your JHED to " + jhed)
        click.echo("Set your GitHub Username to " + github_username)
        click.echo("Set your GitHub Email to " + github_email)
