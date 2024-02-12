import logging

import click
import rpy2.robjects.packages as rpackages
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger

rpy2_logger.setLevel(logging.ERROR)
keyring = rpackages.importr("keyring")
nrow = rpackages.importr("base").nrow


def get_keyring_exists():
    return nrow(keyring.key_list())[0] > 0


def get_password(keyring_name, username):
    try:
        return keyring.key_get(keyring_name, username)[0]
    except:
        return None


def keyring_is_locked():
    return keyring.keyring_is_locked()[0]


def set_keyring_password(keyring_name, username, password):
    if not keyring_name or not username or not password:
        click.secho(
            "💣  Missing keyring name, username, or password.",
            fg="red",
            bold=True,
        )
        click.secho("Keyring has not been updated.", fg="red", bold=True)
        return None

    if keyring_is_locked():
        unlock_keyring()

    keyring.key_set_with_value(keyring_name, username, password)


def unlock_keyring():
    keyring_exists = get_keyring_exists()

    if keyring_exists:
        click.secho(
            "🔐  Unlock your keyring to proceed.", bg="white", fg="red", bold=True
        )
    else:
        click.secho(
            "The Keyring is used to securely store credentials.",
            bg="white",
            fg="red",
            bold=True,
        )
        click.secho(
            "Enter a password to unlock your keying. This should be different from your JHED.\n",
            bg="white",
            fg="red",
            bold=True,
        )

    try:
        keyring.keyring_unlock()
    except Exception as e:
        click.secho("💣  Failed to unlock the keyring. Aborting.", fg="red", bold=True)
        click.secho(
            'If you cannot remember your password, rRun "soar reset-keyring" to delete your \nkeyring and start over. Your saved credentials will be lost.',
            fg="red",
            bold=True,
        )
        exit(1)


def user_has_jhed_password(jhed_username):
    try:
        keyring.key_get("jhed", jhed_username)
        return True
    except:
        return False


def user_has_github_pat(github_username):
    try:
        keyring.key_get("github", github_username)
        return True
    except:
        return False
