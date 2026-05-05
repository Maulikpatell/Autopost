import asyncio
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

from bot.config import API_ID, API_HASH, SESSION_STRING, OWNER_ID, BOT_TOKEN
from bot.database import admins_col
from bot.scheduler import scheduler
from bot.commands import *
from bot.session_gen import start_session, handle_session
from bot.web import start_web_server


# USERBOT (engine)
userbot = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# BOT (UI)
bot = TelegramClient("bot", API_ID, API_HASH)


# ---------------- DEBUG HANDLER ---------------- #
@bot.on(events.NewMessage)
async def debug_all(e):
    print(f"📩 Incoming message: {e.raw_text}")


# ---------------- BOT COMMANDS ---------------- #

@bot.on(events.NewMessage(pattern="/start"))
async def start(event):
    print("⚡ /start triggered")
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
    while True:
        try:
            print("⚡ Starting bot login...")
            await bot.start(bot_token=BOT_TOKEN)
            print("✅ Bot started successfully")
            break
        except FloodWaitError as e:
            print(f"⏳ FloodWait: sleeping {e.seconds}s")
            await asyncio.sleep(e.seconds)
        except Exception as e:
            print(f"❌ Bot start error: {e}")
            await asyncio.sleep(10)


# ---------------- MAIN ---------------- #

async def main():
    print("🚀 Starting system...")

    # 1. Start web server FIRST (for Koyeb health check)
    await start_web_server()

    # 2. Start userbot
    await userbot.start()
    print("✅ Userbot started")

    # 3. Ensure owner exists
    if not await admins_col.find_one({"admin_id": OWNER_ID}):
        await admins_col.insert_one({"admin_id": OWNER_ID})

    # 4. Start bot safely
    await start_bot()

    # 5. Start scheduler
    asyncio.create_task(scheduler(userbot))
    print("📡 Scheduler started")

    print("✅ System fully running")

    # 6. KEEP EVENT LOOP ALIVE (IMPORTANT FIX)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
