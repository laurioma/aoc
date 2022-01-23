package main

import (
	"fmt"
	"os"
	"strings"
	"sync"

	"../intcode"
	"gonum.org/v1/gonum/stat/combin"
)

const MAX_AMP = 5
const MAX_PHASE = 5

func calc_amp(part2 bool, strarr []string) int {
	max := 0
	var ioch [MAX_AMP]chan int
	perm := combin.Permutations(MAX_PHASE, MAX_AMP)
	for _, p := range perm {
		for i := range ioch {
			ioch[i] = make(chan int, 2)
		}
		var runwg sync.WaitGroup
		var wg intcode.RunProgWaitGroups
		wg.Run = &runwg
		for amp := 0; amp < MAX_AMP; amp++ {
			runwg.Add(1)
			// phase
			if part2 {
				ioch[amp] <- p[amp] + 5
			} else {
				ioch[amp] <- p[amp]
			}
			if amp == 0 {
				ioch[amp] <- 0
			}
			nextamp := amp + 1
			if nextamp >= MAX_AMP {
				nextamp = 0
			}

			go intcode.RunProgWG(strarr, ioch[amp], ioch[nextamp], &wg)
		}
		runwg.Wait()
		res := <-ioch[0]
		if max < res {
			max = res
		}
	}
	return max
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	strarr := strings.Split(string(dat), ",")

	ret := calc_amp(false, strarr)
	fmt.Printf("Part1: %v\n", ret)
	ret = calc_amp(true, strarr)
	fmt.Printf("Part2: %v\n", ret)
}
