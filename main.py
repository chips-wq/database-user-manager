import click
from typing import Dict, Type
from databases.base import DatabaseStrategy
from databases.mongodb_strategy import MongoDBStrategy

class DatabaseFactory:
    _strategies: Dict[str, Type[DatabaseStrategy]] = {
        "mongo": MongoDBStrategy
    }

    @classmethod
    def create(cls, db_type: str, connection_string: str) -> DatabaseStrategy:
        strategy_class = cls._strategies.get(db_type.lower())
        if not strategy_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        return strategy_class(connection_string)


@click.command()
@click.option(
    '--db-type',
    type=click.Choice(['mongo'], case_sensitive=False),
    prompt='Database type',
    help='Type of database to configure (mongo)'
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
def main(db_type: str, connection_string: str, username: str, password: str):
    """Create database user and generate connection string."""
    try:
        strategy = DatabaseFactory.create(db_type, connection_string)
        strategy.create_user_and_db(username, password)
        user_conn_string = strategy.get_connection_string(username, password)
        click.echo(f"Connection string: {user_conn_string}")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

if __name__ == "__main__":
    main()