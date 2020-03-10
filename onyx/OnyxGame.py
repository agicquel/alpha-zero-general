import sys
import numpy as np

sys.path.append('..')
from Game import Game
from .OnyxLogic import Board


class OnyxGame(Game):
    def __init__(self, height=None, np_pieces=None):
        Game.__init__(self)
        self._base_board = Board(height, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return self._base_board.np_pieces.shape

    def getActionSize(self):
        return self._base_board.np_pieces.size

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        b.add_stone(action, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        for x, y in self._base_board.with_np_pieces(np_pieces=board).get_all_available():
            valids[self._base_board.size * x + y] = 1
        return valids

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        if b.is_winner(player):
            return 1
        elif b.is_winner(-player):
            return -1
        else:
            return 0

    def getCanonicalForm(self, board, player):
        return player * board

    def getSymmetries(self, board, pi):
        assert(len(pi) == self.getActionSize())
        l = []
        b = self._base_board.with_np_pieces(np_pieces=board)
        pi_board = np.reshape(pi[:-1], (b.size, (b.size + int(b.size / 2))))
        b1 = b[0:b.size-1, 0:b.size-1]
        b2 = b[b.size:int(b.size/2), 0:int(b.size/2)]
        b3 = b[b.size:int(b.size/2), int(b.size/2):b.size]

        for i in range(1, 5):
            for j in [True, False]:
                newB1 = np.rot90(b1, i)
                newB2 = np.rot90(b2, i)
                newB3 = np.rot90(b3, i)
                newPi = np.rot90(pi_board, i)
                if j:
                    newB1 = np.fliplr(newB1)
                    newB2 = np.fliplr(newB2)
                    newB3 = np.fliplr(newB3)
                    newPi = np.fliplr(newPi)
                l += [(newB1, list(newPi.ravel()) + [pi[-1]])]
                l += [(newB2, list(newPi.ravel()) + [pi[-1]])]
                l += [(newB3, list(newPi.ravel()) + [pi[-1]])]

        return l

    def stringRepresentation(self, board):
        return board.to_string()
