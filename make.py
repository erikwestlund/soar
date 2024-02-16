import click
from config import get_project_templates_library_dir
from jinja2 import Template
from project import has_project_of_type, get_project_config
import prompt


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


def make_dbi_connect():
    if has_project_of_type("pmap"):
        click.secho("\n🗂️  Generate a DBI connection file\n", fg="green", bold=True)

        click.secho("(1) Generate for a PMAP project.", fg="white")
        click.secho("(2) Enter arbitrary values.", fg="white")
        click.secho("(3) Cancel\n", fg="white")
        choice = click.prompt("Enter your choice", type=click.Choice(["1", "2", "3"]))

        if choice == "1":
            return generate_dbi_for_pmap_project()


    port = prompt.db_port()
    driver = prompt.odbc_db_driver()
    server = prompt.db_server("win.jhu.edu")
    database = prompt.projection_db_name("table_name")
    tds_version = prompt.free_tds_version()

    values = {
        "port": port,
        "driver": f"\"{driver}\"",
        "server": f"\"{server}\"",
        "database": f"\"{database}\"",
        "tds_version": f"\"{tds_version}\"",
    }

    template = render_dbi_connect_template(values, print=True)
    save_template_to_file("DBI Connection", template, f"dbi_connect_{database}.R", print=True)


def generate_dbi_for_pmap_project():
    click.secho("\nSelect a PMAP Project\n", fg="green", bold=True)

    project_name = prompt.existing_project(project_type="pmap")

    values = {
        "project_name": project_name,
        "port": "project_settings$db_port",
        "driver": "project_settings$db_driver",
        "server": "project_settings$db_server",
        "database": "project_settings$projection_name",
        "tds_version": "project_settings$free_tds_version",
    }

    template = render_dbi_connect_template(values, print=True)
    save_template_to_file("DBI Connection", template, f"dbi_connect_{project_name}.R", print=True)



def save_template_to_file(name, template, filename, print=False):
    path = f"{get_project_templates_library_dir()}/{filename}"

    with open(path, "w") as f:
        f.write(template)

    if print:
        click.secho(f"\n{name} template saved to:\n", fg="green")
        click.secho(f"{path}", fg="white")


def render_dbi_connect_template(values, print=False):
    with open("resources/stubs/dbi_connection.R.j2", "r") as f:
        template = Template(f.read())

    template_string = template.render(
        project=values["project_name"] if "project_name" in values else None,
        port=values["port"],
        driver=values["driver"],
        server=values["server"],
        database=values["database"],
        tds_version=values["tds_version"],
    )

    if print:
        click.secho("\nTemplate:\n", fg="green")
        click.echo(template_string)

    return template_string



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
        choice = click.prompt("Enter your choice", type=click.Choice(["1", "2", "3"]))

    if choice == "1":
        make_dbi_connect()
    elif choice == "2":
        make_kerberos_auth()
    elif choice == "3":
        click.secho("Cancelled.", fg="red", bold=True)
        exit(1)
    else:
        exit(0)
