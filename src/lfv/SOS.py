from lfv.Afsluitboom import MODBUS_PLC_IP
from modbus import *

MODBUS_SOS_IP = MODBUS_PLC_IP

class SOS:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0

        self.Zone1_SnelheidsOnderschijding= []
        self.Zone2_SnelheidsOnderschijding= []

        self.Deel1_Spookrijder = []
        self.Deel2_Spookrijder = []
        self.Deel3_Spookrijder = []
        self.Zone1_Stilstanden = []
        self.Zone2_Stilstanden = []

        self.Zone1_DisabledDetectiepunten = []
        self.Zone2_DisabledDetectiepunten = []
        self.Zone1_DectorenMetStoring = []
        self.Zone2_DectorenMetStoring = []
        self.ModbusInstance = ModbusInstance




    def update(self):
        self.Bereikbaar = self.ModbusInstance.get(MODBUS_SOS_IP,4000)

        Snelheid = self.ModbusInstance.get(MODBUS_SOS_IP,4200,2)
        if Snelheid:
            self.Zone1_SnelheidsOnderschijding = Snelheid[0]
            self.Zone2_SnelheidsOnderschijding = Snelheid[1]

        Stilstand = self.ModbusInstance.get(MODBUS_SOS_IP,4210,2)
        if Stilstand:
            self.Zone1_Stilstanden = Stilstand[0]
            self.Zone2_Stilstanden = Stilstand[1]

        Zonesdisabled = self.ModbusInstance.get(MODBUS_SOS_IP,4220,2)
        if Zonesdisabled:
            self.Zone1_DisabledDetectiepunten = Zonesdisabled[0]
            self.Zone2_DisabledDetectiepunten = Zonesdisabled[1]

        Storing = self.ModbusInstance.get(MODBUS_SOS_IP,4230, 2)
        if Storing:
            self.Zone1_DectorenMetStoring = Storing[0]
            self.Zone1_DectorenMetStoring = Storing[1]

        Spookrijder = self.ModbusInstance.get(MODBUS_SOS_IP,4240, 3)
        if Spookrijder:
            self.Deel1_Spookrijder = Spookrijder[0]
            self.Deel2_Spookrijder = Spookrijder[1]
            self.Deel3_Spookrijder = Spookrijder[2]


    def SetEnabled(self,RijStrook: int, LengtePositoe: int, Beschikbaar: int):
        self.Bereikbaar = Beschikbaar
                                                          
        
