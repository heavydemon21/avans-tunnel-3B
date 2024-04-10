from modbus import *
from lfv.Afsluitboom import MODBUS_PLC_IP

class lfv_check:
   def __init__(self):
        self.modbus = modbus()

   def check(self):
      #TODO: define ip and modbus address
      reg = self.modbus.get(ip=MODBUS_PLC_IP, start_addr=500)
      return (reg == 1)
