from modbus import *

MODBUS_PLC_IP = "192.168.10.1"
MODBUS_AFSLUITBOOM_IP = MODBUS_PLC_IP
class Afsluitboom:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.Stand = 0
        self.Flash = 0
        self.Storing = 0
        self.Beweging = 0
        self.Obstakel = 0

        self.ModbusInstance = ModbusInstance

        self.SetStand([self.Stand])

        

    def update(self):
        regs = self.ModbusInstance.get(MODBUS_AFSLUITBOOM_IP,1006, 6) 
        if regs:
            self.Stand = regs[1]
            self.Bereikbaar = regs[2]  
            self.Beweging = regs[3]
            self.Obstakel = regs[4]
            self.Storing = regs[5]

    def SetStand(self, value):
        if self.Bereikbaar:
            return self.ModbusInstance.set(MODBUS_AFSLUITBOOM_IP, 1006, value)


        
