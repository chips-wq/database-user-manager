from abc import ABC, abstractmethod

class DatabaseStrategy(ABC):
    @abstractmethod
    def create_user_and_db(self, username, user_password):
        """
        Create a user and a corresponding database named `db_<username>`,
        or ensure the user exists and has the necessary privileges.
        """
        pass

    @abstractmethod
    def get_connection_string(self, username, user_password):
        """
        Return the connection string for this database.
        """
        pass