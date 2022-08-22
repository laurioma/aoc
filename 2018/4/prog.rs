use std::env;
use std::fs;
use regex::Regex;
use std::collections::HashMap;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let content = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut sorted: Vec<&str> = content.lines().collect();
    sorted.sort();
    let mut sleep = HashMap::new();
    let mut guard:Option<u32> = None;
    let mut start:Option<u32> = None;
    for ll in sorted {
        let re = Regex::new(r"\[\d+-\d+-\d+ \d+:(\d+)\] (.*)").unwrap();
        let caps = re.captures(ll).unwrap();
        let mm = caps[1].parse::<u32>().unwrap();
        let action = &caps[2];

        if action == "falls asleep" {
            start = Some(mm);
        } else if action == "wakes up" {
            let map = sleep.entry(guard.unwrap()).or_insert(HashMap::new());
            for m in start.unwrap()..mm {
                *map.entry(m).or_insert(0) += 1;
            }
        } else {
            let re1 = Regex::new(r"Guard #(\d+) begins shift").unwrap();
            let caps1 = re1.captures(action).unwrap();
            guard = caps1[1].parse::<u32>().ok();
        }
    }

    let mut most_sleepy:Option<(u32, u32)> = None;
    for (k, v) in &sleep {
        let total:u32 = v.values().sum();
        if most_sleepy.is_none() || most_sleepy.unwrap().1 < total {
            most_sleepy = Some((*k, total));
        }
    }
    let sleepy_min = sleep[&most_sleepy.unwrap().0].iter().
        max_by(|a,b| a.1.cmp(b.1));
    println!("Part1 {}", most_sleepy.unwrap().0 * sleepy_min.unwrap().0);


    let mut most_sleepy2:Option<(u32, u32, u32)> = None;
    for (k, v) in &sleep {
        let max = v.iter().max_by(|a,b| a.1.cmp(b.1)).unwrap();
        if most_sleepy2.is_none() || most_sleepy2.unwrap().1 < *max.1 {
            most_sleepy2 = Some((*k, *max.1, *max.0));
        }
    }
    println!("Part2 {} ", most_sleepy2.unwrap().0 * most_sleepy2.unwrap().2);
}
