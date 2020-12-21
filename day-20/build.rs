use std::env;
use std::fs::File;
use std::path::Path;
use std::io::{Write, BufWriter};

/// reverse the lower 10 bits in the input
#[rustfmt::skip]
fn rev10(n: u16) -> u16 {
    ((n & (1 << 0)) << 9) |
    ((n & (1 << 1)) << 7) |
    ((n & (1 << 2)) << 5) |
    ((n & (1 << 3)) << 3) |
    ((n & (1 << 4)) << 1) |
    ((n & (1 << 5)) >> 1) |
    ((n & (1 << 6)) >> 3) |
    ((n & (1 << 7)) >> 5) |
    ((n & (1 << 8)) >> 7) |
    ((n & (1 << 9)) >> 9)
}

fn run() -> std::io::Result<()> {
    let out_dir = env::var_os("OUT_DIR").unwrap();
    let out_file = Path::new(&out_dir).join("rev10_table.rs");
    let mut out_file = BufWriter::new(File::create(&out_file)?);
    writeln!(out_file, "static REV10_TABLE: [u16; 1024] = [")?;
    for i in 0..1024 {
        writeln!(out_file, "    {},", rev10(i))?;
    }
    writeln!(out_file, "];")?;

    out_file.into_inner()?.sync_all()?;

    println!("cargo:rerun-if-changed=build.rs");
    Ok(())
}

fn main() {
    run().unwrap();
}
