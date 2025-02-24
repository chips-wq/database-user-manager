from pymongo import MongoClient
from pymongo.errors import OperationFailure
from .base import DatabaseStrategy

class MongoDBStrategy(DatabaseStrategy):
    def __init__(self, admin_uri="mongodb://admin:password@localhost:27017/"):
        self.client = MongoClient(admin_uri)
        self.admin_db = self.client['admin']
        self.host = "localhost"
        self.port = 27017

    def create_user_and_db(self, username, user_password):
        db_name = f"db_{username}"
        try:
            # Check if the user already exists.
            user_info = self.admin_db.command("usersInfo", username)
            if user_info.get("users"):
                # If user exists, update the roles if necessary.
                roles = user_info["users"][0].get("roles", [])
                if not any(r.get("role") == "dbOwner" and r.get("db") == db_name for r in roles):
                    self.admin_db.command("updateUser", username, roles=[{'role': 'dbOwner', 'db': db_name}])
                    print(f"MongoDB: Updated user '{username}' with role 'dbOwner' on '{db_name}'.")
                else:
                    print(f"MongoDB: User '{username}' already exists with the correct role on '{db_name}'.")
            else:
                # Create new user if not exists.
                self.admin_db.command(
                    'createUser', username,
                    pwd=user_password,
                    roles=[{'role': 'dbOwner', 'db': db_name}]
                )
                print(f"MongoDB: User '{username}' created with access to database '{db_name}'.")
        except OperationFailure as e:
            print(f"MongoDB: Error creating or updating user: {e}")

    def get_connection_string(self, username, user_password):
        db_name = f"db_{username}"
        return f"mongodb://{username}:{user_password}@{self.host}:{self.port}/{db_name}"
