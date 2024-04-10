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
        self.CurrentTunnelState = StateTunnel.PRE_INIT
        self.jsonMessage = None
        self.lfv_processing = None
        self.start = False
        self.sosStatus = False
        self.lfVOnline = [True,True,True,True,True,True]

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

                await self.parseJSON(message)


                if message.lower() == 'exit':
                    print(("Server: Exiting"))
                    break
                response = f"Server: Received '{message}'."
               
                print("Sent:", response)
        finally:
            connected_clients.remove(websocket)

    # Other methods...

    async def parseJSON(self, message):
        type = json.loads(message)
        typeName = type["type"]

        match typeName:
            case "start":
                print("start")
            case "photocell":
                data = type["on"]
                print(data)
            case "barrier":
                print("barrier")
            case "matrix":
                data = type["open"]
                print(data)
            case "lights":
                data = type["value"]
                print(data)
            case "trafficLights":
                data = type["state"]
                print(data)
            case "sosBericht":
                data = type["statusSOS"]
                print(data)
            case "cctvPreset":
                data = type["preset"]
                print(data)
            case "cctvPreset":
                pan = type["pan"]
                tilt = type["tilt"]
                zoom = type["zoom"]
                print(pan) 
                print(tilt) 
                print(zoom) 

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
                            if self.lfv_processing.Afsluitboom.SetStand([2]):
                                self.lfVOnline[2] = False
                                self.lfvStatussen(self,self.lfVOnline)
                    if type['open'] == False:
                        if self.lfv_processing.Afsluitboom.SetStand([1]):
                            self.lfVOnline[2] = False
                            self.lfvStatussen(self,self.lfVOnline)
            case "matrix": 
                if self.sosStatus == False:
                    data = type["state"]
                    if self.lfv_processing.Matrix.SetStand([data]) == False:
                        self.lfVOnline[3] = False
                        self.lfvStatussen(self,self.lfVOnline)
                    print(data)
            case "lights":
                if self.sosStatus == False:
                    data = type["value"]
                    
                    if self.lfv_processing.Verlichting.SetStand[data] == False:
                        self.lfVOnline[4] = False
                        self.lfvStatussen(self,self.lfVOnline)
                    print(data)
            case "trafficLights":
                if self.sosStatus == False:
                    data = type["state"]
                    if self.lfv_processing.Verkeerslicht.SetStand([data]) == False:
                        self.lfVOnline[5] = False
                        self.lfvStatussen(self,self.lfVOnline)
                    print(data)
            case "sosBericht":
                data = type["statusSOS"]
                self.sosStatus = False
                print(data)

    
    async def broadcast_message(self):
        while True:
            await asyncio.sleep(1)  # Wait for 5 seconds
            # Broadcast the message to all connected clients
        
    async def initWebSocket(self):
       # Start the WebSocket server
        server = await websockets.serve(self.producer, "localhost", 8081)
        print("Server started. Listening on ws://localhost:8081")

        # Start broadcasting messages
        broadcast_task = asyncio.create_task(self.broadcast_message())



        # Wait for the server to close
        await server.wait_closed()

async def run_websocket_server():
    websocketData = WebsocketData()
    await websocketData.initWebSocket()          

asyncio.run(run_websocket_server())
    # Wait for the server to close
