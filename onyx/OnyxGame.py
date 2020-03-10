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
        return self._base_board.np_pieces.size + 1

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        move = (action % width, int(action / width))
        b.add_stone(move, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        for x, y in b.get_all_available():
            valids[x + width * y] = 1
        #print("\n\nvalids = " + str(valids) + "\n\n")
        return np.array(valids)

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

        (b1, b2, b3) = b.split_np_board(b.np_pieces)
        (p1, p2, p3) = b.split_np_board(pi_board)

        for i in range(1, 5):
            for j in [True, False]:
                newB1 = np.rot90(b1, i)
                newB2 = np.rot90(b2, i)
                newB3 = np.rot90(b3, i)

                newP1 = np.rot90(p1, i)
                newP2 = np.rot90(p2, i)
                newP3 = np.rot90(p3, i)

                if j:
                    newB1 = np.fliplr(newB1)
                    newB2 = np.fliplr(newB2)
                    newB3 = np.fliplr(newB3)

                    newP1 = np.fliplr(newP1)
                    newP2 = np.fliplr(newP2)
                    newP3 = np.fliplr(newP3)

                newB = b.reconstruct_np_board(b1, b2, b3)
                newP = b.reconstruct_np_board(p1, p2, p3)
                l += [(newB, list(newP.ravel()) + [pi[-1]])]

        return l

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))

    @staticmethod
    def display(board):
        return str(board)
