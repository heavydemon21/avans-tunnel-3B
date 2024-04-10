from WebSocket import *
from enum import Enum
from lfv_parse import *
from lfv_ready import *

class StateTunnel(Enum):
    PRE_INIT = 0
    INIT = 1
    RUN = 2
    SOS = 3
    STOP = 4

CurrentTunnelState = StateTunnel.PRE_INIT

websocketdata = WebsocketData()

while(1):
    print("test")
    match CurrentTunnelState:
        case StateTunnel.PRE_INIT:
            # Poll holding register to see if PLC's available
            if  lfv_check().check():
                # Send update message to HMI and blocking wait until response
                print("test")
                # Change state
                CurrentTunnelState = StateTunnel.INIT
        case StateTunnel.INIT:
            print("INIT")
            lfv_processing = process_lfv()
            
            # goto next state
            CurrentTunnelState = StateTunnel.RUN
        case StateTunnel.RUN:
            if lfv_processing is not None:
                # update all the lvf's
                lfv_processing.update_all()


            else:
                print("ERROR: lfv_proccesing is not initalized")
            conflict = lfv_processing.detect_confict()
            if conflict:
                CurrentTunnelState = StateTunnel.SOS
            #TODO: from run -> SOS / run -> STOP
        case StateTunnel.SOS:
            print("SOS")
            
            
            #TODO: from SOS -> run
        case StateTunnel.STOP:
            print("STOP")
            
            #TODO: from STOP -> run
        case _:
            print("ERROR: state tunnel")


asyncio.run(runWebSocket())