
from WebSocket import snelheidAutoPerZone, autoPerZone, sosBericht, lfvStatusStoring, lfvStatussen
from lfv.Afsluitboom import Afsluitboom
from lfv.CCTV import Cameras
from lfv.Matrixbord import Matrix
from lfv.Verkeerslicht import Verkeerslicht
from lfv.Verlichting import Verlichting
from lfv.SOS import SOS
from modbus import *
from process_sos import *

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
        

    def  detect_confict(self):
        if self.Sos.Deel1_Spookrijder == 1:
            sosBericht(True, "Spookrijder op deel 1")
            sos_on(self,1)
            return True
        if self.Sos.Deel2_Spookrijder == 1:
            sosBericht(True, "Spookrijder op deel 2")
            sos_on(self,1)
            return True
        if self.Sos.Deel3_Spookrijder == 1:
            sosBericht(True, "Spookrijder op deel 3")
            sos_on(self,1)
            return True

        if self.Sos.Zone1_Stilstanden >= 1:
            sosBericht(True,"stilstand in zone 1")
            sos_on(self,1)
            return True
        if self.Sos.Zone2_Stilstanden >= 1:
            sosBericht(True,"stilstand in zone 2")
            sos_on(self,1)
            return True
        return False

    def update_all(self):
        self.Verlichting.update()
        self.Sos.update()
        self.Verkeerslicht.update()
        self.Afsluitboom.update()
        self.Matrix.update()

