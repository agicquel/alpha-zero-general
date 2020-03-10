import numpy as np


class Board:
    def __init__(self, size=None, np_pieces=None):
        self.size = size or 12
        assert(self.size % 2 == 0)
        if np_pieces is None:
            self.np_pieces = np.zeros([self.size, (self.size + int(self.size / 2))])
        else:
            self.np_pieces = np_pieces
            assert self.np_pieces.shape == ([self.size, (self.size + int(self.size / 2))])

    def add_stone(self, move, player):
        (x, y) = move
        if not self._is_available(x, y):
            raise ValueError("Cannot play at coordinates : (%s,%s) on board %s" % (x, y, self))

        captured = list()
        if self._get_z_dimension(x, y) == 0:
            top = self._is_inbound(x, y + 1, 0) and self.np_pieces[x, y + 1] == (player * -1)
            bottom = self._is_inbound(x, y - 1, 0) and self.np_pieces[x, y - 1] == (player * -1)
            left = self._is_inbound(x - 1, y, 0) and self.np_pieces[x - 1, y] == (player * -1)
            right = self._is_inbound(x + 1, y, 0) and self.np_pieces[x + 1, y] == (player * -1)

            if (x % 2 == 0 and y % 2 == 0) or (x % 2 == 1 and y % 2 == 1):
                if right and bottom and self.np_pieces[x + 1, y - 1] == player:
                    captured.append((x + 1, y))
                    captured.append((x, y - 1))
                if left and top and self.np_pieces[x - 1, y + 1] == player:
                    captured.append((x - 1, y))
                    captured.append((x, y + 1))
            elif (x % 2 == 0 and y % 2 == 1) or (x % 2 == 1 and y % 2 == 0):
                if left and bottom and self.np_pieces[x - 1, y - 1] == player:
                    captured.append((x - 1, y))
                    captured.append((x, y - 1))
                if top and right and self.np_pieces[x + 1, y + 1] == player:
                    captured.append((x, y + 1))
                    captured.append((x + 1, y))

        for cx, cy in captured:
            self.np_pieces[cy, cx] = 0

        self.np_pieces[y, x] = player

    def _get_neighbors(self, x, y):
        neighbors = list()
        z = self._get_z_dimension(x, y)

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
                if self._is_inbound(x / 2 - 1, y / 2, 1):
                    neighbors.append((self.size + x / 2 - 1, y / 2))
                if self._is_inbound(x / 2, y / 2 - 1, 2):
                    neighbors.append((self.size + x / 2, (self.size / 2) + y / 2 - 1))
            elif x % 2 == 0 and y % 2 == 1:
                if self._is_inbound(x - 1, y + 1, 0):
                    neighbors.append((x - 1, y + 1))
                if self._is_inbound(x / 2 - 1, (y - 1) / 2, 1):
                    neighbors.append((self.size + x / 2 - 1, (y - 1) / 2))
                if self._is_inbound(x / 2, (y - 1) / 2, 2):
                    neighbors.append((self.size + x / 2, (self.size / 2) + ((y - 1) / 2)))
            elif x % 2 == 1 and y % 2 == 0:
                if self._is_inbound(x + 1, y - 1, 0):
                    neighbors.append((x + 1, y - 1))
                if self._is_inbound((x - 1) / 2, y / 2, 1):
                    neighbors.append((self.size + (x - 1) / 2, y / 2))
                if self._is_inbound((x - 1) / 2, y / 2 - 1, 2):
                    neighbors.append((self.size + (x - 1) / 2, (self.size / 2) + (y / 2) - 1))
            elif x % 2 == 1 and y % 2 == 1:
                if self._is_inbound(x - 1, y - 1, 0):
                    neighbors.append((x - 1, y - 1))
                if self._is_inbound((x - 1) / 2, (y - 1) / 2, 1):
                    neighbors.append((self.size + ((x - 1) / 2), (y - 1) / 2))
                if self._is_inbound((x - 1) / 2, (y - 1) / 2, 2):
                    neighbors.append((self.size + ((x - 1) / 2), (self.size / 2) + ((y - 1) / 2)))
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
            y = y - (self.size / 2)
            if self._is_inbound(2 * x, 2 * y + 1, 0):
                neighbors.append((2 * x, 2 * y + 1))
            if self._is_inbound(2 * x + 1, 2 * y + 1, 0):
                neighbors.append((2 * x + 1, 2 * y + 1))
            if self._is_inbound(2 * x, 2 * y + 2, 0):
                neighbors.append((2 * x, 2 * y + 2))
            if self._is_inbound(2 * x + 1, 2 * y + 2, 0):
                neighbors.append((2 * x + 1, 2 * y + 2))

        return neighbors

    def _get_z_dimension(self, x, y):
        if x < self.size:
            return 0
        else:
            if y < (self.size / 2):
                return 1
            else:
                return 2

    def _is_inbound(self, x, y, z):
        if z == 0:
            return 0 <= x < self.size and 0 <= y < self.size
        elif z == 1:
            return 0 <= x < (self.size / 2 - 1) and 0 <= y < (self.size / 2)
        elif z == 2:
            return 0 <= x < (self.size / 2) and 0 <= y < (self.size / 2 - 1)
        else:
            return False

    def _is_available(self, x, y):
        if self.np_pieces[x, y] != 0:
            return False
        if self._get_z_dimension(x, y) != 0:
            for nx, ny in self._get_neighbors(x, y):
                if self.np_pieces[nx, ny] != 0:
                    return False
        return True

    def get_all_available(self):
        available = list()
        for y in range(0, self.np_pieces.shape[0]):
            for x in range(0, self.np_pieces.shape[1]):
                if self._is_available(x, y):
                    available.append((x, y))
        return available

    def with_np_pieces(self, np_pieces):
        if np_pieces is None:
            np_pieces = self.np_pieces
        return Board(self.size, np_pieces)

    def is_winner(self, player):
        visited = list()
        if player == 1:
            for y in range(0, self.size - 1):
                visited.clear()
                if self._is_winner_rec(player, visited, (0, y)):
                    return True
        elif player == -1:
            for x in range(0, self.size - 1):
                visited.clear()
                if self._is_winner_rec(player, visited, (x, 0)):
                    return True
        return False

    def _is_winner_rec(self, player, visited, move):
        (x, y) = move

        if player == 1 and y == 11 and self.np_pieces[x, y] == player:
            return True
        elif player == -1 and x == 11 and self.np_pieces[x, y] == player:
            return True

        visited.append(move)
        next_moves = list()
        for nx, ny in self._get_neighbors(x, y):
            if self.np_pieces[nx, ny] == player and not (nx, ny) in visited:
                next_moves.append((nx, ny))

        if len(next_moves) == 0:
            return False
        else:
            b = False
            for next_move in next_moves:
                b = b or self._is_winner_rec(player, visited, next_move)
            return b

    def to_string(self):
        return str(self.np_pieces)
