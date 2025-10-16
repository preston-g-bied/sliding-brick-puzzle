import copy
import Shape
import utils
import random

class GameState:
    def __init__(self, filepath=None):
        # init creates a 2D matrix grid, saves the dimensions, and creates the shapes
        # allow option for empty filepath for copying
        if filepath:
            # read file to extract dimensions and game grid
            try:
                with open(filepath, 'r') as file:
                    # read dimensions from first line
                    dimensions = file.readline().split(',')
                    self.cols = int(dimensions[0])
                    self.rows = int(dimensions[1])
                    # store game grid as a 2D array of integers
                    self.grid = []
                    for _ in range(self.rows):
                        row = file.readline().split(',')
                        row = list(map(int, row[:-1]))
                        self.grid.append(row)
            except FileNotFoundError:
                print(f"Error: The file '{filepath}' was not found.")
        else:
            self.cols = 0
            self.rows = 0
            self.grid = []

        # store base grid
        self.base_grid = copy.deepcopy(self.grid)
        # set all shape positions to 0 in base grid
        for x in range(self.rows):
            for y in range(self.cols):
                if self.base_grid[x][y] > 1:
                    self.base_grid[x][y] = 0

        # create empty shapes dict
        self.shapes = {}

    # the following functions allow GameState to be hashable, so it can be added to a set
    def __eq__(self, other):
        return self.compare(other)
    
    def __hash__(self):
        # a tuple of tuples is immutable, so it can be hashed
        return hash(tuple(map(tuple, self.grid)))

    def print(self):
        print(f'{self.cols}, {self.rows},')

        # loop through rows and print each string
        # aligns for negative numbers and 2-digit numbers
        for r in range(self.rows):
            row = self.grid[r]
            row_string = ''
            for item in row:
                if item < 0 or item > 9:
                    row_string += f' {item},'
                else:
                    row_string += f'  {item},'
            print(row_string)

    def clone(self):
        new_gamestate = GameState()

        # copy the rows and columns and deepcopy the grid
        new_gamestate.cols = self.cols
        new_gamestate.rows = self.rows
        new_gamestate.grid = copy.deepcopy(self.grid)
        new_gamestate.base_grid = copy.deepcopy(self.base_grid)

        return new_gamestate
    
    def is_solved(self):
        # loop over grid and check for -1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.base_grid[row][col] == -1 and self.grid[row][col] != 2:
                    return False
        return True
    
    def _extract_shape_dictionary(self):
        # loops through grid and adds coordinate of each shape to a dictionary
        # the dictionary contains a list of coordinates for each shape
        shape_coords = {}
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] > 1:
                    if self.grid[row][col] not in shape_coords:
                        shape_coords[self.grid[row][col]] = [[row, col]]
                    else:
                        shape_coords[self.grid[row][col]].append([row, col])
        return shape_coords
    
    def _create_shapes(self):
        # from the shape dictionary, a Shape object is created for each dictionary item
        shape_coords = self._extract_shape_dictionary()
        self.shapes = {}
        for id, coords in shape_coords.items():
            new_shape = Shape.Shape(id, coords)
            self.shapes[id] = new_shape

    def get_all_moves(self):
        # create shapes
        if not self.shapes:
            self._create_shapes()
        # get moves is called for each shape, and all moves are appended to a list
        all_moves = []
        # check for master brick first
        if 2 in self.shapes:
            moves = self.shapes[2].get_all_moves(self.grid)
            all_moves += moves
        for shape_id in sorted(self.shapes.keys()):
            if shape_id != 2:
                shape = self.shapes[shape_id]
                moves = shape.get_all_moves(self.grid)
                all_moves += moves
        return all_moves
    
    def print_all_moves(self, all_moves):
        for move in all_moves:
            print(move)

    def apply_move(self, shape_move):
        # create shapes
        if not self.shapes:
            self._create_shapes()
        
        shape_id, move = shape_move
        shape = self.shapes[shape_id]
        
        # clear shape from the grid
        for x, y in shape.coordinates:
            self.grid[x][y] = self.base_grid[x][y]

        # update shape coordinates
        shape.make_move(move)

        # place shape in new position on the grid
        for x, y in shape.coordinates:
            self.grid[x][y] = shape.id

    def apply_move_clone(self, shape_move):
        # creates a new state with the applied move
        new_state = self.clone()
        new_state.apply_move(shape_move)
        return new_state
    
    def compare(self, state2):
        # compares current state with another state
        # if dimensions are unequal, states are unequal
        if self.cols != state2.cols or self.rows != state2.rows:
            return False
        # iterate over grid to make sure each square is equal
        state1_grid = self.grid
        state2_grid = state2.grid
        for x in range(self.rows):
            for y in range(self.cols):
                if state1_grid[x][y] != state2_grid[x][y]:
                    return False
        return True
    
    def normalize(self):
        """Return normalized grid - fixes collision bug"""
        norm = GameState()
        norm.cols = self.cols
        norm.rows = self.rows
        norm.base_grid = copy.deepcopy(self.base_grid)
        
        # Find all unique shape IDs > 2 in row-major order
        shape_ids = []
        seen = set()
        for x in range(norm.rows):
            for y in range(norm.cols):
                sid = self.grid[x][y]
                if sid > 2 and sid not in seen:
                    shape_ids.append(sid)
                    seen.add(sid)
        
        # Create mapping to sequential IDs starting from 3
        id_map = {old_id: i + 3 for i, old_id in enumerate(shape_ids)}
        
        # Create NEW grid with mapped IDs (avoids collisions)
        norm.grid = []
        for x in range(norm.rows):
            new_row = []
            for y in range(norm.cols):
                old_val = self.grid[x][y]
                new_val = id_map.get(old_val, old_val)  # Map if shape, else keep same (walls/empty/goal)
                new_row.append(new_val)
            norm.grid.append(new_row)
        
        return norm
    
    def _rename_shape(self, old_id, new_id):
        # jelper function to rename a shape's ID throughout the grid
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] == old_id:
                    self.grid[x][y] = new_id

def random_walk(state, N):
    # print initial state
    state.print()
    print('\n')
    # set variables for loop
    at_goal = False
    moves = 0
    # loop until goal is reached or moves exceeds N
    while not at_goal and moves < N:
        # get all possible moves and choose a random one
        possible_moves = state.get_all_moves()
        next_move = random.choice(possible_moves)
        # apply the move and normalize the state
        state = state.apply_move_clone(next_move)
        state = state.normalize()
        # print the move
        print(next_move)
        state.print()
        print('\n')
        # check if solved and increment moves
        if state.is_solved():
            at_goal = True
        moves = moves + 1