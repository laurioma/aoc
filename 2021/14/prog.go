package main

import (
    "fmt"
    "os"
    "strings"
    "math"
)

func minmax(ccnt map[byte]int) (int, int) {
    min := math.MaxInt
    max := 0
    for m := range ccnt {
        if ccnt[m] < min {
            min = ccnt[m]
        }
        if ccnt[m] > max {
            max = ccnt[m]
        }
    }
    return min, max
}

func part1(templ string, rules [][2]string) int {
    newt := templ
    for s := 0; s < 10; s++ {
        inserted := 0
        for i := 1; i < len(templ); i++ {
            for _,r := range rules {
                if r[0] == templ[i-1:i+1] {
                    idx := i + inserted
                    newt = newt[0:idx] + r[1] + newt[idx:]
                    inserted += 1
                }
            }
        }
        templ = newt
    }
    ccnt := make(map[byte]int, 0)
    for _,c := range templ {
        ccnt[byte(c)] += 1
    }
    min, max := minmax(ccnt)

    return (max - min)
}

func part2(templ string, rules [][2]string) int {
    pairs := make(map[string]int, 0)
    for i := 1; i < len(templ); i++ {
        k := templ[i-1:i+1]
        pairs[k] += 1
    }
    border1 := templ[0]
    border2 := templ[len(templ)-1]

    for s := 0; s < 40; s++ {
        deleted := make(map[string]struct {string; int}, 0)
        for _, r := range rules {
            if _, ok := pairs[r[0]]; ok {
                deleted[r[0]] = struct {string; int}{r[1], pairs[r[0]]}
                delete(pairs, r[0]);
            }
        }
        for d := range deleted {
            k1 := d[0:1] + deleted[d].string
            k2 := deleted[d].string + d[1:]
            pairs[k1] += deleted[d].int
            pairs[k2] += deleted[d].int
        }
    }
    ccnt := make(map[byte]int)
    for p := range pairs {
        ccnt[p[0]] += pairs[p]
        ccnt[p[1]] += pairs[p]
    }
    // every characrter except border ones are now counted twice
    ccnt[border1] += 1
    ccnt[border2] += 1
    for c := range ccnt {
        ccnt[c] /= 2
    }
    min, max := minmax(ccnt)

    return (max - min)
}


func main() {
    part := 1
    if len(os.Args) > 2 && os.Args[2] == "2" {
        part = 2
    }
    dat, _ := os.ReadFile(os.Args[1])
    strarr := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")
    templ := ""
    rules := make([][2]string, 0)
    getrules := false
    for _, line := range strarr {
        if strings.TrimSpace(line) == "" {
            getrules = true
            continue
        }
        if !getrules {
            templ = line
        } else {
            split := strings.Split(line, " -> ")
            rules = append(rules,  [...]string{split[0], split[1]})
        }
    }
    res := 0
    if part == 1 {
        res = part1(templ, rules)
    } else {
        res = part2(templ, rules)
    }

    fmt.Printf("Part%v: %v", part, res)

    return
}