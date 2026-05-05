from bot.database import channels_col, admins_col
from bot.utils import parse_args

async def is_admin(user_id):
    return await admins_col.find_one({"admin_id": user_id}) is not None


async def require_admin(event):
    if not await is_admin(event.sender_id):
        await event.reply("❌ You are not authorized.")
        return False
    return True


async def help_command(event):
    await event.reply("""
📘 BOT COMMAND GUIDE

/addchannel -100DEST -100SOURCE
/setlimit -100DEST 5
/settime -100DEST 9 23
/setfooter -100DEST Join @channel
/setmode -100DEST replace
/setlink -100DEST https://t.me/yourchannel

/pause -100DEST
/resume -100DEST

/status
""")


async def add_admin(event):
    if not await require_admin(event): return
    user_id = int(parse_args(event.raw_text)[0])

    await admins_col.update_one(
        {"admin_id": user_id},
        {"$set": {"admin_id": user_id}},
        upsert=True
    )

    await event.reply("✅ Admin added")


async def add_channel(event):
    if not await require_admin(event): return
    args = parse_args(event.raw_text)

    dest = int(args[0])
    source = int(args[1])

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {
            "channel_id": dest,
            "source_id": source,
            "daily_limit": 5,
            "last_index": 0,
            "footer": "",
            "mode": "replace",
            "replacement_link": "",
            "start_hour": 9,
            "end_hour": 23,
            "paused": False
        }},
        upsert=True
    )

    await event.reply("✅ Channel added")


async def status(event):
    if not await require_admin(event): return

    channels = await channels_col.find().to_list(None)
    text = "📊 Channels:\n\n"

    for c in channels:
        text += f"{c['channel_id']} → {c['source_id']} | {c['daily_limit']}/day\n"

    await event.reply(text)
