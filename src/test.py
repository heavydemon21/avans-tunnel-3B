CLIENTS = set()

async def broadcast():
    while True:
        for ws in CLIENTS:
            await ws.send("woof")
        await asyncio.sleep(2)

asyncio.create_task(broadcast())

async def handler(websocket, path):
    CLIENTS.add(websocket)
    try:
        async for msg in websocket:
            pass
    finally:
        CLIENTS.remove(websocket)

start_server = websockets.serve(handler, ...)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()