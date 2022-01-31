package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"

	"../intcode"
	"github.com/subchen/go-log"
	"gonum.org/v1/gonum/stat/combin"
)

type Room struct {
	name  string
	doors []string
	items []string
}

func get_line(och <-chan int) string {
	str := ""
	for ch := <-och; true; ch = <-och {
		if ch == '\n' {
			if str == "" {
				continue
			}
			break
		}
		str += string(ch)
	}
	return str
}

func read_until_cmd_prompt(och <-chan int) {
	for true {
		str := get_line(och)
		if str == "Command?" {
			break
		}
	}
}

func write_cmd(ich chan<- int, cmd string) {
	cmd += "\n"
	for _, ch := range cmd {
		ich <- int(ch)
	}
}

func parse_answer(och <-chan int) (bool, Room) {
	state := 0

	name := ""
	doors := make([]string, 0)
	items := make([]string, 0)
	for true {
		str := get_line(och)
		if str == "Command?" {
			break
		}
		if state == 0 {
			if str[0] == '=' {
				name = strings.TrimSpace(str)
			}
			if str == "You can't go that way.\n" {
				panic(str)
			}
			if len(str) > 2 && str[len(str)-1] == ':' {
				state = 1
			}
		} else if state == 1 {
			if str[0] == '-' {
				doors = append(doors, strings.TrimSpace(str[2:]))
			} else {
				if len(str) > 2 && str[len(str)-1] == ':' {
					state = 2
				}
			}
		} else if state == 2 {
			if str[0] == '-' {
				items = append(items, strings.TrimSpace(str[2:]))
			} else {
				state = 4
			}
		}
		if strings.Contains(str, "and you are ejected back to the checkpoint") {
			read_until_cmd_prompt(och)
			return false, Room{name, doors, items}
		} else if strings.Contains(str, "Analysis complete! You may proceed") {
			break
		}
	}
	return true, Room{name, doors, items}
}

func rdir(dir string) string {
	if dir == "north" {
		return "south"
	}
	if dir == "south" {
		return "north"
	}
	if dir == "west" {
		return "east"
	}
	if dir == "east" {
		return "west"
	}
	panic(dir)
}

func go_path(ich chan<- int, och <-chan int, path []string, reverse bool) (bool, Room) {
	log.Debugf("go_path %v %v\n", path, reverse)
	var room Room
	var ok bool
	start := 0
	end := len(path)
	inc := 1
	if reverse {
		start = len(path) - 1
		end = -1
		inc = -1
	}
	for i := start; i != end; i += inc {
		dir := path[i]
		if reverse {
			dir = rdir(dir)
		}
		write_cmd(ich, dir)
		ok, room = parse_answer(och)
		if !ok {
			return false, room
		}
	}
	return true, room
}

func get_items(ich chan<- int, och <-chan int) []string {
	items := make([]string, 0)
	cmd := "inv\n"
	for _, ch := range cmd {
		ich <- int(ch)
	}
	for true {
		str := get_line(och)
		if str == "Command?" {
			break
		}
		if len(str) > 3 && str[0] == '-' {
			items = append(items, strings.TrimSpace(str[2:]))
		}
	}
	return items
}

func item_op(ich chan<- int, och <-chan int, op, item string) {
	write_cmd(ich, op+" "+item)
	read_until_cmd_prompt(och)
}

func try_enter(ich chan<- int, och <-chan int, dir string) bool {
	items := get_items(ich, och)
	log.Debugf("try_enter %v %v\n", dir, items)
	for i := 1; i < len(items); i++ {
		comb := combin.Combinations(len(items), i)
		for _, p := range comb {
			dropped := make([]string, 0)
			for _, pp := range p {
				item_op(ich, och, "drop", items[pp])
				dropped = append(dropped, items[pp])
			}
			write_cmd(ich, dir)
			ok, _ := parse_answer(och)
			if ok {
				log.Debugf("try_enter got in %v\n", dropped)
				return true
			} else {
				log.Debugf("try_enter fail %v\n", dropped)
			}
			for _, d := range dropped {
				item_op(ich, och, "take", d)
			}
		}
	}
	return false
}

func explore(ich chan<- int, och <-chan int) {
	dont_touch := map[string]bool{
		"giant electromagnet": false,
		"escape pod":          false,
		"molten lava":         false,
		"photons":             false,
		"infinite loop":       false,
	}
	visited := make(map[string]bool)
	searcho := make([][]string, 0)
	searcho = append(searcho, make([]string, 0))
	for true {
		if len(searcho) == 0 {
			break
		}
		path := searcho[0]
		searcho = searcho[1:]
		var room Room
		var ok bool
		if len(path) == 0 {
			ok, room = parse_answer(och)
		} else {
			ok, room = go_path(ich, och, path, false)
		}
		if !ok {
			// when failed to get into the room, try to drop some items. Luckily we have all the items here
			if try_enter(ich, och, path[len(path)-1]) {
				return
			} else {
				panic("couldn't get in")
			}
		} else {
			log.Debugf("explore room %v\n", room)
			if _, ok := visited[room.name]; !ok {
				for _, item := range room.items {
					if _, ok := dont_touch[item]; ok {
						continue
					}
					log.Debugf("explore take %v\n", item)
					item_op(ich, och, "take", item)
				}

				visited[room.name] = true
				for _, door := range room.doors {
					npath := make([]string, len(path))
					copy(npath, path)
					npath = append(npath, door)
					searcho = append(searcho, npath)
				}
			}
		}

		// go back to start
		ok, room = go_path(ich, och, path, true)
		if !ok || (len(path) > 0 && room.name != "== Hull Breach ==") {
			panic("failed to go back")
		}
	}
}

func main() {
	log.Default.Level = log.INFO
	dat, _ := os.ReadFile(os.Args[1])
	prog := strings.Split(string(dat), ",")
	ich := make(chan int, 100)
	och := make(chan int, 0)
	go intcode.RunProg(prog, ich, och)

	explore(ich, och)

	re := regexp.MustCompile(`[0-9-]+`)
	for true {
		str := get_line(och)
		log.Debugf("%v", str)
		match := re.FindAllString(str, -1)
		if len(match) > 0 {
			fmt.Printf("Part1: %v", match[0])
			break
		}
	}
}
