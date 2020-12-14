import sys
import time
import re

valid = 0
with open(sys.argv[1]) as f:
    for line in f:
        numbers = re.search('(\d+)-(\d+) ([a-z]): (.*)', line) 
        if (numbers):
            cnt_min = int(numbers.group(1))
            cnt_max = int(numbers.group(2))
            char = numbers.group(3)
            pwd = numbers.group(4)
            count = pwd.count(char)
            ok = "NOT"
            if ((pwd[cnt_min - 1] == char and pwd[cnt_max - 1] != char) or (pwd[cnt_min - 1] != char and pwd[cnt_max - 1] == char)):
                ok = "OK"
                valid+=1
            print("Lines", numbers.group(1), numbers.group(2), numbers.group(3), numbers.group(4), "count", count, pwd[cnt_min - 1],  pwd[cnt_max - 1], "valid", valid, ok, len(pwd))
            
print("valid ", valid)
        

