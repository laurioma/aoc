import * as fs from 'fs';

function run_sim(grid: string[][]) {
    var changes : Array<[[number, number], string]>= []
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[0].length; x++) {        
            var dir = [[0, -1], [0, 1], [-1, 0], [1, 0]]
            var bugc = 0
            dir.forEach((c) => {
                let npos: [number, number] = [x+c[0], y+c[1]]
                if (npos[0] < 0 || npos[1] < 0 || npos[0] >= grid[0].length || npos[1] >= grid.length) {
                    return
                }
                if (grid[npos[1]][npos[0]] == '#') {
                    bugc += 1
                }
            })
            if (grid[y][x] == '#' && bugc != 1) {
                changes.push([[x, y], '.'])
            } else if (grid[y][x] == '.' && (bugc == 1 || bugc == 2)) {
                changes.push([[x, y], '#'])
            }
        }
    }
    changes.forEach((c) => {
        grid[c[0][1]][c[0][0]] = c[1]
    })
}

function count_inner(grids: Map<number, string[][]>, level: number, pos: [number, number]) : number {
    let sz = grids.get(0)[0].length
    if (!grids.has(level+1)) {
        return 0
    }
    let grid = grids.get(level+1)
    let ret = 0
    if (pos[1] == 1 && pos[0] == 2) {
        for (let i = 0; i < sz; i++) {
            if (grid[0][i] == '#') 
                ret += 1
        }
    } else if (pos[1] == 2 && pos[0] == 3) {
        for (let i = 0; i < sz; i++) {
            if (grid[i][sz-1] == '#') 
                ret += 1
        }
    } else if (pos[1] == 3 && pos[0] == 2) {
        for (let i = 0; i < sz; i++) {
            if (grid[sz-1][i] == '#') 
                ret += 1
        }
    } else if (pos[1] == 2 && pos[0] == 1) {
        for (let i = 0; i < sz; i++) {
            if (grid[i][0] == '#') 
                ret += 1
        }
    } else {
        throw new Error("invalid pos")
    }
    return ret
}

function count_outer(grids: Map<number, string[][]>, level: number, pos: [number, number]) : number {
    let sz = grids.get(0)[0].length
    if (!grids.has(level-1)) {
        return 0
    }
    let grid = grids.get(level-1)
    if (pos[0] == -1) {
        if (grid[2][1] == '#') 
            return 1
    } else if (pos[0] == sz) {
        if (grid[2][3] == '#') 
            return 1
    } else if (pos[1] == -1) {
        if (grid[1][2] == '#') 
            return 1
    } else if (pos[1] == sz) {
        if (grid[3][2] == '#') 
            return 1
    } else {
        throw new Error("invalid pos")
    }
    return 0
}

function run_sim2(grids: Map<number, string[][]>, level, maxlevel, up, down: boolean) {
    let sz = grids.get(0)[0].length
    if (!grids.has(level)) {
        grids.set(level, new Array(sz).fill(null).map(() => new Array(sz).fill('.')))
    }
    let grid = grids.get(level)
     
    var changes : Array<[[number, number], string]>= []
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[0].length; x++) {        
            if (x == 2 && y == 2) {
                continue
            }
            var dir = [[0, -1], [0, 1], [-1, 0], [1, 0]]
            var bugc = 0

            var pos: [number, number]= [x,y]
            dir.forEach((c) => {
                let npos: [number, number] = [x+c[0], y+c[1]]
                if (npos[0] == 2 && npos[1] == 2) {
                    bugc += count_inner(grids, level, pos)
                } else if (npos[0] < 0 || npos[1] < 0 || npos[0] >= sz || npos[1] >= sz) {
                    bugc += count_outer(grids, level, npos)
                } else {
                    if (grid[npos[1]][npos[0]] == '#') {
                        bugc += 1
                    }    
                }
            })
            if (grid[y][x] == '#' && bugc != 1) {
                changes.push([[x, y], '.'])
            } else if (grid[y][x] == '.' && (bugc == 1 || bugc == 2)) {
                changes.push([[x, y], '#'])
            }
        }
    }
    if (level - 1 >= -maxlevel && up) {
        run_sim2(grids, level-1, maxlevel, true, false)
    }
    if (level + 1 <= maxlevel && down) {
        run_sim2(grids, level+1, maxlevel, false, true)        
    }
    changes.forEach((c) => {
        grid[c[0][1]][c[0][0]] = c[1]
    })
}

function biodiv(grid: string[][]) : number {
    var biod = 0
    for (let y = 0; y < grid.length; y++) {
        for (let x = 0; x < grid[0].length; x++) {
            if (grid[y][x] == '#') {
                biod += Math.pow(2, (y * grid.length + x))
            }
        }
    }
    return biod
}

function mkgrid(lines: string[]) : string[][]{
    let grid = []
    for (let y = 0; y < lines.length; y++) {
        grid.push(lines[y].split(''))
    }
    return grid
}

function count(grids: Map<number, string[][]>) : number {
    var count = 0
    grids.forEach((grid: string[][], k: number) => {
        grid.forEach((row: string[]) => { 
            row.forEach((v: string) => { 
                if (v == '#')
                    count +=1
            })
        })
    });
    return count
}


const args = process.argv.slice(2);

let f = fs.readFileSync(args[0],'utf8');
let lines = f.split(/\r?\n/)
let grid = mkgrid(lines)

var biodivs = []
var bd
while (true) {
    bd = biodiv(grid)
    const found = biodivs.find(h => h == bd);
    if (found) {
        break
    } 
    biodivs.push(bd)
    run_sim(grid)
}
console.log("Part1", bd)

grid = mkgrid(lines)

let grids = new Map<number, string[][]>([[0, grid]])

let max = 200
for (let i = 0; i < max; i++) {
    run_sim2(grids, 0, max, true, true)
}

console.log("Part2", count(grids))