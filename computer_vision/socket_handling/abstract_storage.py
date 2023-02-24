import sqlite3

from abc import (ABC, abstractmethod,)

class abstract_storage(ABC):
    @abstractmethod
    def __init__(self, db_name: str):
        pass
    
    @abstractmethod
    def add_log(self, pos: int, sensor_type: int, value: int, timestamp=0):
        pass

    @abstractmethod
    def create_project_tables(self):
        pass

    @abstractmethod
    def get_sensor_data(self, pos: int, sensor_type: int):
        pass

    @abstractmethod
    def get_recent_sensor_data(self):
        pass

