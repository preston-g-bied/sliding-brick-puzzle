import utils

class Shape:
    def __init__(self, id, coords):
        # the shape class keeps track of the dimensions, id number, max/min coordinate values, and a list of all coordinate values
        xs = []
        ys = []
        for coord in coords:
            xs.append(coord[0])
            ys.append(coord[1])
        x = max(xs) - min(xs)
        y = max(ys) - min(ys)
        self.min_x = min(xs)
        self.min_y = min(ys)
        self.max_x = max(xs)
        self.max_y = max(ys)
        self.dimensions = (x+1, y+1)
        self.coordinates = coords
        self.id = id

    # the below functions get the four principal faces of shapes by comparing to max/min coordinate values

    def get_top_face(self):
        top_coords = []
        for coord in self.coordinates:
            if coord[0] == self.min_x:
                top_coords.append(coord)
        return top_coords
    
    def get_bottom_face(self):
        bottom_coords = []
        for coord in self.coordinates:
            if coord[0] == self.max_x:
                bottom_coords.append(coord)
        return bottom_coords
    
    def get_left_face(self):
        left_coords = []
        for coord in self.coordinates:
            if coord[1] == self.min_y:
                left_coords.append(coord)
        return left_coords
    
    def get_right_face(self):
        right_coords = []
        for coord in self.coordinates:
            if coord[1] == self.max_y:
                right_coords.append(coord)
        return right_coords
    
    # the below code uses the check functions (from utils) to get all possible moves of a shape
    # it returns a list of moves of the form (shape id, move)
    def get_all_moves(self, grid):
        moves = []
        if utils.check_up(self, grid):
            moves.append((self.id, "up"))
        if utils.check_down(self, grid):
            moves.append((self.id, "down"))
        if utils.check_left(self, grid):
            moves.append((self.id, "left"))
        if utils.check_right(self, grid):
            moves.append((self.id, "right"))
        return moves