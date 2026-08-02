import importlib.metadata
import json

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
@click.option(
    "--password", prompt=True, hide_input=True, help="Admin password"
)
def load(filepath, user, password):
    """Load the file to the database (Protected by Admin Auth)."""
    db = core.connect()
    # Se houver usuários cadastrados, valida autenticação.
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
@click.option(
    "--password", prompt=True, hide_input=True, help="Admin password"
)
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
@click.option(
    "--password", prompt=True, hide_input=True, help="Admin password"
)
@click.pass_context
def remove(ctx, value, user, password, **query):
    """Remove points from user or dept (Protected by Admin Auth)."""
    db = core.connect()
    if not core.authenticate_user(db, user, password):
        print("Error: Invalid admin credentials.")
        raise click.Abort()

    core.add(-value, **query)
    ctx.invoke(show, **query)


@main.command()
@click.option("--user", prompt=True, help="Employee email")
@click.option("--password", prompt=True, hide_input=True, help="Password")
def balance(user, password):
    """View current points balance (Issue #5)."""
    db = core.connect()
    if not core.authenticate_user(db, user, password):
        print("Error: Invalid credentials.")
        raise click.Abort()

    bal = core.get_balance(db, user)
    console = Console()
    console.print(
        f"[bold green]Current Balance for {user}:[/bold green] {bal} points"
    )


@main.command()
@click.option("--user", prompt=True, help="Employee email")
@click.option("--password", prompt=True, hide_input=True, help="Password")
def statement(user, password):
    """View movements statement (Issue #5)."""
    db = core.connect()
    if not core.authenticate_user(db, user, password):
        print("Error: Invalid credentials.")
        raise click.Abort()

    movements = core.get_movements(db, user)
    table = Table(title=f"Statement for {user}")
    table.add_column("Date", style="cyan")
    table.add_column("Actor", style="magenta")
    table.add_column("Value", style="green")

    for mov in movements:
        table.add_row(mov["date"], mov["actor"], str(mov["value"]))

    console = Console()
    console.print(table)


@main.command()
@click.argument("to_email", type=click.STRING)
@click.argument("amount", type=click.INT)
@click.option("--user", prompt=True, help="Sender email")
@click.option(
    "--password", prompt=True, hide_input=True, help="Sender password"
)
def transfer(to_email, amount, user, password):
    """Transfer points to another employee (Issue #6)."""
    db = core.connect()
    success, msg = core.transfer_points(db, user, password, to_email, amount)
    if not success:
        print(f"Error: {msg}")
        raise click.Abort()

    console = Console()
    console.print(f"[bold green]Success:[/bold green] {msg}")
