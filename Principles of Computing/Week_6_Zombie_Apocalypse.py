"""
Student portion of Zombie Apocalypse mini-project

Copy to codeskulptor.com and run.
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7

class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []

    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)   
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie


    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        width = self._grid_width
        height = self._grid_height
        visited = list(self._cells)
        distance_field = [[height * width for dummy_col in range(width)] \
                                          for dummy_row in range(height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        elif entity_type == ZOMBIE:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        for cell in boundary:
            visited[cell[0]][cell[1]] = FULL
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            four_neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor in four_neighbors:
                if visited[neighbor[0]][neighbor[1]] == EMPTY:
                    distance_field[neighbor[0]][neighbor[1]] = distance_field[current_cell[0]][current_cell[1]] + 1
                    visited[neighbor[0]][neighbor[1]] = FULL
                    boundary.enqueue(neighbor)
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        max_neighbors = []
        #print self._human_list
        for index in range(len(self._human_list)):
            human = self._human_list[index]
            eight_neighbors = self.eight_neighbors(human[0], human[1])
            filtered_neighbors = [neighbor for neighbor in eight_neighbors \
                                  if self.is_empty(neighbor[0], neighbor[1])]
            distances = [zombie_distance_field[neighbor[0]][neighbor[1]] for neighbor in filtered_neighbors]
            #print distances
            max_neighbors = [neighbor for neighbor in filtered_neighbors \
                             if zombie_distance_field[neighbor[0]][neighbor[1]] == max(distances)]
            #print max_neighbors
            to_move = random.choice(max_neighbors)
            if zombie_distance_field[human[0]][human[1]] <= zombie_distance_field[to_move[0]][to_move[1]]:
                self._human_list[index] = to_move
                #print to_move
            #print self._human_list
            
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        min_neighbors = []
        #print self._zombie_list
        for index in range(len(self._zombie_list)):
            zombie = self._zombie_list[index]
            four_neighbors = self.four_neighbors(zombie[0], zombie[1])
            filtered_neighbors = [neighbor for neighbor in four_neighbors \
                                  if self.is_empty(neighbor[0], neighbor[1])]
            if len(filtered_neighbors) != 0:
                distances = [human_distance_field[neighbor[0]][neighbor[1]] for neighbor in filtered_neighbors]
                min_neighbors = [neighbor for neighbor in filtered_neighbors \
                                 if human_distance_field[neighbor[0]][neighbor[1]] == min(distances)]
                #print self._zombie_list[index]
                to_move = random.choice(min_neighbors)
                if human_distance_field[zombie[0]][zombie[1]] >= human_distance_field[to_move[0]][to_move[1]]:
                    self._zombie_list[index] = to_move
        #print self._zombie_list[index]
        #print self._zombie_list
    
#a = Apocalypse(5, 5)
#a.add_human(1, 2)
#a.add_zombie(1, 1)
#a.add_zombie(1, 4)
#field = a.compute_distance_field(HUMAN)
#for row in field:
#    print row
#a.move_zombies(field)
#a.move_zombies(field)
#obj = Apocalypse(20, 30, [(4, 15), (5, 15), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 15), (14, 15), (15, 15), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10)], [(12, 12), (7, 12)], [(18, 14), (18, 20), (14, 24), (7, 24), (2, 22)])
#dist = [[19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 4, 5, 600, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24], [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 600, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 1, 2, 600, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 2, 3, 600, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30], [14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 3, 4, 600, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 600, 600, 600, 600, 600, 600, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27], [17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28], [18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29], [19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]]
#for i in dist:
#    print i
#obj.move_humans(dist)
#for i in obj.humans():
#    print i
#obj = Apocalypse(3, 3, [(0, 1), (1, 2), (2, 1)], [(0, 2)], [(1, 1)])
#for human in obj.humans():
#    print human

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

#poc_zombie_gui.run_gui(Apocalypse(30, 40))
