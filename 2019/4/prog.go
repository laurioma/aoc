package main

import (
	"fmt"
	"strconv"
)

func main() {
	range_min := 158126
	range_max := 624574
	cnt1 := 0
	cnt2 := 0
	for i := range_min; i < range_max; i++ {
		nstr := strconv.Itoa(i)
		adj_same := false
		adj_same2 := false
		increasing := true
		for j := 1; j < len(nstr); j += 1 {
			if nstr[j] == nstr[j-1] {
				adj_same = true
			}
			if nstr[j] == nstr[j-1] && (j == 1 || nstr[j] != nstr[j-2]) && (j == len(nstr)-1 || nstr[j] != nstr[j+1]) {
				adj_same2 = true
			}
			if nstr[j] < nstr[j-1] {
				increasing = false
				break
			}
		}
		if adj_same && increasing {
			cnt1 += 1
		}
		if adj_same2 && increasing {
			cnt2 += 1
		}
	}
	fmt.Printf("Part1: %v\n", cnt1)
	fmt.Printf("Part2: %v\n", cnt2)

	return
}
