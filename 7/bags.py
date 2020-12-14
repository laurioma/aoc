import sys
import re

bag_map = dict()
with open(sys.argv[1]) as f:
    for line in f:
        bags = re.search('(.*) bags contain (.*)\.', line) 
        if (bags):
#            print ("CONTAINER {0}".format(bags.group(1)))
            contained = dict()
            for bag in bags.group(2).split(","):
                color = re.search('(\d+) (.*) (bags|bag)', bag) 
                if (color):
                    print("contains", color.group(1), color.group(2))
                    contained[color.group(2)] = color.group(1)
                elif (bag != "no other bags"):
                    print ("PARSE ERR2", bag)
            bag_map[bags.group(1)] = contained
        else:
            print ("PARSE ERR")

print("PARSED", len(bag_map), "colors")   

def contains_shiny_gold(key):
    print ("check", key)
    for col in bag_map[key]:
        if (col == "shiny gold"):
            print (key, "can contain", col)
            return True
        elif(key == col):
            continue;
        elif (contains_shiny_gold(col)):
            print ("recursive", key, "can contain", col)
            return True
    print ("{0} CANT contain shiny gold",key)        
    return False

def check_shiny_gold():
    count = 0
    for key in bag_map:
        if (contains_shiny_gold(key)):
            count+=1
            print ("CAN CONTAIN", key, count)
        else:
            print ("CANT CONTAIN ", key, count)


def count_bags_inside(key, lvl):
    print (lvl, "count", key)
    bags_inside = 0
    for col in bag_map[key]:
        bags_inside += (1 + count_bags_inside(col, lvl+1) ) * int(bag_map[key][col]);
    print (lvl, "done count", key, bags_inside)
    return bags_inside
    

ret = count_bags_inside("shiny gold", 0)
print("COUNTED", ret, "bags")
