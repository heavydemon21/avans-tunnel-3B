




from enum import Enum

from lfv_parse import *



class StateTunnel(Enum):
    INIT = 1
    RUN = 2
    SOS = 3
    STOP = 4


CurrentTunnelState = StateTunnel.INIT;

lfv_processing = process_lfv()

lfv_processing.update_all()

while(1):


#TODO: make universal read and parsing functions

    match CurrentTunnelState:
        case StateTunnel.INIT:
            print("INIT")

            CurrentTunnelState = StateTunnel.RUN
        case StateTunnel.RUN:
            #print("RUN")

            pass


            #TODO: from run -> SOS / run -> STOP
        case StateTunnel.SOS:
            print("SOS")

            #TODO: from SOS -> run
        case StateTunnel.STOP:
            print("STOP")

            #TODO: from STOP -> run
        case _:
            print("ERROR state tunnel")
