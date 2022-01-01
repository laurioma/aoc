package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

//thank Go!
func Abs(x int) int {
	if x < 0 {
		return -x
	}
	return x
}

func Min(a []int) int {
	if len(a) == 0 {
		return 0
	}
	min := a[0]
	for i := 1; i < len(a); i++ {
		if min > a[i] {
			min = a[i]
		}
	}
	return min
}

func mhd(p0, p1 struct{ x, y int }) int {
	return Abs(p0.x-p1.x) + Abs(p0.y-p1.y)
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	lines := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")
	grid := make(map[struct{ x, y int }]int)
	crossing_dst := make([]int, 0)
	crossing_steps := make([]int, 0)
	for wireidx, l := range lines {
		pos := struct{ x, y int }{x: 0, y: 0}
		startpos := pos
		moves := strings.Split(l, ",")
		numsteps := 0
		for _, m := range moves {
			dir := m[0]
			cnt, _ := strconv.Atoi(m[1:])
			for i := 0; i < cnt; i++ {
				if wireidx == 1 {
					if val, ok := grid[pos]; ok {
						if val > 0 {
							crossing_dst = append(crossing_dst, mhd(startpos, pos))
							crossing_steps = append(crossing_steps, val+numsteps)
						}
					}
				}
				if wireidx == 0 {
					grid[pos] = numsteps
				} else {
					grid[pos] = -numsteps
				}
				numsteps += 1
				if dir == 'L' {
					pos.x -= 1
				} else if dir == 'R' {
					pos.x += 1
				} else if dir == 'U' {
					pos.y += 1
				} else if dir == 'D' {
					pos.y -= 1
				}
			}
		}
	}

	fmt.Printf("Part1: %v\n", Min(crossing_dst))
	fmt.Printf("Part2: %v\n", Min(crossing_steps))

	return
}
