import asyncio
import websockets


async def connect_to_websocket():
    user_id = 23
    uri = "ws://localhost:8000/ws/{}".format(user_id)  # Replace user_id with actual user_id from db
    async with websockets.connect(uri) as websocket:
        async for message in websocket:
            print(f"Received: {message}")

asyncio.get_event_loop().run_until_complete(connect_to_websocket())









