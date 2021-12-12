package main

import (
    "fmt"
    "os"
    "strings"
    "strconv"
    "math"
)

func printm(grid [][]uint8) {
    for y := range grid {
        for x := range grid[y] {
            fmt.Printf("%v", grid[y][x])
        }
        fmt.Println()
    }
}

func chk(e error) {
    if e != nil {
        panic(e)
    }
}

func flash(grid [][]uint8, x, y int) int {
    xydirs := [][]int{{-1, -1}, {0, -1}, {1, -1}, {-1, 0}, {1, 0}, {-1, 1}, {0, 1}, {1, 1}}
    flashcnt := 1
    for _, xy := range xydirs {
        xx := x + xy[0]
        yy := y + xy[1]
        if xx >= 0 && xx < len(grid[0]) && yy >= 0 && yy < len(grid) {
            grid[yy][xx]++
            if grid[yy][xx] == 10 {
                flashcnt += flash(grid, xx, yy)
            }
            //fmt.Printf("arr %v %v %v\n", xx, yy, grid[yy][xx]);
        }
    }
    return flashcnt
}

func main() {
    part := 1
    if len(os.Args) > 2 && os.Args[2] == "2" {
        part = 2
    }

    dat, err := os.ReadFile(os.Args[1])
    chk(err)
    dats := string(dat)
    strarr := strings.Split(strings.TrimSpace(strings.ReplaceAll(dats, "\r", "")), "\n")
    grid := make([][]uint8, len(strarr))
    for y, line := range strarr {
        grid[y] = make([]uint8, len(line))
        for x, c := range line {
            intv, _ := strconv.Atoi(string(c))
            grid[y][x] = uint8(intv)
        }
    }

    max := 100
    if part == 2 {
        max = math.MaxInt
    } 
    answer := 0
    part2_goal := len(grid) * len(grid[0])
    for s := 0; s < max; s++ {
        flashcnt := 0
        for y := range grid {
            for x := range grid[y] {
                grid[y][x]++
                if grid[y][x] == 10 {
                    flashcnt += flash(grid, x, y)
                }
            }
        }
        for y := range grid {
            for x := range grid[y] {
                if grid[y][x] > 9 {
                    grid[y][x] = 0
                }
            }
        }
        if part == 2 {
            if flashcnt == part2_goal {
                answer = s+1
                break
            }
        } else {
            answer += flashcnt
        }
        //fmt.Printf("arr: %v %v %v\n", s+1, flashcnt, answer)
        //printm(grid)
    }
    fmt.Printf("Part%v: %v", part, answer)
    
    return
}