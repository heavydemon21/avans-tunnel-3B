from modbus import *

MODBUS_VERKEERSLICHT_IP = "192.168.10.126"

class Verkeerslicht:
    def __init__(self, ModbusInstance: modbus, startAddress : int):
        self.ModbusInstance = ModbusInstance

        self.StartAddress = startAddress
        self.Beschikbaar = 0
        self.Stand = 1
        self.Storing = {}

        self.SetStand([self.Stand])

    def update(self):
        regs = self.ModbusInstance.get(MODBUS_VERKEERSLICHT_IP,self.StartAddress, 4)
        if regs:
             self.Stand = regs[1]
             self.Beschikbaar = regs[2]
             self.Storing = regs[3]

    def SetStand(self, value): # value between 1-2
        return self.ModbusInstance.set(MODBUS_VERKEERSLICHT_IP, self.StartAddress, value)        

