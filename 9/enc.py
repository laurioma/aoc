import re
import sys

preamble = int(sys.argv[2]) if len(sys.argv) > 2 else 25
numbers = []

print ("preamble", preamble)

with open(sys.argv[1]) as f:
    for line in f:
        numbers.append(int(line))

def check_preamble(idx):
    for i in range(idx - preamble, idx):
        for j in range(idx - preamble, idx):
            if i == j:
                continue
            if numbers[i] == numbers[j]:
                continue
            if numbers[idx] == numbers[i] + numbers[j]:
                print("Check OK", idx, i, j, numbers[idx], "=", numbers[i], "+", numbers[j])
                return True
    return False

def find_invalid_number():
    for i in range(preamble, len(numbers)):
        if (not check_preamble(i)):
            print("Check failed:", i, numbers[i])
            return numbers[i]
    return -1

wrong_number = find_invalid_number()

def search_contiguous(number):
    for i in range(len(numbers)):
        checksum = 0
        smallest = sys.maxsize
        largest = 0
        for j in range(i, len(numbers)):
            checksum += numbers[j]
            if largest < numbers[j]:
                largest = numbers[j]
            if smallest > numbers[j]:
                smallest = numbers[j]
            print("check", i, j, numbers[j], checksum, "s", smallest, "l", largest, "sum", smallest + largest)
            if checksum == number:
                print("found!")
                return
            elif checksum > number:
                print("next")
                break
                
search_contiguous(wrong_number)