package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
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

func run_prog(strarr []string, input []int) []int {
	prog := make([]int, len(strarr))
	for i, s := range strarr {
		j, _ := strconv.Atoi(s)
		prog[i] = j
	}
	in_idx := 0
	output := make([]int, 0)
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
			prog[prog[pos+1]] = input[in_idx]
			in_idx += 1
			pos += 2
		} else if op == OP_OUT {
			output = append(output, getp(prog, pos, 1))
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
	return output
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])

	dats := string(dat)
	strarr := strings.Split(dats, ",")

	in := make([]int, 1)
	in[0] = 1
	out := run_prog(strarr, in)
	answ1 := out[len(out)-1]
	in[0] = 5
	out = run_prog(strarr, in)
	answ2 := out[len(out)-1]

	fmt.Printf("Part1: %v\n", answ1)
	fmt.Printf("Part2: %v\n", answ2)

	return
}
