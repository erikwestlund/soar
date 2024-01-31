import click
from configure import get_config
from credentials import get_password, unlock_keyring, keyring_is_locked, user_has_jhed_password, set_keyring_password


def run_mount_home(ctx):
    config = get_config()

    if not config["default"]["jhed_username"]:
        click.secho("JHED username not set. Run configure before proceeding.", fg="red", bold=True)

    if keyring_is_locked():
        unlock_keyring()
        click.secho("Unlocked the keyring.", fg="green")

    jhed_password_set = user_has_jhed_password(config["default"]["jhed_username"])
    if not jhed_password_set:
        jhed_password = click.prompt("Enter your JHED password", hide_input=True)

        if jhed_password != "":
            set_keyring_password(config["default"]["jhed_username"], jhed_password)
    else:
        jhed_password = get_password(config["default"]["jhed_username"])

    string = f"sudo mount -t cifs -o //mtwfs.nas.jh.edu/HOME/ /home/idies/workspace/HOME/ -o username={config['default']['jhed_username']},workgroup=win,uid=idies,password={jhed_password}"

    print(string)
