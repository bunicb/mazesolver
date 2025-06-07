import unittest
from maze import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1.cells),
            num_cols,
        )
        self.assertEqual(
            len(m1.cells[0]),
            num_rows,
        )

    def test_maze_entrance_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.break_entrance_and_exit()
        self.assertFalse(m1.cells[0][0].top_wall)
        self.assertFalse(m1.cells[num_cols - 1][num_rows - 1].bottom_wall)

    def test_maze_reset_visited(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1.reset_visited()
        for col in range(num_cols):
            for row in range(num_rows):
                self.assertFalse(m1.cells[col][row].visited)

if __name__ == "__main__":
    unittest.main()