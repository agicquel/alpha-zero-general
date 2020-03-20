from __future__ import absolute_import, division, print_function, unicode_literals

from onyx.OnyxGame import OnyxGame
import random

g = OnyxGame(size=6)
board = g.getInitBoard()
#n = g.get_debug_board(board).get_neighbors(10, 0)
#print(str(n))
player = 1
#print("\nvalids = " + str(g.getValidMoves(board, 1)) + "\n")

"""v = 0
for y in range(0, board.shape[0]):
    for x in range(0, board.shape[1]):
        board[y, x] = v
        v += 1

print("board = \n" + g.stringRepresentation(board))
"""

#for i in range(10):
#    board, player = g.getNextState(board, player, random.randint(0, g.getActionSize()))

board, player = g.getNextState(board, -1, 10)
#board, player = g.getNextState(board, -1, 7)

print("board = \n" + g.stringRepresentation(board))


#board, player = g.getNextState(board, player, 178)

#print("test js = " + g.get_debug_board(board).string_test_js())

#print("\nvalids = " + str(g.getValidMoves(board, 1)) + "\n")

#board = g.getCanonicalForm(board, -1)
#print("cano = \n" + g.stringRepresentation(board))


#print("test cano js = " + g.get_debug_board(board).string_test_js())
#print("\nvalids = " + str(g.getValidMoves(board, 1)) + "\n")

#end = g.getGameEnded(board, -1)
#print("end = " + str(end))

#print("board = \n" + g.stringRepresentation(board))

