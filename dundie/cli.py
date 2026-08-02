import json

import importlib.metadata
import rich_click as click
from rich.console import Console
from rich.table import Table

from dundie import core

click.rich_click.TEXT_MARKUP = True
click.rich_click.TEXT_MARKUP = True
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True
click.rich_click.OPTIONS_TABLE_COLUMN_TYPES = False
click.rich_click.OPTIONS_TABLE_HELP_SECTIONS = True


@click.group()
@click.version_option(importlib.metadata.version("dundie"))
def main():
    """Dundier MIfflin Rewards System
    This CLI application controls DM rewards
    """


@main.command()
@click.argument("filepath", type=click.Path(exists=True))
@click.option("--user", prompt=True, help="Admin username/email")
@click.option("--password", prompt=True, hide_input=True, help="Admin password")
def load(filepath, user, password):
    """Load the file to the database (Protected by Admin Auth)."""
    db = core.connect()
    # Se houver usuários cadastrados, valida autenticação. Se for primeira carga, aceita credencial inicial.
    if db.get("users") and not core.authenticate_user(db, user, password):
        print("Error: Invalid admin credentials.")
        raise click.Abort()

    table = Table(title="Dundie Mifflin Associates")
    headers = ["name", "dept", "role", "created", "e-mail"]
    for header in headers:
        table.add_column(header, style="magenta")

    result = core.load(filepath)
    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--output", default=None)
def show(output, **query):
    """Shows information about users"""
    result = core.read(**query)
    if output:
        with open(output, "w") as output_file:
            output_file.write(json.dumps(result))

    if not result:
        print("Nothing to show")
        return

    table = Table(title="Dundie Mifflin Report")
    for key in result[0]:
        table.add_column(key.title(), style="magenta")

    for person in result:
        table.add_row(*[str(value) for value in person.values()])

    console = Console()
    console.print(table)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--email", required=False)
@click.option("--dept", required=False)
@click.option("--user", prompt=True, help="Admin username/email")
@click.option("--password", prompt=True, hide_input=True, help="Admin password")
@click.pass_context
def add(ctx, value, user, password, **query):
    """Add points to the user or dept (Protected by Admin Auth)."""
    db = core.connect()
    if not core.authenticate_user(db, user, password):
        print("Error: Invalid admin credentials.")
        raise click.Abort()

    core.add(value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.argument("value", type=click.INT, required=True)
@click.option("--dept", required=False)
@click.option("--email", required=False)
@click.option("--user", prompt=True, help="Admin username/email")
@click.option("--password", prompt=True, hide_input=True, help="Admin password")
@click.pass_context
def remove(ctx, value, user, password, **query):
    """Remove points from user or dept (Protected by Admin Auth)."""
    db = core.connect()
    if not core.authenticate_user(db, user, password):
        print("Error: Invalid admin credentials.")
        raise click.Abort()

    core.add(-value, **query)
    ctx.invoke(show, **query)
