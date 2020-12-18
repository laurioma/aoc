import json
import datetime
import sys

with open('lead.txt', encoding="utf-8") as json_file:
    data = json.load(json_file)
#    print(data)


#buses.sort(key=lambda x: x[0], reverse=True)

mem = data["members"]
print("members", len(mem))

def daysplaces(daynr):
    dayplaces = {}
    for i in range(1,18):
        times = []
        for m in mem:
            comp = mem[m]["completion_day_level"]
            key = str(i)
            if key in comp:
                if '1' in comp[key] and '2' in comp[key]:
                    t1 = comp[key]['1']['get_star_ts']
                    t2 = comp[key]['2']['get_star_ts']
                    lvl2 = int(t2) - int(t1)
                    name = mem[m]["name"]
                    if not name:
                        name = "a"+mem[m]["id"]
                    times.append([name, lvl2])
        times.sort(key = lambda x: x[1])
#+        print (times)
        place = 1
        for t in times:
            if not t[0] in dayplaces:
                dayplaces[t[0]] = {}
            dayplaces[t[0]][i] = [t[1], place]
            dayplaces[t[0]]["sum"] = dayplaces[t[0]].get("sum", 0) + t[1]
            dayplaces[t[0]]["avg"] = dayplaces[t[0]]["sum"]  / len(dayplaces[t[0]])
            dayplaces[t[0]]["points"] = dayplaces[t[0]].get("points", 0) + (len(mem) - place)
            place += 1

    if (daynr < 0):
        print("{0:23}".format("day"), end=' ')
        for i in range(1,18):
            print(" {0:<12}".format(i), end=' ')
        print()
        place = 1
        for k in sorted(dayplaces, key=lambda x: dayplaces[x]["points"], reverse=True):
            print("{0:2} {1:15} {2:4}".format(place, k[0:15], dayplaces[k]["points"]), end=' ')
            for i in range(1,18):
                time = "0"
                dayplace = 0
                if i in dayplaces[k]:
                    time = str(datetime.timedelta(seconds=dayplaces[k][i][0]))
                    dayplace = dayplaces[k][i][1]
                print("{0:2} {1:10}".format(dayplace, time[0:10]), end = ' ')
            print()
            place += 1
    else:
        place = 1
        for k in sorted(dayplaces, key=lambda x: dayplaces[x][daynr]):
            if daynr in dayplaces[k]:
                print(place, k, "{0}({1})".format(datetime.timedelta(seconds=dayplaces[k][i][0]), dayplaces[k][daynr][1]))
                place += 1

daynr = -1 if len(sys.argv) < 2 else int(sys.argv[1])
daysplaces(daynr)