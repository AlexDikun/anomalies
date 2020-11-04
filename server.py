# WS server

import asyncio
import websockets
import numpy as np

from queue import Queue
from funclib import *


async def transfer(websocket, path):
    if storage.full():
        while not storage.empty():
            array = storage.get()
            find_repeat(array)

    barr = await websocket.recv()
    arr = np.frombuffer(barr)
    print("recieve  ", arr)
    storage.put(arr)


if __name__ == '__main__':

    storage = Queue(maxsize=15)

    start_server = websockets.serve(transfer, "localhost", 8765)
    print("server is running...")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
