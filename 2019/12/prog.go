package main

import (
	"fmt"
	"os"

	"gonum.org/v1/gonum/stat/combin"
)

func abs(i int64) int64 {
	if i < 0 {
		return -i
	}
	return i
}

func energy(pos, vel *[4][3]int64) int64 {
	var e int64
	for m := 0; m < len(pos); m++ {
		var pot int64
		var kin int64
		for d := 0; d < 3; d++ {
			pot += abs(pos[m][d])
			kin += abs(vel[m][d])
		}
		e += pot * kin
	}
	return e
}

func get_stepper(nmoons int) func(pos, vel *[4][3]int64) {
	comb := combin.Combinations(nmoons, 2) // return closure using comb to avoid recalculating combin.Combinations
	return func(pos, vel *[4][3]int64) {
		for _, c := range comb {
			// fmt.Printf("%v\n", c)
			m1 := &pos[c[0]]
			m2 := &pos[c[1]]
			v1 := &vel[c[0]]
			v2 := &vel[c[1]]

			for d := 0; d < 3; d++ {
				if m1[d] > m2[d] {
					v1[d] -= 1
					v2[d] += 1
				} else if m1[d] < m2[d] {
					v1[d] += 1
					v2[d] -= 1
				}
			}
		}
		for m := 0; m < len(pos); m++ {
			for d := 0; d < 3; d++ {
				pos[m][d] += vel[m][d]
			}
		}
	}
}

// greatest common divisor (GCD) via Euclidean algorithm
func GCD(a, b int64) int64 {
	for b != 0 {
		t := b
		b = a % b
		a = t
	}
	return a
}

// find Least Common Multiple (LCM) via GCD
func LCM(a, b int64, integers ...int64) int64 {
	result := a * b / GCD(a, b)

	for i := 0; i < len(integers); i++ {
		result = LCM(result, integers[i])
	}

	return result
}

func main() {
	pos := [4][3]int64{{3, 2, -6}, {-13, 18, 10}, {-8, -1, 13}, {5, 10, 4}}
	if len(os.Args) > 1 && os.Args[1] == "test" {
		pos = [4][3]int64{{-1, 0, 2}, {2, -10, -7}, {4, -8, 8}, {3, 5, -1}}
	}
	var vel [4][3]int64
	orig_pos := pos
	orig_vel := vel

	step := get_stepper(len(pos))
	for i := 0; i < 1000; i++ {
		step(&pos, &vel)
	}
	fmt.Printf("Part1: %v\n", energy(&pos, &vel))

	var nsteps int64
	var steps_to_equal [3]int64
	done := false
	pos = orig_pos
	vel = orig_vel
	for !done {
		step(&pos, &vel)
		nsteps += 1

		eq := [3]bool{true, true, true}
		for m := 0; m < len(pos); m++ {
			for d := 0; d < 3; d++ {
				if eq[d] && (orig_pos[m][d] != pos[m][d] || orig_vel[m][d] != vel[m][d]) {
					eq[d] = false
				}
			}
		}
		done = true
		for d := 0; d < 3; d++ {
			if eq[d] && steps_to_equal[d] == 0 {
				steps_to_equal[d] = nsteps
			}
			if steps_to_equal[d] == 0 {
				done = false
			}
		}
	}
	fmt.Printf("Part2: %v\n", LCM(steps_to_equal[0], steps_to_equal[1], steps_to_equal[2]))

}
