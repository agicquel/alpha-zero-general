import numpy as np


class Board:
    def __init__(self, size=None, np_pieces=None):
        self.size = size or 6
        assert (self.size % 2 == 0)
        if np_pieces is None:
            self.np_pieces = np.zeros([self.size, (self.size + int(self.size / 2))])
        else:
            self.np_pieces = np_pieces
            assert self.np_pieces.shape == (self.size, (self.size + int(self.size / 2)))

    # player = -1 --> BLACK
    # player = 1 --> WHITE
    def add_stone(self, move, player):
        (x, y) = move
        if not self.is_available(x, y):
            raise ValueError("Cannot play at coordinates : (%s,%s) on board :\n%s" % (x, y, self))

        captured = list()
        if self.get_z_dimension(x, y) == 0:
            top = self._is_inbound(x, y + 1, 0) and int(self.np_pieces[y + 1, x]) == int(player * -1)
            bottom = self._is_inbound(x, y - 1, 0) and int(self.np_pieces[y - 1, x]) == int(player * -1)
            left = self._is_inbound(x - 1, y, 0) and int(self.np_pieces[y, x - 1]) == int(player * -1)
            right = self._is_inbound(x + 1, y, 0) and int(self.np_pieces[y, x + 1]) == int(player * -1)

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                if right and bottom and int(self.np_pieces[y - 1, x + 1]) == int(player):
                    captured.append((x + 1, y))
                    captured.append((x, y - 1))
                if left and top and int(self.np_pieces[y + 1, x - 1]) == int(player):
                    captured.append((x - 1, y))
                    captured.append((x, y + 1))
            elif (x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0):
                if left and bottom and int(self.np_pieces[y - 1, x - 1]) == int(player):
                    captured.append((x - 1, y))
                    captured.append((x, y - 1))
                if top and right and int(self.np_pieces[y + 1, x + 1]) == int(player):
                    captured.append((x, y + 1))
                    captured.append((x + 1, y))

        for cx, cy in captured:
            self.np_pieces[cy, cx] = 0

        self.np_pieces[y, x] = player

    def get_neighbors(self, x, y):
        neighbors = list()
        z = self.get_z_dimension(x, y)

        if z == 0:
            if self._is_inbound(x, y - 1, z):
                neighbors.append((x, y - 1))
            if self._is_inbound(x + 1, y, z):
                neighbors.append((x + 1, y))
            if self._is_inbound(x, y + 1, z):
                neighbors.append((x, y + 1))
            if self._is_inbound(x - 1, y, z):
                neighbors.append((x - 1, y))

            if x % 2 == 0 and y % 2 == 0:
                if self._is_inbound(x + 1, y + 1, 0):
                    neighbors.append((x + 1, y + 1))
                if self._is_inbound(int(x / 2) - 1, int(y / 2), 1):
                    neighbors.append((self.size + int(x / 2) - 1, int(y / 2)))
                if self._is_inbound(int(x / 2), int(y / 2) - 1, 2):
                    neighbors.append((self.size + int(x / 2), (int(self.size / 2)) + int(y / 2) - 1))
            elif x % 2 == 0 and y % 2 == 1:
                if self._is_inbound(x - 1, y + 1, 0):
                    neighbors.append((x - 1, y + 1))
                if self._is_inbound(int(x / 2) - 1, int((y - 1) / 2), 1):
                    neighbors.append((self.size + int(x / 2) - 1, int((y - 1) / 2)))
                if self._is_inbound(int(x / 2), int((y - 1) / 2), 2):
                    neighbors.append((self.size + int(x / 2), int(self.size / 2) + int((y - 1) / 2)))
            elif x % 2 == 1 and y % 2 == 0:
                if self._is_inbound(x + 1, y - 1, 0):
                    neighbors.append((x + 1, y - 1))
                if self._is_inbound(int((x - 1) / 2), int(y / 2), 1):
                    neighbors.append((self.size + int((x - 1) / 2), int(y / 2)))
                if self._is_inbound(int((x - 1) / 2), int(y / 2) - 1, 2):
                    neighbors.append((self.size + int((x - 1) / 2), int(self.size / 2) + int(y / 2) - 1))
            elif x % 2 == 1 and y % 2 == 1:
                if self._is_inbound(x - 1, y - 1, 0):
                    neighbors.append((x - 1, y - 1))
                if self._is_inbound(int((x - 1) / 2), int((y - 1) / 2), 1):
                    neighbors.append((self.size + int(((x - 1) / 2)), int((y - 1) / 2)))
                if self._is_inbound(int((x - 1) / 2), int((y - 1) / 2), 2):
                    neighbors.append((self.size + int((x - 1) / 2), int(self.size / 2) + int((y - 1) / 2)))
        elif z == 1:
            x = x - self.size
            if self._is_inbound(2 * x + 1, 2 * y, 0):
                neighbors.append((2 * x + 1, 2 * y))
            if self._is_inbound(2 * x + 2, 2 * y, 0):
                neighbors.append((2 * x + 2, 2 * y))
            if self._is_inbound(2 * x + 1, 2 * y + 1, 0):
                neighbors.append((2 * x + 1, 2 * y + 1))
            if self._is_inbound(2 * x + 2, 2 * y + 1, 0):
                neighbors.append((2 * x + 2, 2 * y + 1))
        elif z == 2:
            x = x - self.size
            y = y - int(self.size / 2)
            if self._is_inbound(2 * x, 2 * y + 1, 0):
                neighbors.append((2 * x, 2 * y + 1))
            if self._is_inbound(2 * x + 1, 2 * y + 1, 0):
                neighbors.append((2 * x + 1, 2 * y + 1))
            if self._is_inbound(2 * x, 2 * y + 2, 0):
                neighbors.append((2 * x, 2 * y + 2))
            if self._is_inbound(2 * x + 1, 2 * y + 2, 0):
                neighbors.append((2 * x + 1, 2 * y + 2))

        return neighbors

    def get_z_dimension(self, x, y):
        if x < self.size:
            return 0
        else:
            if y < int(self.size / 2):
                return 1
            else:
                return 2

    def _is_inbound(self, x, y, z):
        if z == 0:
            return 0 <= x < self.size and 0 <= y < self.size
        elif z == 1:
            return 0 <= x < (int(self.size / 2) - 1) and 0 <= y < int(self.size / 2)
        elif z == 2:
            return 0 <= x < int(self.size / 2) and 0 <= y < (int(self.size / 2) - 1)
        else:
            return False

    def is_available(self, x, y):
        if not (0 <= x < self.np_pieces.shape[1] and 0 <= y < self.np_pieces.shape[0]):
            return False

        if int(self.np_pieces[y, x]) != 0:
            return False

        z = self.get_z_dimension(x, y)
        if z != 0:
            if z == 1 and not self._is_inbound(x - self.size, y, z):
                return False
            elif z == 2 and not self._is_inbound(x - self.size, y - int(self.size / 2), z):
                return False

            for nx, ny in self.get_neighbors(x, y):
                if int(self.np_pieces[ny, nx]) != 0:
                    return False
        return True

    def get_all_available(self):
        available = list()
        for y in range(0, self.np_pieces.shape[0]):
            for x in range(0, self.np_pieces.shape[1]):
                if self.is_available(x, y):
                    available.append((x, y))
        return available

    def with_np_pieces(self, np_pieces):
        if np_pieces is None:
            np_pieces = self.np_pieces
        return Board(self.size, np_pieces)

    def is_winner(self, player):
        visited = list()
        if player == 1:
            for y in range(self.size - 1):
                if int(self.np_pieces[y, 0]) == int(player):
                    visited.clear()
                    if self._is_winner_rec(player, visited, (0, y)):
                        return True
        elif player == -1:
            for x in range(self.size - 1):
                if int(self.np_pieces[0, x]) == int(player):
                    visited.clear()
                    if self._is_winner_rec(player, visited, (x, 0)):
                        return True
        return False

    def _is_winner_rec(self, player, visited, move):
        (x, y) = move

        if player == -1 and y == (self.size - 1) and int(self.np_pieces[y, x]) == int(player):
            return True
        elif player == 1 and x == (self.size - 1) and int(self.np_pieces[y, x]) == int(player):
            return True

        visited.append(move)
        next_moves = list()
        for nx, ny in self.get_neighbors(x, y):
            if int(self.np_pieces[ny, nx]) == int(player) and not (nx, ny) in visited:
                next_moves.append((nx, ny))

        if len(next_moves) == 0:
            return False
        else:
            b = False
            for next_move in next_moves:
                b = b or self._is_winner_rec(player, visited, next_move)
            return b

    def __str__(self):
        return str(self.np_pieces)

    def split_np_board(self, board):
        b1 = board[0:self.size, 0:self.size]
        b2 = board[0:int(self.size / 2), self.size:self.size + int(self.size / 2) - 1]
        b3 = board[int(self.size / 2):self.size - 1, self.size:self.size + int(self.size / 2)]
        return b1, b2, b3

    def reconstruct_np_board(self, b1, b2, b3):
        board = np.zeros(self.np_pieces.shape)
        for y in range(0, board.shape[0]):
            for x in range(0, board.shape[1]):
                z = self.get_z_dimension(x, y)
                val = 0
                if z == 0:
                    val = b1[y, x]
                elif z == 1 and self._is_inbound(x - self.size, y, z):
                    val = b2[y, x - self.size]
                elif z == 2 and self._is_inbound(x - self.size, y - int(self.size / 2), z):
                    val = b3[y - int(self.size / 2), x - self.size]
                board[y, x] = val
        return board

    def build_pi_board(self, pi):
        size = self.size
        width = size + int(size / 2)
        pi_board = np.zeros([size, width])

        pos = 0
        for p in pi:
            (x, y) = (pos % width, int(pos / width))
            pi_board[y, x] = p
            pos = pos + 1

        return pi_board

    def rotate_board(self, board, n):
        if n == 0:
            return board
        (b1, b2, b3) = self.split_np_board(np.copy(board))
        new_b1 = np.rot90(b1, 1 if n > 0 else -1)
        new_b2 = np.rot90(b2, 1 if n > 0 else -1)
        new_b3 = np.rot90(b3, 1 if n > 0 else -1)
        new_b1 = np.fliplr(new_b1)
        new_b2 = np.fliplr(new_b2)
        new_b3 = np.fliplr(new_b3)
        new_b1 = new_b1 * -1
        new_b2 = new_b2 * -1
        new_b3 = new_b3 * -1
        return self.rotate_board(self.reconstruct_np_board(new_b1, new_b3, new_b2), n - (1 if n > 0 else -1))

    def string_test_js(self):
        black = "black are : ["
        white = "white are : ["

        for y in range(0, self.np_pieces.shape[0]):
            for x in range(0, self.np_pieces.shape[1]):
                value = int(self.np_pieces[y, x])
                if value == 0:
                    continue
                z = self.get_z_dimension(x, y)
                coord = ""
                if z == 0:
                    coord = chr(ord('A') + x) + "," + str(y + 1)
                elif z == 1:
                    x = x - self.size
                    coord = chr(ord('A') + 2 * x + 1) + "-" + chr(ord('A') + 2 * x + 2)
                    coord += "," + str(2 * y + 1) + "-" + str(2 * y + 2)
                elif z == 2:
                    x = x - self.size
                    y = y - int(self.size / 2)
                    coord = chr(ord('A') + 2 * x) + "-" + chr(ord('A') + 2 * x + 1)
                    coord += "," + str(2 * y + 2) + "-" + str(2 * y + 3)

                if value == -1:
                    black = black + "'" + coord + "', "
                elif value == 1:
                    white = white + "'" + coord + "', "

        black = black + "]\n"
        white = white + "]\n"

        return black + white
