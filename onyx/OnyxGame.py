import sys
import numpy as np

sys.path.append('..')
from Game import Game
from .OnyxLogic import Board


class OnyxGame(Game):
    def __init__(self, size=None, np_pieces=None):
        Game.__init__(self)
        self.base_board = Board(size, np_pieces)

    def getInitBoard(self):
        return self.base_board.np_pieces

    def getBoardSize(self):
        return self.base_board.np_pieces.shape[0], self.base_board.np_pieces.shape[1]

    def getActionSize(self):
        return self.base_board.np_pieces.size

    def getNextState(self, board, player, action):
        b = self.base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        move = (action % width, int(action / width))

        if player == -1:
            can = self.getCanonicalForm(board, -1)
            board2 = self.base_board.with_np_pieces(can)
            board2.add_stone(move, 1)
            return board2.rotate_board(board2.np_pieces * -1, 1), -player
        else:
            b.add_stone(move, 1)
            return b.np_pieces, -player

    def getValidMoves(self, board, player):
        b = self.base_board.with_np_pieces(np_pieces=board)
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
        b = self.base_board.with_np_pieces(np_pieces=board)
        if b.is_winner(player):
            return 1
        elif b.is_winner(-player):
            return -1
        elif len(b.get_all_available()) == 0:
            return 1e-4
        else:
            return 0

    def getCanonicalForm(self, board, player):
        b = self.base_board.with_np_pieces(np_pieces=np.copy(board))
        if player == 1:
            return b.np_pieces
        return b.rotate_board(b.np_pieces * -1, -1)

    def getSymmetries(self, board, pi):
        assert (len(pi) == self.getActionSize())
        symmetries = []
        b = self.base_board.with_np_pieces(np_pieces=board)
        pi_board = np.reshape(pi, (b.size, (b.size + int(b.size / 2))))

        symmetries += [(board, list(pi_board.ravel()))]
        symmetries += [(b.rotate_board(board, 2), list(b.rotate_board(pi_board, 2).ravel()))]

        (p1, p2, p3) = b.split_np_board(pi_board)
        new_p1 = np.flipud(p1)
        new_p2 = np.flipud(p2)
        new_p3 = np.flipud(p3)
        new_p1 = np.fliplr(new_p1)
        new_p2 = np.fliplr(new_p2)
        new_p3 = np.fliplr(new_p3)
        new_p = b.reconstruct_np_board(new_p1, new_p2, new_p3)
        symmetries += [(b.rotate_board(board, 2), list(new_p.ravel()))]

        """(b1, b2, b3) = b.split_np_board(b.np_pieces)
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
                symmetries += [(new_b, list(new_p.ravel()))]"""

        return symmetries

    def stringRepresentation(self, board):
        return str(self.base_board.with_np_pieces(np_pieces=board))

    @staticmethod
    def display(board):
        print(" -----------------------")
        print(' '.join(map(str, range(len(board[0])))))
        print(board)
        print(" -----------------------")

    def convert_action_to_str(self, board, action):
        b = self.base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        (x, y) = (action % width, int(action / width))
        z = b.get_z_dimension(x, y)
        coord = ""
        if z == 0:
            coord = chr(ord('A') + x) + "," + str(y + 1)
        elif z == 1:
            x = x - b.size
            coord = chr(ord('A') + 2 * x + 1) + "-" + chr(ord('A') + 2 * x + 2)
            coord += "," + str(2 * y + 1) + "-" + str(2 * y + 2)
        elif z == 2:
            x = x - b.size
            y = y - int(b.size / 2)
            coord = chr(ord('A') + 2 * x) + "-" + chr(ord('A') + 2 * x + 1)
            coord += "," + str(2 * y + 2) + "-" + str(2 * y + 3)
        return coord

    def convert_action_to_coord(self, board, action):
        b = self.base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)
        return action % width, int(action / width)

    def convert_action_to_int(self, board, action):
        b = self.base_board.with_np_pieces(np_pieces=np.copy(board))
        width = b.size + int(b.size / 2)

        coords = action.split(",")
        assert (len(coords) == 2)
        abscissa = coords[0].split("-")
        ordinate = coords[1].split("-")

        x = ord(abscissa[0]) - ord('A')
        y = int(ordinate[0]) - 1

        if len(abscissa) == 2 and len(ordinate) == 2:
            if y % 2 == 0 and x % 2 == 1:
                x = b.size + int((x - 1) / 2)
                y = int(y / 2)
            elif y % 2 == 1 and x % 2 == 0:
                x = b.size + int(x / 2)
                y = int((y - 1) / 2) + int(b.size / 2)
            else:
                raise Exception("Coordinates are incorrect")

        return y * width + x
