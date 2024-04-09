from pyModbusTCP.client import ModbusClient

class modbus:
    c: ModbusClient

    def __init__(self):
        self.port = 502

    def get(self, ip: str, start_addr, len: int = 1):
        self.c = ModbusClient(host=ip, port=self.port, auto_open=True, auto_close=True)
        regs = self.c.read_holding_registers(start_addr, len)
        if regs:
            return regs
        else:
            #ToDo add Error handling here
            return None
   
        # data is array of ints for subsequent addresses.
    def set(self, ip: str, start_addr: int, data):
        self.c = ModbusClient(host=ip, port=self.port, auto_open=True, auto_close=True)
        return self.c.write_multiple_registers(start_addr, data)
