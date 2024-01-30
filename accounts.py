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
