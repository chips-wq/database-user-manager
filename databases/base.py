from abc import ABC, abstractmethod

class DatabaseStrategy(ABC):
    @abstractmethod
    def __init__(self, connection_string: str):
        pass

    @abstractmethod
    def ensure_user_and_db(self, username: str, password: str) -> None:
        pass

    @abstractmethod
    def get_connection_string(self, username: str, password: str) -> str:
        pass

    @abstractmethod
    def test_connection(self) -> bool:
        pass