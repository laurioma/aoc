package main

import (
    "fmt"
    "os"
	"strings"
	"sort"
)

var closing = map[string]string {"(": ")", "[": "]", "{": "}", "<": ">" }
var closingsc = map[string]int {")": 3, "]": 57, "}": 1197, ">": 25137 }
var closingsc2 = map[string]int {")": 1, "]": 2, "}": 3, ">": 4 }

func chk(e error) {
    if e != nil {
        panic(e)
    }
}

func containsValue(m map[string]string, v string) bool {
	for _, x := range m {
		if x == v {
			return true
		}
	}
	return false
}

func parse(instr string) (bool, string, [] string) {
	var opening [] string
	for i := 0; i < len(instr); i++ {
		var s = string(instr[i])
		if _, ok := closing[s]; ok {
			opening = append(opening, s)
		} else if containsValue(closing, s) {
			if s == closing[opening[len(opening)-1]] {
				if len(opening) > 0 {
					opening = opening[:len(opening)-1]
				}
			} else {
				return false, s, opening
			}
		} else {
			panic("invalid input" + s)
		}
	}
	return true, "", opening
}

func main() {
	dat, err := os.ReadFile(os.Args[1])
    chk(err)
	dats := string(dat)
	arr := strings.Split(strings.ReplaceAll(dats, "\r", ""), "\n")

	answ := 0
	var incompl [] string
	for i := 0; i < len(arr); i++ {
		ok, val, _ := parse(arr[i])
		if !ok {
			answ += closingsc[val]
		} else {
			incompl = append(incompl, arr[i])
		}
	}
	fmt.Println("Part1", answ)
	var scores [] int
	for i := 0; i < len(incompl); i++ {
		_, _, remaining := parse(incompl[i])
		score := 0
		for i := len(remaining)-1; i >= 0; i-- {
			score *= 5
			score += closingsc2[closing[remaining[i]]]
		}
		scores = append(scores, score)
	}
	sort.Ints(scores)
	fmt.Println("Part2:", scores[len(scores)/2])
}