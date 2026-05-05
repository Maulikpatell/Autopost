import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from bot.config import API_ID, API_HASH, SESSION_STRING, OWNER_ID
from bot.database import admins_col
from bot.scheduler import scheduler
from bot.commands import *

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if await is_admin(event.sender_id):
        await event.reply("✅ You are admin. Use /help")
    else:
        await event.reply("🤖 Private bot.")


@client.on(events.NewMessage(pattern="/help"))
async def _(e): await help_command(e)

@client.on(events.NewMessage(pattern="/addadmin"))
async def _(e): await add_admin(e)

@client.on(events.NewMessage(pattern="/addchannel"))
async def _(e): await add_channel(e)

@client.on(events.NewMessage(pattern="/setsource"))
async def _(e): await set_source(e)

@client.on(events.NewMessage(pattern="/status"))
async def _(e): await status(e)


async def main():
    await client.start()

    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    print("🚀 Bot Started")

    await asyncio.sleep(5)  # startup delay
    await scheduler(client)


with client:
    client.loop.run_until_complete(main())
