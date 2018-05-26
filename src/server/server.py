#!/usr/bin/env python

import asyncio
import websockets
import signal
import sys
import json

import game

#SEND_UPDATES_DELAY = 1.0 / 60
SEND_UPDATES_DELAY = 1.0 / 1

class Client:
    def __init__(self, websocket, game):
        self.websocket = websocket
        self.game = game
        self.id = None

    async def connect(self):
        #self.game.create_player()
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
        # send updates
        while True:
            players, nonplayers = self.game.get_fish()
            message = json.dumps({
                'id': self.id,
                'players': [{
                    'id': p.id,
                    'x': p.x,
                    'y':p.y,
                    'size': p.size,
                } for p in players],
                'nonplayers': [{
                    'x': p.x,
                    'y':p.y,
                    'size': p.size,
                } for p in nonplayers],
            })
            await self.websocket.send(message)
            await asyncio.sleep(SEND_UPDATES_DELAY)

    def __repr__(self):
        return 'Client (id = %d)' % (self.id)


class Server:
    def __init__(self):
        self.clients = set()
        self.game = game.Game()

    def start_server(self, port):
        # run server
        server = websockets.serve(self.handle_connection, 'localhost', port)
        asyncio.get_event_loop().run_until_complete(server)
        # Stop event loop on ^C
        signal.signal(signal.SIGINT, asyncio.get_event_loop().close)
        # run game
        asyncio.get_event_loop().run_until_complete(self.game_loop())
        asyncio.get_event_loop().run_forever()

    async def handle_connection(self, websocket, path):
        client = Client(websocket, self.game)
        self.clients.add(client)
        try:
            await client.connect()
        except websockets.exceptions.ConnectionClosed:
            self.clients.remove(client)

    async def game_loop(self):
        counter = 0
        while True:
            if counter % 10 == 0:
                self.game.create_nonplayer(counter, 3, 1, game.LEFT)
            counter += 1
            if counter == 100:
                counter = 0

            self.game.move_loop()
            print('game loop')
            #players, nonplayers = self.game.get_fish()
            #print(nonplayers)
            await asyncio.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) == 2:
        server = Server()
        server.start_server(sys.argv[1])
    else:
        print('Usage: {} PORT'.format(sys.argv[0]))
        sys.exit(1)
