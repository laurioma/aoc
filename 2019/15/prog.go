package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

const (
	WALL  int = 0
	EMPTY     = 1
	OXYG      = 2
)

const (
	MOVE_N int = 1
	MOVE_S     = 2
	MOVE_W     = 3
	MOVE_E     = 4
)

func printm(grid map[[2]int]int, pos, tl, br [2]int) {
	for y := br[1]; y <= tl[1]; y++ {
		for x := tl[0]; x <= br[0]; x++ {
			var o string
			xy := [2]int{x, y}
			if xy == pos {
				o = "D"
			} else if _, ok := grid[xy]; !ok {
				o = "?"
			} else if grid[xy] == EMPTY {
				o = "."
			} else if grid[xy] == WALL {
				o = "#"
			} else if grid[xy] == OXYG {
				o = "O"
			} else {
				panic("invalid value")
			}
			fmt.Printf("%v", o)
		}
		fmt.Println()
	}
}

func find_path(room map[[2]int]int, src [2]int, dst [2]int) (bool, [][2]int) {
	visited := make(map[[2]int]bool)
	movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
	searcho := make([][][2]int, 0)
	searcho = append(searcho, [][2]int{src})
	for len(searcho) > 0 {
		path := searcho[0]
		pos := path[len(path)-1]

		visited[pos] = true
		if pos == dst {
			return true, path
		}
		searcho = searcho[1:]
		for _, m := range movec {
			npos := [2]int{pos[0] + m[0], pos[1] + m[1]}
			if _, ok := visited[npos]; !ok {
				if _, ok := room[npos]; (ok && room[npos] != WALL) || npos == dst {
					npath := make([][2]int, len(path))
					copy(npath, path)
					npath = append(npath, npos)
					searcho = append(searcho, npath)
				}
			}
		}

	}
	return false, make([][2]int, 0)
}

func updateroom(room map[[2]int]int, pos [2]int, val int, tl, br *[2]int) {
	room[pos] = val
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
}

func fill_o(room map[[2]int]int, tl, br [2]int) int {
	timer := 0
	for true {
		// get list of O-s
		oxloc := make([][2]int, 0)
		for k, v := range room {
			if v == OXYG {
				oxloc = append(oxloc, k)
			}
		}
		// expand each O
		full := true
		for _, ox := range oxloc {
			movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
			for i := 0; i < 4; i++ {
				npos := [2]int{ox[0] + movec[i][0], ox[1] + movec[i][1]}
				if room[npos] == EMPTY {
					room[npos] = OXYG
					full = false
				}
			}
		}
		// if nowhere to expand, then done
		if full {
			break
		}
		timer += 1
	}
	return timer
}

func run_game(prog []string, part int) {
	ich := make(chan int, 1)
	och := make(chan int, 0)

	room := make(map[[2]int]int)

	go intcode.RunProg(prog, ich, och)
	// go MockProg(prog, ich, och)
	// for moves N(1) S(2) W(3) E(4)
	movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
	searcho := make([][2]int, 0)
	pos := [2]int{0, 0}
	tl := [2]int{0, 0}
	br := [2]int{0, 0}
	updateroom(room, pos, EMPTY, &tl, &br)
	foundempty := true
	for true {
		if foundempty {
			for i := 0; i < 4; i++ {
				npos := [2]int{pos[0] + movec[i][0], pos[1] + movec[i][1]}
				if _, ok := room[npos]; !ok {
					searcho = append(searcho, npos)
				}
			}
		}

		if len(searcho) == 0 {
			break
		}
		chkpos := searcho[0]
		searcho = searcho[1:]

		ok, path := find_path(room, pos, chkpos)
		if !ok {
			panic("no path")
		}
		resp := 0
		for i, p := range path {
			if i == 0 {
				continue
			}
			stepx := p[0] - pos[0]
			stepy := p[1] - pos[1]
			if stepx == 0 && stepy == -1 {
				ich <- MOVE_N
			} else if stepx == 0 && stepy == 1 {
				ich <- MOVE_S
			} else if stepx == -1 && stepy == 0 {
				ich <- MOVE_W
			} else if stepx == 1 && stepy == 0 {
				ich <- MOVE_E
			} else {
				panic("invalid step")
			}
			resp = <-och
			if resp != WALL {
				pos[0] = pos[0] + stepx
				pos[1] = pos[1] + stepy
			}
			if i < len(path)-1 {
				if resp != EMPTY {
					panic("unexpected resp")
				}
			}
		}
		foundempty = resp == EMPTY
		updateroom(room, chkpos, resp, &tl, &br)

		if resp == OXYG && part == 1 {
			break
		}
	}
	// printm(room, pos, tl, br)
	if part == 1 {
		_, p := find_path(room, [2]int{0, 0}, pos)
		fmt.Printf("Part1: %v\n", len(p)-1)
	} else {
		fmt.Printf("Part2: %v\n", fill_o(room, tl, br))
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	run_game(prog, 1)
	run_game(prog, 2)
}
