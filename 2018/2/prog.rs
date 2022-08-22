use std::env;
use std::fs;
use std::collections::HashMap;

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];

    let content = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let (mut count2, mut count3) = (0, 0);
    for id in content.split_whitespace() {
        let mut check = HashMap::new();
        for c in id.chars() {
            *check.entry(c).or_insert(0) += 1;
        }
        for ch in check.iter() {
            if *ch.1 == 2 {
                count2 += 1;
                break;
            }
        }
        for ch in check.iter() {
            if *ch.1 == 3 {
                count3 += 1;
                break
            }
        }
    }
    println!("Part1 {}", count2*count3);

    'l1: for id1 in content.split_whitespace() {
        for id2 in content.split_whitespace() {
            let (mut count, mut pos, mut neqpos) = (0, 0, 0);
            for it in id1.chars().zip(id2.chars()) {
                let (i1, i2) = it;
                if i1 != i2 {
                    count += 1;
                    neqpos = pos;
                }
                pos += 1;
            }
            if count == 1 {
                let mut ret = id1.to_string();
                ret.remove(neqpos);
                println!("Part2 {}", ret);
                break 'l1;
            }
        }
    }
}