from modbus import modbus

t = modbus('86.88.46.183', 502)

print(t.get(1000, 5))
print(t.set(1000, [0]))
print(t.get(1000, 5))
