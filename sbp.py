import sys
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
    gs.create_shapes()
    all_moves = gs.get_all_moves()
    gs.print_all_moves(all_moves)