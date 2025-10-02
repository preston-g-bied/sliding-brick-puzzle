import copy

class GameState:
    def __init__(self, filepath=None):
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