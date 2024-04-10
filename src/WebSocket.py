import asyncio
import websockets
import json
from enum import Enum
from lfv_ready import *
from lfv_parse import *
connected_clients = set()


class StateTunnel(Enum):
    PRE_INIT = 0
    INIT = 1
    RUN = 2
    SOS = 3
    STOP = 4

class WebsocketData:
    def __init__(self):
        self.CurrentTunnelState = StateTunnel.INIT
        self.jsonMessage = None
        self.lfv_processing = None
        self.start = False
        self.sosStatus = False

    async def stateMachine(self):
         while True:
            await asyncio.sleep(1)
            match self.CurrentTunnelState:
                case StateTunnel.PRE_INIT:
                    print("PRE INIT")
                    # Poll holding register to see if PLC's available
                    if  lfv_check().check():
                        # Send update message to HMI and blocking wait until response
                        print(self.jsonMessage)
                        # Change state
                        self.startStatus(self,True)
                        CurrentTunnelState = StateTunnel.INIT
                case StateTunnel.INIT:
                    print("INIT")
                    while(self.start == False):
                        await asyncio.sleep(1)
                        print(self.jsonMessage)
                    self.lfv_processing = process_lfv()
                    
                    # goto next state
                    self.CurrentTunnelState = StateTunnel.RUN
                case StateTunnel.RUN:
                    print("RUN")
                    if self.lfv_processing is not None:
                        # update all the lvf's
                        self.lfv_processing.update_all()
                        #self.snelheidAutoPerZone()
                        #self.lfvStatussen
                    else:
                        print("ERROR: lfv_proccesing is not initalized")
                    conflict = self.lfv_processing.detect_conflict()
                    match conflict:
                        case 1:
                            self.sosBericht(True, "Spookrijder op deel 1")
                        case 2:
                            self.sosBericht(True, "Spookrijder op deel 2")
                        case 3:
                            self.sosBericht(True, "Spookrijder op deel 3")
                        case 4:
                            self.sosBericht(True,"stilstand in zone 1")
                        case 5:
                            self.sosBericht(True,"stilstand in zone 2")
                    if conflict > 0:
                        self.sosStatus == True
                        self.CurrentTunnelState = StateTunnel.SOS
                    #TODO: from run -> SOS / run -> STOP
                case StateTunnel.SOS:
                    print("SOS")
                    
                    if self.sosStatus == False:
                         self.CurrentTunnelState == StateTunnel.RUN
                         
                    #TODO: from SOS -> run
                case StateTunnel.STOP:
                    print("STOP")
                    
                    #TODO: from STOP -> run
                case _:
                    print("ERROR: state tunnel")

    async def producer(self, websocket, path):
        print('prod')
        connected_clients.add(websocket)
        try:
            async for message in websocket:
                print("Received:", message)
                await self.parseJSON(message)

                if message.lower() == 'exit':
                    await websocket.send("Server: Exiting")
                    break
                response = f"Server: Received '{message}'."
                await websocket.send(response)
                print("Sent:", response)
        finally:
            connected_clients.remove(websocket)

    # Other methods...


    

    

    async def broadcast_message(self):
        while True:
            await asyncio.sleep(5)  # Wait for 5 seconds
            # Broadcast the message to all connected clients
            for ws in connected_clients:
                await ws.send("Broadcast message: This is a broadcast message from the server.")
        
    async def initWebSocket(self):
        server = await websockets.serve(self.producer, "localhost", 8081)
        print("Server started. Listening on ws://localhost:8081")

        # Start broadcasting messages
        broadcast_task = asyncio.create_task(self.stateMachine())
        # Wait for the server to close
        await server.wait_closed()

            # 3B -> HMI

    # Actuele snelheid per auto per zone 
    async def snelheidAutoPerZone(self, toegangSnelheid, ingangSnelheid, centraleSnelheid, verlatingSnelheid):
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
    async def autoPerZone(self, autos):
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
    async def sosBericht(self, statusSOS, storingBericht):
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
    async def lfvStatusStoring(self, storingLFV):
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
    async def lfvStatussen(self, statusLFV):
        data = {}
        # naam van functie
        data['type'] = "lfvStatussen"
        # array met storing statussen voor lfvs | array index = nummer LFV | array[true, false, false, true...]
        data['statusLFV'] = statusLFV
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)

    async def startStatus(self, statusStart):
        data = {}
        # naam van functie
        data['type'] = "lfvReady"
      
        data['ready'] = statusStart
        data = json.dumps(data)
        data = str(data)
        for ws in connected_clients:
            await ws.send(data)


    async def parseJSON(self, message):
        type = json.loads(message)
        typeName = type["type"]
        match typeName:
            case "start":
                self.start = True
            case "photocell":
                if self.sosStatus == False:
                    data = type["on"] 
                    print(data)
            case "barrier":
                print("barrier")
                if self.sosStatus == False:
                    if type['open']:
                            self.lfv_processing.Afsluitboom.Stand([2])
                    if type['open'] == False:
                        self.lfv_processing.Afsluitboom.Stand([1])
            case "matrix": 
                if self.sosStatus == False:
                    data = type["state"]
                    self.lfv_processing.Matrix.SetStand([data])
                    print(data)
            case "lights":
                if self.sosStatus == False:
                    data = type["value"]
                    self.lfv_processing.Verlichting.SetStand[data]
                    print(data)
            case "trafficLights":
                if self.sosStatus == False:
                    data = type["state"]
                    self.lfv_processing.Verkeerslicht.SetStand([data])
                    print(data)
            case "sosBericht":
                data = type["statusSOS"]
                self.sosStatus = False
                print(data)

    

async def run_websocket_server():
    websocketData = WebsocketData()
    await websocketData.initWebSocket()          

asyncio.run(run_websocket_server())
    # Wait for the server to close
