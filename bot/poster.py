import asyncio
from bot.caption import process_caption


async def post_single(client, config, messages_col):
    source = config["source_id"]
    channel = config["channel_id"]

    doc = await messages_col.find_one({"source_id": source})
    if not doc or not doc["message_ids"]:
        return None

    ids = doc["message_ids"]
    index = config["last_index"] % len(ids)
    msg_id = ids[index]

    try:
        msg = await client.get_messages(source, ids=msg_id)

        caption = process_caption(msg.text, config)

        if msg.media:
            await client.send_file(channel, msg.media, caption=caption)
        else:
            await client.send_message(channel, caption)

        return (index + 1) % len(ids)

    except Exception as e:
        print(f"❌ Post failed: {e}")
        await asyncio.sleep(10)
        return index  # retry next cycle
