"""
Student facing code for Tantrix Solitaire
http://www.jaapsch.net/puzzles/tantrix.htm

Game is played on a grid of hexagonal tiles.
All ten tiles for Tantrix Solitaire and place in a corner of the grid.
Click on a tile to rotate it.  Cick and drag to move a tile.

Goal is to position the 10 provided tiles to form
a yellow, red or  blue loop of length 10

Copy to codeskulptor.com and run.
"""

# Core modeling idea - a triangular grid of hexagonal tiles are 
# model by integer tuples of the form (i, j, k) 
# where i + j + k == size and i, j, k >= 0.

# Each hexagon has a neighbor in one of six directions
# These directions are modeled by the differences between the 
# tuples of these adjacent tiles

# Numbered directions for hexagonal grid, ordered clockwise at 60 degree intervals
DIRECTIONS = {0 : (-1, 0, 1), 1 : (-1, 1, 0), 2 : (0, 1, -1), 
              3 : (1, 0, -1), 4 : (1, -1, 0), 5 : (0,  -1, 1)}

def reverse_direction(direction):
    """
    Helper function that returns opposite direction on hexagonal grid
    """
    num_directions = len(DIRECTIONS)
    return (direction + num_directions / 2) % num_directions



# Color codes for ten tiles in Tantrix Solitaire
# "B" denotes "Blue", "R" denotes "Red", "Y" denotes "Yellow"
SOLITAIRE_CODES = ["BBRRYY", "BBRYYR", "BBYRRY", "BRYBYR", "RBYRYB",
                "YBRYRB", "BBRYRY", "BBYRYR", "YYBRBR", "YYRBRB"]


# Minimal size of grid to allow placement of 10 tiles
MINIMAL_GRID_SIZE = 4



class Tantrix:
    """
    Basic Tantrix game class
    """
    
    def __init__(self, size):
        """
        Create a triangular grid of hexagons with size + 1 tiles on each side.
        """
        assert size >= MINIMAL_GRID_SIZE
        self._tiling_size = size
        # Initialize dictionary tile_value to contain codes for ten
        # tiles in Solitaire Tantrix in one 4x4 corner of grid
        self._tile_value = {}
        value_index = 0
        for i_index in range(MINIMAL_GRID_SIZE):
            for j_index in range(MINIMAL_GRID_SIZE):
                for k_index in range(size - 3, size + 1):
                    if i_index + j_index + k_index == 6:
                        self._tile_value[(i_index, j_index, k_index)] = SOLITAIRE_CODES[value_index]
                        value_index += 1

    def __str__(self):
        """
        Return string of dictionary of tile positions and values
        """
        return str(self._tile_value)
        
    def get_tiling_size(self):
        """
        Return size of board for GUI
        """
        return self._tiling_size
    
    def tile_exists(self, index):
        """
        Return whether a tile with given index exists
        """
        if index in self._tile_value:
            return True
        return False
    
    def place_tile(self, index, code):
        """
        Play a tile with code at cell with given index
        """
        self._tile_value[index] = code       

    def remove_tile(self, index):
        """
        Remove a tile at cell with given index
        and return the code value for that tile        """
        return self._tile_value.pop(index)
               
    def rotate_tile(self, index):
        """
        Rotate a tile clockwise at cell with given index
        """
        self._tile_value[index] = self._tile_value[index][1:] + self._tile_value[index][0]

    def get_code(self, index):
        """
        Return the code of the tile at cell with given index
        """
        return self._tile_value[index]

    def get_neighbor(self, index, direction):
        """
        Return the index of the tile neighboring the tile with given index in given direction
        """
        index = list(index)
        for times in range(3):
            index[times] += DIRECTIONS[direction][times]
        return tuple(index)

    def is_legal(self):
        """
        Check whether a tile configuration obeys color matching rules for adjacent tiles
        """
        for tile in self._tile_value:
            for direction in DIRECTIONS:
                neighbor = self.get_neighbor(tile, direction)
                if neighbor in self._tile_value:
                    tile_code = self.get_code(tile)
                    neighbor_code = self.get_code(neighbor)
                    if tile_code[direction] != neighbor_code[reverse_direction(direction)]:
                        return False
        return True
                
    def has_loop(self, color):
        """
        Check whether a tile configuration has a loop of size 10 of given color
        """
        if self.is_legal() == False:
            return False
        connected_tile = 0
        for tile in self._tile_value:
            code = self.get_code(tile)
            direction1 = code.find(color)
            direction2 = code.rfind(color)
            neighbor1 = self.get_neighbor(tile, direction1)
            if neighbor1 not in self._tile_value:
                return False
            neighbor1_code = self.get_code(neighbor1)
            neighbor2 = self.get_neighbor(tile, direction2)
            if neighbor2 not in self._tile_value:
                return False
            neighbor2_code = self.get_code(neighbor2)
            if code[direction1] == neighbor1_code[reverse_direction(direction1)]:
                if code[direction2] == neighbor2_code[reverse_direction(direction2)]:
                    connected_tile += 1
        if connected_tile == len(SOLITAIRE_CODES):
            return True
        return False
    
# run GUI for Tantrix
import poc_tantrix_gui
poc_tantrix_gui.TantrixGUI(Tantrix(6))