import click
from rpy2.rinterface_lib.callbacks import logger as rpy2_logger
import logging
import rpy2.robjects.packages as rpackages

rpy2_logger.setLevel(logging.ERROR)
keyring = rpackages.importr("keyring")


def user_has_jhed_password(jhed_username):
    try:
        keyring.key_get("jhed", jhed_username)
        return True
    except:
        return False


def unlock_keyring():
    click.secho("🔐 Unlock your keyring to proceed.", bg="white", fg="red", bold=True)
    try:
        keyring.keyring_unlock()
    except Exception as e:
        click.secho("💣 Failed to unlock the keyring. Aborting.", fg="red", bold=True)
        exit(1)


def keyring_is_locked():
    return keyring.keyring_is_locked()[0]


def get_password(username):
    return keyring.key_get("jhed", username)
