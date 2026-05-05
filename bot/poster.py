import asyncio
import random
from bot.caption import process_caption

async def post_channel(client, config, messages_col):
    if config.get("paused"):
        return None

    source = config["source_id"]
    channel = config["channel_id"]

    doc = await messages_col.find_one({"source_id": source})
    if not doc or not doc["message_ids"]:
        return None

    ids = doc["message_ids"]
    start = config["last_index"]
    limit = config["daily_limit"]

    for i in range(limit):
        index = (start + i) % len(ids)
        msg_id = ids[index]

        msg = await client.get_messages(source, ids=msg_id)
        caption = process_caption(msg.text, config)

        await client.send_file(channel, msg.media, caption=caption)

        await asyncio.sleep(random.randint(20, 60))

    return (start + limit) % len(ids)
