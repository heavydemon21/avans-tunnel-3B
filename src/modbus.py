from pyModbusTCP.client import ModbusClient

# ---- Internal functions ----
def mbclient_set(ip: str, port: int = 0):
   if port == 0:
      c = ModbusClient(host=ip, auto_open=True, auto_close=True)
   else:
      c = ModbusClient(host=ip, port=port, auto_open=True, auto_close=True)
   return c

# ---- External functions ----
def modbus_get(ip: str, port: int = 0):
   c = mbclient_set(ip=ip, port=port)
   
   regs = c.read_holding_registers(0,2)

   if regs:
      print(regs)
      return regs
   else:
      #ToDo add Error handling here
      return None
   

def modbus_set(mb_addr: int, data, ip: str, port: int = 0):
   c = mbclient_set(ip=ip, port=port)

   return c.write_multiple_registers(mb_addr, data)



