import asyncio
from datetime import datetime
from bot.queue_worker import channel_queue, worker
from bot.poster import create_post_task
from bot.indexer import update_source
from bot.database import channels_col, messages_col, admins_col


def is_allowed(hour, start, end):
    if start < end:
        return start <= hour < end
    return hour >= start or hour < end


async def channel_scheduler(client, config):
    channel_id = config["channel_id"]
    queue = channel_queue.get_queue(channel_id)

    asyncio.create_task(worker(client, channel_id, queue))

    while True:
        if config.get("paused"):
            await asyncio.sleep(60)
            continue

        now = datetime.now().hour

        if not is_allowed(now, config["start_hour"], config["end_hour"]):
            await asyncio.sleep(300)
            continue

        # update source
        admins = [a["admin_id"] async for a in admins_col.find()]
        await update_source(client, config["source_id"], admins, messages_col)

        # create post task
        task = await create_post_task(client, config, messages_col)
        await queue.put(task)

        # interval
        active_hours = (
            config["end_hour"] - config["start_hour"]
            if config["end_hour"] > config["start_hour"]
            else 24 - config["start_hour"] + config["end_hour"]
        )

        interval = (active_hours * 3600) // max(config["daily_limit"], 1)

        await asyncio.sleep(interval)


async def scheduler(client):
    channels = await channels_col.find().to_list(None)

    for config in channels:
        asyncio.create_task(channel_scheduler(client, config))

    while True:
        await asyncio.sleep(3600)            if config["end_hour"] > config["start_hour"]
            else (24 - config["start_hour"] + config["end_hour"])
        )

        interval = (active_hours * 3600) // max(config["daily_limit"], 1)

        # Post ONE message only
        new_index = await post_single(client, config, messages_col)

        if new_index is not None:
            await channels_col.update_one(
                {"channel_id": channel_id},
                {"$set": {"last_index": new_index}}
            )

        await asyncio.sleep(interval)


async def scheduler(client):
    channels = await channels_col.find().to_list(None)

    for config in channels:
        asyncio.create_task(channel_worker(client, config))

    while True:
        await asyncio.sleep(3600)
