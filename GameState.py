import copy
import Shape
import utils

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

        self._create_shapes()

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

        return new_gamestate
    
    def is_solved(self):
        # loop over grid and check for -1
        for row in range(self.rows):
            for col in range(self.cols):
                if self.grid[row][col] == -1:
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
        # get moves is called for each shape, and all moves are appended to a list
        all_moves = []
        for shape in self.shapes.values():
            moves = shape.get_all_moves(self.grid)
            all_moves += moves
        return all_moves
    
    def print_all_moves(self, all_moves):
        for move in all_moves:
            print(move)

    def apply_move(self, shape_move):
        shape_id, move = shape_move
        shape = self.shapes[shape_id]
        
        # clear shape from the grid
        for x, y in shape.coordinates:
            self.grid[x][y] = 0

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
        norm = self.clone()
        next_idx = 3
        for x in range(norm.rows):
            for y in range(norm.cols):
                if norm.grid[x][y] == next_idx:
                    next_idx += 1
                elif norm.grid[x][y] > next_idx:
                    norm._swap_idx(next_idx, norm.grid[x][y])
                    next_idx += 1
        return norm
    
    def _swap_idx(self, idx1, idx2):
        for x in range(self.rows):
            for y in range(self.cols):
                if self.grid[x][y] == idx1:
                    self.grid[x][y] = idx2
                elif self.grid[x][y] == idx2:
                    self.grid[x][y] = idx1