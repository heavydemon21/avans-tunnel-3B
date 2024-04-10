from typing import List
from modbus import *

MODBUS_VERLICHTING_IP = ""

class Zone:
    def __init__(self, ModbusInstance: modbus, startAddress: int ):
        self.StartAddress = startAddress
        self.niveau = 0
        self.capaciteit_beschikbaar = 0
        self.energieverbruik = 0
        self.branduren = 0
        self.ModbusInstance = ModbusInstance

        self.SetAutoRegeling([1])
    
    # TODO: maak deze functie
    def SetAutoRegeling(self, value): # aan | uit
        pass

    def SetStand(self, value ): # value between 0-10
        return self.ModbusInstance.set(MODBUS_VERLICHTING_IP,self.StartAddress+1, value)


class Verlichting:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.Richting = 0 # aflopend | oplopend
        self.ModbusInstance = ModbusInstance
        self.Zones: List[Zone] = []

        self.StartAddresses = start_addresses = [3500,3506, 3512, 3518]  # start addresses
        
        for start_address in start_addresses:
            zone = Zone(ModbusInstance, start_address)
            self.Zones.append(zone)


    def update(self):
        for zone in self.Zones:
            regs = self.ModbusInstance.get(MODBUS_VERLICHTING_IP,zone.StartAddress, 6)
            if regs:
                zone.niveau = regs[2]  
                zone.capaciteit_beschikbaar = regs[3]
                zone.energieverbruik = regs[4]
                zone.branduren = regs[5]
                self.Bereikbaar = 1
        
    def SetStand(self, value: int):
        return self.ModbusInstance.set(MODBUS_VERLICHTING_IP,2500, value)
