#![allow(unused_imports)] // XXX

use std::convert::{TryFrom, TryInto};
use std::fmt::Write;
use std::fs;
use std::path::Path;
use std::str::FromStr;

use anyhow::{anyhow, bail, ensure, Context, Result};
use yall::{Logger, log_macros::*};

mod grid;
mod types;

use grid::Grid;
use types::*;

fn parse_input(filename: impl AsRef<Path>) -> Result<Vec<Tile>> {
    let input = fs::read_to_string(filename)?;
    let mut lines = input.lines();
    let mut tiles = Vec::new();
    let mut done = false;
    while !done {
        let mut current = String::new();
        loop {
            match lines.next() {
                Some("") => break,
                Some(line) => {
                    current.push_str(line);
                    current.push_str("\n");
                }
                None => {
                    done = true;
                    break;
                }
            }
        }
        //debug!("parsing tile '{}'", current);
        tiles.push(current.parse()?);
    }
    Ok(tiles)
}

// return squr(count) if count is a perfect square
fn int_sqrt(count: usize) -> Result<usize> {
    let sqrt = (count as f64).sqrt() as usize;
    if sqrt * sqrt == count {
        Ok(sqrt)
    } else {
        Err(anyhow!("number of tiles {} is not square", count))
    }
}

fn run() -> Result<()> {
    Logger::with_verbosity(5).init();
    let tiles = parse_input("sample-input.txt")?;
    //for tile in tiles.iter() {
    //    trace!("{:#}", tile);
    //}

    let grid_size = int_sqrt(tiles.len())?;

    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {:#}", e);
        std::process::exit(1);
    }
}
