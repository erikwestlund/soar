import click

class Configure:
    def __init__(self):
        pass

    def run(self):
        jhed = click.prompt("Enter your JHED (without @jh.edu)")
        github_username = click.prompt("Enter your GitHub username")
        github_email = click.prompt("Enter the email address associated with your GitHub username")
        click.secho("Set your JHED to " + jhed, fg="green")
        click.secho("Set your GitHub Username to " + github_username, fg="green")
        click.secho("Set your GitHub Email to " + github_email, fg="green")
