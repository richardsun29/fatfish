#!/usr/bin/env python

import asyncio
import websockets

async def listen():
    async with websockets.connect('ws://localhost:8765') as websocket:
        i = 1
        while True:
            msg = await websocket.recv()
            print(msg)
            await websocket.send('client ' + str(i))
            i += 1

asyncio.get_event_loop().run_until_complete(listen())
