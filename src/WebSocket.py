#!/usr/bin/env python

import asyncio
import json
from enum import Enum

from websockets.server import serve

async def echo(websocket):
    async for message in websocket:

        array = [60, 70, 50, 60]
        data = autoPerZone(array)

        data = json.dumps(data)
        data = str(data)
        print(data)


        await websocket.send(message)

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever 


# 3B -> HMI

# Actuele snelheid per auto per zone 
def snelheidAutoPerZone(toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
        data = {}
        # naam van functie      
        data['functie'] = "snelheidAutoPerZone"
        # doorsturen auto snelheden per zone | array index = auto nummer | array[90, 100, 70, 30...]
        data['snelHedenToegang'] = toegangSnelheid
        data['snelHedeningang'] = ingangSnelheid
        data['snelHedencentrale'] = centraleSnelheid
        data['snelHedenverlating'] = verlatingSnelheid

        return data

# Hoeveel auto’s per zone 
def autoPerZone(autos):
        data = {}
        # naam van functie
        data['type'] = "autoPerZone"
        # doorsturen autos per zone | array index = zone [toegangszone, ingangszone, centralezone, verlatingzone] | array[15, 8, 9, 23]
        data['autos'] = autos

        return data

# SOS/storing bericht 
def sosBericht(statusSOS, storingBericht):
        data = {}
        # naam van functie
        data['functie'] = "sosBericht"
        # boolean met status van SOS
        data['statusSOS'] = statusSOS
        # Bericht voor de storing
        data['storingBericht'] = storingBericht

        return data

# Status bericht per LFV (storing) 
def lfvStatusStoring(storingLFV):
        data = {}
        # naam van functie
        data['functie'] = "lfvStatusStoring"
        # array met storingen voor lfvs | array index = nummer LFV | array[false, true, false, false...]
        data['storingLFV'] = storingLFV

        return data

# Status bericht per LFV (status van LFV) 
def lfvStatussen(statusLFV):
        data = {}
        # naam van functie
        data['functie'] = "lfvStatussen"
        # array met storing statussen voor lfvs | array index = nummer LFV | array[true, false, false, true...]
        data['statusLFV'] = statusLFV

        return data

asyncio.run(main())