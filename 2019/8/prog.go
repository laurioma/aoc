package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
)

func printm(grid [][]uint8) {
	for y := range grid {
		for x := range grid[y] {
			fmt.Printf("%v", grid[y][x])
		}
		fmt.Println()
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	w := 25
	h := 6
	cnt0 := 0
	cnt1 := 0
	cnt2 := 0
	layeridx := 0
	answ1 := 0
	mincnt := math.MaxInt
	image := make([][]uint8, h)
	for y := range image {
		image[y] = make([]uint8, w)
		for x := range image[y] {
			image[y][x] = 2
		}
	}
	for i, d := range dat {
		if i%(w*h) == 0 {
			if i > 0 {
				if cnt0 < mincnt {
					mincnt = cnt0
					answ1 = cnt1 * cnt2
				}
				layeridx += 1
			}
			cnt0 = 0
			cnt1 = 0
			cnt2 = 0
		}
		x := (i - layeridx*w*h) % w
		y := (i - layeridx*w*h) / w

		pix, _ := strconv.Atoi(string(d))
		if pix == 0 || pix == 1 {
			if image[y][x] == 2 {
				image[y][x] = uint8(pix)
			}
		}

		if pix == 0 {
			cnt0 += 1
		}
		if pix == 1 {
			cnt1 += 1
		}
		if pix == 2 {
			cnt2 += 1
		}
	}
	fmt.Printf("Part1: %v\n", answ1)
	fmt.Printf("Part2:\n")
	printm(image)
}
