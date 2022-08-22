use std::env;
use std::fs;
use std::collections::HashSet;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let content = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let numbers: Vec<i32> = content
        .split_whitespace()
        .map(|s| s.parse().expect("parse error"))
        .collect();

    let mut sum = 0;
    for num in numbers.iter() {
        sum += num;
    }
    println!("Part1 {}", sum);

    sum = 0;
    let mut check = HashSet::new();
    let mut twice = 0;
    let mut found = false;
    while !found {
        for num in numbers.iter() {
            sum += num;
            if !check.contains(&sum) {
                check.insert(sum);
            } else {
                twice = sum;
                found = true;
                break
            }
        }
    }
    println!("Part2 {}", twice);
}