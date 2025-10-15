from GameState import GameState
from collections import deque
import time

def bfs(state: GameState):
    # keep track of execution time
    start_time = time.time()

    # normalize initial state
    state = state.normalize()

    # frontier is a FIFO queue with initial state
    # stores a tuple with the state and the list of moves needed to reach it
    frontier = deque()
    frontier.append((state, []))

    frontier_set = set()
    frontier_set.add(state)

    # create set of reached states and add initial state
    reached = set()

    # return if at the goal state
    if state.is_solved():
        end_time = time.time()
        duration = end_time - start_time
        state.print()
        print(f"Total search time: {int(duration*1000)}ms")
        print("Total nodes visited: 1")
        print("Total solution length: 1")
        return

    # loop while frontier is not empty
    while frontier:
        # pop state from frontier and get all possible moves (expand)
        state, previous_moves = frontier.popleft()
        # check if popped state is goal
        if state.is_solved():
            end_time = time.time()
            duration = end_time - start_time
            # print all moves needed to get to goal, and keep track of length
            for m in previous_moves:
                print(m)
            state.print()
            print(f"Total search time: {int(duration*1000)}ms")
            print(f"Total nodes visited: {len(reached)}")
            print(f"Total solution length: {len(previous_moves)}")
            return
        # add popped state to reached
        reached.add(state)
        # loop through possible moves
        for move in state.get_all_moves():
            # get state of possible move
            move_state = state.apply_move_clone(move).normalize()
            if move_state not in reached and move_state not in frontier_set:
                # if not reached state, add to reached and frontier
                frontier.append((move_state, previous_moves + [move]))
                frontier_set.add(move_state)

def dfs(state: GameState):
    # keep track of execution time
    start_time = time.time()

    # normalize initial state
    state = state.normalize()

    # frontier is a LIFO stack with initial state
    # stores a tuple with the state and the list of moves needed to reach it
    frontier = deque()
    frontier.append((state, []))

    frontier_set = set()
    frontier_set.add(state)

    # create set of reached states and add initial state
    reached = set()

    # return if at the goal state
    if state.is_solved():
        end_time = time.time()
        duration = end_time - start_time
        state.print()
        print(f"Total search time: {int(duration*1000)}ms")
        print("Total nodes visited: 1")
        print("Total solution length: 1")
        return

    # loop while frontier is not empty
    while frontier:
        # pop state from frontier and get all possible moves (expand)
        state, previous_moves = frontier.pop()
        # check if popped state is goal
        if state.is_solved():
            end_time = time.time()
            duration = end_time - start_time
            # print all moves needed to get to goal, and keep track of length
            for m in previous_moves:
                print(m)
            state.print()
            print(f"Total search time: {int(duration*1000)}ms")
            print(f"Total nodes visited: {len(reached)}")
            print(f"Total solution length: {len(previous_moves)}")
            return
        # add popped state to reached
        reached.add(state)
        # loop through possible moves
        for move in state.get_all_moves():
            # get state of possible move
            move_state = state.apply_move_clone(move).normalize()
            if move_state not in reached and move_state not in frontier_set:
                # if not reached state, add to reached and frontier
                frontier.append((move_state, previous_moves + [move]))
                frontier_set.add(move_state)