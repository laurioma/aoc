package main

import (
    "fmt"
    "os"
    "strings"
//    "strconv"
//    "math"
)

func chk(e error) {
    if e != nil {
        panic(e)
    }
}

func is_upper(s string) bool {
    return strings.ToUpper(s) == s
}

func cnt_in_slice(a string, list []string) int {
    cnt := 0
    for _, b := range list {
        if b == a {
            cnt++
        }
    }
    return cnt
}

func find_all_paths(graph map[string][]string, paths map[string]bool, start, end string, path []string, allowtwice string) {
    npath := make([]string, len(path))
    copy(npath, path)
    npath = append(npath, start)

    if start == end {
        joinp := strings.Join(npath,"")
        paths[joinp] = true
        return
    }
    // start not in graph
    if _, ok := graph[start]; !ok {
        return
    }
    for _, node := range graph[start] {
        allowcnt := 0
        if allowtwice != "" && node == allowtwice {
            allowcnt = 1
        }
        if cnt_in_slice(node, npath) <= allowcnt || is_upper(node) {
            find_all_paths(graph, paths, node, end, npath, allowtwice)
        }
    }
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
    graph := make(map[string][]string)
    for _, line := range strarr {
        split := strings.Split(line, "-")
        graph[split[0]] = append(graph[split[0]], split[1])
        graph[split[1]] = append(graph[split[1]], split[0])
    }
    // go has no set..
    paths := make(map[string]bool)
    if part == 1 {
        path := make([]string, 0)
        find_all_paths(graph, paths, "start", "end", path, "")
    } else {
        small_caves := make([]string, 0)
        for k, _ := range graph { 
            if k != "start" && k != "end" && !is_upper(k) {
                small_caves = append(small_caves, k)
            }
        }
        for _, c := range small_caves {
            path := make([]string, 0)
            find_all_paths(graph, paths, "start", "end", path, c)
        }
    }
    fmt.Printf("Part%v: %v", part, len(paths))
    return
}