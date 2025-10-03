import sys
import ast
from GameState import GameState

command = sys.argv[1]

if command == "print":
    gs = GameState('SBP-levels/' + sys.argv[2])
    gs.print()

if command == "done":
    gs = GameState('SBP-levels/' + sys.argv[2])
    print(gs.is_solved())

if command == "availableMoves":
    gs = GameState('SBP-levels/' + sys.argv[2])
    all_moves = gs.get_all_moves()
    gs.print_all_moves(all_moves)

if command == "applyMove":
    gs = GameState('SBP-levels/' + sys.argv[2])

    # convert arg to tuple
    arg = sys.argv[3].strip('()')
    parts = arg.split(',')
    move_tuple = (int(parts[0]), parts[1])
    
    gs.apply_move(move_tuple)
    gs.print()