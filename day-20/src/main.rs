#![allow(unused_imports)] // XXX

use std::convert::{TryFrom, TryInto};
use std::fmt;
use std::str::FromStr;

use anyhow::{anyhow, bail, ensure, Context, Result};
use lazy_static::lazy_static;
use regex::Regex;

mod grid;
mod types;

fn run() -> Result<()> {
    println!("TODO!");
    Ok(())
}

fn main() {
    if let Err(e) = run() {
        eprintln!("Error: {:#}", e);
        std::process::exit(1);
    }
}
