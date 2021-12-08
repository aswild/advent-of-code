#![allow(dead_code)] // XXX

use std::cmp::Ordering;
use std::convert::{TryFrom, TryInto};
use std::fmt;
use std::str::FromStr;

use anyhow::{anyhow, bail, ensure, Context, Result};
use lazy_static::lazy_static;
use regex::Regex;

pub const TILE_SIZE: usize = 10;

// this defines static REV10_TABLE: [u16; 1024].
// Used in Edge::flip, but the include! macro has to be called here in global scope rather than
// inside a function body.
include!(concat!(env!("OUT_DIR"), "/rev10_table.rs"));

#[derive(Clone, Copy, Eq, PartialEq)]
pub enum Point {
    Black,
    White,
}

impl Point {
    #[inline]
    pub fn as_str(&self) -> &'static str {
        match self {
            Self::Black => ".",
            Self::White => "#",
        }
    }

    fn parse_row(s: &str) -> Result<[Point; TILE_SIZE]> {
        ensure!(s.len() == TILE_SIZE, "Invalid point row length '{}'", s);
        let mut row = [Point::default(); TILE_SIZE];
        for (i, c) in s.chars().enumerate() {
            row[i] = match c {
                '.' => Point::Black,
                '#' => Point::White,
                _ => bail!("Invalid character '{}' in row string", c),
            };
        }
        Ok(row)
    }
}

impl Default for Point {
    fn default() -> Self {
        Point::Black
    }
}

impl fmt::Display for Point {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

#[derive(Clone, Copy, Debug, Eq, PartialEq)]
pub enum Orientation {
    /// the original orientation. orig north side faces north
    North,
    /// 90 deg clockwise rotation. orig north side faces east
    East,
    /// 180 deg rotation
    South,
    /// 270 deg clockwise rotation
    West,
    /// horizontal flip (N/S still N/S, E/W flip to W/E)
    FlipNorth,
    /// horizontal flip, then 90 deg rotation. orig north faces east
    FlipEast,
    /// vertical flip, same as horizontal flip + 180 rotation. orig north faces south
    FlipSouth,
    /// vertical flip, then 90 deg rotation. orig north faces west (same as horiz flip + 270 deg)
    FlipWest,
}

/// An edge is represented as a 10-bit number. Horizontal edges are always stored left to right
/// (west to east), vertical edges are top to bottom (north to south), as MSB first in the lower 10
/// bits of the u16.
///
/// Example tile:
///   ..##.#..#.
///   ##..#.....
///   #...##..#.
///   ####.#...#
///   ##.##.###.
///   ##...#.###
///   .#.#.#..##
///   ..#....#..
///   ###...#.#.
///   ..###..###
/// North edge is 0011010010 = 210 = 0x0d2
/// East  edge is 0001011001 =  89 = 0x059
/// South edge is 0011100111 = 231 = 0x0e7
/// West  edge is 0111110010 = 498 = 0xf12
#[derive(Clone, Copy, Default, Eq, PartialEq)]
pub struct Edge(u16);

impl Edge {
    #[inline]
    pub fn flip(&self) -> Edge {
        Edge(REV10_TABLE[self.0 as usize])
    }
}

impl fmt::Debug for Edge {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "Edge(0x{:03x})", self.0)
    }
}

impl fmt::Display for Edge {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        for i in (0..10).rev() {
            if (self.0 & (1 << i)) != 0 {
                f.write_str("#")?;
            } else {
                f.write_str(".")?;
            }
        }
        Ok(())
    }
}

impl TryFrom<&[Point]> for Edge {
    type Error = anyhow::Error;
    fn try_from(points: &[Point]) -> Result<Self, Self::Error> {
        ensure!(
            points.len() == TILE_SIZE,
            "Invalid Edge array length {}",
            points.len()
        );
        let mut val = 0u16;
        for p in points.iter() {
            let bit = match p {
                Point::White => 1,
                Point::Black => 0,
            };
            val = (val << 1) | bit;
        }
        Ok(Edge(val))
    }
}

impl FromStr for Edge {
    type Err = anyhow::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        ensure!(
            s.len() == TILE_SIZE,
            "Invalid Edge string length. Expected {} got {}",
            TILE_SIZE,
            s.len()
        );
        let mut val = 0u16;
        for c in s.chars() {
            let bit = match c {
                '#' => 1,
                '.' => 0,
                //_ => return Err(format!("Invalid character '{}' in Edge string", c)),
                _ => bail!("Invalid character '{}' in Edge string", c),
            };
            val = (val << 1) | bit;
        }
        Ok(Edge(val))
    }
}

#[derive(Clone, Copy, Default, Eq, PartialEq)]
pub struct TileEdges {
    pub n: Edge,
    pub e: Edge,
    pub s: Edge,
    pub w: Edge,
}

impl TileEdges {
    pub fn orient(&self, o: Orientation) -> TileEdges {
        match o {
            Orientation::North => *self,
            Orientation::East => TileEdges {
                n: self.w.flip(),
                e: self.n,
                s: self.e.flip(),
                w: self.s,
            },
            Orientation::South => TileEdges {
                n: self.s.flip(),
                e: self.w.flip(),
                s: self.n.flip(),
                w: self.e.flip(),
            },
            Orientation::West => TileEdges {
                n: self.e,
                e: self.s.flip(),
                s: self.w,
                w: self.n.flip(),
            },
            Orientation::FlipNorth => TileEdges {
                n: self.n.flip(),
                e: self.w,
                s: self.s.flip(),
                w: self.e,
            },
            Orientation::FlipEast => TileEdges {
                n: self.e.flip(),
                e: self.n.flip(),
                s: self.w.flip(),
                w: self.s.flip(),
            },
            Orientation::FlipSouth => TileEdges {
                n: self.s,
                e: self.e.flip(),
                s: self.n,
                w: self.w.flip(),
            },
            Orientation::FlipWest => TileEdges {
                n: self.w,
                e: self.s,
                s: self.e,
                w: self.n,
            },
        }
    }
}

/// Representation of a Tile's id and edges, sortable by ID
#[derive(Clone, Copy, Default, Eq)]
pub struct TileIdEdges {
    pub id: u32,
    pub edges: TileEdges,
}

impl Ord for TileIdEdges {
    fn cmp(&self, other: &Self) -> Ordering {
        self.id.cmp(&other.id)
    }
}

impl PartialOrd for TileIdEdges {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

impl PartialEq for TileIdEdges {
    fn eq(&self, other: &Self) -> bool {
        self.id == other.id
    }
}

#[derive(Clone, Copy, Default, Eq, PartialEq)]
pub struct Tile {
    pub id: u32,
    pub points: [[Point; TILE_SIZE]; TILE_SIZE],
}

impl fmt::Debug for Tile {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        f.debug_struct("Tile").field("id", &self.id).finish()
    }
}

impl fmt::Display for Tile {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        if f.alternate() {
            writeln!(f, "Tile {}:", self.id)?;
        }
        for row in self.points.iter() {
            for point in row.iter() {
                f.write_str(point.as_str())?;
            }
            f.write_str("\n")?;
        }
        Ok(())
    }
}

impl FromStr for Tile {
    type Err = anyhow::Error;
    fn from_str(s: &str) -> Result<Self, Self::Err> {
        lazy_static! {
            static ref ID_RE: Regex = Regex::new(r"^Tile (\d+):$").unwrap();
        }

        let mut tile = Tile::default();
        let mut lines = s.lines();
        let id_line = lines.next().ok_or_else(|| anyhow!("No tile id line"))?;
        tile.id = ID_RE
            .captures(id_line)
            .ok_or_else(|| anyhow!("Failed to parse tile id line"))?
            .get(1)
            .unwrap()
            .as_str()
            .parse()
            .context("Failed to parse tile id number")?;

        for i in 0..TILE_SIZE {
            let line = lines
                .next()
                .ok_or_else(|| anyhow!("Incomplete data for tile {}", tile.id))?;
            tile.points[i] = Point::parse_row(line)
                .with_context(|| format!("Failed parsing row {} of tile {}", i, tile.id))?;
        }

        Ok(tile)
    }
}

impl Tile {
    pub fn edges(&self) -> TileEdges {
        // lots of unwrapping here, safe because Tile always has the right format.
        // north and south edges are easy, just use the first and last rows
        let n = self.points[0].as_ref().try_into().unwrap();
        let s = self.points[TILE_SIZE - 1].as_ref().try_into().unwrap();
        // east and west are slightly trickier, this makes a temporary vec allocation but oh well
        let e = self
            .points
            .iter()
            .map(|row| row[TILE_SIZE - 1])
            .collect::<Vec<_>>()
            .as_slice()
            .try_into()
            .unwrap();
        let w = self
            .points
            .iter()
            .map(|row| row[0])
            .collect::<Vec<_>>()
            .as_slice()
            .try_into()
            .unwrap();
        TileEdges { n, e, s, w }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    static TILE_STR: &str = "\
        Tile 1171:\n\
        .##...#...\n\
        .........#\n\
        ....##....\n\
        #.#...##.#\n\
        .....#....\n\
        .#...#...#\n\
        ###.......\n\
        .#........\n\
        #........#\n\
        #..##.##.#\n";

    static TILE_PARSED: Tile = {
        use Point::Black as B;
        use Point::White as W;
        Tile {
            id: 1171,
            points: [
                [B, W, W, B, B, B, W, B, B, B],
                [B, B, B, B, B, B, B, B, B, W],
                [B, B, B, B, W, W, B, B, B, B],
                [W, B, W, B, B, B, W, W, B, W],
                [B, B, B, B, B, W, B, B, B, B],
                [B, W, B, B, B, W, B, B, B, W],
                [W, W, W, B, B, B, B, B, B, B],
                [B, W, B, B, B, B, B, B, B, B],
                [W, B, B, B, B, B, B, B, B, W],
                [W, B, B, W, W, B, W, W, B, W],
            ],
        }
    };

    #[test]
    fn tile_parsing() {
        let tile = match Tile::from_str(TILE_STR) {
            Ok(tile) => tile,
            Err(err) => panic!("failed parsing tile: {}", err),
        };
        assert_eq!(tile, TILE_PARSED);

        let edges = tile.edges();
        assert_eq!(edges.n.to_string().as_str(), ".##...#...");
        assert_eq!(edges.e.to_string().as_str(), ".#.#.#..##");
        assert_eq!(edges.s.to_string().as_str(), "#..##.##.#");
        assert_eq!(edges.w.to_string().as_str(), "...#..#.##");
        assert_eq!(edges.n.0, 0b0110001000);
        assert_eq!(edges.e.0, 0b0101010011);
        assert_eq!(edges.s.0, 0b1001101101);
        assert_eq!(edges.w.0, 0b0001001011);
    }

    #[test]
    fn edge_flip() {
        let edges = TILE_PARSED.edges();
        assert_eq!(edges.n.flip().to_string().as_str(), "...#...##.");
        assert_eq!(edges.e.flip().to_string().as_str(), "##..#.#.#.");
        assert_eq!(edges.s.flip().to_string().as_str(), "#.##.##..#");
        assert_eq!(edges.w.flip().to_string().as_str(), "##.#..#...");
    }

    #[test]
    fn reorient() {
        static ORIENTATIONS: [Orientation; 8] = [
            Orientation::North,
            Orientation::East,
            Orientation::South,
            Orientation::West,
            Orientation::FlipNorth,
            Orientation::FlipEast,
            Orientation::FlipSouth,
            Orientation::FlipWest,
        ];

        // array of edges (as strings) as returned by TileEdges::orient
        static REORIENTED_STR: [[&'static str; 4]; 8] = [
            // North - same as original
            [".##...#...", ".#.#.#..##", "#..##.##.#", "...#..#.##"],
            // East - 90 CW
            ["##.#..#...", ".##...#...", "##..#.#.#.", "#..##.##.#"],
            // South - 180
            ["#.##.##..#", "##.#..#...", "...#...##.", "##..#.#.#."],
            // West - 90 CCW
            [".#.#.#..##", "#.##.##..#", "...#..#.##", "...#...##."],
            // FlipNorth - horizontal flip across vertical axis
            ["...#...##.", "...#..#.##", "#.##.##..#", ".#.#.#..##"],
            // FlipEast - horizontal flip then 90 CW
            ["##..#.#.#.", "...#...##.", "##.#..#...", "#.##.##..#"],
            // FlipSouth - vertical flip across horizontal axis
            ["#..##.##.#", "##..#.#.#.", ".##...#...", "##.#..#..."],
            // FlipWest - vertical flip then 90 CW (or horiz flip then 90CCW)
            ["...#..#.##", "#..##.##.#", ".#.#.#..##", ".##...#..."],
        ];

        let edges = TILE_PARSED.edges();
        for i in 0..8 {
            let oe = edges.orient(ORIENTATIONS[i]);
            let n = REORIENTED_STR[i][0].parse().unwrap();
            let e = REORIENTED_STR[i][1].parse().unwrap();
            let s = REORIENTED_STR[i][2].parse().unwrap();
            let w = REORIENTED_STR[i][3].parse().unwrap();
            assert_eq!(oe.n, n);
            assert_eq!(oe.e, e);
            assert_eq!(oe.s, s);
            assert_eq!(oe.w, w);
        }
    }
}
