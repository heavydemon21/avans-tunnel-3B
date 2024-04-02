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


# 3B -> HMI

# Actuele snelheid per auto per zone 
async def snelheidAutoPerZone(functie, toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
        data = {}
        # naam van functie      
        data['functie'] = functie
        # doorsturen auto snelheden per zone | array index = auto nummer | array[90, 100, 70, 30...]
        data['snelHedenToegang'] = toegangSnelheid
        data['snelHedeningang'] = ingangSnelheid
        data['snelHedencentrale'] = centraleSnelheid
        data['snelHedenverlating'] = verlatingSnelheid
        json_data = json.dumps(data)
        print(json_data)

# Hoeveel auto’s per zone 
async def autoPerZone(functie, autos):
        data = {}
        # naam van functie
        data['functie'] = functie
        # doorsturen autos per zone | array index = zone [toegangszone, ingangszone, centralezone, verlatingzone] | array[15, 8, 9, 23]
        data['autos'] = autos
        json_data = json.dumps(data)
        print(json_data)

# SOS/storing bericht 
async def sosBericht(functie, statusSOS, storingBericht):
        data = {}
        # naam van functie
        data['functie'] = functie
        # boolean met status van SOS
        data['statusSOS'] = statusSOS
        # Bericht voor de storing
        data['storingBericht'] = storingBericht
        json_data = json.dumps(data)
        print(json_data)

# Status bericht per LFV (storing) 
async def lfvStatusStoring(functie, storingLFV):
        data = {}
        # naam van functie
        data['functie'] = functie
        # array met storingen voor lfvs | array index = nummer LFV | array[1, 0, 1, 1...]
        data['storingenLFV'] = storingLFV
        json_data = json.dumps(data)
        print(json_data)

# Status bericht per LFV (status van LFV) 
async def lfvStatussen(functie, statusLFV):
        data = {}
        # naam van functie
        data['functie'] = functie
        # array met storing statussen voor lfvs | array index = nummer LFV | array[1, 1, 1, 0...]
        data['storingenLFV'] = statusLFV
        json_data = json.dumps(data)
        print(json_data)

asyncio.run(main())