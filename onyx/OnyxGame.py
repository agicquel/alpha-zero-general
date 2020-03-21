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
        return self._base_board.np_pieces.size

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        move = (action % width, int(action / width))

        if player == -1:
            can = self.getCanonicalForm(board, -1)
            board2 = self._base_board.with_np_pieces(can)
            board2.add_stone(move, 1)
            return board2.rotate_board(board2.np_pieces, 1), -player
        else:
            b.add_stone(move, 1)
            return b.np_pieces, -player

    def getValidMoves(self, board, player):
        b = self._base_board.with_np_pieces(np_pieces=board)
        valid_moves = [0] * self.getActionSize()
        legal_moves = b.get_all_available()

        if len(legal_moves) == 0:
            valid_moves[-1] = 1
            return np.array(valid_moves)

        width = b.size + int(b.size / 2)
        for x, y in legal_moves:
            valid_moves[x + width * y] = 1

        return np.array(valid_moves)

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
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        if player == 1:
            return b.np_pieces
        return b.rotate_board(b.np_pieces, -1)

    def getSymmetries(self, board, pi):
        assert (len(pi) == self.getActionSize())
        symmetries = []
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        pi_board = np.reshape(pi, (b.size, (b.size + int(b.size / 2))))

        (b1, b2, b3) = b.split_np_board(b.np_pieces)
        (p1, p2, p3) = b.split_np_board(pi_board)

        for i in [True, False]:
            for j in [True, False]:
                new_b1 = b1
                new_b2 = b2
                new_b3 = b3
                new_p1 = p1
                new_p2 = p2
                new_p3 = p3

                if i:
                    new_b1 = np.flipud(new_b1)
                    new_b2 = np.flipud(new_b2)
                    new_b3 = np.flipud(new_b3)
                    new_p1 = np.flipud(new_p1)
                    new_p2 = np.flipud(new_p2)
                    new_p3 = np.flipud(new_p3)
                if j:
                    new_b1 = np.fliplr(new_b1)
                    new_b2 = np.fliplr(new_b2)
                    new_b3 = np.fliplr(new_b3)
                    new_p1 = np.fliplr(new_p1)
                    new_p2 = np.fliplr(new_p2)
                    new_p3 = np.fliplr(new_p3)

                new_b = b.reconstruct_np_board(new_b1, new_b2, new_b3)
                new_p = b.reconstruct_np_board(new_p1, new_p2, new_p3)
                symmetries += [(new_b, list(new_p.ravel()))]

        return symmetries

    def stringRepresentation(self, board):
        return str(self._base_board.with_np_pieces(np_pieces=board))

    @staticmethod
    def display(board):
        print(" -----------------------")
        print(' '.join(map(str, range(len(board[0])))))
        print(board)
        print(" -----------------------")
