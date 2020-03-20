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
        return self._base_board.np_pieces.shape[0], self._base_board.np_pieces.shape[1]

    def getActionSize(self):
        return self._base_board.np_pieces.size  # - self._base_board.size

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        move = (action % width, int(action / width))
        (x, y) = move

        if player == -1:
            """print("old = " + str((x, y)))
            z = b.get_z_dimension(x, y)
            tmp = y
            if z == 0:
                print("z0")
                y = b.size - 1 - x
                x = tmp
            elif z == 1:
                print("z1")
                y = b.np_pieces.shape[0] - x
                x = b.np_pieces.shape[1] + tmp
            elif z == 2:
                print("z2")
                y = x - b.size
                x = b.size + y - int(b.size / 2)
            print("new = " + str((x, y)))
            move = (x, y)"""
            can = self.getCanonicalForm(board, -1)
            board2 = self._base_board.with_np_pieces(can)
            board2.add_stone(move, 1)

            (b1, b2, b3) = b.split_np_board(board2.np_pieces)

            newB1 = np.rot90(b1, 1)
            newB2 = np.rot90(b2, 1)
            newB3 = np.rot90(b3, 1)
            newB1 = np.fliplr(newB1)
            newB2 = np.fliplr(newB2)
            newB3 = np.fliplr(newB3)
            newB1 = newB1 * -1
            newB2 = newB2 * -1
            newB3 = newB3 * -1
            newB = b.reconstruct_np_board(newB1, newB3, newB2)

            return (newB, -player)

        # valid_check = self.getValidMoves(board, player)
        # print("valid_check[move] = " + str(valid_check[action]))

        #if not b.is_available(x, y):
        #    print("\n/!\ Action not possible : " + str(move) + "/!\\n")
        #    return (b.np_pieces, -player)
        # print("Player " + str(player) + " played : " + str(move) + "\n")

        # print("before add : \n" + b.string_test_js())
        b.add_stone(move, player)
        # print("after add : \n" + b.string_test_js())
        # print("valids for next : " + str(len(b.get_all_available())))
        # print("getGameEnded(1) ? : \n" + str(self.getGameEnded(b.np_pieces, 1)))
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        valids = [0] * self.getActionSize()
        legal_moves = b.get_all_available()

        if len(legal_moves) == 0:
            valids[-1] = 1
            return np.array(valids)

        width = b.size + int(b.size / 2)
        for x, y in legal_moves:
            valids[x + width * y] = 1

        return np.array(valids)

    def getGameEnded(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        if b.is_winner(player):
            return 1
        elif b.is_winner(-player):
            return -1
        elif len(b.get_all_available()) == 0:
            return 1e-4
        else:
            return 0

    def getCanonicalForm(self, board, player):
        # return board
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        if player == 1:
            return b.np_pieces
        (b1, b2, b3) = b.split_np_board(b.np_pieces)

        newB1 = np.rot90(b1, -1)
        newB2 = np.rot90(b2, -1)
        newB3 = np.rot90(b3, -1)

        newB1 = np.fliplr(newB1)
        newB2 = np.fliplr(newB2)
        newB3 = np.fliplr(newB3)

        newB1 = newB1 * -1
        newB2 = newB2 * -1
        newB3 = newB3 * -1

        newB = b.reconstruct_np_board(newB1, newB3, newB2)
        return newB

    def getSymmetries(self, board, pi):
        #return [(board, pi)]
        assert (len(pi) == self.getActionSize())
        # print("\npi = " + str(pi) + "\n")
        l = []
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        # pi_board = b.build_pi_board(pi)

        # pi_board = np.reshape(pi[:-1], (b.size, (b.size + int(b.size / 2))))
        pi_board = np.reshape(pi, (b.size, (b.size + int(b.size / 2))))

        (b1, b2, b3) = b.split_np_board(b.np_pieces)
        (p1, p2, p3) = b.split_np_board(pi_board)

        # for i in range(1, 5):
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

                """newB = b.reconstruct_np_board(newB1, newB2, newB3)
                newP = b.reconstruct_np_board(newP1, newP2, newP3)
                l += [(newB, list(newP.ravel()))]"""

                """if i % 2 == 0:
                    newB = b.reconstruct_np_board(newB1, newB2, newB3)
                    newP = b.reconstruct_np_board(newP1, newP2, newP3)
                else:
                    newB = b.reconstruct_np_board(newB1, newB3, newB2)
                    newP = b.reconstruct_np_board(newP1, newP3, newP2)"""

                newB = b.reconstruct_np_board(newB1, newB2, newB3)
                newP = b.reconstruct_np_board(newP1, newP2, newP3)
                # l += [(newB, list(newP.ravel()) + [pi[-1]])]
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
