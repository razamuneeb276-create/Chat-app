import os
import asyncio
import websockets

connected_users = set()


async def chat(websocket):
    connected_users.add(websocket)

    try:
        async for message in websocket:
            for user in connected_users:
                if user != websocket:
                    await user.send(message)

    except websockets.exceptions.ConnectionClosed:
        pass

    finally:
        connected_users.discard(websocket)


async def main():
    port = int(os.environ.get("PORT", 8765))

    async with websockets.serve(
        chat,
        "0.0.0.0",
        port
    ):
        print("ONLINE CHAT SERVER STARTED")
        await asyncio.Future()


asyncio.run(main())
