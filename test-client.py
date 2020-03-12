#!/usr/bin/env python

# WS client example

import asyncio
import websockets


async def hello():
  uri = "ws://localhost:8080"
  async with websockets.connect(uri) as websocket:

    print('awaiting messages')

    msg = await websocket.recv()
    print(f"< {msg}")

asyncio.get_event_loop().run_until_complete(hello())
asyncio.get_event_loop().run_forever()
