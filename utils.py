from enum import Enum

class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

# the below code checks up/down/left/right
# it checks to make sure that the spaces above the top/bottom/left/right face of a shape are the values 0 or -1

def check_up(shape, grid):
    top_face = shape.get_top_face()
    for coord in top_face:
        x, y = coord
        if x - 1 < 0:
            return False
        if grid[x-1][y] > 0:
            return False
    return True

def check_down(shape, grid):
    bottom_face = shape.get_bottom_face()
    for coord in bottom_face:
        x, y, = coord
        if x + 1 >= len(grid):
            return False
        if grid[x+1][y] > 0:
            return False
    return True

def check_left(shape, grid):
    left_face = shape.get_left_face()
    for coord in left_face:
        x, y = coord
        if y - 1 < 0:
            return False
        if grid[x][y-1] > 0:
            return False
    return True

def check_right(shape, grid):
    right_face = shape.get_right_face()
    for coord in right_face:
        x, y = coord
        if y + 1 >= len(grid):
            return False
        if grid[x][y+1] > 0:
            return False
    return True