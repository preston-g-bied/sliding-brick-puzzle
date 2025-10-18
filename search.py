from GameState import GameState
from collections import deque
import time
from queue import PriorityQueue

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

def dls(state: GameState, depth_limit):
    # keep track of execution time
    start_time = time.time()

    # normalize initial state
    state = state.normalize()

    # frontier is a LIFO stack with initial state
    # stores a tuple with the state and the list of moves needed to reach it
    frontier = deque()
    frontier.append((state, []))

    # manually track visited nodes with no reached list
    nodes_visited = 0

    # return if at the goal state
    if state.is_solved():
        return ([], 1)

    # loop while frontier is not empty
    while frontier:
        # pop state from frontier and get all possible moves (expand)
        state, previous_moves = frontier.pop()
        nodes_visited += 1
        # check if popped state is goal
        if state.is_solved():
            return (previous_moves, nodes_visited)

        # check for depth cutoff
        if len(previous_moves) < depth_limit:
            # loop through possible moves
            for move in state.get_all_moves():
                # get state of possible move
                move_state = state.apply_move_clone(move).normalize()
                frontier.append((move_state, previous_moves + [move]))

    return (None, nodes_visited)

def ids(state: GameState):
    # keep track of time, total nodes, and current depth
    start_time = time.time()
    total_nodes = 0
    depth = 0

    while True:
        # return solution state and nodes expanded
        solution, nodes = dls(state, depth)
        # keep track of total nodes
        total_nodes += nodes

        if solution is not None:
            # found solution - print results
            end_time = time.time()
            duration = end_time - start_time
            for m in solution:
                print(m)
            final_state = state.normalize()
            for m in solution:
                final_state = final_state.apply_move_clone(m)
            final_state.print()
            print(f"Total search time: {int(duration*1000)}ms")
            print(f"Total nodes visited: {total_nodes}")
            print(f"Total solution length: {len(solution)}")
            return
        
        depth += 1

def manhattan_distance(state: GameState):
    # if the state is solved, distance is 0
    if state.is_solved():
        return 0
    # find a coordinate for the goal and for the target shape
    # i am just picking the first two i see
    goal_coordinate = None
    target_coordinate = None
    for x in range(state.rows):
        for y in range(state.cols):
            if state.base_grid[x][y] == -1:
                goal_coordinate = [x, y]
                break
        if goal_coordinate is not None:
            break
    for x in range(state.rows):
        for y in range(state.cols):
            if state.grid[x][y] == 2:
                target_coordinate = [x, y]
                break
        if target_coordinate is not None:
            break
    # find manhattan distance between goal and target
    x1, y1 = target_coordinate
    x2, y2 = goal_coordinate
    return abs(x2 - x1) + abs(y2 - y1)

def h(state: GameState):
    return manhattan_distance(state)

def astar(state: GameState):
    # keep track of execution time
    start_time = time.time()

    # normalize initial state
    state = state.normalize()

    # frontier is a priority queue sorted by g(n) + h(n)
    frontier = PriorityQueue()
    counter = 0
    frontier.put((h(state), counter, (state, [])))
    counter += 1

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
        priority, _, state_moves = frontier.get()
        state, previous_moves = state_moves
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
        if state in reached:
            continue
        # add popped state to reached
        reached.add(state)
        # loop through possible moves
        for move in state.get_all_moves():
            # get state of possible move
            move_state = state.apply_move_clone(move).normalize()
            # if not reached state, add to reached and frontier
            g = len(previous_moves) + 1
            f = g + h(move_state)
            frontier.put((f, counter, (move_state, previous_moves + [move])))
            counter += 1