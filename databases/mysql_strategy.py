import mysql.connector
from mysql.connector import Error as MySQLError
from .base import DatabaseStrategy
from dataclasses import dataclass
from urllib.parse import urlparse, parse_qs
import logging

logger = logging.getLogger(__name__)

# MySQL specific error codes
USER_ALREADY_EXISTS_CODE = 1396
DB_ALREADY_EXISTS_CODE = 1007

@dataclass
class MySQLConfig:
    host: str
    port: int = 3306
    user: str = 'root'
    password: str = ''

class MySQLStrategy(DatabaseStrategy):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.config = self._parse_connection_string(connection_string)
        self.connection = self._create_connection()
        if not self.test_connection():
            raise MySQLError("Failed to connect to MySQL")

    def _create_connection(self):
        return mysql.connector.connect(
            host=self.config.host,
            port=self.config.port,
            user=self.config.user,
            password=self.config.password
        )

    def test_connection(self) -> bool:
        try:
            if self.connection and self.connection.is_connected():
                return True
            return False
        except MySQLError:
            return False

    def ensure_user_and_db(self, username: str, password: str) -> None:
        try:
            db_name = self._generate_db_name(username)
            cursor = self.connection.cursor()
            
            # Create database if not exists
            try:
                logger.info(f"Ensuring database '{db_name}' exists")
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
                logger.debug(f"Database '{db_name}' is ready")
            except MySQLError as e:
                if e.errno != DB_ALREADY_EXISTS_CODE:
                    logger.error(f"Failed to create database '{db_name}': {str(e)}")
                    raise
                logger.info(f"Database '{db_name}' already exists")
            
            # Try to create user
            try:
                logger.info(f"Creating new user '{username}' with access to database '{db_name}'")
                # MySQL 8+ syntax for creating users
                cursor.execute(f"CREATE USER '{username}'@'%' IDENTIFIED BY '{password}'")
                logger.info(f"Successfully created user '{username}'")
            except MySQLError as e:
                if e.errno == USER_ALREADY_EXISTS_CODE:
                    logger.info(f"User '{username}' already exists, updating password")
                    cursor.execute(f"ALTER USER '{username}'@'%' IDENTIFIED BY '{password}'")
                    logger.info(f"Successfully updated password for user '{username}'")
                else:
                    logger.error(f"Failed to manage user '{username}': {str(e)}")
                    raise

            # Grant privileges
            try:
                cursor.execute(f"GRANT ALL PRIVILEGES ON `{db_name}`.* TO '{username}'@'%'")
                cursor.execute("FLUSH PRIVILEGES")
                logger.info(f"Granted privileges on '{db_name}' to '{username}'")
            except MySQLError as e:
                logger.error(f"Failed to grant privileges: {str(e)}")
                raise

            # Clean up
            cursor.close()
            
        except MySQLError as e:
            logger.error(f"Operation failed for user '{username}': {str(e)}")
            raise Exception(f"Failed to ensure user: {str(e)}")

    def get_connection_string(self, username: str, password: str) -> str:
        db_name = self._generate_db_name(username)
        return f"mysql://{username}:{password}@{self.config.host}:{self.config.port}/{db_name}"

    def _generate_db_name(self, username: str) -> str:
        return f"db_{username}"

    def _parse_connection_string(self, connection_string: str) -> MySQLConfig:
        try:
            parsed = urlparse(connection_string)
            query_params = parse_qs(parsed.query)
            
            return MySQLConfig(
                host=parsed.hostname or "localhost",
                port=parsed.port or 3306,
                user=parsed.username or "root",
                password=parsed.password or ""
            )
        except Exception as e:
            raise ValueError(f"Invalid connection string format: {str(e)}")