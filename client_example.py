import uvloop
import websockets


async def client():
    uri = "ws://localhost:6789"
    async with websockets.connect(uri) as websocket:
        while True:
            message = await websocket.recv()
            print(f"CLIENT - Received message: {message}")


if __name__ == "__main__":
    uvloop.run(client())
