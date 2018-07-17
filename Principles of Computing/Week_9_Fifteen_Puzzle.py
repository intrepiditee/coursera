"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Copy to codeskulptor.com and run.
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid = None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction
            for row in self._grid:
                print row
            print
            
    ##################################################################
    # Phase one methods
    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(target_row, target_col) != 0:
            print 'Error 1: Current number is not 0'
            return False
        current = 0
        for row in range(target_row + 1, self.get_height()):
            if target_col == self.get_width() - 1:
                current = self._grid[row][0]
            else:
                current = self._grid[row - 1][-1] + 1
            column = self._grid[row]
            for grid in column:
                if grid != current:
                    print 'Error 2'
                    return False
                current += 1
        if target_col != self.get_width() - 1:
            current = self._grid[target_row][target_col + 1]
            for grid in self._grid[target_row][target_col + 1:]:
                if  grid != current:
                    print 'Error 3'
                    return False
                current += 1
        return True
    
    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        # replace with your code
        string = ''
        target = self.current_position(target_row, target_col)
        row_difference = target_row - target[0]
        #print 'Row difference', row_difference
        col_difference = target_col - target[1]
        #print 'Col difference', col_difference
        string += 'u' * row_difference
        if col_difference > 0:
            string += 'l' * col_difference
            if row_difference == 0 and col_difference > 1:
                string += 'urrdl' * (col_difference - 1)
            if row_difference == 1:
                string += 'urrdl' * (col_difference - 1)
                string += 'dru'
            if row_difference > 1:
                string += 'drrul' * (col_difference - 1)
                string += 'dru'
        elif col_difference < 0:
            col_difference = abs(col_difference)
            string += 'r' * col_difference
            if row_difference == 1:
                string += 'ulldr' * (col_difference - 1)
                string += 'ullddru'
            if row_difference > 1:
                string += 'dllur' * (col_difference - 1)
                string += 'dlu'
        string += 'lddru' * (row_difference - 1)
        if row_difference > 0:
            string += 'ld'
        print 'Interior Path', string
        self.update_puzzle(string)
        assert self.lower_row_invariant(target_row, target_col - 1), 'False string'
        return string

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        # replace with your code
        string = ''
        target = self.current_position(target_row, 0)
        row_difference = target_row - target[0]
        col_difference = target[1]
        string += 'u' * row_difference
        if col_difference > 0:
            string += 'r' * (col_difference - 1)
            if row_difference > 1:
                string += 'druld' * (row_difference - 1)
            string += 'rulld' * (col_difference - 1)
            string += 'ruldrdlurdluurddlu'
        elif col_difference == 0:
            string += 'rddlu' * (row_difference - 2)
            if row_difference > 1:
                string += 'rd'
                string += 'l'
                string += 'ruldrdlurdluurddlu'
        string += 'r' * (self._width - 1)
        print 'Col 0 Path', string
        self.update_puzzle(string)
        assert self.lower_row_invariant(target_row - 1, self._width -1), 'False string'
        return string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.get_number(0, target_col) != 0:
            return False
        current = 0
        for row in range(2, self.get_height()):
            if target_col == self.get_width() - 1:
                current = self._grid[row][0]
            else:
                current = self._grid[row - 1][-1] + 1
            column = self._grid[row]
            for grid in column:
                if grid != current:
                    print 'Error 4'
                    return False
                current += 1
        current = self._grid[1][target_col]
        for grid in self._grid[1][target_col:]:
            if  grid != current:
                print 'Error 5'
                return False
            current += 1
        return True

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        # replace with your code
        if self.lower_row_invariant(1, target_col):
            return True
        return False

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        string = ''
        assert self.row0_invariant(target_col), 'False precondition'
        target = self.current_position(0, target_col)
        row_difference = target[0]
        col_difference = target_col - target[1]
        if row_difference == 0:
            if col_difference == 1:
                string += 'ld'
            elif col_difference > 1:
                string += 'l' * col_difference
                string += 'drrul' * (col_difference - 2)
                string += 'druld'
                string += 'urdlurrdluldrruld'
        elif row_difference == 1:
            if col_difference == 1:
                string += 'lld'
                string += 'urdlurrdluldrruld'
            elif col_difference > 1:
                string += 'ld'
                string += 'l' * (col_difference - 1)
                string += 'urrdl' * (col_difference - 2)
                string += 'urdlurrdluldrruld'
        print 'Row 0 Path', string
        self.update_puzzle(string)
        assert self.row1_invariant(target_col - 1), 'False string'
        return string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        # replace with your code
        print target_col
        assert self.row1_invariant(target_col), 'False precondition'
        string = ''
        target = self.current_position(1, target_col)
        row_difference = 1 - target[0]
        col_difference = target_col - target[1]
        string += 'u' * row_difference
        if col_difference > 0:
            string += 'l' * col_difference
            if row_difference == 0:
                string += 'urrdl' * (col_difference - 1)
                string += 'ur'
            elif row_difference == 1:
                string += 'drrul' * (col_difference - 1)
                string += 'dru'
        elif col_difference < 0:
            col_difference = abs(col_difference)
            string += 'r' * col_difference
            string += 'dllur' * (col_difference - 1)
            string += 'dlu'
        print 'Row 1 Path', string
        self.update_puzzle(string)
        assert self.row0_invariant(target_col), 'False string'
        return string

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        string = ''
        num1 = self.get_number(0, 0)
        num2 = self.get_number(0, 1)
        num3 = self.get_number(1, 0)
        max_num = max([num1, num2, num3])
        min_num = min([num1, num2, num3])
        if num1 == min_num and num2 == max_num:
            string += 'ul'
        elif num1 == max_num and num3 == min_num:
            string += 'ul'
            string += 'rdlu' * 2
        elif num2 == min_num and num3 == max_num:
            string += 'ul'
            string += 'rdlu'
        print '2x2 Path', string
        self.update_puzzle(string)
        return string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        # replace with your code
        string = ''
        width = self._width
        height = self._height
        zero = self.current_position(0, 0)
        row_to_zero = height - 1 - zero[0]
        col_to_zero = width - 1 - zero[1]
        string += 'r' * col_to_zero
        string += 'd' * row_to_zero
        self.update_puzzle(string)
        if width == 2 and height == 2:
            string += self.solve_2x2()
        elif width > 2 and height == 2:
            for col in range(width - 1, 1, -1):
                string += self.solve_row1_tile(col)
                string += self.solve_row0_tile(col)
            string += self.solve_2x2()
        elif width == 2 and height > 2:
            for row in range(height - 1, 1, -1):
                for col in range(width - 1, 0, -1):
                    string += self.solve_interior_tile(row, col)
                string += self.solve_col0_tile(row)
            string += self.solve_2x2()
        elif width > 2 and height > 2:
            for row in range(height - 1, 1, -1):
                for col in range(width - 1, 0, -1):
                    string += self.solve_interior_tile(row, col)
                string += self.solve_col0_tile(row)
            #for row in range(height - 1, -1, -1):
            for col in range(width - 1, 1, -1):
                string += self.solve_row1_tile(col)
                string += self.solve_row0_tile(col)
            string += self.solve_2x2()
        return string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4,4))
#a = Puzzle(2, 2, [[1, 2], [0, 3]])
#b = Puzzle(3, 3, [[1, 3, 2], [0, 4, 5], [6, 7, 8]])
#c = Puzzle(4, 4, [[2,3,12,5],[6,9,7,8],[13,10,11,14],[1,4,0,15]])
#d = Puzzle(4, 2, [[3,5],[2,4],[1,6],[0,7]])
#e = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#print a
#a.solve_col0_tile(1)
#print a.lower_row_invariant(1, 0)
#print b
#b.solve_col0_tile(2)
#b.solve_interior_tile(2, 1)
#print b.lower_row_invariant(2, 1)
#print d
#d.solve_col0_tile(3)
#print c
#c.solve_interior_tile(3, 2)
#print d
#d.solve_interior_tile(2, 1)
#print e 