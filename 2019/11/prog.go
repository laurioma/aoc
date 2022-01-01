package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

func printm(grid map[[2]int]int, pos, tl, br [2]int) {
	for y := br[1]; y <= tl[1]; y++ {
		for x := tl[0]; x <= br[0]; x++ {
			o := "."
			xy := [2]int{x, y}
			if xy == pos {
				o = "X"
			} else if grid[xy] == 1 {
				o = "#"
			}
			fmt.Printf("%v", o)
		}
		fmt.Println()
	}
}

func MockProg(prog []string, read <-chan int, write chan<- int) {
	commands := [][2]int{{1, 0}, {0, 0}, {1, 0}, {1, 0}, {0, 1}, {1, 0}, {1, 0}}
	for _, c := range commands {
		<-read
		write <- c[0]
		write <- c[1]
	}
	close(write)
}

func run_painting(prog []string, part int) {
	ich := make(chan int, 1)
	och := make(chan int, 0)

	ship := make(map[[2]int]int)
	pos := [2]int{0, 0}
	dir := 0 // 0 up 1 left 2 down 3 right
	if part == 1 {
		ich <- 0
	} else {
		ich <- 1 // initially on black
	}
	go intcode.RunProg(prog, ich, och)
	// go MockProg(strarr, ich, och)
	count := 0
	var tl, br [2]int
	for true {
		paintc, ok := <-och
		if !ok {
			break
		}
		if paintc != 0 && paintc != 1 {
			panic(fmt.Sprintf("invalid paint value %v", paintc))
		}
		if ship[pos] != paintc {
			count += 1
		}
		ship[pos] = paintc
		if pos[0] <= tl[0] {
			tl[0] = pos[0]
		}
		if pos[1] >= tl[1] {
			tl[1] = pos[1]
		}
		if pos[0] >= br[0] {
			br[0] = pos[0]
		}
		if pos[1] <= br[1] {
			br[1] = pos[1]
		}
		turn, ok := <-och
		// println("got values", paintc, turn, dir)
		if !ok {
			panic("shouldn't stop here")
		}
		// turn left 90 deg
		if turn == 0 {
			if dir == 0 {
				pos[0] -= 1
			} else if dir == 1 {
				pos[1] -= 1
			} else if dir == 2 {
				pos[0] += 1
			} else if dir == 3 {
				pos[1] += 1
			} else {
				panic("dir")
			}
			if dir-1 < 0 {
				dir = 3
			} else {
				dir = dir - 1
			}
			// turn right 90 deg
		} else if turn == 1 {
			if dir == 0 {
				pos[0] += 1
			} else if dir == 1 {
				pos[1] += 1
			} else if dir == 2 {
				pos[0] -= 1
			} else if dir == 3 {
				pos[1] -= 1
			} else {
				panic("dir")
			}
			if dir+1 > 3 {
				dir = 0
			} else {
				dir = dir + 1
			}
		} else {
			panic(fmt.Sprintf("invalid turn value %v", turn))
		}
		ich <- ship[pos]
	}
	if part == 1 {
		fmt.Printf("Part1: %v\n", len(ship))
	} else {
		fmt.Printf("Part2:\n")
		printm(ship, pos, tl, br)
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	run_painting(prog, 1)
	run_painting(prog, 2)
}
