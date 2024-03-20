from modbus import *

modbus_get("localhost")

modbus_set(10, [44, 55], "localhost")

