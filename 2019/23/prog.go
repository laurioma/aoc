package main

import (
	"fmt"
	"os"
	"reflect"
	"strings"
	"sync"

	"../intcode"
)

const NCOMP = 50

func run(prog []string, part2 bool) int {
	ichs := make([]chan int, NCOMP)
	ochs := make([]chan int, NCOMP)
	var rdwg sync.WaitGroup
	var wg intcode.RunProgWaitGroups
	wg.Rd = &rdwg
	for i := 0; i < NCOMP; i++ {
		ichs[i] = make(chan int, 0)
		ochs[i] = make(chan int, 2*NCOMP)
		rdwg.Add(3)
		go intcode.RunProgWG(prog, ichs[i], ochs[i], &wg)
		ichs[i] <- i
		ichs[i] <- -1 //apparently first time we need to input -1 to get some output
	}
	natx := 0
	naty := 0
	naty_prev := -1
	cases := make([]reflect.SelectCase, len(ochs)+1)
	for i, ch := range ochs {
		cases[i] = reflect.SelectCase{Dir: reflect.SelectRecv, Chan: reflect.ValueOf(ch)}
	}
	cases[len(cases)-1] = reflect.SelectCase{Dir: reflect.SelectDefault}
	for true {
		chosen, a, _ := reflect.Select(cases)
		if chosen < NCOMP {
			x, _ := <-ochs[chosen]
			y, _ := <-ochs[chosen]

			addr := a.Interface().(int)
			if addr == 255 {
				if !part2 {
					return y
				} else {
					natx = x
					naty = y
				}
			} else {
				rdwg.Add(2)
				ichs[addr] <- x
				ichs[addr] <- y
			}
		} else {
			// wait until all the goroutines have done processing and wait for input
			rdwg.Wait()
			lenout := 0
			for i := 0; i < NCOMP; i++ {
				lenout += len(ochs[i])
			}

			if lenout == 0 {
				rdwg.Add(2)
				ichs[0] <- natx
				ichs[0] <- naty
				if part2 && naty == naty_prev {
					return naty
				}
				naty_prev = naty
			}
		}

	}
	return 0
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")

	fmt.Printf("start router\n")
	answ1 := run(prog, false)
	fmt.Printf("Part1: %v\n", answ1)
	answ2 := run(prog, true)
	fmt.Printf("Part2: %v\n", answ2)
}
