import * as fs from 'fs';
import { createPriorityQueue } from '@algorithm.ts/priority-queue'


function try_resolve_gate(maze: string[], x:number, y:number): [string, [number, number]] {
    // horizontal
    if (maze[y].length > x+1 && maze[y][x+1].match(/[A-Z]/i)) {
        if (maze[y].length > x+2 && maze[y][x+2] == '.') {
            return [maze[y].substring(x, x+2), [x+2, y]];
        } else if (x-1 >= 0 && maze[y][x-1] == '.') {
            return [maze[y].substring(x, x+2), [x-1, y]];
        }
    // vertical
    } else if (maze.length > y+1 && maze[y+1][x].match(/[A-Z]/i)) {
        if (maze.length > y+2 && maze[y+2][x] == '.') {
            return [maze[y][x]+maze[y+1][x], [x, y+2]];
        } else if (y-1 >= 0 && maze[y-1][x] == '.') {
            return [maze[y][x]+maze[y+1][x], [x, y-1]];
        }
    }
}

function is_outer_gate(x: number, y: number, w: number, h: number): boolean {
    if (x < 2 || y < 2 || x >= w-2 || y >= h - 2) {
        return true
    } else {
        return false
    }
}

function find_path(maze: string[], src: [number, number], dst: [number, number]) :number {
    // console.log("find_path ", src, dst)
    var visited = new Map<string,boolean>()
    var movec = [[0, -1], [0, 1], [-1, 0], [1, 0]]
    var searcho = []
    searcho.push([src, 0, ]) // pos, dist
    while (searcho.length > 0) {
        let [pos, dist] = searcho.shift()
        visited.set(pos.join(','), true)

        if (pos[0] == dst[0] && pos[1] == dst[1]) {
            // console.log("find_path found")
            return  dist
        }
        movec.forEach((c) => {
            let npos: [number, number] = [pos[0]+c[0], pos[1]+c[1]]
            if (npos[0] < 0 || npos[1] < 0 || npos[0] >= maze[0].length || npos[1] >= maze.length) {
                return
            }
            // console.log("find_path check npos", npos, maze.has(npos.join(',')), maze.get(npos.join(',')) )
            if (!visited.get(npos.join(',')) && maze[npos[1]][npos[0]] == '.' ) {
                searcho.push([npos, dist+1])
            }
        })
    }
    return -1
}

// from gate to gate distances. Adds I and O suffices for gate names
function create_distance_map(maze: string[], gates: Map<string, [number,number][]>): Map<string, Map<string, number>> {
    let dist = new Map<string, Map<string, number>>()
    for (let [k1,v1] of Array.from(gates)) {
        for (let i1 of [0,1]) {
            for (let [k2,v2] of Array.from(gates)) {
                for (let i2 of [0,1]){
                    let key1 = k1 + (i1 == 0? 'O' : 'I')
                    let key2 = k2 + (i2 == 0? 'O' : 'I')
                    let pos1 = v1[i1]
                    let pos2 = v2[i2]
                    let d = find_path(maze, pos1, pos2)
                    if (d >= 0) {
                        if (!dist.has(key1)) {
                            dist.set(key1, new Map<string,number>())
                        }
                        dist.get(key1).set(key2, d)
                    }
                }
            }
        }
    }
    return dist
}

function solve_maze(distm: Map<string, Map<string, number>>, src: string, dst: string, part2: boolean) : [number, [string, number, number][]] {
    let searcho = createPriorityQueue<[string, number, number, [string, number, number][]]>((x, y) => y[1] - x[1])
    var visited = new Map<number, Map<string,boolean>>()
    searcho.enqueue([src, 0, 0, [[src, 0, 0]]])
    while (searcho.size() > 0) {
        let [pos, dist, level, path] = searcho.dequeue()
        
        // console.log("solve curr", pos, dist, level)
        if (pos == dst) {
            return [dist, path]
        }
        if (!visited.has(level)) {
            visited.set(level, new Map<string,boolean>())
        }
        let lvisited = visited.get(level)
        lvisited.set(pos, true)
        if (distm.has(pos)) {
            let connections = distm.get(pos)
            connections.forEach((d: number, key: string) => {
                // for part2 outer gates except AAO & ZZO closed on level0
                if (part2 && level == 0 && key[2] == "O" && key != "AAO" && key != "ZZO") {
                    return
                }
                // AAO ZZO closed on other levels
                if (level > 0 && (key == "AAO" || key == "ZZO")) {
                    return
                }
                if (!lvisited.has(key)) {
                    let newd = dist + d
                    let nkey = key[2] == 'I'? key.substring(0,2)+"O": key.substring(0,2)+"I"
                    newd += 1
                    // dont go from ZZO to ZZI
                    if (key == "ZZO") {
                        nkey = key
                        newd -=1
                    } 
                    var nlevel = 0
                    if (part2) {
                        nlevel = key[2]=="I"?  level+1 : level-1
                    } 
                    // console.log("solve add ", key, nkey, dist, d, newd, nlevel)
                    var npath = [...path]
                    npath.push([nkey, nlevel, d])
                    searcho.enqueue([nkey, newd, nlevel, npath])
                }
            });
        }
    }
    return [-1, []]
}


const args = process.argv.slice(2);

let f = fs.readFileSync(args[0],'utf8');
let maze = f.split(/\r?\n/)

let gates = new Map<string, [number,number][] >();
for (let y = 0; y < maze.length; y++) {
    for (let x = 0; x < maze[0].length; x++) {
        if (maze[y][x].match(/[A-Z]/i)) {
            let g = try_resolve_gate(maze, x, y)
            if (g) {
                if (!gates.has(g[0])) {
                    gates.set(g[0], [[0,0],[0,0]])
                }
                if (is_outer_gate(x,y, maze[0].length, maze.length)) {
                    gates.get(g[0])[0] = g[1]
                } else {
                    gates.get(g[0])[1] = g[1]
                }
            }
        } 
    }      
}
// console.log(maze)
// console.log(gates)

let dm = create_distance_map(maze, gates)
// console.log(dm)


let [r1, p1] = solve_maze(dm, "AAO", "ZZO", false)
console.log("Part1", r1)


let [r2, p2] = solve_maze(dm, "AAO", "ZZO", true)
console.log("Part2", r2)

