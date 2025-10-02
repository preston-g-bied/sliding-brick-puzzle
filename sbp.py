import sys
from GameState import GameState

command = sys.argv[1]

if command == "print":
    gs = GameState('SBP-levels/' + sys.argv[2])
    gs.print()