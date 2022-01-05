package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"

	"../intcode"
)

const (
	ORI_N int = 1
	ORI_W     = 2
	ORI_S     = 3
	ORI_E     = 4
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
			if _, ok := grid[[2]int{x, y}]; !ok {
				fmt.Printf(".")
			} else {
				fmt.Printf("%c", grid[[2]int{x, y}])
			}
		}
		fmt.Println()
	}
}

// writes O into each intersection and returns list of intersections
func get_and_mark_intersect(grid map[[2]int]uint8) [][2]int {
	res := make([][2]int, 0)
	for k, _ := range grid {
		movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}
		count := 0
		for _, m := range movec {
			cpos := [2]int{k[0] + m[0], k[1] + m[1]}
			if _, ok := grid[cpos]; ok {
				count += 1
			}
		}
		if count >= 3 {
			grid[k] = 'O'
			res = append(res, k)
		}
	}

	return res
}

func get_bot(grid map[[2]int]uint8) [2]int {
	for k, v := range grid {
		if v == '<' || v == '>' || v == '^' || v == 'v' {
			return k
		}
	}
	return [2]int{-1, -1}
}

func append_path(path []string, orient int, prev_pos [2]int, pos [2]int) ([]string, int) {
	// path turned west
	if pos[1] == prev_pos[1] && pos[0] == prev_pos[0]-1 && orient != ORI_W {
		if orient == ORI_N {
			path = append(path, "L")
		} else if orient == ORI_S {
			path = append(path, "R")
		} else {
			panic("inv orient")
		}
		orient = ORI_W
		path = append(path, "0")
		// path turned east
	} else if pos[1] == prev_pos[1] && pos[0] == prev_pos[0]+1 && orient != ORI_E {
		if orient == ORI_N {
			path = append(path, "R")
		} else if orient == ORI_S {
			path = append(path, "L")
		} else {
			panic("inv orient2")
		}
		orient = ORI_E
		path = append(path, "0")
		// path turned north
	} else if pos[0] == prev_pos[0] && pos[1] == prev_pos[1]-1 && orient != ORI_N {
		if orient == ORI_E {
			path = append(path, "L")
		} else if orient == ORI_W {
			path = append(path, "R")
		} else {
			panic("inv orient3")
		}
		orient = ORI_N
		path = append(path, "0")
		// path turned south
	} else if pos[0] == prev_pos[0] && pos[1] == prev_pos[1]+1 && orient != ORI_S {
		if orient == ORI_E {
			path = append(path, "R")
		} else if orient == ORI_W {
			path = append(path, "L")
		} else {
			panic("inv orient4")
		}
		orient = ORI_S
		path = append(path, "0")
	}
	if len(path) > 0 {
		prevn, _ := strconv.Atoi(path[len(path)-1])
		path[len(path)-1] = strconv.Itoa(prevn + 1)
	}
	return path, orient
}

// does all possible turns on each intersection
func find_all_paths(grid map[[2]int]uint8, prev_pos [2]int, pos [2]int, path []string, orient int, paths *[][]string) {
	movec := [][2]int{{0, -1}, {0, 1}, {-1, 0}, {1, 0}}

	moved := true
	for moved {
		path, orient = append_path(path, orient, prev_pos, pos)

		if grid[pos] == '#' {
			grid[pos] = 'H'
		}
		moved = false
		if grid[pos] == 'O' {
			for _, m := range movec {
				x := pos[0] + m[0]
				y := pos[1] + m[1]
				npos := [2]int{x, y}

				if _, ok := grid[npos]; ok && grid[npos] == '#' {
					newgrid := map[[2]int]uint8{}
					for k, v := range grid {
						newgrid[k] = v
					}

					npath := make([]string, 0)
					npath = append(npath, path...)
					find_all_paths(newgrid, pos, npos, npath, orient, paths)
				}
			}
		} else {
			for _, m := range movec {
				x := pos[0] + m[0]
				y := pos[1] + m[1]
				npos := [2]int{x, y}
				if _, ok := grid[npos]; ok && prev_pos != npos {
					prev_pos = pos
					pos = npos
					moved = true
					break
				}
			}
		}
	}

	notvisited := 0
	for _, v := range grid {
		if v == '#' {
			notvisited += 1
		}
	}
	if notvisited == 0 {
		*paths = append(*paths, path)
	}
}

// try all possible subprograms for A. replace them with A,0
// in what remains try all possible subprograms for B. replace them with B,0
// in what remains try all possible subprograms for C. replace them with C,0. If no R and L remaining in string then done
func try_subprogs(path []string, subp int) (bool, string, []string) {
	ret := make([]string, 0)
	subs := []string{"A", "B", "C"}
	s := strings.Join(path, ",")
	if subp >= len(subs) {
		return false, "", ret
	}
	subprog := subs[subp]
	min_len := 2
	for slen := 10; slen >= min_len; slen -= 2 {
		for start := 0; start+slen < len(path); start += 2 {
			s1 := strings.Join(path[start:start+slen], ",")
			found := false
			// should not have A,B,C in subpath
			for ch := 0; ch < len(subs); ch++ {
				if strings.Count(s1, subs[ch]) > 0 {
					found = true
					break
				}
			}
			if found {
				continue
			}
			r := subprog + ",0"
			repl := strings.ReplaceAll(s, s1, r)
			if strings.Count(repl, "L") == 0 && strings.Count(repl, "R") == 0 {
				ret = append(ret, s1)
				return true, repl, ret
			} else {
				ok, templ, subs := try_subprogs(strings.Split(repl, ","), subp+1)
				if ok {
					ret = append(ret, s1)
					ret = append(ret, subs...)
					return true, templ, ret
				}
			}
		}
	}

	return false, "", ret
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	ich := make(chan int, 1)
	och := make(chan int, 0)

	go intcode.RunProg(prog, ich, och)

	mazestr := ""
	ok := true
	ch := 0
	for ok {
		ch, ok = <-och
		mazestr += string(ch)
	}

	lines := strings.Split(strings.ReplaceAll(mazestr, "\r", ""), "\n")
	grid := map[[2]int]uint8{}
	bounds := [2]int{len(lines[0]), len(lines) - 2}
	for y := 0; y < bounds[1]; y++ {
		for x := 0; x < bounds[0]; x++ {
			if lines[y][x] != '.' {
				grid[[2]int{x, y}] = lines[y][x]
			}
		}
	}

	intersect := get_and_mark_intersect(grid)
	// printm(grid)
	res1 := 0
	for _, is := range intersect {
		res1 += is[0] * is[1]
	}
	fmt.Printf("Part1: %v\n", res1)

	pos := get_bot(grid)
	pp := make([]string, 0)
	allpath := make([][]string, 0)
	find_all_paths(grid, pos, pos, pp, ORI_N, &allpath)
	// sort shorter paths first
	sort.Slice(allpath, func(p, q int) bool {
		return len(allpath[p]) < len(allpath[q])
	})
	template := ""
	subprogs := []string{}
	for i := 0; i < len(allpath); i++ {
		ok, template, subprogs = try_subprogs(allpath[i], 0)
		if ok {
			break
		}
	}
	template = strings.ReplaceAll(template, ",0", "")

	prog[0] = "2"
	ich = make(chan int, 1)
	och = make(chan int, 0)
	go intcode.RunProg(prog, ich, och)

	for ch = <-och; ch != ':'; ch = <-och {
	}
	<-och
	for _, t := range template {
		ich <- int(t)
	}
	ich <- '\n'

	for _, subp := range subprogs {
		for ch = <-och; ch != ':'; ch = <-och {
		}
		<-och
		for _, sch := range subp {
			ich <- int(sch)
		}
		ich <- '\n'

	}
	for ch = <-och; ch != '?'; ch = <-och {
	}
	<-och
	ich <- 'n'
	ich <- '\n'
	res2 := 0
	for ch = <-och; ch != 0; ch = <-och {
		res2 = ch
	}
	fmt.Printf("Part2: %d\n", res2)
}
