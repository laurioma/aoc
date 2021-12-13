package main

import (
    "fmt"
    "os"
    "strings"
    "strconv"
)

func printp(coords map[[2]int]bool) {
    maxx := 0
    maxy := 0
    for c := range coords {
        if c[0] > maxx {
            maxx = c[0]
        }
        if c[1] > maxy {
            maxy = c[1]
        }
    }
    for y := 0; y <= maxy; y++ {
        for x := 0; x <= maxx; x++ {
            if _, ok := coords[[...]int{x, y}]; ok {
                fmt.Printf("#")
            } else {
                fmt.Printf(".")
            }
        }
        fmt.Println()
    }
}

func foldy(coords map[[2]int]bool, y int) {
    remove := make([][2]int, 0)
    add := make([][2]int, 0)
    for c := range coords {
        if c[1] > y {
            remove = append(remove, c)
            newy := y - (c[1] - y)
            add = append(add, [...]int{c[0], newy})
        }
    }
    for _, r := range remove {
        delete(coords, r)
    }
    for _, a := range add {
        coords[a] = true
    }
}

func foldx(coords map[[2]int]bool, x int) {
    remove := make([][2]int, 0)
    add := make([][2]int, 0)
    for c := range coords {
        if c[0] > x {
            remove = append(remove, c)
            newx := x - (c[0] - x)
            add = append(add, [...]int{newx, c[1]})
        }
    }
    for _, r := range remove {
        delete(coords, r)
    }
    for _, a := range add {
        coords[a] = true
    }
}

func main() {
    part := 1
    if len(os.Args) > 2 && os.Args[2] == "2" {
        part = 2
    }

    dat, _ := os.ReadFile(os.Args[1])
    dats := string(dat)
    strarr := strings.Split(strings.TrimSpace(strings.ReplaceAll(dats, "\r", "")), "\n")
    coords := make(map[[2]int]bool, 0)
    instr := make([][2]int, 0)
    getinstr := false
    for _, line := range strarr {
        if strings.TrimSpace(line) == "" {
            getinstr = true
            continue
        }

        if !getinstr {
            split := strings.Split(line, ",")
            v1,_ := strconv.Atoi(split[0])
            v2,_ := strconv.Atoi(split[1])
            coords[[...]int{v1, v2}] = true
        } else {
            split := strings.Split(line, "=")
            v1 := 1
            if split[0] == "fold along y" {
                v1 = 2
            }
            v2,_ := strconv.Atoi(split[1])
            instr = append(instr, [...]int{v1, v2})
        }
    }
    if part == 1 {
        if instr[0][0] == 1 {
            foldx(coords, instr[0][1])
        } else {
            foldy(coords, instr[0][1])
        }
        fmt.Printf("Part1: %v", len(coords))
    } else {
        for _, i := range instr {
            if i[0] == 1 {
                foldx(coords, i[1])
            } else {
                foldy(coords, i[1])
            }
        }
        fmt.Printf("Part2:\n")
        printp(coords)
    }
    return
}