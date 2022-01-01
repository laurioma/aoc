package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

const (
	ADD int = 1
	MUL     = 2
	END     = 99
)

func run_prog(strarr []string, noun, verb int) int {
	prog := make([]int, len(strarr))
	for i, s := range strarr {
		j, _ := strconv.Atoi(s)
		prog[i] = j
	}
	prog[1] = noun
	prog[2] = verb
	pos := 0
	for true {
		if prog[pos] == ADD {
			a1 := prog[prog[pos+1]]
			a2 := prog[prog[pos+2]]
			prog[prog[pos+3]] = a1 + a2
			pos += 4
		} else if prog[pos] == MUL {
			a1 := prog[prog[pos+1]]
			a2 := prog[prog[pos+2]]
			prog[prog[pos+3]] = a1 * a2
			pos += 4
		} else if prog[pos] == END {
			break
		} else {
			panic("invalid opcode")
		}
	}
	return prog[0]
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])

	dats := string(dat)
	strarr := strings.Split(dats, ",")

	answ1 := run_prog(strarr, 12, 2)
	answ2 := 0
	for i := 0; i < len(strarr); i++ {
		for j := 0; j < len(strarr); j++ {
			if run_prog(strarr, i, j) == 19690720 {
				answ2 = i*100 + j
				break
			}
		}
	}

	fmt.Printf("Part1: %v\n", answ1)
	fmt.Printf("Part2: %v\n", answ2)

	return
}
