import asyncio
import websockets
import json

connected_clients = set()
class WebsocketData:
    def __init__(self):
        self.jsonMessage = None

    async def producer(self, websocket, path):
        connected_clients.add(websocket)
        try:
            async for message in websocket:
                print("Received:", message)
                self.jsonMessage = message
                if message.lower() == 'exit':
                    await websocket.send("Server: Exiting")
                    break
                response = f"Server: Received '{message}'."
                await websocket.send(response)
                print("Sent:", response)
        finally:
            connected_clients.remove(websocket)

    # Other methods...


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

    
    async def initWebSocket(self):
        # Start the WebSocket server
        server = await websockets.serve(self.producer, "localhost", 8081)
        print("Server started. Listening on ws://localhost:8081")

    # Wait for the server to close
