package main

import (
	"fmt"
	"os"
	"strconv"
)

func abs(a int) int {
	if a < 0 {
		return -a
	}
	return a
}

func get_coeffs(coeffs []int, step, outl int) []int {
	outcoeffs := make([]int, 0)
	for i := 0; i < outl; i++ {
		outcoeffs = append(outcoeffs, coeffs[int((i+1)/(step+1))%len(coeffs)])
	}
	return outcoeffs
}

func fft(sigin []int, phases int) {
	coeffs := []int{0, 1, 0, -1}
	coeffscache := map[int][]int{}
	for i := 0; i < phases; i++ {
		for j := 0; j < len(sigin); j++ {
			if _, ok := coeffscache[j]; !ok {
				coeffscache[j] = get_coeffs(coeffs, j, len(sigin))
			}
			mulcoeffs := coeffscache[j]
			res := 0
			for l := 0; l < len(sigin); l++ {
				res += mulcoeffs[l] * sigin[l]
			}
			sigin[j] = abs(res) % 10
		}
	}
}

func fft2(sigin []int, phases, offset int) {

	for i := 0; i < phases; i++ {
		res := 0
		prevsign := 0
		for j := offset; j < len(sigin); j++ {
			if j == offset {
				for l := len(sigin) - 1; l >= offset; l-- {
					res += sigin[l]
				}
			} else {
				res -= prevsign
			}

			prevsign = sigin[j]
			sigin[j] = abs(res) % 10
		}
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	sig := string(dat)
	signal := make([]int, 0)

	for _, c := range sig {
		i, _ := strconv.Atoi(string(c))
		signal = append(signal, i)
	}
	numrep := 100
	sigfft := make([]int, 0)
	sigfft = append(sigfft, signal...)
	fft(sigfft, numrep)
	fmt.Printf("Part1 %v\n", sigfft[0:8])

	lenmult := 10000
	offset, _ := strconv.Atoi(sig[0:7])
	sigfft2 := make([]int, 0)
	for i := 0; i < lenmult; i++ {
		sigfft2 = append(sigfft2, signal...)
	}
	fft2(sigfft2, numrep, offset)
	fmt.Printf("Part2 %v\n", sigfft2[offset:offset+8])
}
