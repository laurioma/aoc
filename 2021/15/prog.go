package main

import (
    "fmt"
    "os"
    "strings"
    "strconv"
    "container/heap"
)

type pq_item struct {
	coords  [2]int
	cost int
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

type priority_queue []*pq_item

func (pq priority_queue) Len() int { return len(pq) }

func (pq priority_queue) Less(i, j int) bool {
	return pq[i].cost < pq[j].cost
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

func (pq *priority_queue) update(item *pq_item, coords [2]int, cost int) {
	item.coords = coords
	item.cost = cost
	heap.Fix(pq, item.index)
}

func printm(grid [][]uint8) {
    for y := range grid {
        for x := range grid[y] {
            fmt.Printf("%v", grid[y][x])
        }
        fmt.Println()
    }
}

func dijkstra(grid [][]uint8, start [2]int, end [2]int) int {
    visited := make(map[[2]int]bool, 0)

    pq := make(priority_queue, 0)
    heap.Init(&pq)

    heap.Push(&pq, &pq_item {
		coords: [2]int{0,0},
		cost: 0,
	})

    for pq.Len() > 0 {
        item := heap.Pop(&pq).(*pq_item)
//		fmt.Printf("pop %v\n", item)

        // if not visited
        if _, ok := visited[item.coords]; !ok {
            visited[item.coords] = true
            if item.coords == end {
                return item.cost
            }
            xydirs := [][]int{{-1, 0}, {0, -1}, {0, 1}, {1, 0}}
            for _, xy := range xydirs {
                x := item.coords[0] + xy[0]
                y := item.coords[1] + xy[1]
                if 0 <= x && x < len(grid[0]) && 0 <= y && y < len(grid) {
                    newcoords := [2]int{x, y}
                    if _, ok := visited[newcoords]; !ok {
                        newcost := item.cost + int(grid[y][x])
//                        fmt.Printf("push %v %v\n", newcoords, newcost)
                        heap.Push(&pq, &pq_item {
                            coords: newcoords,
                            cost: newcost,
                        })
                    }
                }
            }
        }
	}
    return 0
}

func main() {
    part := 1
    if len(os.Args) > 2 && os.Args[2] == "2" {
        part = 2
    }
    dat, _ := os.ReadFile(os.Args[1])
    strarr := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")
    grid := make([][]uint8, len(strarr))
    for y, line := range strarr {
        grid[y] = make([]uint8, len(line))
        for x, c := range line {
            intv, _ := strconv.Atoi(string(c))
            grid[y][x] = uint8(intv)
        }
    }
    //printm(grid)

    res := 0
    if part == 1 {
        res = dijkstra(grid, [2]int{0,0}, [2]int{len(grid) - 1, len(grid[0]) - 1})
    } else {
        maxrep := 5
        grid1 := make([][]uint8, len(grid) * maxrep)

        for y := 0; y < maxrep; y++ {
            for x := 0; x < maxrep; x++ {
                for yy := 0; yy < len(grid); yy++ {
                    dsty := y*len(grid) + yy
                    if len(grid1[dsty]) == 0 {
                        grid1[dsty] = make([]uint8, len(grid[0]) * maxrep)
                    }
                    for xx := 0; xx < len(grid[0]); xx++ {
                        dstx := x*len(grid[0]) + xx
                        dst := grid[yy][xx] + uint8(x + y)
                        if dst > 9 {
                            grid1[dsty][dstx] = dst % 9
                        } else {
                            grid1[dsty][dstx] = dst
                        }
                    }    
                }
            }    
        }
        //printm(grid1)
        res = dijkstra(grid1, [2]int{0,0}, [2]int{len(grid1) - 1, len(grid1[0]) - 1})
    }

    fmt.Printf("Part%v: %v", part, res)

    return
}