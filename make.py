import click
from jinja2 import Template


def make_kerberos_auth(ctx):
    realm = click.prompt("Enter the realm.", default="WIN.AD.JHU.EDU")
    kdc = click.prompt(
        "Enter the key distribution cluster (KDC.", default="ESGWINMTW6.WIN.AD.JHU.EDU"
    )

    with open("resources/stubs/kerberos_auth.txt", "r") as f:
        template = Template(f.read())

    kerberos_auth = template.render(realm=realm, kdc=kdc)

    click.secho("✅  Done. Template:\n", fg="green")
    click.echo(kerberos_auth)

    click.secho(
        "\n📁  Copied rendered auth file to /temporary/placeholder/kerberos_auth.txt",
        fg="green",
    )
    click.secho("📁  Copied driver files to /temporary/placeholder/", fg="green")


def make_dbi_connect(ctx):
    pass

def run_select_make_options(ctx, option):
    if option:
        if option == "dbi-connect":
            choice = "1"
        elif option == "kerberos":
            choice = "2"
        else:
            click.secho("Invalid option.", fg="red", bold=True)
            exit(1)
    else:
        click.secho("🔨  Generate code from templates\n", fg="green", bold=True)
        click.secho("Select from one of the below options:\n", fg="green")
        click.secho("(1) Make an ODBC DBI connection file", fg="white")
        click.secho("(2) Scaffold Kerberos authentication", fg="white")
        click.secho("(3) Cancel\n", fg="white")
        choice = click.prompt(
            "Enter your choice", type=click.Choice(["1", "2", "3", "4"])
        )

    if choice == "1":
        make_dbi_connect()
    elif choice == "2":
        make_kerberos_auth()
    elif choice == "3":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)
    else:
        exit(0)