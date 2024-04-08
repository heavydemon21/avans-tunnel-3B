from typing import List
from modbus import *

#TODO fix hardcoded addresses

class CCTV:
    def __init__(self, ModbusInstance: modbus, start_address: int):
        self.Bereikbaar = 0
        self.IdentificatieCode = 0
        self.PanStand = 180
        self.TiltStand = 0
        self.ZoomStand = 10
        self.FocusStand = {}
        self.Diafragma = {}
        self.Preset = 0

        self.ModbusInstance = ModbusInstance
        self.start_address = start_address

    def SetTilt(self, tilt):
        if self.Bereikbaar:
            self.TiltStand = tilt
            self.ModbusInstance.set(self.start_address + 1, tilt)

    def SetPan(self, pan):
        if self.Bereikbaar:
            self.PanStand = pan
            self.ModbusInstance.set(self.start_address, pan)

    def SetZoom(self, zoom):
        if self.Bereikbaar:
            self.ZoomStand = zoom
            self.ModbusInstance.set(self.start_address + 2, zoom)

    def SetPreset(self, preset):
        if self.Bereikbaar:
            self.Preset = preset
            self.ModbusInstance.set(self.start_address + 3, preset)

class Cameras:
    def __init__(self, ModbusInstance: modbus, num_cameras: int):
        self.cameras: List[CCTV] = []
        self.ModbusInstance = ModbusInstance
        self.num_cameras = num_cameras

        for i in range(num_cameras):
            start_address = 5100 + (i * 4)
            camera = CCTV(ModbusInstance, start_address)
            self.cameras.append(camera)

