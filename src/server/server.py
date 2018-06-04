#!/usr/bin/env python

import asyncio
import websockets
import sys
import json
import random

import game

SEND_UPDATES_DELAY = 1.0 / 30
GAME_LOOP_DELAY = 1.0 / 30

class Client:
    def __init__(self, websocket, game):
        self.websocket = websocket
        self.game = game
        self.id = None

    async def connect(self):
        # start sending/receiving
        recv_task = asyncio.ensure_future(self.receive_data())
        send_task = asyncio.ensure_future(self.send_data())
        await asyncio.gather(recv_task, send_task)

    async def disconnect(self):
        # cleanup
        self.game.remove_player(self.id)

    async def receive_data(self):
        # listen
        while True:
            message = await self.websocket.recv()
            #print('receive_data: ' + message)
            message = json.loads(message)
            action = message['action']
            data = message['data']

            if action == 'newplayer':
                self.id = self.game.create_player(data['name'], 50, 50)

            if action == 'move':
                self.game.move_player(self.id, data['x'], data['y'])

    async def send_data(self):
        # send updates
        while True:
            message = json.dumps(self.game.get_game_state(self.id))
            await self.websocket.send(message)
            await asyncio.sleep(SEND_UPDATES_DELAY)

    def __repr__(self):
        return 'Client (id = %d)' % (self.id)


class Server:
    def __init__(self):
        self.clients = set()
        self.game = game.Game()

    def start_server(self, ip, port):
        # run server
        server = websockets.serve(self.handle_connection, ip, port)
        asyncio.get_event_loop().run_until_complete(server)
        # run game
        asyncio.get_event_loop().run_until_complete(self.game_loop())
        asyncio.get_event_loop().run_forever()

    async def handle_connection(self, websocket, path):
        client = Client(websocket, self.game)
        self.clients.add(client)
        try:
            await client.connect()
        except websockets.exceptions.ConnectionClosed:
            await client.disconnect()
            self.clients.remove(client)

    def rand_size(self):
        if random.random() < 0.1:
            return random.uniform(30, 100)
        else:
            return random.uniform(1, 5)

    async def game_loop(self):
        counter = 0
        while True:
            if counter % 100 == 0:
                self.game.create_nonplayer(counter, self.rand_size(), 3, game.LEFT)
            elif counter % 100 == 50:
                self.game.create_nonplayer(counter, self.rand_size(), 3, game.RIGHT)
            counter += 1
            if counter == 500:
                counter = 0

            self.game.move_loop()
            #players, nonplayers = self.game.get_fish()
            #print(nonplayers)
            await asyncio.sleep(0.1)


if __name__ == '__main__':
    if len(sys.argv) == 3:
        server = Server()
        server.start_server(sys.argv[1], sys.argv[2])
    else:
        print('Usage: {} IP PORT'.format(sys.argv[0]))
        sys.exit(1)
