#!/usr/bin/env python

import asyncio
import websockets
import signal
import sys
import json

#SEND_UPDATES_DELAY = 1.0 / 60
SEND_UPDATES_DELAY = 1.0 / 1

class Client:
    def __init__(self, id, websocket):
        self.id = id
        self.websocket = websocket

    async def connect(self):
        # start sending/receiving
        recv_task = asyncio.ensure_future(self.receive_data())
        send_task = asyncio.ensure_future(self.send_data())
        await asyncio.gather(recv_task, send_task)

    async def receive_data(self):
        # listen
        while True:
            message = await self.websocket.recv()
            print('receive_data: ' + message)
            message = json.loads(message)

    async def send_data(self):
        i = 1
        # send updates
        while True:
            message = 'send_data: ' + str(i)
            await self.websocket.send(message)
            await asyncio.sleep(SEND_UPDATES_DELAY)
            i += 1

    def __repr__(self):
        return 'Client (id = %d)' % (self.id)


class Server:
    def __init__(self):
        self.clients = set()
        self.next_id = 1

    def get_new_id(self):
        self.next_id += 1
        return self.next_id

    def start_server(self, port):
        server = websockets.serve(self.handle_connection, 'localhost', port)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
        # Stop event loop on ^C
        signal.signal(signal.SIGINT, asyncio.get_event_loop().close)

    async def handle_connection(self, websocket, path):
        client = Client(self.get_new_id(), websocket)
        self.clients.add(client)
        try:
            await client.connect()
        except websockets.exceptions.ConnectionClosed:
            self.clients.remove(client)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        server = Server()
        server.start_server(sys.argv[1])
    else:
        print('Usage: {} PORT'.format(sys.argv[0]))
        sys.exit(1)
