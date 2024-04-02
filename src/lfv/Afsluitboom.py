from modbus import *


class Afsluitboom:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.Stand = 0
        self.Flash = 0
        self.Storing = 0
        self.Beweging = 0
        self.Obstakel = 0

        self.ModbusInstance = ModbusInstance

    def update(self):
        regs = self.ModbusInstance.get(1000, 6) 
        if regs:
            self.Stand = regs[1]
            self.Bereikbaar = regs[2]  
            self.Beweging = regs[3]
            self.Obstakel = regs[4]
            self.Storing = regs[5]

    def SetStand(self, value):
        if self.Bereikbaar:
            self.ModbusInstance.set(1000, value)


        
