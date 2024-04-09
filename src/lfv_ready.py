from modbus import *


class lfv_check:
   def __init__(self):
        self.modbus = modbus()

   def check(self):
      #TODO: define ip and modbus address
      reg = self.modbus.get(ip="0.0.0.0", start_addr=1000)
