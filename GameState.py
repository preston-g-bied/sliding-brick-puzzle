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

        self.create_shapes()

    def print(self):
        print(f'{self.cols}, {self.rows},')

        # loop through rows and print each string
        # aligns for negative numbers
        for r in range(self.rows):
            row = self.grid[r]
            row_string = ''
            for item in row:
                if item < 0:
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
    
    def extract_shape_dictionary(self):
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
    
    def create_shapes(self):
        # from the shape dictionary, a Shape object is created for each dictionary item
        shape_coords = self.extract_shape_dictionary()
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