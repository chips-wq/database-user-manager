import click
import logging
from databases.factory import DatabaseFactory

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

SUPPORTED_DATABASES = ['mongo', 'mysql', 'postgresql']

@click.group()
def cli():
    """Database management utilities."""
    pass

@cli.command(name='create')
@click.option(
    '--db-type',
    type=click.Choice(SUPPORTED_DATABASES, case_sensitive=False),
    prompt='Database type',
    help=f'Type of database to configure ({','.join(SUPPORTED_DATABASES)})'
)
@click.option(
    '--connection-string',
    prompt='Admin connection string',
    help='Admin connection string for the database'
)
@click.option(
    '--username',
    prompt=True,
    help='Database username to create'
)
@click.option(
    '--password',
    prompt=True,
    hide_input=True,
    confirmation_prompt=True,
    help='Password for the database user'
)
def create_user(db_type: str, connection_string: str, username: str, password: str):
    """Create database user and generate connection string."""
    try:
        strategy = DatabaseFactory.create(db_type, connection_string)
        strategy.ensure_user_and_db(username, password)
        user_conn_string = strategy.get_connection_string(username, password)
        click.echo(f"Connection string: {user_conn_string}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command(name='verify')
@click.option(
    '--db-type',
    type=click.Choice(SUPPORTED_DATABASES, case_sensitive=False),
    prompt='Database type',
    help=f'Type of database to configure ({','.join(SUPPORTED_DATABASES)})'
)
@click.option(
    '--connection-string',
    prompt='Connection string',
    help='Connection string to verify'
)
def verify_connection(db_type: str, connection_string: str):
    """Verify if a connection string is valid by attempting to connect."""
    try:
        strategy = DatabaseFactory.create(db_type, connection_string)
        if strategy.test_connection():
            click.echo(click.style("✓ Connection successful!", fg="green"))
        else:
            click.echo(click.style("✗ Connection failed!", fg="red"))
            raise click.Abort()
    except Exception as e:
        click.echo(click.style(f"✗ Error: {str(e)}", fg="red"), err=True)
        raise click.Abort()

if __name__ == "__main__":
    cli()