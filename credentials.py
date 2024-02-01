import logging
import os

import click
import rpy2.robjects.packages as rpackages
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger

rpy2_logger.setLevel(logging.ERROR)
keyring = rpackages.importr("keyring")


def get_password(username):
    try:
        return keyring.key_get("jhed", username)[0]
    except:
        return None


def keyring_is_locked():
    return keyring.keyring_is_locked()[0]


def set_keyring_password(jhed_username, jhed_password):
    keyring.key_set_with_value("jhed", jhed_username, jhed_password)


def unlock_keyring():
    click.secho("🔐 Unlock your keyring to proceed.", bg="white", fg="red", bold=True)
    click.secho(
        "If this is your first time, pick a password different from your JHED's.",
        bg="white",
        fg="red",
        bold=True,
    )
    try:
        keyring.keyring_unlock()
    except Exception as e:
        click.secho("💣 Failed to unlock the keyring. Aborting.", fg="red", bold=True)
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
