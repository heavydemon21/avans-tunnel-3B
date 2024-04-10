from modbus import modbus

t = modbus()
ip="192.168.10.126"

print(t.get(ip, 0, 5))
# print(t.set(ip, 0, [1]))
# print(t.get(ip, 0, 5))
