import unittest
import random

# Import functions from your project file
from Picross import generate_random_grid, generate_clues

class TestPicross(unittest.TestCase):

    # -----------------------------
    # RANDOM GRID GENERATION TESTS
    # -----------------------------
    def test_random_grid_size(self):
        for size in [1, 5, 10, 15]:
            grid = generate_random_grid(size)
            self.assertEqual(len(grid), size)
            self.assertTrue(all(len(row) == size for row in grid))

    def test_random_grid_values(self):
        grid = generate_random_grid(10)
        for row in grid:
            for cell in row:
                self.assertIn(cell, [0, 1])

    # -----------------------------
    # CLUE GENERATION TESTS
    # -----------------------------
    def test_clues_empty_grid(self):
        grid = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]
        row_clues, col_clues = generate_clues(grid)
        self.assertEqual(row_clues, [[0], [0], [0]])
        self.assertEqual(col_clues, [[0], [0], [0]])

    def test_clues_full_grid(self):
        grid = [
            [1, 1],
            [1, 1]
        ]
        row_clues, col_clues = generate_clues(grid)
        self.assertEqual(row_clues, [[2], [2]])
        self.assertEqual(col_clues, [[2], [2]])

    def test_clues_mixed_grid(self):
        grid = [
            [1, 0, 1, 1],
            [0, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 1, 0, 1]
        ]
        row_clues, col_clues = generate_clues(grid)

        self.assertEqual(row_clues, [
            [1, 2],
            [1],
            [3],
            [1, 1]
        ])

        self.assertEqual(col_clues, [
            [1, 1],
            [2],
            [3],
            [1, 1]
        ])

    # -----------------------------
    # STRESS TESTS
    # -----------------------------
    def test_large_grid_clues(self):
        size = 30
        grid = generate_random_grid(size)
        row_clues, col_clues = generate_clues(grid)

        self.assertEqual(len(row_clues), size)
        self.assertEqual(len(col_clues), size)

    # -----------------------------
    # RANDOMIZED CONSISTENCY TEST
    # -----------------------------
    def test_clue_consistency(self):
        """Ensure clues match the grid definition for many random grids."""
        for _ in range(50):
            size = random.randint(3, 12)
            grid = generate_random_grid(size)
            row_clues, col_clues = generate_clues(grid)

            # Validate row clues manually
            for i, row in enumerate(grid):
                expected = []
                count = 0
                for cell in row:
                    if cell == 1:
                        count += 1
                    else:
                        if count:
                            expected.append(count)
                            count = 0
                if count:
                    expected.append(count)
                if not expected:
                    expected = [0]
                self.assertEqual(row_clues[i], expected)

            # Validate column clues manually
            for j in range(size):
                expected = []
                count = 0
                for i in range(size):
                    if grid[i][j] == 1:
                        count += 1
                    else:
                        if count:
                            expected.append(count)
                            count = 0
                if count:
                    expected.append(count)
                if not expected:
                    expected = [0]
                self.assertEqual(col_clues[j], expected)


if __name__ == "__main__":
    unittest.main()