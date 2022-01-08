package main

import (
	"container/heap"
	"fmt"
	"math"
	"os"
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

func key_to_keyflag(key uint8) int {
	return (1 << (key - MINKEY))
}

func keyflag_to_key(key int) uint8 {
	for k := MINKEY; k <= MAXKEY; k++ {
		mask := (1 << (k - MINKEY))
		if key&mask == mask {
			return uint8(k)
		}
	}
	return 0
}

func keyflags_to_str(key int) string {
	ret := ""
	for i := 0; i < 32; i++ {
		k := keyflag_to_key(key & (1 << i))
		if k != 0 {
			ret += string(k)
		}
	}
	return ret
}

type SearchD struct {
	pos     [2]int
	steps   int
	reqkeys int
	gotkeys int
}

func find_path(grid map[[2]int]uint8, src [2]int, dst uint8) (bool, int, [2]int, int, int) {
	visited := make(map[[2]int]bool)
	movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
	searcho := make([]SearchD, 0)
	searcho = append(searcho, SearchD{src, -1, 0, 0})
	for len(searcho) > 0 {
		sd := searcho[0]
		sd.steps += 1
		visited[sd.pos] = true
		if grid[sd.pos] >= MINKEY && grid[sd.pos] <= MAXKEY {
			sd.gotkeys |= key_to_keyflag(grid[sd.pos])
		}
		if grid[sd.pos] >= MINDOOR && grid[sd.pos] <= MAXDOOR {
			doorkey := grid[sd.pos] + uint8(MINKEY-MINDOOR)
			if (sd.gotkeys & key_to_keyflag(doorkey)) == 0 {
				sd.reqkeys |= key_to_keyflag(doorkey)
			}
		}
		if v, ok := grid[sd.pos]; ok && v == dst {
			return true, sd.steps, sd.pos, sd.reqkeys, sd.gotkeys
		}
		searcho = searcho[1:]
		for _, m := range movec {
			npos := [2]int{sd.pos[0] + m[0], sd.pos[1] + m[1]}
			if _, ok := visited[npos]; !ok {
				if _, ok := grid[npos]; ok && grid[npos] != WALL {
					searcho = append(searcho, SearchD{npos, sd.steps, sd.reqkeys, sd.gotkeys})
				}
			}
		}
	}
	return false, -1, [2]int{0, 0}, 0, 0
}

type PathCacheKey struct {
	from [2]int
	to   uint8
}
type PathCacheVal struct {
	ok      bool
	npos    [2]int
	reqkeys int
	gotkeys int
	steps   int
}

func find_path_cached(pathcache map[PathCacheKey]PathCacheVal, grid map[[2]int]uint8, src [2]int, dst uint8, keys int) (bool, int, [2]int, int) {
	key := PathCacheKey{src, dst}
	if v, ok := pathcache[key]; ok {
		if v.ok && (v.reqkeys&keys) == v.reqkeys {
			return true, v.steps, v.npos, (keys | v.gotkeys)
		} else {
			return false, 0, [2]int{0, 0}, 0
		}
	} else {
		ok, nsteps, npos, reqkeys, gotkeys := find_path(grid, src, dst)
		pathcache[key] = PathCacheVal{ok: ok, npos: npos, reqkeys: reqkeys, gotkeys: gotkeys, steps: nsteps}
		if ok && (reqkeys&keys) == reqkeys {
			return ok, nsteps, npos, (keys | gotkeys)
		} else {
			return false, 0, [2]int{0, 0}, 0
		}
	}
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
	keys     int
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

func replace_char(s string, idx int, c rune) string {
	r := []rune(s)
	r[idx] = c
	return string(r)
}

func collect_keys(grid map[[2]int]uint8, pos [][2]int, findkeys string) int {
	beststates := map[string]int{}
	pathcache := map[PathCacheKey]PathCacheVal{}
	pq := make(priority_queue, 0)
	heap.Init(&pq)
	heap.Push(&pq, &pq_item{
		pos:      pos,
		findkeys: findkeys,
		keys:     0,
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
				ok, nsteps, npos, nkeys := find_path_cached(pathcache, grid, item.pos[b], uint8(k), item.keys)
				if ok {
					botloc := replace_char(item.botloc, b, k)
					keystr := keyflags_to_str(nkeys)
					searchstate := botloc + keystr // state is robot locations + all the keys we have
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
						if key_to_keyflag(uint8(nk))&nkeys == 0 {
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
	// f, err := os.Create("prog.prof")
	// if err != nil {
	// 	log.Fatal(err)
	// }
	// pprof.StartCPUProfile(f)
	// defer pprof.StopCPUProfile()

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
