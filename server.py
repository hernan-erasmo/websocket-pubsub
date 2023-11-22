import asyncio
import websockets
from datetime import datetime
import uvloop


class PubSub:
    def __init__(self):
        self.waiter = asyncio.Future()

    def publish(self, value):
        waiter, self.waiter = self.waiter, asyncio.Future()
        waiter.set_result((value, self.waiter))

    async def subscribe(self):
        waiter = self.waiter
        while True:
            value, waiter = await waiter
            yield value

    __aiter__ = subscribe


async def producer(pubsub):
    """
    Replace this with the actual data retrieval logic
    """
    while True:
        data = f"Data from producer at {datetime.now()}"
        pubsub.publish(data)
        await asyncio.sleep(1)


async def server(pubsub):
    async def handler(websocket):
        async for message in pubsub:
            await websocket.send(message)

    async with websockets.serve(handler, "localhost", 6789):
        await asyncio.Future()  # run forever


async def main():
    pubsub = PubSub()

    # Create a task for the producer function
    producer_task = asyncio.create_task(producer(pubsub))

    # Create a task for the WebSocket server
    server_task = asyncio.create_task(server(pubsub))

    # Wait for both tasks to complete
    await asyncio.gather(producer_task, server_task)


if __name__ == "__main__":
    uvloop.run(main())
