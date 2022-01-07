package main

import (
	"container/heap"
	"fmt"
	"math"
	"os"
	"sort"
	"strings"
)

const (
	WALL    uint8 = '#'
	ENRANCE       = '@'
	EMPTY         = '.'
	MINDOOR       = 'A'
	MAXDOOR       = 'Z'
	MINKEY        = 'a'
	MAXKEY        = 'z'
)

func printm(grid map[[2]int]uint8) {
	xm := 0
	ym := 0
	for k := range grid {
		if k[0] > xm {
			xm = k[0]
		}
		if k[1] > ym {
			ym = k[1]
		}
	}
	for y := 0; y <= ym; y++ {
		for x := 0; x <= xm; x++ {
			fmt.Printf("%c", grid[[2]int{x, y}])
		}
		fmt.Println()
	}
}

func can_pass(obj uint8, keys string) bool {
	if obj == WALL {
		return false
	} else if obj == EMPTY || obj == ENRANCE {
		return true
	} else if obj == WALL {
		return false
	} else if obj >= MINKEY && obj <= MAXKEY {
		return true
	} else if obj >= MINDOOR && obj <= MAXDOOR {
		diff := MINKEY - MINDOOR
		for _, k := range keys {
			if uint8(k)-uint8(diff) == obj {
				return true
			}
		}
		return false
	} else {
		panic(fmt.Sprintf("uncnown obj %v", obj))
	}
}

type SearchD struct {
	pos   [2]int
	steps int
	keys  string
}

func find_path(grid map[[2]int]uint8, src [2]int, dst uint8, keys string) (bool, int, [2]int, string) {
	visited := make(map[[2]int]bool)
	movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
	searcho := make([]SearchD, 0)
	searcho = append(searcho, SearchD{src, -1, keys})
	for len(searcho) > 0 {
		sd := searcho[0]
		sd.steps += 1

		visited[sd.pos] = true
		if grid[sd.pos] >= MINKEY && grid[sd.pos] <= MAXKEY {
			if strings.Index(sd.keys, string(grid[sd.pos])) < 0 {
				sd.keys += string(grid[sd.pos])
			}
		}
		if v, ok := grid[sd.pos]; ok && v == dst {
			return true, sd.steps, sd.pos, sd.keys
		}
		searcho = searcho[1:]
		for _, m := range movec {
			npos := [2]int{sd.pos[0] + m[0], sd.pos[1] + m[1]}
			if _, ok := visited[npos]; !ok {
				if _, ok := grid[npos]; ok && can_pass(grid[npos], sd.keys) {
					searcho = append(searcho, SearchD{npos, sd.steps, sd.keys})
				}
			}
		}
	}
	return false, 0, [2]int{0, 0}, ""
}

func get_entrances(grid map[[2]int]uint8) [][2]int {
	ret := make([][2]int, 0)
	for k, v := range grid {
		if v == ENRANCE {
			ret = append(ret, k)
		}
	}
	return ret
}

func get_keys(grid map[[2]int]uint8) string {
	ret := ""
	for _, v := range grid {
		if v >= MINKEY && v <= MAXKEY {
			ret += string(v)
		}
	}
	return ret
}

type pq_item struct {
	pos      [][2]int
	findkeys string
	keys     string
	steps    int
	botloc   string
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

type priority_queue []*pq_item

func (pq priority_queue) Len() int { return len(pq) }

func (pq priority_queue) Less(i, j int) bool {
	return pq[i].steps < pq[j].steps
}

func (pq priority_queue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *priority_queue) Push(x interface{}) {
	n := len(*pq)
	item := x.(*pq_item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *priority_queue) Pop() interface{} {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // avoid memory leak
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

func sort_string(s string) string {
	r := []rune(s)
	sort.Slice(r, func(i, j int) bool {
		return r[i] < r[j]
	})
	return string(r)
}

func replace_char(s string, idx int, c rune) string {
	r := []rune(s)
	r[idx] = c
	return string(r)
}

func collect_keys(grid map[[2]int]uint8, pos [][2]int, findkeys string) int {
	beststates := map[string]int{}
	pq := make(priority_queue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &pq_item{
		pos:      pos,
		findkeys: findkeys,
		keys:     "",
		// botloc is actually the letter of the key where bot is standing currently
		// bot will be allways standing on the last key what it picked up
		botloc: "@@@@",
		steps:  0,
	})
	best := math.MaxInt
	for pq.Len() > 0 {
		item := heap.Pop(&pq).(*pq_item)

		for _, k := range item.findkeys {
			for b := 0; b < len(pos); b++ {
				ok, nsteps, npos, nkeys := find_path(grid, item.pos[b], uint8(k), item.keys)
				if ok {
					botloc := replace_char(item.botloc, b, k)
					searchstate := botloc + sort_string(nkeys) // state is robot locations + all the keys we have
					currsteps := item.steps + nsteps
					if _, ok := beststates[searchstate]; !ok {
						beststates[searchstate] = currsteps
					} else {
						// if we have been in this state with better score then continue
						if beststates[searchstate] <= currsteps {
							continue
						} else {
							beststates[searchstate] = currsteps
						}
					}

					nfindkeys := ""
					for _, nk := range item.findkeys {
						if strings.Index(nkeys, string(nk)) < 0 {
							nfindkeys += string(nk)
						}
					}
					// found all keys
					if nfindkeys == "" {
						if best > currsteps {
							best = currsteps
						}
					}
					nextpos := make([][2]int, 0)
					nextpos = append(nextpos, item.pos...)
					nextpos[b] = npos
					heap.Push(&pq, &pq_item{
						pos:      nextpos,
						findkeys: nfindkeys,
						keys:     nkeys,
						botloc:   botloc,
						steps:    currsteps,
					})
					break
				}
			}
		}
	}
	return best
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	lines := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")
	grid := map[[2]int]uint8{}
	bounds := [2]int{len(lines[0]), len(lines)}
	for y := 0; y < bounds[1]; y++ {
		for x := 0; x < bounds[0]; x++ {
			grid[[2]int{x, y}] = lines[y][x]
		}
	}
	// printm(grid)
	entr := get_entrances(grid)
	allkeys := get_keys(grid)

	res1 := collect_keys(grid, entr, allkeys)
	fmt.Printf("Part1: %v\n", res1)

	pos := entr[0]
	grid[pos] = '#'
	grid[[2]int{pos[0] + 1, pos[1]}] = '#'
	grid[[2]int{pos[0] - 1, pos[1]}] = '#'
	grid[[2]int{pos[0], pos[1] + 1}] = '#'
	grid[[2]int{pos[0], pos[1] - 1}] = '#'
	grid[[2]int{pos[0] - 1, pos[1] - 1}] = '@'
	grid[[2]int{pos[0] + 1, pos[1] - 1}] = '@'
	grid[[2]int{pos[0] - 1, pos[1] + 1}] = '@'
	grid[[2]int{pos[0] + 1, pos[1] + 1}] = '@'
	// printm(grid)

	entr = get_entrances(grid)
	res2 := collect_keys(grid, entr, allkeys)
	fmt.Printf("Part2: %v\n", res2)
}
