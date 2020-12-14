import sys
import time

with open(sys.argv[1]) as f:
    lines = f.readlines()
    
timestamp = int(lines[0])

buses = []
bus_idx = 0

for b in lines[1].split(","):
    if b != 'x':
        buses.append([int(b), bus_idx, (int(b) - bus_idx) % int(b)]);
    bus_idx += 1

print("ts", timestamp, "buses", buses)

wait_time = sys.maxsize
best_bus = 0
for bus in buses:
    depart = (int(timestamp / bus[0])+1)* bus[0]
    if wait_time > (depart - timestamp):
        wait_time = (depart - timestamp)
        best_bus = bus[0]
    print("div ", timestamp / bus[0], " depart ", depart, " min_dst ", wait_time, "best_bus", best_bus, "mul", wait_time*best_bus)

print("answer p1", wait_time*best_bus)

buses.sort(key=lambda x: x[0], reverse=True)
print("sorted", buses)
timestamp = 0

start_t = time.time()

#bruteforce

# lap = 1
# while (True):
    # timestamp = buses[0][0] * lap - buses[0][1]
    # lap+=1
    # failed = False
    # for i in range(1, len(buses)):
        # check = timestamp + buses[i][1]
        # if check % buses[i][0] != 0:
# #               print("Fail ts", timestamp, "bus", i, buses[i], "bus_dep", next_depart, "diff", diff, "diff wanted", buses[i][1])
            # failed = True
            # break;

    # if lap & 0xffffff == 0xffffff:
        # print ("ts", timestamp, "time", time.time() - start_t)
    # if not failed:
        # print ("Success", timestamp)
        # break;

#CRT https://en.wikipedia.org/wiki/Chinese_remainder_theorem
lap = 0
step = buses[0][0]
timestamp = buses[0][2]
state = 1
while (True):
    timestamp += step
    
    failed = False

#    print ("ts ", timestamp, "step", step)
    if timestamp % buses[state][0] == buses[state][2]:
        step *= buses[state][0]
        state += 1
        print("state ", state, "step", step)
        if state == len(buses):
            print("FOUND?", timestamp)
            check = True
            for i in range(len(buses)):
                if timestamp % buses[i][0] != buses[i][2]:
                    print("Fail ts", timestamp, "bus", i, buses[i], "diff wanted", buses[i][1])
                    check = False
                    break
            if check:
                print("Found!!")
            break

print("answer p2", timestamp)