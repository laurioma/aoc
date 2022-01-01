package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func get_fuel(n int) int {
	fuel := n/3 - 2
	if fuel < 0 {
		return 0
	}
	return fuel + get_fuel(fuel)
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])

	dats := string(dat)
	strarr := strings.Split((strings.ReplaceAll(dats, "\r", "")), "\n")
	fuelsum1 := 0
	fuelsum2 := 0
	for _, s := range strarr {
		n, _ := strconv.Atoi(string(s))
		fuelsum2 += get_fuel(n)
		fuelsum1 += n/3 - 2
	}

	fmt.Printf("Part1: %v\n", fuelsum1)
	fmt.Printf("Part2: %v\n", fuelsum2)

	return
}
