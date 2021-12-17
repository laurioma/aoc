package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
)

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	re := regexp.MustCompile(`[0-9-]+`)
	match := re.FindAll(dat, -1)
	x1, _ := strconv.Atoi(string(match[0]))
	x2, _ := strconv.Atoi(string(match[1]))
	y1, _ := strconv.Atoi(string(match[2]))
	y2, _ := strconv.Atoi(string(match[3]))

	besty := math.MinInt
	targets := make([][2]int, 0)
	for startvy := y1; startvy < -y1; startvy++ {
		for startvx := 0; startvx <= x2; startvx++ {
			pos := [2]int{0, 0}
			posl := make([][2]int, 0)
			vel := [2]int{startvx, startvy}
			maxy := math.MinInt
			//			fmt.Printf("running sim %v %v %v\n", vel, ax, ay)
			for pos[0] <= x2 && pos[1] >= y1 {
				pos = [2]int{pos[0] + vel[0], pos[1] + vel[1]}
				posl = append(posl, pos)
				if pos[1] > maxy {
					maxy = pos[1]
				}

				if vel[0] > 0 {
					vel[0] -= 1
				}
				vel[1] -= 1

				if x1 <= pos[0] && pos[0] <= x2 && y1 <= pos[1] && pos[1] <= y2 {
					if besty < maxy {
						besty = maxy
					}
					// fmt.Printf("in target %v %v %v %v\n", maxy, besty, startvx, startvy)
					targets = append(targets, [2]int{startvx, startvy})
					break
				}
			}
		}
	}
	fmt.Printf("Part1: %v\n", besty)
	fmt.Printf("Part2: %v\n", len(targets))

	return
}
