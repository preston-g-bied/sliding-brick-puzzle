from GameState import GameState
from collections import deque
import time

def bfs(state: GameState):
    # keep track of execution time
    start_time = time.time()

    # normalize initial state
    normalized_state = state.normalize()

    # frontier is a FIFO queue with initial state
    # stores a tuple with the state and the list of moves needed to reach it
    frontier = deque()
    frontier.append((state, []))

    # create set of reached states and add initial state
    reached = set()
    reached.add(normalized_state)

    # return if at the goal state
    if normalized_state.is_solved():
        end_time = time.time()
        duration = end_time - start_time
        normalized_state.print()
        print(f"Total search time: {int(duration*1000)}ms")
        print("Total nodes visited: 1")
        print("Total solution length: 1")
        return normalized_state

    # loop while frontier is not empty
    while not len(frontier) == 0:
        # pop state from frontier and get all possible moves (expand)
        state, previous_moves = frontier.popleft()
        possible_moves = state.get_all_moves()
        # loop through possible moves
        for move in possible_moves:
            # get state of possible move
            move_state = state.apply_move_clone(move)
            normalized_move_state = move_state.normalize()
            if normalized_move_state not in reached:
                # check if state is goal
                if normalized_move_state.is_solved():
                    end_time = time.time()
                    duration = end_time - start_time
                    # print all moves needed to get to goal, and keep track of length
                    for m in previous_moves:
                        print(m)
                    print(move)
                    move_state.print()
                    print(f"Total search time: {int(duration*1000)}ms")
                    print(f"Total nodes visited: {len(reached)+1}")
                    print(f"Total solution length: {len(previous_moves)+1}")
                    return move_state
                 # if not reached state, add to reached and frontier
                reached.add(normalized_move_state)
                frontier.append((move_state, previous_moves + [move]))