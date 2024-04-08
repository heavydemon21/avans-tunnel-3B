



from lfv.Afsluitboom import Afsluitboom
from lfv.CCTV import Cameras
from lfv.Matrixbord import Matrix
from lfv.Verkeerslicht import Verkeerslicht
from lfv.Verlichting import Verlichting
from lfv.SOS import SOS
from modbus import *


class process_lfv:
    def __init__(self, ip : str, port : int):
        self.modbus = modbus(ip= ip, port=port)
        self.Verlichting = Verlichting(self.modbus)
        self.Sos = SOS(self.modbus)
        self.Verkeerslicht = Verkeerslicht(self.modbus, 4)
        self.Matrix = Matrix(self.modbus)
        self.Afsluitboom = Afsluitboom(self.modbus)

        NumberOfCameras = 3
        self.cameras = Cameras(self.modbus, NumberOfCameras)
        


    def update_all(self):
        self.Verlichting.update()
        self.Sos.update()
        self.Verkeerslicht.update()
        self.Afsluitboom.update()
        self.Matrix.update()

