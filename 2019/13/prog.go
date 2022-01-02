package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

func printm(grid map[[2]int]int, tl, br [2]int) {
	for y := tl[1]; y <= br[1]; y++ {
		for x := tl[0]; x <= br[0]; x++ {
			var o string
			xy := [2]int{x, y}
			if grid[xy] == 0 {
				o = " "
			} else if grid[xy] == 1 {
				o = "H"
			} else if grid[xy] == 2 {
				o = "#"
			} else if grid[xy] == 3 {
				o = "T"
			} else if grid[xy] == 4 {
				o = "O"
			} else {
				panic("invalid value")
			}
			fmt.Printf("%v", o)
		}
		fmt.Println()
	}
}

func run_game(prog []string, part int) {
	ich := make(chan int, 1)
	och := make(chan int, 0)

	board := make(map[[2]int]int)
	pos := [2]int{0, 0}
	if part > 1 {
		prog[0] = "2"
	}
	go intcode.RunProg(prog, ich, och)
	xm := 0
	ym := 0
	board_done := false
	paddlex := 0
	score := 0
	for true {
		x := <-och
		y := <-och
		id, ok := <-och
		if !ok {
			break
		}
		if id == 3 {
			paddlex = x
		}
		if x > xm {
			xm = x
		}
		if y > ym {
			ym = y
		}
		if x < 0 {
			// fmt.Printf("score %v\n", id)
			score = id
			if !board_done {
				ich <- 0
			}
			board_done = true
		} else {
			pos[0] = x
			pos[1] = y
			board[pos] = id
		}
		// fmt.Printf("%v %v %v p %v\n", x, y, id, paddlex)

		if board_done && id == 4 {
			// printm(board, [2]int{0, 0}, [2]int{xm, ym})
			if paddlex > x {
				ich <- -1
			} else if paddlex < x {
				ich <- 1
			} else {
				ich <- 0
			}
		}
	}
	// printm(board, [2]int{0, 0}, [2]int{xm, ym})
	if part == 1 {
		cnt := 0
		for _, v := range board {
			if v == 2 {
				cnt += 1
			}
		}
		fmt.Printf("Part1: %v\n", cnt)
	} else {
		fmt.Printf("Part2: %v\n", score)
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	run_game(prog, 1)
	run_game(prog, 2)
}
