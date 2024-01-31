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

    click.secho("✅ Done. Template:\n", fg="green")
    click.echo(kerberos_auth)

    click.secho(
        "\n📁 Copied rendered auth file to /temporary/placeholder/kerberos_auth.txt",
        fg="green",
    )
    click.secho("📁 Copied driver files to /temporary/placeholder/", fg="green")
