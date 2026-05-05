from motor.motor_asyncio import AsyncIOMotorClient
from bot.config import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["telegram_bot"]

channels_col = db["channels"]
messages_col = db["messages"]
admins_col = db["admins"]
