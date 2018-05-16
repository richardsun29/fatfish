#!/usr/bin/env python

import asyncio
import websockets
import signal
import sys

#send_updates_delay = 1.0 / 60
send_updates_delay = 1.0 / 1

# TODO: class that contains websocket and any other info needed (player name, )

# listen
async def receive_data(websocket):
    while True:
        try:
            message = await websocket.recv()
        except websockets.exceptions.ConnectionClosed:
            return

        print('receive_data: ' + message + ' ' + str(websocket))


# send updates
async def send_data(websocket):
    i = 1
    while True:
        try:
            message = 'send_data: ' + str(i)
            await websocket.send(message)
        except websockets.exceptions.ConnectionClosed:
            return

        await asyncio.sleep(send_updates_delay)
        i += 1


async def handle_connection(websocket, path):
    consumer_task = asyncio.ensure_future(receive_data(websocket))
    producer_task = asyncio.ensure_future(send_data(websocket))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )

    for task in pending:
        task.cancel()


def start_server(port):
    server = websockets.serve(handle_connection, 'localhost', port)

    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

    # Stop event loop on ^C
    signal.signal(signal.SIGINT, asyncio.get_event_loop().close)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: {} PORT'.format(sys.argv[0]))
        sys.exit(1)
    start_server(sys.argv[1])
