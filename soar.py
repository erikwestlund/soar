import click

@click.group("setup")
@click.pass_context
def setup(ctx, command):
   """Tools for making CrunchR soar"""
   click.echo("Installing R packages...")

@click.group("configure")
@click.pass_context
def configure(ctx, command):
   """Configure your CrunchR instance"""
   click.echo("Configuring...")

def main():
   setup(prog_name="setup")

if __name__ == '__main__':
   main()
