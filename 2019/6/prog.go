package main

import (
	"fmt"
	"os"
	"strings"
)

func count(orbits map[string][]string, start string) int {
	ret := 1
	if val, ok := orbits[start]; ok {
		for _, chkp := range val {
			if chkp != "COM" {
				ret += count(orbits, chkp)
			}
		}
	}
	return ret
}

func find(orbits map[string][]string, orbits_bw map[string][]string, start string, end string) (bool, int) {
	visited := make(map[string]bool, 0)

	check := make([]struct {
		string
		int
	}, 0)
	check = append(check, struct {
		string
		int
	}{start, 0})

	for len(check) > 0 {
		pos := check[0].string
		dst := check[0].int
		if pos == end {
			return true, dst - 2
		}
		check = check[1:]
		visited[pos] = true
		if val, ok := orbits[pos]; ok {
			for _, chkp := range val {
				if _, ok := visited[chkp]; !ok {
					check = append(check, struct {
						string
						int
					}{chkp, dst + 1})
				}
			}
		}
		if val, ok := orbits_bw[pos]; ok {
			for _, chkp := range val {
				if _, ok := visited[chkp]; !ok {
					check = append(check, struct {
						string
						int
					}{chkp, dst + 1})
				}
			}
		}
	}
	return false, 0
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	lines := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")

	orbits := make(map[string][]string, 0)
	orbits_bw := make(map[string][]string, 0)
	for _, l := range lines {
		a := strings.Split(l, ")")
		if _, ok := orbits[a[1]]; !ok {
			orbits[a[1]] = make([]string, 0)
		}
		orbits[a[1]] = append(orbits[a[1]], a[0])
		if _, ok := orbits_bw[a[0]]; !ok {
			orbits_bw[a[0]] = make([]string, 0)
		}
		orbits_bw[a[0]] = append(orbits_bw[a[0]], a[1])
	}

	sum := 0
	for k, _ := range orbits {
		sum += count(orbits, k)
	}
	fmt.Printf("Part1: %v\n", sum)

	ok, len := find(orbits, orbits_bw, "YOU", "SAN")
	if !ok {
		panic("Not found")
	}
	fmt.Printf("Part2: %v\n", len)
}
