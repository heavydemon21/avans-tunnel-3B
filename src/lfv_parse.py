



from lfv.Afsluitboom import Afsluitboom
from lfv.CCTV import CCTV
from lfv.Matrixbord import Matrix
from lfv.Verkeerslicht import Verkeerslicht
from lfv.Verlichting import Verlichting
from lfv.SOS import SOS
from modbus import *


class process_lfv:
    def __init__(self):
        self.modbus = modbus(ip= "86.88.46.183" , port=502)
        self.Verlichting = Verlichting(self.modbus)
        self.Sos = SOS(self.modbus)
        self.Verkeerslicht = Verkeerslicht(self.modbus)
        self.Matrix = Matrix(self.modbus)
        self.Afsluitboom = Afsluitboom(self.modbus)

        #TODO: fix harcoded camera
        self.Camera1 = CCTV(self.modbus)
        


    def update_all(self):
        self.Verlichting.update()
        self.Sos.update()
        self.Verkeerslicht.update()
        self.Afsluitboom.update()
        self.Matrix.update()

