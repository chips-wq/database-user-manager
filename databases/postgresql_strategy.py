import psycopg2
from psycopg2 import errors
from .base import DatabaseStrategy
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

# PostgreSQL specific error codes
DUPLICATE_DATABASE_ERROR = '42P04'
DUPLICATE_OBJECT_ERROR = '42710'

@dataclass
class PostgreSQLConfig:
    host: str
    port: int = 5432
    user: str = 'postgres'
    password: str = ''
    database: str = 'postgres'  # Default database to connect to

class PostgreSQLStrategy(DatabaseStrategy):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.config = self._parse_connection_string(connection_string)
        self.connection = self._create_connection()
        if not self.test_connection():
            raise psycopg2.OperationalError("Failed to connect to PostgreSQL")

    def _create_connection(self):
        return psycopg2.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database
        )

    def test_connection(self) -> bool:
        try:
            if self.connection:
                cursor = self.connection.cursor()
                cursor.execute("SELECT 1")
                cursor.close()
                return True
            return False
        except psycopg2.Error:
            return False

    def ensure_user_and_db(self, username: str, password: str) -> None:
        try:
            db_name = self._generate_db_name(username)
            
            # Create a fresh connection with autocommit already enabled
            # This avoids the "set_session cannot be used inside a transaction" error
            conn = psycopg2.connect(
                host=self.config.host,
                port=self.config.port,
                user=self.config.user,
                password=self.config.password,
                database=self.config.database
            )
            conn.autocommit = True
            cursor = conn.cursor()
            
            # Create user if not exists (PostgreSQL doesn't have direct IF NOT EXISTS for users)
            try:
                logger.info(f"Creating new user '{username}'")
                cursor.execute(f"CREATE USER {username} WITH PASSWORD '{password}'")
                logger.info(f"Successfully created user '{username}'")
            except psycopg2.errors.DuplicateObject:
                logger.info(f"User '{username}' already exists, updating password")
                cursor.execute(f"ALTER USER {username} WITH PASSWORD '{password}'")
                logger.info(f"Successfully updated password for user '{username}'")
            
            # Create database if not exists
            try:
                logger.info(f"Ensuring database '{db_name}' exists")
                cursor.execute(f"CREATE DATABASE {db_name} OWNER {username}")
                logger.debug(f"Database '{db_name}' is ready")
            except psycopg2.errors.DuplicateDatabase:
                logger.info(f"Database '{db_name}' already exists")
                # Ensure the owner is correct
                cursor.execute(f"ALTER DATABASE {db_name} OWNER TO {username}")
                logger.debug(f"Updated owner for database '{db_name}'")
            
            # Grant privileges (if needed)
            cursor.execute(f"GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {username}")
            logger.info(f"Granted privileges on '{db_name}' to '{username}'")
            
            # Clean up
            cursor.close()
            conn.close()
            
        except psycopg2.Error as e:
            logger.error(f"Operation failed for user '{username}': {str(e)}")
            raise Exception(f"Failed to ensure user: {str(e)}")

    def get_connection_string(self, username: str, password: str) -> str:
        db_name = self._generate_db_name(username)
        return f"postgresql://{username}:{password}@{self.config.host}:{self.config.port}/{db_name}"

    def _generate_db_name(self, username: str) -> str:
        return f"db_{username}"

    def _parse_connection_string(self, connection_string: str) -> PostgreSQLConfig:
        try:
            parsed = urlparse(connection_string)
            query_params = parse_qs(parsed.query)
            
            return PostgreSQLConfig(
                host=parsed.hostname or "localhost",
                port=parsed.port or 5432,
                user=parsed.username or "postgres",
                password=parsed.password or "",
                database=parsed.path.lstrip('/') if parsed.path else "postgres"
            )
        except Exception as e:
            raise ValueError(f"Invalid connection string format: {str(e)}")
