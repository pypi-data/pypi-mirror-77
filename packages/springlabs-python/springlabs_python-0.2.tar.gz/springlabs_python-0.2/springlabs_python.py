import click
import time
import os
import re
from utils import createDjangoProject


def validate_name(ctx, param, value):
    """
        Función que valida si nommbre del proyecto se encuentra en formato correcto
    """
    namesNoValid = ["api", "core", "graphql_api", "tests", "models_app"]
    validName = re.compile(
        r"^(?=.{8,20}$)(?![_])(?!.*[_]{2})[a-z0-9_]+(?<![_])$")
    if validName.search(value) == None:
        message = "The project name should only contain lowercase letters,numbers,underscores"
        raise click.BadParameter(message)
    if value in namesNoValid:
        raise click.BadParameter(
            f"The project name can't be called such as one of the following list {namesNoValid}")
    return value


def validate_database(ctx, param, value):
    """
        Función que valida que opciones de database sean adecuadas según el
        framework:
        Django  ->  (postgres, mysql)
        Flask   ->  (mongo)
    """
    db_accepted_flask = ["mongo", ]
    db_accepted_django = ["postgres", "mysql"]
    if ctx.params['framework'] == "Django":
        if value in db_accepted_django:
            return value
        else:
            message = f"invalid choice from framework Django: {value}"
            possibilities = db_accepted_django
    elif ctx.params['framework'] == "Flask":
        if value in db_accepted_flask:
            return value
        else:
            message = f"invalid choice from framework Flask: {value}"
            possibilities = db_accepted_flask

    raise click.NoSuchOption(
        option_name="option_name", message=message, possibilities=possibilities)


@click.group(invoke_without_command=False)
@click.version_option(version="1.0", prog_name="Springlabs Manager", message="%(prog)s, v%(version)s")
@click.pass_context
def cli(ctx):
    """Springlabs Manager projects."""
    ctx.invoked_subcommand


@cli.command()
@click.option('-fw', '--framework',
              prompt='Framework a utilizar',
              default="Django",
              show_default=True,
              type=click.Choice(['Django', 'Flask'], case_sensitive=False),
              help='Python Framework to use')
@click.option('-db', '--database',
              prompt='Database a utilizar',
              default="postgres",
              show_default=True,
              type=click.Choice(
                  ['postgres', 'mysql', 'mongo'], case_sensitive=False),
              help='Database engine to use',
              callback=validate_database)
@click.option('-d', '--diseno',
              prompt='Diseño de database a utilizar',
              default="logico",
              show_default=True,
              type=click.Choice(
                  ['logico', 'fisico'], case_sensitive=False),
              help='Database design to use')
@click.option('-n', '--name',
              prompt='Project Name',
              help='Project Name',
              callback=validate_name)
def create_project(framework, database, name, diseno):
    """ Create a new Python project """
    if framework == "Django":
        message, result = createDjangoProject(
            name=name, database=database, design=diseno)
        if result == True:
            message = f"Se creó proyecto {framework}-{database}({diseno}) [{name}] correctamente"
            click.echo(message)
        else:
            click.echo("Error: " + message)


if __name__ == '__main__':
    cli()
