package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func move(pos, cnt int) int {
	return ((pos + cnt - 1) % 10) + 1
}

type CacheKey struct {
	p1p, p2p, p1s, p2s int
}

func round_cached(cache map[CacheKey][2]int, rolls []int, p1p, p2p, p1s, p2s int) [2]int {
	k := CacheKey{p1p: p1p, p2p: p2p, p1s: p1s, p2s: p2s}
	if _, ok := cache[k]; ok {
		return cache[k]
	}
	wins1 := 0
	wins2 := 0
	for r1 := range rolls {
		p1pnew := move(p1p, rolls[r1])
		p1snew := p1s + p1pnew
		if p1snew >= 21 {
			wins1 += 1
			continue
		} else {
			for r2 := range rolls {
				p2pnew := move(p2p, rolls[r2])
				p2snew := p2s + p2pnew
				if p2snew >= 21 {
					wins2 += 1
					continue
				}

				w := round_cached(cache, rolls, p1pnew, p2pnew, p1snew, p2snew)
				wins1 += w[0]
				wins2 += w[1]
			}
		}
	}
	cache[k] = [2]int{wins1, wins2}
	return [2]int{wins1, wins2}
}

func round_nocache(rolls map[int]int, p1p, p2p, p1s, p2s, cnt1, cnt2 int) [2]int {
	wins1 := 0
	wins2 := 0
	for r1 := range rolls {
		p1cnt := rolls[r1]
		p1pnew := move(p1p, r1)
		p1snew := p1s + p1pnew
		if p1snew >= 21 {
			wins1 += cnt1 * cnt2 * p1cnt
			continue
		} else {
			for r2 := range rolls {
				p2cnt := rolls[r2]
				p2pnew := move(p2p, r2)
				p2snew := p2s + p2pnew
				if p2snew >= 21 {
					wins2 += cnt1 * cnt2 * p1cnt * p2cnt
					continue
				}

				w := round_nocache(rolls, p1pnew, p2pnew, p1snew, p2snew, cnt1*p1cnt, cnt2*p2cnt)
				wins1 += w[0]
				wins2 += w[1]
			}
		}
	}
	return [2]int{wins1, wins2}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	re := regexp.MustCompile(`[0-9-]+`)
	match := re.FindAll(dat, -1)
	p1, _ := strconv.Atoi(string(match[1]))
	p2, _ := strconv.Atoi(string(match[3]))

	fmt.Printf("Part2: %v %v\n", p1, p2)
	method := "cached"
	if len(os.Args) > 2 {
		method = os.Args[2]
	}

	var wins [2]int
	if method == "cached" {
		rolls := make([]int, 0)
		for i := 1; i <= 3; i++ {
			for j := 1; j <= 3; j++ {
				for k := 1; k <= 3; k++ {
					rolls = append(rolls, i+j+k)
				}
			}
		}
		cache := map[CacheKey][2]int{}
		fmt.Printf("r: %v \n", rolls)
		wins = round_cached(cache, rolls, p1, p2, 0, 0)
	} else {
		rolls := map[int]int{}
		for i := 1; i <= 3; i++ {
			for j := 1; j <= 3; j++ {
				for k := 1; k <= 3; k++ {
					rolls[i+j+k] += 1
				}
			}
		}
		fmt.Printf("rolls %v\n", rolls)
		wins = round_nocache(rolls, p1, p2, 0, 0, 1, 1)
	}

	fmt.Printf("Part2: %v\n", wins)

	return
}
