from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from .config import get_settings, Settings
from .db.mongodb_util import close_mongo_connection, connect_to_mongo
from .db.mongodb import get_database
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

class User(BaseModel):
    name: str
    email: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings: Settings = app.dependency_overrides.get(get_settings, get_settings)()
    connect_to_mongo_on_startup = app.dependency_overrides.get(connect_to_mongo, connect_to_mongo)
    close_mongo_connection_on_shutdown = app.dependency_overrides.get(close_mongo_connection, close_mongo_connection)

    connect_to_mongo_on_startup()
    yield
    close_mongo_connection_on_shutdown()

app = FastAPI(lifespan=lifespan)

# Read (GET) operation
@app.get('/users/')
async def get_records(db: AsyncIOMotorClient = Depends(get_database)):
    get_cursor = db.users.find({})

    all_record = []
    async for record in get_cursor:
        userid = str(record["_id"])
        del record["_id"]
        record["id"] = userid
        all_record.append(record)

    return {"user": all_record}

# Create (POST) operation
@app.post('/users/')
async def create_user(user: User, db: AsyncIOMotorClient = Depends(get_database)):
    user_data = user.model_dump()
    inserted_user = await db.users.insert_one(user_data)
    userid = str(user_data["_id"])
    del user_data["_id"]
    user_data["id"] = userid

    return {**user_data}

# Update (PUT) operation
@app.put("/users/{user_id}")
async def update_user(user_id: str, user: User, db: AsyncIOMotorClient = Depends(get_database)):
    user_data = user.model_dump()
    result = await db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_data})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

# Delete (DELETE) operation
@app.delete("/users/{user_id}")
async def delete_user(user_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")
