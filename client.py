# WS client - sensor factory

import asyncio
import websockets
from time import sleep
from random import randint

import numpy as np
import pandas as pd

from itertools import cycle
from bigdata import *


async def transfer(arr):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        barr = arr.tobytes()
        await websocket.send(barr)
        print("send  ", arr)


if __name__ == '__main__':

    while(True) :
        for arr in cycle(all):
        	asyncio.get_event_loop().run_until_complete(transfer(arr))
        	sleep(randint(1, 5))
