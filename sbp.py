import sys
from GameState import GameState
from GameState import random_walk
from search import bfs, dfs, ids, astar

def handle_print(args):
    gs = GameState('SBP-levels/' + args[0])
    gs.print()

def handle_done(args):
    gs = GameState('SBP-levels/' + args[0])
    print(gs.is_solved())

def handle_available_moves(args):
    gs = GameState('SBP-levels/' + args[0])
    all_moves = gs.get_all_moves()
    gs.print_all_moves(all_moves)

def handle_apply_move(args):
    gs = GameState('SBP-levels/' + args[0])

    # convert arg to tuple
    arg = args[1].strip('()')
    parts = arg.split(',')
    move_tuple = (int(parts[0]), parts[1])
    
    gs.apply_move(move_tuple)
    gs.print()

def handle_compare(args):
    gs1 = GameState('SBP-levels/' + args[0])
    gs2 = GameState('SBP-levels/' + args[1])
    print(gs1.compare(gs2))

def handle_norm(args):
    gs = GameState('SBP-levels/' + args[0])
    norm_gs = gs.normalize()
    norm_gs.print()

def handle_random(args):
    gs = GameState('SBP-levels/' + args[0])
    N = int(args[1])
    random_walk(gs, N)

def handle_bfs(args):
    gs = GameState('SBP-levels/' + args[0])
    bfs(gs)

def handle_dfs(args):
    gs = GameState('SBP-levels/' + args[0])
    dfs(gs)

def handle_ids(args):
    gs = GameState('SBP-levels/' + args[0])
    ids(gs)

def handle_astar(args):
    gs = GameState('SBP-levels/' + args[0])
    astar(gs, "manhattan")

def handle_competition(args):
    gs = GameState('SBP-levels/' + args[0])
    astar(gs, "manhattan_penalty")

command_handlers = {
    'print': handle_print,
    'done': handle_done,
    'availableMoves': handle_available_moves,
    'applyMove': handle_apply_move,
    'compare': handle_compare,
    'norm': handle_norm,
    'random': handle_random,
    'bfs': handle_bfs,
    'dfs': handle_dfs,
    'ids': handle_ids,
    'astar': handle_astar,
    'competition': handle_competition
}

command = sys.argv[1]
handler = command_handlers[command]
handler(sys.argv[2:])