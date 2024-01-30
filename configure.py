import click
import keyring
import os


def set_credentials(self):
    jhed_username = click.prompt("Enter your JHED (without @jh.edu)")
    jhed_password = click.prompt(
        "Enter your JHED password (your password will be securely stored in the system credential manager)",
        hide_input=True,
    )
    github_username = click.prompt("Enter your GitHub username")
    github_email = click.prompt(
        "Enter the email address associated with your GitHub username"
    )

    set_jhed_username(jhed_username)
    set_keyring_password(jhed_username, jhed_password)
    set_github_username(github_username)
    set_github_email(github_email)


def set_jhed_username(self, jhed_username):
    os.environ["user_jhed"] = jhed_username
    click.secho("Set your JHED username to " + jhed_username, fg="green")


def set_keyring_password(self, jhed_username, jhed_password):
    keyring.set_password("jhed", jhed_username, jhed_password)
    click.secho(
        "Stored your JHED password in the system credential manager", fg="green"
    )


def set_github_username(self, github_username):
    os.environ["github_username"] = github_username
    click.secho("Set your GitHub username to " + github_username, fg="green")


def set_github_email(self, github_email):
    os.environ["github_email"] = github_email
    click.secho("Set your GitHub email to " + github_email, fg="green")
