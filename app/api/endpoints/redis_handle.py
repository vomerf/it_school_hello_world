
import redis.asyncio as redis
from fastapi import APIRouter


router = APIRouter()
redis_client = redis.Redis(host="localhost", port=6379, db=0)


@router.get("/set/{key}/{value}")
async def set_key(key: str, value: str):
    await redis_client.set(key, value)
    return {"status": "ok", "key": key, "value": value}


@router.get("/get/{key}")
async def get_key(key: str):
    value = await redis_client.get(key)
    if value is None:
        return {"error": "Key not found"}
    return {"key": key, "value": value.decode()}
