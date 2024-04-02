from modbus import modbus

t = modbus('86.88.46.183', 502)

def sos_on():
    #traffic lights
    t.set(00,[1])
    t.set(4,[1])
    t.set(8,[1])
    t.set(12,[1])
    #barrier
    t.set(1000,[1])
    t.set(1006,[1])
    #lights
    t.set(2000,[10])
def sos_off():
    #traffic lights
    t.set(00,[2])
    t.set(4,[2])
    t.set(8,[2])
    t.set(12,[2])
    #barrier
    t.set(1000,[2])
    t.set(1006,[2])
    #lights
    for i in range(7):
        t.set(3001 + (i*6),[1])


def read_onderschrijding():
    #sos detectors rijstrook 1
    #onderschrijding
    result_list = []
    result_list.append(t.get(4100, 21))
    result_list.append(t.get(4200, 21))
    result_list.append(t.get(4300, 21))
    result_list.append(t.get(4400, 21))
    #print("onderschrijding:")
    #print(list)
    return list

def read_stilstand():
    #sos detectors rijstrook 1
    #onderschrijding
    result_list = []
    result_list.append(t.get(4125, 21))
    result_list.append(t.get(4225, 21))
    result_list.append(t.get(4325, 21))
    result_list.append(t.get(4425, 21))
    # print("stilstand:")
    # print(list)
    return list
    
def read_disabled():
    result_list = []
    result_list.append(t.get(4150, 21))
    result_list.append(t.get(4250, 21))
    result_list.append(t.get(4350, 21))
    result_list.append(t.get(4450, 21))
    #print("Disabled:")
    #print(list)
    return list

def read_storing():
    result_list = []
    result_list.append(t.get(4175, 21))
    result_list.append(t.get(4275, 21))
    result_list.append(t.get(4375, 21))
    result_list.append(t.get(4475, 21))
    #print("storing:")
    #print(list)
    return list
# def check_conflict():
    

def check_conflict():
    stilstand_list = read_stilstand()
    onderschrijding_list = read_onderschrijding()
    disabled_list = read_disabled()
    storing_list = read_storing()
    # test variable
    # stilstand_list = [[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
    # onderschrijding_list = [[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
    # disabled_list = [[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
    # storing_list = [[0,0,0,1],[1,1,0,0],[1,0,1,0],[1,0,0,1]]
    stilstand_count = 0
    for lane_idx, lane in enumerate(stilstand_list):
        for position_idx, position in enumerate(lane):
            if position > 0:
                sos_on()
                stilstand_count = stilstand_count + 1
                print("stilstand op stook %d en positie: %d" % (lane_idx, position_idx))

    for lane_idx, lane in enumerate(onderschrijding_list):
        for position_idx, position in enumerate(lane):
            if position > 0:
                print("onderschrijding op stook %d en positie: %d" % (lane_idx, position_idx))

    for lane_idx, lane in enumerate(storing_list):
        for position_idx, position in enumerate(lane):
            if position > 0:
                print("storing op stook %d en positie: %d" % (lane_idx, position_idx))
    if stilstand_count == 0:
        sos_off()

check_conflict()