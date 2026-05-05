import asyncio
from bot.caption import process_caption

async def create_post_task(client, config, messages_col):
    async def task():
        source = config["source_id"]
        channel = config["channel_id"]

        doc = await messages_col.find_one({"source_id": source})
        if not doc or not doc["message_ids"]:
            return

        ids = doc["message_ids"]
        index = config["last_index"] % len(ids)
        msg_id = ids[index]

        msg = await client.get_messages(source, ids=msg_id)
        caption = process_caption(msg.text, config)

        if msg.media:
            await client.send_file(channel, msg.media, caption=caption)
        else:
            await client.send_message(channel, caption)

    return task
