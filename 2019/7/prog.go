package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
	"sync"

	"gonum.org/v1/gonum/stat/combin"
)

const (
	OP_ADD  int = 1
	OP_MUL      = 2
	OP_IN       = 3
	OP_OUT      = 4
	OP_JMPT     = 5
	OP_JMPF     = 6
	OP_LESS     = 7
	OP_EQ       = 8
	OP_END      = 99
)
const (
	PMODE_POS int = 0
	PMODE_IMM     = 1
)

func getp(prog []int, pos int, pidx int) int {
	pmode := prog[pos] % 1000 / 100
	if pidx == 2 {
		pmode = prog[pos] % 10000 / 1000
	}
	if pmode == PMODE_IMM {
		return prog[pos+pidx]
	} else {
		return prog[prog[pos+pidx]]
	}
}

func run_prog(idx int, strarr []string, read <-chan int, write chan<- int, wg *sync.WaitGroup) {
	defer wg.Done()

	prog := make([]int, len(strarr))
	for i, s := range strarr {
		j, _ := strconv.Atoi(s)
		prog[i] = j
	}
	pos := 0
	for true {
		op := prog[pos] % 100

		if op == OP_ADD {
			prog[prog[pos+3]] = getp(prog, pos, 1) + getp(prog, pos, 2)
			pos += 4
		} else if op == OP_MUL {
			prog[prog[pos+3]] = getp(prog, pos, 1) * getp(prog, pos, 2)
			pos += 4
		} else if op == OP_IN {
			// fmt.Printf("try read %v\n", idx)
			r := <-read
			// fmt.Printf("try read %v %v\n", idx, r)
			prog[prog[pos+1]] = r
			pos += 2
		} else if op == OP_OUT {
			// fmt.Printf("write %v %v\n", idx, getp(prog, pos, 1))
			write <- getp(prog, pos, 1)
			pos += 2
		} else if op == OP_JMPT {
			if getp(prog, pos, 1) != 0 {
				pos = getp(prog, pos, 2)
			} else {
				pos += 3
			}
		} else if op == OP_JMPF {
			if getp(prog, pos, 1) == 0 {
				pos = getp(prog, pos, 2)
			} else {
				pos += 3
			}
		} else if op == OP_LESS {
			if getp(prog, pos, 1) < getp(prog, pos, 2) {
				prog[prog[pos+3]] = 1
			} else {
				prog[prog[pos+3]] = 0
			}
			pos += 4
		} else if op == OP_EQ {
			if getp(prog, pos, 1) == getp(prog, pos, 2) {
				prog[prog[pos+3]] = 1
			} else {
				prog[prog[pos+3]] = 0
			}
			pos += 4
		} else if op == OP_END {
			break
		} else {
			panic("invalid opcode")
		}
	}
}

const MAX_AMP = 5
const MAX_PHASE = 5

func calc_amp(part2 bool, strarr []string) int {
	max := 0
	var ioch [MAX_AMP]chan int
	for i := range ioch {
		ioch[i] = make(chan int, 2)
	}
	perm := combin.Permutations(MAX_PHASE, MAX_AMP)
	for _, p := range perm {

		var wg sync.WaitGroup
		for amp := 0; amp < MAX_AMP; amp++ {
			wg.Add(1)
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
			go run_prog(amp, strarr, ioch[amp], ioch[nextamp], &wg)
		}
		wg.Wait()
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
