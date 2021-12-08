import sys 

def printm(matrix):
    for r in matrix:
        for c in r:
            print("%1d" % int(c), end='')
        print("")

def range2(start, stop):
    step = -1 if start > stop else 1
    return range(start, stop + step, step)

#maxv = 10
maxv = 1000
def run(part2):
    matrix = [[0 for i in range(maxv)] for j in range(maxv)]
    with open(sys.argv[1]) as f:
        for line in f:
            tokens = line.split()
            xy1 = tokens[0].split(',')
            xy2 = tokens[2].split(',')
            x1 = int(xy1[0])
            y1 = int(xy1[1])
            x2 = int(xy2[0])
            y2 = int(xy2[1])
        
            #print(tokens, x1, y1, x2, y2)
            if (x1 == x2 or y1 == y2):
                for y in range2(y1, y2):
                    for x in range2(x1, x2):
                        #print(x, y)
                        matrix[y][x] += 1
                #printm(matrix)
            else:
                if not part2:
                    print("nonv")
                    continue
                for y in range2(y1, y2):
                    for x in range2(x1, x2):
                        #print(x, y)
                        matrix[y][x] += 1
                        if x == x2 and y == y2:
                            break
                        y += -1 if y1 > y2 else 1
                    if x == x2 and y == y2:
                        break
                #printm(matrix)

        ans = 0
        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x] >1:
                    ans += 1
        print (ans)
            
run(0) if len(sys.argv) < 3 or sys.argv[2] == "1" else run(1)