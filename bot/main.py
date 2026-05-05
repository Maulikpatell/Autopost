import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from bot.config import API_ID, API_HASH, SESSION_STRING, OWNER_ID
from bot.database import admins_col
from bot.scheduler import scheduler
from bot.commands import *
from bot.session_gen import start_session, handle_session

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)


# ---------------- BASIC ---------------- #

@client.on(events.NewMessage(pattern="/start"))
async def start(event):
    if await is_admin(event.sender_id):
        await event.reply("✅ You are admin. Use /help")
    else:
        await event.reply("🤖 Private bot.")


# ---------------- COMMANDS ---------------- #

@client.on(events.NewMessage(pattern="/help"))
async def _(e): await help_command(e)

@client.on(events.NewMessage(pattern="/addadmin"))
async def _(e): await add_admin(e)

@client.on(events.NewMessage(pattern="/addchannel"))
async def _(e): await add_channel(e)

@client.on(events.NewMessage(pattern="/removechannel"))
async def _(e): await remove_channel(e)

@client.on(events.NewMessage(pattern="/setsource"))
async def _(e): await set_source(e)

@client.on(events.NewMessage(pattern="/setlimit"))
async def _(e): await set_limit(e)

@client.on(events.NewMessage(pattern="/settime"))
async def _(e): await set_time(e)

@client.on(events.NewMessage(pattern="/setfooter"))
async def _(e): await set_footer(e)

@client.on(events.NewMessage(pattern="/setmode"))
async def _(e): await set_mode(e)

@client.on(events.NewMessage(pattern="/setlink"))
async def _(e): await set_link(e)

@client.on(events.NewMessage(pattern="/pause"))
async def _(e): await pause_channel(e)

@client.on(events.NewMessage(pattern="/resume"))
async def _(e): await resume_channel(e)

@client.on(events.NewMessage(pattern="/status"))
async def _(e): await status(e)


# ---------------- SESSION GENERATOR ---------------- #

@client.on(events.NewMessage(pattern="/gensession"))
async def _(e):
    if not await is_admin(e.sender_id):
        return await e.reply("❌ Not allowed")
    await start_session(e)


@client.on(events.NewMessage)
async def session_flow(e):
    await handle_session(e)


# ---------------- MAIN ---------------- #

async def main():
    await client.start()

    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    print("🚀 Bot Started")

    await asyncio.sleep(5)
    await scheduler(client)


with client:
    client.loop.run_until_complete(main())async def main():
    await client.start()

    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    print("🚀 Bot Started")

    await asyncio.sleep(5)  # startup delay
    await scheduler(client)


with client:
    client.loop.run_until_complete(main())
