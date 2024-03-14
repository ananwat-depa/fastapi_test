from app.main import app
from app.db.mongodb_util import connect_to_mongo, close_mongo_connection
from app.db.mongodb import db
from app.config import get_settings, Settings
import pytest
import pytest_asyncio
from dotenv import load_dotenv
from mongomock_motor import AsyncMongoMockClient
from motor.core import AgnosticDatabase
import logging
from functools import lru_cache
from bson import ObjectId
import copy

load_dotenv()

def connect_to_mongo_mock():
    if(db.client is None):
        logging.info("Connecting Database...")
        db.client = AsyncMongoMockClient("", connectTimeoutMS=250)
        logging.info("Database Connection Success!")


def close_mongo_connection_mock():
    logging.info("Closing Database...")
    db.client.close()
    logging.info("Successfully Closing Database")



@lru_cache
def get_settings_mock():
    return Settings(ENV="TEST")

def get_database_mock() -> AgnosticDatabase:
    return db.client[Settings().DATABASE_NAME]

@pytest.fixture(scope="function")
def database_mock():
    return get_database_mock()

@pytest_asyncio.fixture(scope="function")
async def mock_app():
    app.dependency_overrides[get_settings] = get_settings_mock
    app.dependency_overrides[connect_to_mongo] = connect_to_mongo_mock
    app.dependency_overrides[close_mongo_connection] = close_mongo_connection_mock
    yield app

@pytest_asyncio.fixture(scope="function")
async def mock_database():
    db = get_database_mock()
    mock_data = [
        {
            "_id": ObjectId("65f23e05146d8e3d8f9166c2"),
            "name": "name1",
            "email": "abc@xyz.com"
        },
        {
            "_id": ObjectId("65f23e31146d8e3d8f9166c3"),
            "name": "name2",
            "email": "abc@def.com"
        },
        {
            "_id": ObjectId("65f23e3697aaa46e75094227"),
            "name": "name3",
            "email": "def@xyz.com"
        }
    ]
    await db.users.insert_many(mock_data)
    return_data = copy.deepcopy(mock_data)
    for data in return_data:
        data["id"] = str(data["_id"])
        del data["_id"]
    yield return_data
    await db.users.delete_many({})

@pytest_asyncio.fixture(scope="function")
async def mock_data():
    payload={
        "name": "test",
        "email": "test@test.com"
    }
    yield payload
    db = get_database_mock()
    await db.users.delete_many({})


@pytest_asyncio.fixture(scope="function")
async def modified_data():
    payload={
        "name": "modified name",
        "email": "mod@email.com"
    }
    yield payload
    db = get_database_mock()
    await db.users.delete_many({})
