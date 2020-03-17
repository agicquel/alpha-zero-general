import sys
import numpy as np

sys.path.append('..')
from Game import Game
from .OnyxLogic import Board


class OnyxGame(Game):
    def __init__(self, size=None, np_pieces=None):
        Game.__init__(self)
        self._base_board = Board(size, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return self._base_board.np_pieces.shape

    def getActionSize(self):
        return self._base_board.np_pieces.size

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        move = (action % width, int(action / width))
        (x, y) = move
        if not b.is_available(x, y):
            return (board, -player)
        b.add_stone(move, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        valids = [0] * self.getActionSize()
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        legals = b.get_all_available()
        #print("\nlegals size = " + str(len(legals)) + "\n")
        for x, y in legals:
            valids[x + width * y] = 1
        #print("\n\nvalids = " + str(valids) + "\n\n")
        return np.array(valids)

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        if b.is_winner(player):
            return player
        elif b.is_winner(-player):
            return -player
        else:
            return 0

    def getCanonicalForm(self, board, player):
        #return player * board
        if player == 1:
            return board
        b = self._base_board.with_np_pieces(np_pieces=board)
        (b1, b2, b3) = b.split_np_board(b.np_pieces)
        newB1 = np.rot90(b1, player)
        newB2 = np.rot90(b2, player)
        newB3 = np.rot90(b3, player)

        newB1 = np.fliplr(newB1)
        newB2 = np.fliplr(newB2)
        newB3 = np.fliplr(newB3)

        newB1 = newB1 * player
        newB2 = newB2 * player
        newB3 = newB3 * player

        newB = b.reconstruct_np_board(newB1, newB3, newB2)
        return newB

    def getSymmetries(self, board, pi):
        assert(len(pi) == self.getActionSize())
        l = []
        b = self._base_board.with_np_pieces(np_pieces=board)

        #pi_board = np.reshape(pi[:-1], (b.size, (b.size + int(b.size / 2))))
        pi_board = np.reshape(pi, (b.size, (b.size + int(b.size / 2))))

        (b1, b2, b3) = b.split_np_board(b.np_pieces)
        (p1, p2, p3) = b.split_np_board(pi_board)

        #for i in range(1, 5):
        for i in [True, False]:
            for j in [True, False]:
                newB1 = b1
                newB2 = b2
                newB3 = b3
                newP1 = p1
                newP2 = p2
                newP3 = p3

                """newB1 = np.rot90(b1, i)
                newB2 = np.rot90(b2, i)
                newB3 = np.rot90(b3, i)

                newP1 = np.rot90(p1, i)
                newP2 = np.rot90(p2, i)
                newP3 = np.rot90(p3, i)"""

                if i:
                    newB1 = np.flipud(newB1)
                    newB2 = np.flipud(newB2)
                    newB3 = np.flipud(newB3)
                    newP1 = np.flipud(newP1)
                    newP2 = np.flipud(newP2)
                    newP3 = np.flipud(newP3)
                if j:
                    newB1 = np.fliplr(newB1)
                    newB2 = np.fliplr(newB2)
                    newB3 = np.fliplr(newB3)
                    newP1 = np.fliplr(newP1)
                    newP2 = np.fliplr(newP2)
                    newP3 = np.fliplr(newP3)

                newB = b.reconstruct_np_board(newB1, newB2, newB3)
                newP = b.reconstruct_np_board(newP1, newP2, newP3)
                #l += [(newB, list(newP.ravel()) + [pi[-1]])]
                l += [(newB, list(newP.ravel()))]

        return l

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))

    @staticmethod
    def display(board):
        print(" -----------------------")
        print(' '.join(map(str, range(len(board[0])))))
        print(board)
        print(" -----------------------")

    def get_debug_board(self, board):
        return self._base_board.with_np_pieces(np_pieces=board)
