import sys
#6-7 z: dqzzzjbzz

matrix = []
with open(sys.argv[1]) as f:
    for line in f:
        if line.rstrip() == "":
            break
        matrix.append(line.rstrip())


print("rows ", len(matrix),  " c ", len(matrix[0]))

def ride(stepl, stepd):
    col = stepl
    count = 0
    for i in range(1,int(len(matrix)/stepd)):       
        row = i*stepd
        col_ = col % len(matrix[0])
#        print("row", row,  "col", col, " ", col_, len(matrix[row]), len(matrix))
        if (matrix[row][col_] == '#'):
            count+=1
        col += stepl

    print("done: count ", count)
    return count


r = ride(3, 1)
print ("part1 res ", r)

r1 = ride(1, 1)
r2 = ride(3, 1)
r3 = ride(5, 1)
r4 = ride(7, 1)
r5 = ride(1, 2)

print ("part2 res ", r1*r2*r3*r4*r5)
