from motor.core import AgnosticClient, AgnosticDatabase
from ..config import settings

class DataBase:
    client: AgnosticClient = None

db = DataBase()


def get_database() -> AgnosticDatabase:
    return db.client[settings.DATABASE_NAME]