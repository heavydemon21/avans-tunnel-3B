


from modbus import *

class SOS:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.SnelheidsOnderschijding= []
        self.Spookrijder = []
        self.Stilstanden = []
        self.DisabledDetectiepunten = []
        self.DectorenMetStoring = []
        self.ModbusInstance = ModbusInstance


    def update(self):
        self.Bereikbaar = self.ModbusInstance.get(4000)
        self.SnelheidsOnderschijding = self.ModbusInstance.get(4100,20)
        self.Stilstanden = self.ModbusInstance.get(4125, 20)
        self.DisabledDetectiepunten = self.ModbusInstance.get(4150,20)
        self.DectorenMetStoring = self.ModbusInstance.get(4175, 20)

    #TODO: verbeter set
    def SetEnabled(self,RijStrook: int, LengtePositoe: int, Beschikbaar: int):
        self.Bereikbaar = Beschikbaar
                                                          
        
