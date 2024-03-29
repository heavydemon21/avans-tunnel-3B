from modbus import *

class Zone:
    def __init__(self, ModbusInstance: modbus, startAddress: int ):
        self.StartAddress = startAddress
        self.Beschikbaar = {}
        self.Stand = {}
        self.Storing = {}
        self.ModbusInstance = ModbusInstance

    def SetStand(self, value: int): # value between 1-2
        self.ModbusInstance.set(self.StartAddress, value)


class Verkeerslicht:
    def __init__(self, ModbusInstance: modbus):
        self.ModbusInstance = ModbusInstance
        self.Zones = []

        self.StartAddresses = start_addresses = [0000, 0004]  # start addresses
        
        for start_address in start_addresses:
            zone = Zone(ModbusInstance, start_address)
            self.Zones.append(zone)


    def update(self):
        for zone in self.Zones:
            regs = self.ModbusInstance.get(zone.StartAddress, 4)
            if regs:
                zone.Stand = regs[1]
                zone.Beschikbaar = regs[2]
                zone.Storing = regs[3]
        

