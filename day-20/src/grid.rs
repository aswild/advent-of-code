#![allow(dead_code)] // XXX

use std::ops::{Index, IndexMut, Range};

/// A generic 2D grid with elements stored in row-major order.
pub struct Grid<T> {
    // Invariant: data.len() == rows * cols
    data: Box<[T]>,
    rows: usize,
    cols: usize,
}

impl<T> Grid<T> {
    /// Take data in row-major order to intrepret this as a Grid.
    ///
    /// Panics if data.len() != rows * cols
    pub fn from_vec(data: Vec<T>, rows: usize, cols: usize) -> Self {
        assert_eq!(
            data.len(),
            rows * cols,
            "grid dimensions don't match data length"
        );
        Self {
            data: data.into_boxed_slice(),
            rows,
            cols,
        }
    }

    /// Get a reference to an element at the given row and column. Returns None if out of bounds.
    pub fn get(&self, row: usize, col: usize) -> Option<&T> {
        // check that both rows and cols are in-bounds, to avoid out-of-bounds column numbers
        // silently wrap around to the next row.
        if row >= self.rows || col >= self.cols {
            None
        } else {
            // safety: we verified that row and col are in bounds
            Some(unsafe { self.get_unchecked(row, col) })
        }
    }

    /// Get a mutable reference to an element at the given row and column. Returns None if out of
    /// bounds.
    pub fn get_mut(&mut self, row: usize, col: usize) -> Option<&mut T> {
        if row >= self.rows || col >= self.cols {
            None
        } else {
            Some(unsafe { self.get_unchecked_mut(row, col) })
        }
    }

    /// Access the linear underlying slice. Its length is `self.rows * self.columns`
    pub fn as_slice(&self) -> &[T] {
        &*self.data
    }

    /// Access the linear underlying slice mutably.
    pub fn as_mut_slice(&mut self) -> &mut [T] {
        &mut *self.data
    }

    /// Return an iterator over the (row, column) index pairs in this grid
    pub fn iter_indices(&self) -> IterIndices {
        IterIndices {
            row: 0,
            col: 0,
            rows: self.rows,
            cols: self.cols,
        }
    }

    /// Get an entry without bounds checking. Results in undefined behavior if `row * col` exceeds
    /// `self.rows * self.cols - 1`
    #[inline]
    pub unsafe fn get_unchecked(&self, row: usize, col: usize) -> &T {
        self.data.get_unchecked(row * self.cols + col)
    }

    /// Get an entry mutably without bounds checking. Results in undefined behavior if `row * col`
    /// exceeds `self.rows * self.cols - 1`
    #[inline]
    pub unsafe fn get_unchecked_mut(&mut self, row: usize, col: usize) -> &mut T {
        self.data.get_unchecked_mut(row * self.cols + col)
    }

    /// Get a Range to slice out a row, panice if out of bounds. (used for Index(Mut))
    fn index_row_range(&self, row: usize) -> Range<usize> {
        // panic message similar to rust's built in slice out of bounds message
        assert!(
            row < self.rows,
            "index out of bounds: rows is {} but the index is {}",
            self.rows,
            row
        );
        let start = row * self.cols;
        let end = start + self.cols;
        start..end
    }
}

impl<T> Grid<T>
where
    T: Default + Clone,
{
    /// Create a new Grid with the given number of rows and columns, filled in with the type's
    /// Default value.
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            data: vec![<T as Default>::default(); rows * cols].into_boxed_slice(),
            rows,
            cols,
        }
    }
}

impl<T> Index<usize> for Grid<T> {
    type Output = [T];

    /// Indexing with usize returns a slice of the selected row. Panics if out of bounds
    fn index(&self, row: usize) -> &[T] {
        &self.data[self.index_row_range(row)]
    }
}

impl<T> Index<(usize, usize)> for Grid<T> {
    type Output = T;

    /// Indexing with a tuple is equivalent to `get()`, but panics if out of bounds
    fn index(&self, index: (usize, usize)) -> &T {
        self.get(index.0, index.1).expect("index out of bounds")
    }
}

impl<T> IndexMut<usize> for Grid<T> {
    /// Indexing with usize returns a slice of the selected row. Panics if out of bounds
    fn index_mut(&mut self, row: usize) -> &mut [T] {
        // have to split this to its own line to avoid confusing the borrow checker
        let range = self.index_row_range(row);
        &mut self.data[range]
    }
}

impl<T> IndexMut<(usize, usize)> for Grid<T> {
    /// Indexing with a tuple is equivalent to `get()`, but panics if out of bounds
    fn index_mut(&mut self, index: (usize, usize)) -> &mut T {
        self.get_mut(index.0, index.1).expect("index out of bounds")
    }
}

/// Iterator structure over `(row, col)` pairs of indices. Created with [`Grid::iter_indices`].
/// This specifically doesn't store a reference to a Grid to to make iterating over a owned/mut
/// Grid easier.
pub struct IterIndices {
    row: usize,
    col: usize,
    rows: usize,
    cols: usize,
}

impl Iterator for IterIndices {
    type Item = (usize, usize);
    fn next(&mut self) -> Option<Self::Item> {
        // row and col point to the next element to return, when row goes out of bounds, we're done
        if self.row < self.rows {
            debug_assert!(self.col < self.cols);
            let ret = (self.row, self.col);
            // move to the next column
            self.col += 1;
            // if we pass the end of a column, move to the start of the next row
            if self.col >= self.cols {
                self.col = 0;
                self.row += 1;
            }
            Some(ret)
        } else {
            None
        }
    }
}

#[cfg(test)]
mod tests {
    use super::Grid;

    #[test]
    fn test_grid() {
        let v = (1i32..=12).collect();

        let mut g = Grid::from_vec(v, 4, 3);
        assert_eq!(g[0], [1, 2, 3]);
        assert_eq!(g[3], [10, 11, 12]);
        assert_eq!(g.get(0, 0), Some(&1));
        assert_eq!(g.get(3, 1), Some(&11));
        assert_eq!(g.get(0, 5), None);
        assert_eq!(g.get(6, 1), None);

        g[0][0] = 100;
        assert_eq!(g[0][0], 100);
        assert_eq!(g.get(0, 0), Some(&100));

        let e: &mut i32 = g.get_mut(0, 1).unwrap();
        *e = 200;
        assert_eq!(g[0][1], 200);
        assert_eq!(g[(0, 0)], 100);
        assert_eq!(g[(0, 1)], 200);

        // slightly weird that we need an extra & at the callsite, but otherwise the indexing
        // operation derefs the result of index(), producing an unsized [T].
        let row_1 = &g[1];
        assert_eq!(row_1[1], 5);

        assert_eq!(g.as_slice(), [100, 200, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]);
    }

    #[test]
    #[should_panic(expected = "grid dimensions don't match data length")]
    fn from_vec_panic() {
        // panics because rows/cols don't match vec length
        let v = (1i32..=12).collect();
        let _ = Grid::from_vec(v, 5, 5);
    }

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn index_panic_1() {
        let v = (1i32..=12).collect();
        let g = Grid::from_vec(v, 4, 3);
        let _ = g[0][10];
    }

    #[test]
    #[should_panic(expected = "index out of bounds")]
    fn index_panic_2() {
        let v = (1i32..=12).collect();
        let g = Grid::from_vec(v, 4, 3);
        let _ = &g[100];
    }

    #[test]
    fn iter_indices() {
        let g = Grid::<u8>::new(2, 3);
        let mut i = g.iter_indices();
        assert_eq!(i.next(), Some((0, 0)));
        assert_eq!(i.next(), Some((0, 1)));
        assert_eq!(i.next(), Some((0, 2)));
        assert_eq!(i.next(), Some((1, 0)));
        assert_eq!(i.next(), Some((1, 1)));
        assert_eq!(i.next(), Some((1, 2)));
        assert_eq!(i.next(), None);
        assert_eq!(i.next(), None);
    }
}
