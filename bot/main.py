import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession

from bot.config import API_ID, API_HASH, SESSION_STRING, OWNER_ID, BOT_TOKEN
from bot.database import admins_col
from bot.scheduler import scheduler
from bot.commands import *
from bot.session_gen import start_session, handle_session
from bot.web import start_web_server


# USERBOT (core engine)
userbot = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# BOT (UI layer) — DO NOT auto-start here
bot = TelegramClient("bot", API_ID, API_HASH)


# ---------------- BOT COMMANDS ---------------- #

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


# ---------------- SESSION ---------------- #

@bot.on(events.NewMessage(pattern="/gensession"))
async def _(e):
    if not await is_admin(e.sender_id):
        return await e.reply("❌ Not allowed")
    await start_session(e)


@bot.on(events.NewMessage)
async def session_flow(e):
    await handle_session(e)


# ---------------- SAFE BOT START ---------------- #

async def start_bot():
    from telethon.errors import FloodWaitError

    while True:
        try:
            await bot.start(bot_token=BOT_TOKEN)
            print("✅ Bot started")
            break
        except FloodWaitError as e:
            print(f"⏳ FloodWait: sleeping {e.seconds}s")
            await asyncio.sleep(e.seconds)


# ---------------- MAIN ---------------- #

async def main():
    print("🚀 Starting system...")

    # Start web FIRST (so health check passes)
    await start_web_server()

    # Start userbot
    await userbot.start()

    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    # Start bot safely (no crash loop)
    await start_bot()

    # Start scheduler
    asyncio.create_task(scheduler(userbot))

    print("✅ System fully running")

    # Keep running
    await bot.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
