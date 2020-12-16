use std::collections::HashMap;

#[derive(Debug)]
struct MemoryGame {
    /// the 1-indexed turn that has just been completed
    turn: usize,
    /// the last number spoken
    last: usize,
    /// map of which turn each number was most recently spoken.
    /// Does NOT include the most recent turn.
    hist: HashMap<usize, usize>,
}

impl MemoryGame {
    fn new(start_numbers: &[usize]) -> Self {
        // only map the first N-1 starting numbers
        let turn = start_numbers.len() - 1;
        let hist = start_numbers[..turn]
            .iter()
            .enumerate()
            .map(|(i, &n)| (n, i + 1))
            .collect();

        // the final starting number goes into last
        Self {
            turn: turn + 1,
            last: start_numbers[turn],
            hist,
        }
    }

    fn step(&mut self) {
        let new: usize = self.hist
            .get(&self.last)
            .map(|prev_turn| self.turn - prev_turn)
            .unwrap_or(0);

        // now that we're done needing it, add the previous turn to the history
        self.hist.insert(self.last, self.turn);
        // complete this turn
        self.turn += 1;
        self.last = new;
    }
}

fn main() {
    //const TURN_COUNT: usize = 2020;
    //static STARTING_NUMBERS: &[usize] = &[0, 3, 6];
    const TURN_COUNT: usize = 30_000_000;
    static STARTING_NUMBERS: &[usize] = &[9, 6, 0, 10, 18, 2, 1];

    let mut game = MemoryGame::new(STARTING_NUMBERS);
    while game.turn < TURN_COUNT {
        //println!("turn {}: last {}", game.turn, game.last);
        game.step()
    }

    println!("last number is {}", game.last);
}
