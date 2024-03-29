from modbus import *

#TODO fix hardcoded addresses
class CCTV:
    def __init__(self, ModbusInstance: modbus):
        self.Bereikbaar = 0
        self.IdentificatieCode = 0
        self.PanStand = 180
        self.TiltStand = 0
        self.ZoomStand = 10
        self.FocusStand = {}
        self.Diafragma = {}
        self.Preset = 0

        self.ModbusInstance = ModbusInstance


    def SetTilt(self, tilt):
        if self.Bereikbaar:
            self.TiltStand = tilt
            self.ModbusInstance.set(5001, tilt)

    def SetPan(self, pan):
        if self.Bereikbaar:
            self.PanStand = pan
            self.ModbusInstance.set(5000, pan)


    def SetZoom(self, zoom):
        if self.Bereikbaar:
            self.ZoomStand = zoom
            self.ModbusInstance.set(5002, zoom)

    def SetPreset(self, preset):
        if self.Bereikbaar:
            self.Preset = preset
            self.ModbusInstance.set(5003,preset)
