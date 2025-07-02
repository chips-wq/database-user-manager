from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from .base import DatabaseStrategy
from dataclasses import dataclass
from urllib.parse import urlparse
import logging

logger = logging.getLogger(__name__)

# MongoDB specific error codes
USER_ALREADY_EXISTS_CODE = 51003
USER_ALREADY_EXISTS_MSG = "already exists"

@dataclass
class MongoDBConfig:
    host: str
    port: int
    auth_database: str = 'admin'

class MongoDBStrategy(DatabaseStrategy):
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.client = MongoClient(connection_string)
        self.config = self._parse_connection_string(connection_string)
        if not self.test_connection():
            raise ConnectionFailure("Failed to connect to MongoDB")

    def test_connection(self) -> bool:
        try:
            self.client.admin.command('ping')
            return True
        except ConnectionFailure:
            return False

    def ensure_user_and_db(self, username: str, password: str) -> None:
        try:
            db_name = self._generate_db_name(username)
            try:
                logger.info(f"Creating new user '{username}' with database '{db_name}'")
                # Create user in admin database with specific permissions
                self.client.admin.command(
                    "createUser",
                    username,
                    pwd=password,
                    roles=[
                        {"role": "readWrite", "db": db_name},
                    ]
                )
                logger.info(f"Successfully created user '{username}'")
            except OperationFailure as e:
                if e.code == USER_ALREADY_EXISTS_CODE:
                    # Additional validation of error message
                    assert USER_ALREADY_EXISTS_MSG in str(e.details['errmsg']), \
                        f"Unexpected error message for code {USER_ALREADY_EXISTS_CODE}: {e.details}"
                    logger.info(f"User '{username}' already exists, updating password and roles")
                    # Update existing user
                    self.client.admin.command(
                        "updateUser",
                        username,
                        pwd=password,
                        roles=[
                            {"role": "readWrite", "db": db_name},
                        ]
                    )
                    logger.info(f"Successfully updated user '{username}'")
                else:
                    logger.error(f"Failed to manage user '{username}': {str(e)}")
                    raise

            # Ensure database exists
            logger.debug(f"Ensuring database '{db_name}' exists")
            self.client[db_name].test.insert_one({"_id": "init"})
            self.client[db_name].test.delete_one({"_id": "init"})
            logger.debug(f"Database '{db_name}' is ready")

        except OperationFailure as e:
            logger.error(f"Operation failed for user '{username}': {str(e)}")
            raise Exception(f"Failed to ensure user: {str(e)}")

    def get_connection_string(self, username: str, password: str) -> str:
        db_name = self._generate_db_name(username)
        return (f"mongodb://{username}:{password}@"
                f"{self.config.host}:{self.config.port}/{db_name}?authSource=admin")

    def _generate_db_name(self, username: str) -> str:
        return f"db_{username}"

    def _parse_connection_string(self, connection_string: str) -> MongoDBConfig:
        try:
            parsed = urlparse(connection_string)
            return MongoDBConfig(
                host=parsed.hostname,
                port=parsed.port or 27017
            )
        except Exception as e:
            raise ValueError(f"Invalid connection string format: {str(e)}")
