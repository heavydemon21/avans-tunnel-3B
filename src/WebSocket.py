#!/usr/bin/env python

import asyncio
import json
from enum import Enum

from websockets.server import serve

async def echo(websocket):
    async for message in websocket:

        toegangSnelheid = [60] 
        ingangSnelheid = [50, 40, 30] 
        centraleSnelheid = [50, 40, 30] 
        verlatingSnelheid = [50, 40, 30] 

        snelheidAutoPerZone(toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid)
       
        await websocket.send("test")

async def main():
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever


# 3B -> HMI

# Actuele snelheid per auto per zone 
async def snelheidAutoPerZone(toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
        data = {}
        # naam van functie      
        data['functie'] = "snelheidAutoPerZone"
        # doorsturen auto snelheden per zone | array index = auto nummer | array[90, 100, 70, 30...]
        data['snelHedenToegang'] = toegangSnelheid
        data['snelHedeningang'] = ingangSnelheid
        data['snelHedencentrale'] = centraleSnelheid
        data['snelHedenverlating'] = verlatingSnelheid
        json_data = json.dumps(data)
      
        print(data.getvalue())
        return json_data

# Hoeveel auto’s per zone 
async def autoPerZone(autos):
        data = {}
        # naam van functie
        data['type'] = "autoPerZone"
        # doorsturen autos per zone | array index = zone [toegangszone, ingangszone, centralezone, verlatingzone] | array[15, 8, 9, 23]
        data['autos'] = autos
        json_data = json.dumps(data)

        print(json_data)

# SOS/storing bericht 
async def sosBericht(statusSOS, storingBericht):
        data = {}
        # naam van functie
        data['functie'] = "sosBericht"
        # boolean met status van SOS
        data['statusSOS'] = statusSOS
        # Bericht voor de storing
        data['storingBericht'] = storingBericht
        json_data = json.dumps(data)

        print(json_data)

# Status bericht per LFV (storing) 
async def lfvStatusStoring(storingLFV):
        data = {}
        # naam van functie
        data['functie'] = "lfvStatusStoring"
        # array met storingen voor lfvs | array index = nummer LFV | array[false, true, false, false...]
        data['storingLFV'] = storingLFV
        json_data = json.dumps(data)

        print(json_data)

# Status bericht per LFV (status van LFV) 
async def lfvStatussen(statusLFV):
        data = {}
        # naam van functie
        data['functie'] = "lfvStatussen"
        # array met storing statussen voor lfvs | array index = nummer LFV | array[true, false, false, true...]
        data['statusLFV'] = statusLFV
        json_data = json.dumps(data)

        print(json_data)

asyncio.run(main())