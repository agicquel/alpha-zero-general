from __future__ import absolute_import, division, print_function, unicode_literals

from onyx.OnyxGame import OnyxGame
"""
g = OnyxGame(size=12)
board = g.getInitBoard()
#n = g.get_debug_board(board).get_neighbors(10, 0)
#print(str(n))
for i in range(12):
    board, player = g.getNextState(board, 1, i*18)

board = g.getCanonicalForm(board, -1)

end = g.getGameEnded(board, -1)
print("end = " + str(end))

#board = g.getCanonicalForm(b.np_pieces, -1)
print("board = \n" + g.stringRepresentation(board))

#print(g.get_debug_board(board).is_available(12, 0))

"""

import tensorflow as tf
print("Num GPUs Available: ", len(tf.config.experimental.list_physical_devices('GPU')))
