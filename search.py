from GameState import GameState
from collections import deque

def bfs(state: GameState):
    # return if at the goal state
    if state.is_solved():
        state.print()
        return state
    
    # frontier is a FIFO queue with initial state
    frontier = deque()
    frontier.append(state)

    # create set of reached states and add initial state
    reached = set()
    reached.add(state)

    # loop while frontier is not empty
    while not len(frontier) == 0:
        # pop state from frontier and get all possible moves (expand)
        state = frontier.pop()
        possible_moves = state.get_all_moves()
        # loop through possible moves
        for move in possible_moves:
            # get state of possible move
            move_state = state.apply_move_clone(move)
            # check if state is goal
            if move_state.is_solved():
                move_state.print()
                return move_state
            # if not reached state, add to reached and frontier
            if move_state not in reached:
                reached.add(move_state)
                frontier.append(move_state)