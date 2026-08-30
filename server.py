import os
from aiohttp import web
import asyncio
import websockets

connected_users = set()


async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_users.add(ws)

    try:
        async for message in ws:
            if message.type == web.WSMsgType.TEXT:
                for user in list(connected_users):
                    if user != ws and not user.closed:
                        await user.send_str(message.data)

    finally:
        connected_users.discard(ws)

    return ws


async def health(request):
    return web.Response(text="OK")


async def main():
    port = int(os.environ.get("PORT", 10000))

    app = web.Application()

    app.router.add_get("/healthz", health)
    app.router.add_get("/ws", websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(
        runner,
        "0.0.0.0",
        port
    )

    await site.start()

    print("ONLINE CHAT SERVER STARTED")

    await asyncio.Future()


asyncio.run(main())
