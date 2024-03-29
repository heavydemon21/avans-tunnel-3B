from modbus import *

class Zone:
    def __init__(self, ModbusInstance: modbus, startAddress: int ):
        self.StartAddress = startAddress
        self.niveau = {}
        self.capaciteit_beschikbaar = {}
        self.energieverbruik = {}
        self.branduren = {}
        self.ModbusInstance = ModbusInstance

    def SetAutoRegeling(self, value): # aan | uit
        pass

    def SetStand(self, value: int): # value between 0-10
        self.ModbusInstance.set(self.StartAddress+1, value)


class Verlichting:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.Richting = 0 # aflopend | oplopend
        self.ModbusInstance = ModbusInstance
        self.Zones = []

        self.StartAddresses = start_addresses = [3000, 3006, 3012, 3018, 3024, 3030, 3036]  # start addresses
        
        for start_address in start_addresses:
            zone = Zone(ModbusInstance, start_address)
            self.Zones.append(zone)


    def update(self):
        for zone in self.Zones:
            regs = self.ModbusInstance.get(zone.StartAddress, 6)
            if regs:
                zone.niveau = regs[2]  
                zone.capaciteit_beschikbaar = regs[3]
                zone.energieverbruik = regs[4]
                zone.branduren = regs[5]
                self.Bereikbaar = 1
        

