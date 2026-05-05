from bot.database import channels_col, admins_col
from bot.utils import parse_args


# ---------------- ADMIN CHECK ---------------- #

async def is_admin(user_id):
    return await admins_col.find_one({"admin_id": user_id}) is not None


async def require_admin(event):
    if not await is_admin(event.sender_id):
        await event.reply("❌ You are not authorized.")
        return False
    return True


# ---------------- VALIDATION ---------------- #

def valid_hour(h):
    return 0 <= h <= 23


def valid_limit(n):
    return n > 0


# ---------------- HELP ---------------- #

async def help_command(event):
    await event.reply("""
📘 BOT COMMAND GUIDE

━━━━━━━━━━━━━━━
👤 ADMIN
/addadmin 123456789

━━━━━━━━━━━━━━━
📡 CHANNEL
/addchannel -100DEST -100SOURCE
/removechannel -100DEST
/setsource -100DEST -100SOURCE

━━━━━━━━━━━━━━━
⚙️ SETTINGS
/setlimit -100DEST 5
/settime -100DEST 9 23
/setfooter -100DEST Join @channel
/setmode -100DEST remove|replace|keep
/setlink -100DEST https://t.me/yourchannel

━━━━━━━━━━━━━━━
🎛️ CONTROL
/pause -100DEST
/resume -100DEST

━━━━━━━━━━━━━━━
📊 INFO
/status

━━━━━━━━━━━━━━━
""")


# ---------------- ADMIN ---------------- #

async def add_admin(event):
    if not await require_admin(event): return

    try:
        user_id = int(parse_args(event.raw_text)[0])
    except:
        return await event.reply("❌ Usage: /addadmin <user_id>")

    await admins_col.update_one(
        {"admin_id": user_id},
        {"$set": {"admin_id": user_id}},
        upsert=True
    )

    await event.reply(f"✅ Admin added: {user_id}")


# ---------------- CHANNEL ---------------- #

async def add_channel(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /addchannel <dest> <source>")

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


async def remove_channel(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if not args:
        return await event.reply("❌ Usage: /removechannel <dest>")

    dest = int(args[0])

    await channels_col.delete_one({"channel_id": dest})
    await event.reply("❌ Channel removed")


async def set_source(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /setsource <dest> <source>")

    dest = int(args[0])
    source = int(args[1])

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"source_id": source}}
    )

    await event.reply("✅ Source updated")


# ---------------- SETTINGS ---------------- #

async def set_limit(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /setlimit <dest> <limit>")

    dest = int(args[0])
    limit = int(args[1])

    if not valid_limit(limit):
        return await event.reply("❌ Limit must be > 0")

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"daily_limit": limit}}
    )

    await event.reply("✅ Limit updated")


async def set_time(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 3:
        return await event.reply("❌ Usage: /settime <dest> <start> <end>")

    dest = int(args[0])
    start = int(args[1])
    end = int(args[2])

    if not valid_hour(start) or not valid_hour(end):
        return await event.reply("❌ Hours must be between 0–23")

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"start_hour": start, "end_hour": end}}
    )

    await event.reply("✅ Time updated")


async def set_footer(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /setfooter <dest> <text>")

    dest = int(args[0])
    footer = " ".join(args[1:])

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"footer": footer}}
    )

    await event.reply("✅ Footer updated")


async def set_mode(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /setmode <dest> <mode>")

    dest = int(args[0])
    mode = args[1]

    if mode not in ["remove", "replace", "keep"]:
        return await event.reply("❌ Mode must be remove/replace/keep")

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"mode": mode}}
    )

    await event.reply("✅ Mode updated")


async def set_link(event):
    if not await require_admin(event): return

    args = parse_args(event.raw_text)

    if len(args) < 2:
        return await event.reply("❌ Usage: /setlink <dest> <link>")

    dest = int(args[0])
    link = args[1]

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"replacement_link": link}}
    )

    await event.reply("✅ Link updated")


# ---------------- CONTROL ---------------- #

async def pause_channel(event):
    if not await require_admin(event): return

    dest = int(parse_args(event.raw_text)[0])

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"paused": True}}
    )

    await event.reply("⏸️ Paused")


async def resume_channel(event):
    if not await require_admin(event): return

    dest = int(parse_args(event.raw_text)[0])

    await channels_col.update_one(
        {"channel_id": dest},
        {"$set": {"paused": False}}
    )

    await event.reply("▶️ Resumed")


# ---------------- STATUS ---------------- #

async def status(event):
    if not await require_admin(event): return

    channels = await channels_col.find().to_list(None)

    if not channels:
        return await event.reply("⚠️ No channels configured")

    text = "📊 CHANNEL STATUS\n\n"

    for c in channels:
        text += (
            f"📡 {c['channel_id']}\n"
            f"→ Source: {c['source_id']}\n"
            f"→ Limit: {c['daily_limit']}/day\n"
            f"→ Time: {c['start_hour']}–{c['end_hour']}\n"
            f"→ Paused: {c['paused']}\n\n"
        )

    await event.reply(text)
