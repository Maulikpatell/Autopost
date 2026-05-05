import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon import Bot

from bot.config import (
    API_ID, API_HASH, SESSION_STRING, OWNER_ID, BOT_TOKEN
)
from bot.database import admins_col
from bot.scheduler import scheduler
from bot.commands import *
from bot.session_gen import start_session, handle_session


# USERBOT (core engine)
userbot = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# BOT (UI layer)
bot = TelegramClient("bot", API_ID, API_HASH).start(bot_token=BOT_TOKEN)


# ---------------- BOT COMMANDS (UI) ---------------- #

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    if await is_admin(event.sender_id):
        await event.reply("✅ Admin panel ready. Use /help")
    else:
        await event.reply("❌ Access denied")


@bot.on(events.NewMessage(pattern="/help"))
async def _(e): await help_command(e)

@bot.on(events.NewMessage(pattern="/addadmin"))
async def _(e): await add_admin(e)

@bot.on(events.NewMessage(pattern="/addchannel"))
async def _(e): await add_channel(e)

@bot.on(events.NewMessage(pattern="/removechannel"))
async def _(e): await remove_channel(e)

@bot.on(events.NewMessage(pattern="/setsource"))
async def _(e): await set_source(e)

@bot.on(events.NewMessage(pattern="/setlimit"))
async def _(e): await set_limit(e)

@bot.on(events.NewMessage(pattern="/settime"))
async def _(e): await set_time(e)

@bot.on(events.NewMessage(pattern="/setfooter"))
async def _(e): await set_footer(e)

@bot.on(events.NewMessage(pattern="/setmode"))
async def _(e): await set_mode(e)

@bot.on(events.NewMessage(pattern="/setlink"))
async def _(e): await set_link(e)

@bot.on(events.NewMessage(pattern="/pause"))
async def _(e): await pause_channel(e)

@bot.on(events.NewMessage(pattern="/resume"))
async def _(e): await resume_channel(e)

@bot.on(events.NewMessage(pattern="/status"))
async def _(e): await status(e)


# SESSION GENERATOR (still uses userbot API)
@bot.on(events.NewMessage(pattern="/gensession"))
async def _(e):
    if not await is_admin(e.sender_id):
        return await e.reply("❌ Not allowed")
    await start_session(e)


@bot.on(events.NewMessage)
async def session_flow(e):
    await handle_session(e)


# ---------------- MAIN ---------------- #

async def main():
    await userbot.start()

    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    print("🚀 Hybrid system started")

    await asyncio.sleep(5)

    # run scheduler on USERBOT (important)
    asyncio.create_task(scheduler(userbot))

    await bot.run_until_disconnected()


asyncio.run(main())
