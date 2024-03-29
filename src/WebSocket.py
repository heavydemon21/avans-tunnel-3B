#!/usr/bin/env python

import asyncio
import json
from enum import Enum

from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        

        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

async def autoPerZone(functie, autos):
        data = {}
        # naam van functie
        data['functie'] = functie
        # doorsturen autos per zone | array[toegangszone, ingangszone, centralezone, verlatingzone]
        data['autos'] = beschikbaar
        json_data = json.dumps(data)
        print(json_data)

async def snelheidAutoPerZone(functie, toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
        data = {}
        # naam van functie
        data['functie'] = functie
        # doorsturen auto snelheden per zone | array[90, 100, 70, 30...]
        data['snelHedenToegang'] = toegangSnelheid
        data['snelHedeningang'] = ingangSnelheid
        data['snelHedencentrale'] = centraleSnelheid
        data['snelHedenverlating'] = verlatingSnelheid
        json_data = json.dumps(data)
        print(json_data)

async def snelheidAutoPerZone(functie, storingLFV):
        data = {}
        # naam van functie
        data['functie'] = functie
        # array met storingen voor lfvs | array[1, 0, 1, 1...]
        data['storingenLFV'] = storingLFV
        json_data = json.dumps(data)
        print(json_data)

async def snelheidAutoPerZone(functie, statusLFV):
        data = {}
        # naam van functie
        data['functie'] = functie
        # array met statussen voor lfvs | array[1, 1, 1, 0...]
        data['storingenLFV'] = statusLFV
        json_data = json.dumps(data)
        print(json_data)

asyncio.run(main())
