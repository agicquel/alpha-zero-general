from onyx.OnyxGame import OnyxGame

g = OnyxGame()
board = g.getInitBoard()
#n = g.get_debug_board(board).get_neighbors(10, 0)
#print(str(n))
#for i in range(12):
#    board, player = g.getNextState(board, 1, i*18)
#board, player = g.getNextState(board, 1, 0)
#end = g.getGameEnded(board, 1)
valids = g.getValidMoves(board, 1)
print(str(valids))
print(board)
#print(g.get_debug_board(board).is_available(12, 0))
#print(end)

