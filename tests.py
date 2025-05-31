import unittest

from resources import Maze

class Tests(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(m1._Maze__cells),
            num_cols,
        )
        self.assertEqual(
            len(m1._Maze__cells[0]),
            num_rows,
        )

    def test_maze_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertFalse(
            m1._Maze__cells[0][0].has_top_wall
        )
        self.assertFalse(
            m1._Maze__cells[11][9].has_bottom_wall
        )
    
    def test_maze_reset_visited(self):
        num_cols = 3
        num_rows = 3
        m1 = Maze(0, 0, num_rows, num_cols, 10, 10)
        m1._Maze__reset_cells_visited()
        for i in range(num_cols):
            for j in range(num_rows):
                self.assertFalse(
                    m1._Maze__cells[i][j].visited
                )

    
if __name__ == "__main__":
    unittest.main()