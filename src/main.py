




from enum import Enum
from modbus import *
from lfv_read_parse import *


port = 502
TunnelIP= "86.88.46.183"


class StateTunnel(Enum):
    INIT = 1
    RUN = 2
    SOS = 3
    STOP = 4


CurrentTunnelState = StateTunnel.INIT;


while(1):


#TODO: make universal read and parsing functions

    match CurrentTunnelState:
        case StateTunnel.INIT:
            print("INIT")

            CurrentTunnelState = StateTunnel.RUN
        case StateTunnel.RUN:
            print("RUN")

            #TODO: from run -> SOS / run -> STOP
        case StateTunnel.SOS:
            print("SOS")

            #TODO: from SOS -> run
        case StateTunnel.STOP:
            print("STOP")

            #TODO: from STOP -> run
        case _:
            print("ERROR state tunnel")


    #barrier_reg = modbus_get(ip = IP.BARRIER.value,port = port);
    #cctv_reg = modbus_get(ip = IP.CCTV.value, port = port);
    #sos_reg = modbus_get(ip = IP.SOS.value, port = port);
    #trafficl_reg = modbus_get(ip = IP.TRAFFICLIGHT.value, port = port);
    #tunnell_reg = modbus_get(ip = IP.TUNNELLIGHT.value, port = port);
    #mtm_reg = modbus_get(ip = IP.MTM.value, port = port);


    #barrier_data = get_barrier_data(barrier_reg)
    #trafficl_data = get_trafficl_data(trafficl_reg)
    #tunnell_data = get_tunnell_data(tunnell_reg)
    #mtm_data = get_mtm_data(mtm_reg)
