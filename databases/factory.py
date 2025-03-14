from typing import Dict, Type
from databases.base import DatabaseStrategy
from databases.mongodb_strategy import MongoDBStrategy
from databases.mysql_strategy import MySQLStrategy
from databases.postgresql_strategy import PostgreSQLStrategy

class DatabaseFactory:
    _strategies: Dict[str, Type[DatabaseStrategy]] = {
        "mongo": MongoDBStrategy,
        "mysql": MySQLStrategy,
        "postgresql": PostgreSQLStrategy
    }

    @classmethod
    def create(cls, db_type: str, connection_string: str) -> DatabaseStrategy:
        strategy_class = cls._strategies.get(db_type.lower())
        if not strategy_class:
            raise ValueError(f"Unsupported database type: {db_type}")
        return strategy_class(connection_string)
