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
	OP_RELB     = 9
	OP_END      = 99
)
const (
	PMODE_POS int = 0
	PMODE_IMM     = 1
	PMODE_REL     = 2
)

func get_pmode(op, pidx int) int {
	pmode := op % 1000 / 100
	if pidx == 2 {
		pmode = op % 10000 / 1000
	} else if pidx == 3 {
		pmode = op % 100000 / 10000
	}
	return pmode
}

func getp(prog map[int]int, pos int, pidx int, relbase int) int {
	pmode := get_pmode(prog[pos], pidx)
	if pmode == PMODE_REL {
		offset := prog[pos+pidx]
		return prog[relbase+offset]
	} else if pmode == PMODE_IMM {
		return prog[pos+pidx]
	} else {
		return prog[prog[pos+pidx]]
	}
}

func putp(prog map[int]int, pos, pidx, relbase, val int) {
	pmode := get_pmode(prog[pos], pidx)
	wra := 0
	if pmode == PMODE_REL {
		offset := prog[pos+pidx]
		wra = relbase + offset
	} else {
		wra = prog[pos+pidx]
	}
	prog[wra] = val
}

func run_prog(strarr []string, input []int) []int {
	prog := make(map[int]int)
	for i, s := range strarr {
		j, _ := strconv.Atoi(s)
		prog[i] = j
	}
	pos := 0
	in_idx := 0
	output := make([]int, 0)
	relbase := 0
	for true {
		op := prog[pos] % 100
		res := 0
		// fmt.Printf("ex %v %v %v %v\n", op, prog[pos], pos, relbase)

		if op == OP_ADD {
			res = getp(prog, pos, 1, relbase) + getp(prog, pos, 2, relbase)
			putp(prog, pos, 3, relbase, res)
			pos += 4
		} else if op == OP_MUL {
			res = getp(prog, pos, 1, relbase) * getp(prog, pos, 2, relbase)
			putp(prog, pos, 3, relbase, res)
			pos += 4
		} else if op == OP_IN {
			r := input[in_idx]
			putp(prog, pos, 1, relbase, r)
			in_idx += 1
			pos += 2
		} else if op == OP_OUT {
			output = append(output, getp(prog, pos, 1, relbase))
			pos += 2
		} else if op == OP_JMPT {
			if getp(prog, pos, 1, relbase) != 0 {
				pos = getp(prog, pos, 2, relbase)
			} else {
				pos += 3
			}
		} else if op == OP_JMPF {
			if getp(prog, pos, 1, relbase) == 0 {
				pos = getp(prog, pos, 2, relbase)
			} else {
				pos += 3
			}
		} else if op == OP_LESS {
			if getp(prog, pos, 1, relbase) < getp(prog, pos, 2, relbase) {
				res = 1
			} else {
				res = 0
			}
			putp(prog, pos, 3, relbase, res)
			pos += 4
		} else if op == OP_EQ {
			if getp(prog, pos, 1, relbase) == getp(prog, pos, 2, relbase) {
				res = 1
			} else {
				res = 0
			}
			putp(prog, pos, 3, relbase, res)
			pos += 4
		} else if op == OP_RELB {
			relbase += getp(prog, pos, 1, relbase)
			pos += 2
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
	strarr := strings.Split(string(dat), ",")
	in := make([]int, 1)
	in[0] = 1
	out := run_prog(strarr, in)
	if len(out) != 1 {
		panic("invald output")
	}
	fmt.Printf("Part1: %v\n", out[0])
	in[0] = 2
	out = run_prog(strarr, in)
	if len(out) != 1 {
		panic("invald output")
	}
	fmt.Printf("Part2: %v\n", out[0])

}
