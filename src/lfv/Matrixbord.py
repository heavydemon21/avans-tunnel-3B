from modbus import *


class Matrix:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.Stand = 0
        self.Flash = 0
        self.Storing = 0
        self.ModbusInstance = ModbusInstance

    def update(self):
        regs = self.ModbusInstance.get(7000, 5)
        if regs:
            self.Stand = regs[1]
            self.Bereikbaar = regs[2]  
            self.Flash = regs[3]
            self.Storing = regs[4]

    def SetStand(self, value):
        if self.Bereikbaar:
            self.ModbusInstance.set(7000, value)


        
