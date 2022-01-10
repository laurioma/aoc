package main

import (
	"fmt"
	"os"
	"strings"

	"../intcode"
)

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	ich := make(chan int, 1)
	och := make(chan int, 0)
	go intcode.RunProg(prog, ich, och)

	// read the "Input instructions:\n" prompt
	for ch := <-och; ch != '\n'; ch = <-och {
	}
	sprog := `NOT A T
NOT T T
AND B T
AND C T
NOT T T
AND D T
OR T J
WALK
`
	for _, c := range sprog {
		ich <- int(c)
	}

	res1 := 0
	for ch := <-och; ch != 0; ch = <-och {
		// fmt.Printf("%c", ch)
		res1 = ch
	}

	fmt.Printf("Part1: %v\n", res1)

	ich = make(chan int, 1)
	och = make(chan int, 0)
	go intcode.RunProg(prog, ich, och)

	// read the "Input instructions:\n" prompt
	for ch := <-och; ch != '\n'; ch = <-och {
	}
	sprog = `NOT A T
NOT T T
AND B T
AND C T
NOT T T
AND D T
NOT I J
NOT J J
OR F J
AND E J
OR H J
AND T J
RUN
`
	for _, c := range sprog {
		ich <- int(c)
	}

	res2 := 0
	for ch := <-och; ch != 0; ch = <-och {
		// fmt.Printf("%c", ch)
		res2 = ch
	}
	fmt.Printf("Part2: %v\n", res2)
}
