package main

import (
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"
)

func read_bitstr(s *string, len int) int {
	bits := (*s)[0:len]
	*s = (*s)[len:]
	ret, _ := strconv.ParseInt(bits, 2, 0)
	return int(ret)
}

type decoded_packet struct {
	bitlen int
	ver    int
	typ    int
	value  int
	subp   []decoded_packet
}

func decode_packet(s *string, versum *int) decoded_packet {
	startlen := len(*s)
	ver := read_bitstr(s, 3)
	typ := read_bitstr(s, 3)
	*versum += ver
	value := 0
	subp := make([]decoded_packet, 0)

	if typ == 4 {
		for true {
			cont := read_bitstr(s, 1)
			v := read_bitstr(s, 4)
			value = (value << 4) + v
			if cont == 0 {
				break
			}
		}
	} else {
		lenid := read_bitstr(s, 1)
		if lenid == 0 {
			plen := read_bitstr(s, 15)
			remaining := plen
			for remaining > 6 {
				packet := decode_packet(s, versum)
				remaining -= packet.bitlen
				subp = append(subp, packet)
			}
		} else {
			numsub := read_bitstr(s, 11)
			for i := 0; i < numsub; i++ {
				packet := decode_packet(s, versum)
				subp = append(subp, packet)
			}
		}
	}
	return decoded_packet{bitlen: (startlen - len(*s)), typ: typ, value: value, subp: subp}
}

func calculate(packet decoded_packet) int {

	if packet.typ == 4 {
		return packet.value
	} else if packet.typ == 0 {
		sum := 0
		for _, sp := range packet.subp {
			sum += calculate(sp)
		}
		return sum
	} else if packet.typ == 1 {
		prod := 1
		for _, sp := range packet.subp {
			prod *= calculate(sp)
		}
		return prod
	} else if packet.typ == 2 {
		min := math.MaxInt
		for _, sp := range packet.subp {
			v := calculate(sp)
			if min > v {
				min = v
			}
		}
		return min
	} else if packet.typ == 3 {
		max := 0
		for _, sp := range packet.subp {
			v := calculate(sp)
			if max < v {
				max = v
			}
		}
		return max
	} else if packet.typ == 5 {
		sp1 := calculate(packet.subp[0])
		sp2 := calculate(packet.subp[1])
		if sp1 > sp2 {
			return 1
		} else {
			return 0
		}
	} else if packet.typ == 6 {
		sp1 := calculate(packet.subp[0])
		sp2 := calculate(packet.subp[1])
		if sp1 < sp2 {
			return 1
		} else {
			return 0
		}
	} else {
		if packet.typ != 7 {
			panic("invalid packet type")
		}
		sp1 := calculate(packet.subp[0])
		sp2 := calculate(packet.subp[1])
		if sp1 == sp2 {
			return 1
		} else {
			return 0
		}
	}
}

func main() {
	dat, _ := os.ReadFile(os.Args[1])
	strarr := strings.Split(strings.ReplaceAll(string(dat), "\r", ""), "\n")

	for _, line := range strarr {
		bitstr := ""
		for _, c := range line {
			i, _ := strconv.ParseInt(string(c), 16, 0)
			bits := fmt.Sprintf("%04b", i)
			for _, b := range bits {
				bitstr += string(b)
			}
		}
		versum := 0
		p := decode_packet(&bitstr, &versum)

		fmt.Printf("Part1: %v\n", versum)
		fmt.Printf("Part1: %v\n", calculate(p))
	}

	return
}
