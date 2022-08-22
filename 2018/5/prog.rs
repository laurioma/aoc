use std::env;
use std::fs;
use std::collections::HashSet;
use std::collections::VecDeque;

fn react(poly: &mut VecDeque<char>) -> &VecDeque<char> {
    let mut pos = 0;
    loop {
        let mut found = false;
        for idx in pos..poly.len()-1 {
            let char1 = poly[idx];
            let char2 = poly[idx+1];
            if char1.to_lowercase().eq(char2.to_lowercase()) && char1.is_uppercase() != char2.is_uppercase() {
                found = true;
                pos = idx;
                break;
            }
        }
        if found {
            poly.drain(pos..pos+2);
            if pos > 0 {
                pos -= 1;
            }
        } else {
            break;
        }
        if poly.len() < 2 {
            break;
        }
    }
    return poly;
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let file_path = &args[1];
    let content = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let mut poly_in = content.chars().collect::<VecDeque<_>>();
    let poly = react(&mut poly_in);
    println!("Part1: {}", poly.len());

    let charset = content.to_lowercase().chars().collect::<HashSet<_>>();
    let mut shortest = content.len();
    for c in charset.iter() {
        let c_u = &c.to_uppercase().next().unwrap();
        let mut poly_in = content.chars().collect::<VecDeque<_>>();
        poly_in.retain(|ch| ch != c && ch != c_u);
        let res = react(&mut poly_in);
        if shortest > res.len() {
            shortest = res.len();
        }
    }
    println!("Part2: {}", shortest);
}
