import sys
import time
import re

int_list = []
with open(sys.argv[1]) as f:
    for line in f:
        int_list.append(int(line))

print("Lines", int_list, "sz ", len(int_list))

for i in range(len(int_list)): 
    for j in range(len(int_list)):
        for k in range(len(int_list)):
            if (int_list[i] + int_list[j] + int_list[k] == 2020):
                print("i", i, "j", j, "k", k , int_list[i], int_list[j], int_list[k], "mul", int_list[j] * int_list[i] * int_list[k])