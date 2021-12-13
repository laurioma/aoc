package main

import (
    "fmt"
    "os"
    "strings"
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

func find_all_paths(graph map[string][]string, start, end string, path []string, part2 bool, twice string) int {
    if part2 && twice == "" && !is_upper(start) && cnt_in_slice(start, path) == 1 {
        twice = start
    }

    npath := make([]string, len(path))
    copy(npath, path)
    npath = append(npath, start)

    if start == end {
        return 1
    }
    // start not in graph
    if _, ok := graph[start]; !ok {
        return 0
    }
    count := 0
    for _, node := range graph[start] {
        if cnt_in_slice(node, npath) == 0 || is_upper(node) || (part2 && node != "start" && twice == "") {
            count += find_all_paths(graph, node, end, npath, part2, twice)
        }
    }
    return count
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

    path := make([]string, 0)   
    cnt := find_all_paths(graph, "start", "end", path, part == 2, "")
    fmt.Printf("Part%v: %v", part, cnt)
    return
}