package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

func checkfit(grid map[[2]int]uint8, x, y int) (bool, int, int) {
	const WH = 100 - 1
	// TL
	if _, ok := grid[[2]int{x - WH, y - WH}]; !ok {
		return false, 0, 0
	}
	// TR
	if _, ok := grid[[2]int{x, y - WH}]; !ok {
		return false, 0, 0
	}
	// BL
	if _, ok := grid[[2]int{x - WH, y}]; !ok {
		return false, 0, 0
	}
	// BR
	if _, ok := grid[[2]int{x, y}]; !ok {
		return false, 0, 0
	}
	return true, x - WH, y - WH
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")

	grid := map[[2]int]uint8{}

	for y := 0; y < 50; y++ {
		for x := 0; x < 50; x++ {
			ich := make(chan int, 2)
			och := make(chan int, 2)

			go intcode.RunProg(prog, ich, och)
			ich <- x
			ich <- y
			r, _ := <-och
			if r == 1 {
				grid[[2]int{x, y}] = uint8(r)
			}
		}
	}

	// printm(grid)
	fmt.Printf("Part1: %v\n", len(grid))

	starty := 1980
	ym := 2085
	startx := 1500
	xm := 2500
	answ2 := 0
readl:
	for y := starty; y < ym; y++ {
		for x := startx; x < xm; x++ {
			ich := make(chan int, 2)
			och := make(chan int, 2)

			go intcode.RunProg(prog, ich, och)
			ich <- x
			ich <- y
			r, _ := <-och
			if r == 1 {
				grid[[2]int{x, y}] = uint8(r)
			}
			ok, fx, fy := checkfit(grid, x, y)
			if ok {
				// fmt.Printf("Found! %v %v %v %v\n", fx, fy, x, y)
				answ2 = fx*10000 + fy
				break readl
			}
		}
	}

	fmt.Printf("Part2: %v\n", answ2)
}
