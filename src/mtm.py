
from pyModbusTCP.client import ModbusClient

CONST_MTM_STARTADDR = 7000
CONST_MTM_IP = "192.168.10.111"

c = ModbusClient(host=CONST_MTM_IP, auto_open=True,auto_close=True)

class mtm:
    def __init__(self, Board):
        BoardStartAddress = CONST_MTM_STARTADDR + (Board * 10 - 10)
        self.Board = Board
        self.BoardCommand = BoardStartAddress
        self.BoardStand = BoardStartAddress + 1
        self.BoardAvailable = BoardStartAddress + 2
        self.BoardFlash = BoardStartAddress + 3
        self.BoardMalfunction = BoardStartAddress + 4

    def ReadHoldingRegisters(self, start = 0, NumReg = 1):
        regs = c.read_holding_registers(start-1, NumReg)
        if regs :
            print("mtm board: %d,  %s" %self.Board %regs)
            return regs
        else:
            print("Error reading mtm board: %d" %self.Board)

    def WriteRegister(self, Value):
        c.write_single_register(self.BoardCommand, Value)

