from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure
from .base import DatabaseStrategy
from dataclasses import dataclass
from urllib.parse import urlparse

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

    def create_user_and_db(self, username: str, password: str) -> None:
        try:
            db_name = self._generate_db_name(username)
            self.client[db_name].command(
                "createUser",
                username,
                pwd=password,
                roles=[{"role": "dbOwner", "db": db_name}]
            )
        except OperationFailure as e:
            raise Exception(f"Failed to create user: {str(e)}")

    def get_connection_string(self, username: str, password: str) -> str:
        return (f"mongodb://{username}:{password}@"
                f"{self.config.host}:{self.config.port}")

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