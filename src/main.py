




from enum import Enum
from modbus import *
from lfv_read_parse import get_barrier_data
int port = 502

class IP(Enum):
    BARRIER = "192.168.10.102"
    CCTV = "192.168.10.110"
    SOS = "192.168.10.125"
    TRAFFICLIGHT = "192.168.10.126" 
    TUNNELLIGHT = ""
    MTM = ""


while(1):
    barrier_reg = modbus_get(ip = IP.BARRIER.value,port = port);
    cctv_reg = modbus_get(ip = IP.CCTV.value, port = port);
    sos_reg = modbus_get(ip = IP.SOS.value, port = port);
    trafficl_reg = modbus_get(ip = IP.TRAFFICLIGHT.value, port = port);
    tunnell_reg = modbus_get(ip = IP.TUNNELLIGHT.value, port = port);
    mtm_reg = modbus_get(ip = IP.MTM.value, port = port);


    barrier_data = get_barrier_data(barrier_reg)
    trafficl_data = get_trafficl_data(trafficl_reg)
    tunnell_data = get_tunnell_data(tunnell_reg)
    mtm_data = get_mtm_data(mtm_reg)

    

    
