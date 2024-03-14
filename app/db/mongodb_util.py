import logging

from motor.motor_asyncio import AsyncIOMotorClient
from ..config import settings
from .mongodb import db


def connect_to_mongo():
    logging.info("Connecting Database...")
    db.client = AsyncIOMotorClient(str(settings.MONGO_URI))
    logging.info("Database Connection Success!")


def close_mongo_connection():
    logging.info("Closing Database...")
    db.client.close()
    logging.info("Successfully Closing Database")