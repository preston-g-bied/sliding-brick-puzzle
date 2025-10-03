import utils

class Shape:
    def __init__(self, id, coords):
        # the shape class keeps track of the dimensions, id number, max/min coordinate values, and a list of all coordinate values
        self.coordinates = coords
        self.id = id
        self.update_min_max()
        x = self.max_x - self.min_x
        y = self.max_y - self.min_y
        self.dimensions = (x+1, y+1)

    def update_min_max(self):
        xs = []
        ys = []
        for coord in self.coordinates:
            xs.append(coord[0])
            ys.append(coord[1])
        self.min_x = min(xs)
        self.min_y = min(ys)
        self.max_x = max(xs)
        self.max_y = max(ys)

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
    
    def get_all_moves(self, grid):
        # the below code uses the check functions (from utils) to get all possible moves of a shape
        # it returns a list of moves of the form (shape id, move)
        moves = []
        if utils.check_up(self, grid):
            moves.append((self.id, utils.Direction.UP.value))
        if utils.check_down(self, grid):
            moves.append((self.id, utils.Direction.DOWN.value))
        if utils.check_left(self, grid):
            moves.append((self.id, utils.Direction.LEFT.value))
        if utils.check_right(self, grid):
            moves.append((self.id, utils.Direction.RIGHT.value))
        return moves
    
    def make_move(self, move):
        # adjust the x or y value of all coordinates depending on the move direction
        if move == utils.Direction.UP:
            for coord in self.coordinates:
                coord[0] -= 1
        if move == utils.Direction.DOWN:
            for coord in self.coordinates:
                coord[0] += 1
        if move == utils.Direction.LEFT:
            for coord in self.coordinates:
                coord[1] -= 1
        if move == utils.Direction.RIGHT:
            for coord in self.coordinates:
                coord[1] += 1
        self.update_min_max()