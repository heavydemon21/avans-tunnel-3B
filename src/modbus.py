from pyModbusTCP.client import ModbusClient

class modbus:
   c: ModbusClient = None

   def __init__(self, ip: str, port: int = 0):
      if port == 0:
         self.c = ModbusClient(host=ip, auto_open=True, auto_close=True)
      else:
         self.c = ModbusClient(host=ip, port=port, auto_open=True, auto_close=True)

   def get(self, start_addr, len: int = 1):
      regs = self.c.read_holding_registers(start_addr, len)
      if regs:
         return regs
      else:
         #ToDo add Error handling here
         return None
   
   # data is array of ints for subsequent addresses.
   def set(self, start_addr: int, data):
      return self.c.write_multiple_registers(start_addr, data)
