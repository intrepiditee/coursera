"""
Clone of 2048 game.

Copy to codeskulptor.com and run.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    non_zero_line = []
    result = []
    is_appended = False
    # imitate slide without merging
    for number in line:
        if number != 0:
            non_zero_line.append(number)
    # merging
    for element in range(len(non_zero_line)):
        if is_appended:
            is_appended = False
        else:
            if element == len(non_zero_line) - 1:
                result.append(non_zero_line[element])
            else:
                if non_zero_line[element] == non_zero_line[element + 1]:
                    result.append(non_zero_line[element] + non_zero_line[element + 1])
                    is_appended = True
                else:
                    result.append(non_zero_line[element])
                    is_appended = False
    result.extend([0] * (len(line) - len(result)))
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        self._initial_cells = {UP:  [(row, column) for row in range(self._grid_height) \
                              for column in range(self._grid_width) if row == 0],
                        DOWN: [(row, column) for row in range(self._grid_height) \
                              for column in range(self._grid_width) if row == self._grid_height - 1],
                        RIGHT:[(row, column) for row in range(self._grid_height) \
                              for column in range(self._grid_width) if column == self._grid_width - 1],
                        LEFT: [(row, column) for row in range(self._grid_height) \
                              for column in range(self._grid_width) if column == 0]}
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        # replace with your code
        self._grid = [[0 for dummy_column in range(self._grid_width)] for dummy_row in range(self._grid_height)]
        for dummy_num in range(2):
            self.new_tile()
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        # replace with your code
        return_string = ''
        for row in range(self._grid_height):
            return_string += str(self._grid[row]) + '\n'
        return str(return_string)

    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        original_grid = []
        for row in self._grid:
            original_row = list(row)
            original_grid.append(original_row)
        steps = 0
        if direction == UP or direction == DOWN:
            steps = self._grid_height
        elif direction == LEFT or direction == RIGHT:
            steps = self._grid_width
        to_move = []
        for initial_cell in self._initial_cells[direction]:
            for step in range(steps):
                new_row = initial_cell[0] + step * OFFSETS[direction][0]
                new_column = initial_cell[1] + step * OFFSETS[direction][1]
                to_move.append(self._grid[new_row][new_column])
            to_move = merge(to_move)
            row = initial_cell[0]
            column = initial_cell[1]
            for step in range(steps):
                self._grid[row + OFFSETS[direction][0] * step][column + OFFSETS[direction][1] * step] = to_move[step]
            to_move = []
        if original_grid != self._grid:
            self.new_tile()
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        while True:
            random_row = random.randrange(self._grid_height)
            random_column = random.randrange(self._grid_width)
            if self._grid[random_row][random_column] == 0:
                self._grid[random_row][random_column] = random.choice([2] * 9 + [4])
                break

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        # replace with your code
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        # replace with your code
        return self._grid[row][col]

poc_2048_gui.run_gui(TwentyFortyEight(4, 4))