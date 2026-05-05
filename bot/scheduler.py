import asyncio
from datetime import datetime
from bot.poster import post_channel
from bot.indexer import update_source
from bot.database import channels_col, messages_col, admins_col

def is_allowed(now, start, end):
    if start < end:
        return start <= now < end
    return now >= start or now < end

async def scheduler(client):
    while True:
        channels = await channels_col.find().to_list(None)
        admins = [a["admin_id"] for a in await admins_col.find().to_list(None)]

        for config in channels:
            now = datetime.now().hour

            if not is_allowed(now, config["start_hour"], config["end_hour"]):
                continue

            await update_source(client, config["source_id"], admins, messages_col)

            new_index = await post_channel(client, config, messages_col)

            if new_index is not None:
                await channels_col.update_one(
                    {"channel_id": config["channel_id"]},
                    {"$set": {"last_index": new_index}}
                )

        await asyncio.sleep(300)
