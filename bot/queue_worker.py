import asyncio
from telethon.errors import FloodWaitError

class ChannelQueue:
    def __init__(self):
        self.queues = {}

    def get_queue(self, channel_id):
        if channel_id not in self.queues:
            self.queues[channel_id] = asyncio.Queue()
        return self.queues[channel_id]


channel_queue = ChannelQueue()


async def worker(client, channel_id, queue):
    while True:
        task = await queue.get()

        try:
            await task()

        except FloodWaitError as e:
            print(f"⏳ Flood wait {e.seconds}s")
            await asyncio.sleep(e.seconds)

        except Exception as e:
            print(f"❌ Worker error: {e}")

        await asyncio.sleep(2)  # base cooldown
        queue.task_done()
