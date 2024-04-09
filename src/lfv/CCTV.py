from typing import List
from modbus import *

MODBUS_CCTV_IP = "192.168.10.110"

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

        self.SetTilt(self.TiltStand)
        self.SetPan(self.PanStand)
        self.SetPreset(self.Preset)
        self.SetZoom(self.ZoomStand)

    def SetTilt(self, tilt):
            self.TiltStand = tilt
            self.ModbusInstance.set(MODBUS_CCTV_IP,self.start_address + 1, tilt)

    def SetPan(self, pan):
            self.PanStand = pan
            self.ModbusInstance.set(MODBUS_CCTV_IP, self.start_address, pan)

    def SetZoom(self, zoom):
            self.ZoomStand = zoom
            self.ModbusInstance.set(MODBUS_CCTV_IP,self.start_address + 2, zoom)

    def SetPreset(self, preset):
            self.Preset = preset
            self.ModbusInstance.set(MODBUS_CCTV_IP,self.start_address + 3, preset)

class Cameras:
    def __init__(self, ModbusInstance: modbus, num_cameras: int):
        self.cameras: List[CCTV] = []
        self.ModbusInstance = ModbusInstance
        self.num_cameras = num_cameras

        for i in range(num_cameras):
            start_address = 5100 + (i * 4)
            camera = CCTV(ModbusInstance, start_address)
            self.cameras.append(camera)

