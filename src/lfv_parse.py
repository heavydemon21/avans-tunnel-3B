
from lfv.Afsluitboom import Afsluitboom
from lfv.CCTV import Cameras
from lfv.Matrixbord import Matrix
from lfv.Verkeerslicht import Verkeerslicht
from lfv.Verlichting import Verlichting
from lfv.SOS import SOS
from modbus import *

class process_lfv:
    def __init__(self):
        self.modbus = modbus()
        self.Verlichting = Verlichting(self.modbus)
        self.Sos = SOS(self.modbus)
        self.Verkeerslicht = Verkeerslicht(self.modbus, 4)
        self.Matrix = Matrix(self.modbus)
        self.Afsluitboom = Afsluitboom(self.modbus)

        NumberOfCameras = 3
        self.cameras = Cameras(self.modbus, NumberOfCameras)
        

    def  detect_conflict(self):
        if self.Sos.Deel1_Spookrijder == 1:
            # sosBericht(True, "Spookrijder op deel 1")
            sos_on(self,1)
            return 1
        if self.Sos.Deel2_Spookrijder == 1:
            # sosBericht(True, "Spookrijder op deel 2")
            sos_on(self,1)
            return 2
        if self.Sos.Deel3_Spookrijder == 1:
            # sosBericht(True, "Spookrijder op deel 3")
            sos_on(self,1)
            return 3

        if self.Sos.Zone1_Stilstanden >= 1:
            # sosBericht(True,"stilstand in zone 1")
            sos_on(self,1)
            return 4
        if self.Sos.Zone2_Stilstanden >= 1:
            # sosBericht(True,"stilstand in zone 2")
            sos_on(self,1)
            return 5
        return 0

    def update_all(self):
        self.Verlichting.update()
        self.Sos.update()
        self.Verkeerslicht.update()
        self.Afsluitboom.update()
        self.Matrix.update()

def sos_on(lfv: process_lfv , zone: int):
    lfv.Verkeerslicht.SetStand([1])
    while lfv.Verkeerslicht.Stand != 1:
        lfv.Verkeerslicht.update()
    lfv.Afsluitboom.SetStand([1])
    for z in lfv.Verlichting.Zones:
        z.SetAutoRegeling(False)
    lfv.Verlichting.SetStand([10])
    lfv.Matrix.SetStand([1])
    #TODO camera stand toevoegen


def sos_off(lfv: process_lfv ):
    lfv.Afsluitboom.SetStand([2])
    while lfv.Afsluitboom.Stand != 3:
        lfv.Afsluitboom.update()
    lfv.Verkeerslicht.SetStand([2])
    for zone in lfv.Verlichting.Zones:
        zone.SetAutoRegeling(True)
    lfv.Matrix.SetStand([0])
    