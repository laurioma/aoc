import sys

answer = 0
seats = []
#B:1 R:1
with open(sys.argv[1]) as f:
    for line in f:
        res = 0
        for i in range(10):
            print ("i", i, "c:", i, line[i])
            if line[i] == 'B' or line[i] == 'R':
                res += pow(2, 9-i)
        seats.append(res);        
        print ("res", res)
        if answer < res:
            answer = res
#        numbers = re.search('()', line) 
seats.sort()

print ("p1 answ ", answer)

for i in range(1, len(seats)):
    if (abs(seats[i-1] - seats[i]) > 1):
        print("my seat:", i-1, i, seats[i-1], seats[i], "answ p2", seats[i-1] + 1)

