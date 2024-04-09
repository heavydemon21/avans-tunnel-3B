import asyncio
import websockets
import json

connected_clients = set()

async def producer(websocket, path):
    connected_clients.add(websocket)
    try:
        async for message in websocket:
            print("Received:", message)
            if message.lower() == 'exit':
                await websocket.send("Server: Exiting")
                break
            response = f"Server: Received '{message}'."
            await websocket.send(response)
            print("Sent:", response)
    finally:
        connected_clients.remove(websocket)
        
async def main():
    # Start the WebSocket server
    server = await websockets.serve(producer, "localhost", 8081)
    print("Server started. Listening on ws://localhost:8081")

    asyncio.create_task(runCode())
    # Wait for the server to close
    await server.wait_closed()

async def runCode():
     while True:
        await asyncio.sleep(5)  # Wait for 5 seconds

        # Broadcast the message to all connected clients
        array = [20, 70, 50, 60]
        await snelheidAutoPerZone(array, array, array, array)
        await autoPerZone(array)


# 3B -> HMI

# Actuele snelheid per auto per zone 
async def snelheidAutoPerZone(toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
        data = {}
        # naam van functie      
        data['type'] = "snelheidAutoPerZone"
        # doorsturen auto snelheden per zone | array index = auto nummer | array[90, 100, 70, 30...]
        data['snelHedenToegang'] = toegangSnelheid
        data['snelHedeningang'] = ingangSnelheid
        data['snelHedencentrale'] = centraleSnelheid
        data['snelHedenverlating'] = verlatingSnelheid
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

# Hoeveel auto’s per zone 
async def autoPerZone(autos):
        data = {}
        # naam van functie
        data['type'] = "autoPerZone"
        # doorsturen autos per zone | array index = zone [toegangszone, ingangszone, centralezone, verlatingzone] | array[15, 8, 9, 23]
        data['autos'] = autos
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

# SOS/storing bericht 
async def sosBericht(statusSOS, storingBericht):
        data = {}
        # naam van functie
        data['type'] = "sosBericht"
        # boolean met status van SOS
        data['statusSOS'] = statusSOS
        # Bericht voor de storing
        data['storingBericht'] = storingBericht
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

# Status bericht per LFV (storing) 
async def lfvStatusStoring(storingLFV):
        data = {}
        # naam van functie
        data['type'] = "lfvStatusStoring"
        # array met storingen voor lfvs | array index = nummer LFV | array[false, true, false, false...]
        data['storingLFV'] = storingLFV
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

# Status bericht per LFV (status van LFV) 
async def lfvStatussen(statusLFV):
        data = {}
        # naam van functie
        data['type'] = "lfvStatussen"
        # array met storing statussen voor lfvs | array index = nummer LFV | array[true, false, false, true...]
        data['statusLFV'] = statusLFV
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

asyncio.run(main())
