use std::env;
use std::fs;
use regex::Regex;
use std::collections::HashMap;
use itertools::iproduct;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let content = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut points = HashMap::new();
    let mut ids: Vec<(i32, i32, i32, i32,i32)> = Vec::new();
    for ll in content.lines() {
        let re = Regex::new(r"#(\d+) @ (\d+),(\d+): (\d+)x(\d+)").unwrap();
        let caps = re.captures(ll).unwrap();

        let id = caps[1].parse::<i32>().unwrap();
        let x = caps[2].parse::<i32>().unwrap();
        let y = caps[3].parse::<i32>().unwrap();
        let w = caps[4].parse::<i32>().unwrap();
        let h = caps[5].parse::<i32>().unwrap();
        ids.push((id, x, y, w, h));
        for coord in iproduct!(x..x+w, y..y+h) {
            *points.entry(coord).or_insert(0) += 1;
        }
    }
    let mut answ = 0;
    for rcnt in points.values() {
        if *rcnt > 1 {
            answ += 1;
        }
    }
    println!("Part1 {}", answ);
    answ = 0;
    for (id, x, y, w, h) in ids {
        let mut overlap = false;
        for coord in iproduct!(x..x+w, y..y+h) {
            if *points.get(&coord).unwrap() > 1 {
                overlap = true;
                break;
            }
        }
        if !overlap {
            answ = id;
            break;
        }
    }
    println!("Part2 {}", answ);
}
