package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	strarr := strings.Split(string(dat), ",")
	ich := make(chan int, 1)
	och := make(chan int, 0)

	ich <- 1
	go intcode.RunProg(strarr, ich, och)
	for o := range och {
		fmt.Printf("Part1: %v\n", o)
	}
	och = make(chan int, 0)
	ich <- 2
	go intcode.RunProg(strarr, ich, och)
	for o := range och {
		fmt.Printf("Part2: %v\n", o)
	}

}
