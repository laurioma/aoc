package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type ReactionD struct {
	outcnt  int
	inchems []string
	incnts  []int
}

func get_inputs(rd map[string]ReactionD, exess map[string]int, chem string, cnt int, l int) int {
	if _, ok := rd[chem]; !ok {
		return cnt
	}

	if exess[chem] >= cnt {
		exess[chem] -= cnt
		return 0
	} else if exess[chem] > 0 {
		cnt -= exess[chem]
		exess[chem] = 0
	}
	numreact := cnt / rd[chem].outcnt
	if cnt%rd[chem].outcnt > 0 {
		numreact += 1
	}
	exess[chem] += (numreact*rd[chem].outcnt - cnt)
	retcnt := 0
	for i, src := range rd[chem].inchems {
		incnt := get_inputs(rd, exess, src, rd[chem].incnts[i]*numreact, l+1)
		retcnt += incnt
	}

	return retcnt
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	lines := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")
	reacts := make(map[string]ReactionD)
	exess := make(map[string]int)
	for _, l := range lines {
		inout := strings.Split(l, "=>")
		inputs := strings.Split(inout[0], ",")
		dst := strings.Split(strings.TrimSpace(inout[1]), " ")
		dstcnt, _ := strconv.Atoi(dst[0])
		inchems := make([]string, 0)
		incnts := make([]int, 0)
		for _, i := range inputs {
			ii := strings.Split(strings.TrimSpace(i), " ")
			inchems = append(inchems, ii[1])
			ic, _ := strconv.Atoi(ii[0])
			incnts = append(incnts, ic)
		}
		reacts[dst[1]] = ReactionD{outcnt: dstcnt, inchems: inchems, incnts: incnts}
	}
	cnt := get_inputs(reacts, exess, "FUEL", 1, 0)

	fmt.Printf("Part1 %v\n", cnt)

	ore := 1000000000000
	fcnt_ok := ore / cnt
	fcnt_f := fcnt_ok * 2
	fcnt_prev := 0
	fcnt := 0
	// binary search for suitable fuel amount
	for true {
		exess = make(map[string]int)
		fcnt = fcnt_ok + (fcnt_f-fcnt_ok)/2
		cnt = get_inputs(reacts, exess, "FUEL", fcnt, 0)
		if cnt < ore {
			fcnt_ok = fcnt
		} else {
			fcnt_f = fcnt
		}
		if fcnt_prev == fcnt {
			break
		}
		fcnt_prev = fcnt
	}

	fmt.Printf("Part2 %v\n", fcnt)

}
