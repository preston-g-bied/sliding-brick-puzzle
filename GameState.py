class GameState:
    def __init__(self, filepath):
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

    def print(self):
        print(f'{self.cols}, {self.rows},')
        for r in range(self.rows):
            row = self.grid[r]
            row_string = ''
            for item in row:
                if item < 0:
                    row_string += f' {item},'
                else:
                    row_string += f'  {item},'
            print(row_string)