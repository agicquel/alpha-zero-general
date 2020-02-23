import numpy as np


class Board:
    def __init__(self, size=None, np_pieces=None):
        self.size = size or 12
        if np_pieces is None:
            self.np_pieces = np.zeros([self.size, (self.size + self.size / 2)])
        else:
            self.np_pieces = np_pieces
            assert self.np_pieces.shape == ([self.size, (self.size + self.size / 2)])

    def add_stone(self, move, player):
        (x, y) = move

        if self.np_pieces[z, x, y] != 0:
            raise ValueError("Cannot play at coordinates : (%s,%s,%s) on board %s" % (x, y, z, self))
        else:
            self.np_pieces[z, x, y] = player

    def _is_available(self, x, y):
        return True

    def _get_neighbors(self, x , y):
        neighbors = list()
        z = self._get_z_dimension(x, y)

        if z == 0:
            if self._is_inbound(x, y-1, z): neighbors.append((x, y-1))
            if self._is_inbound(x+1, y, z): neighbors.append((x+1, y))
            if self._is_inbound(x, y+1, z): neighbors.append((x, y+1))
            if self._is_inbound(x-1, y, z): neighbors.append((x-1, y))

            if x % 2 == 0 and y % 2 == 0:
            elif x % 2 == 0 and y % 2 == 1:
            elif x % 2 == 1 and y % 2 == 0:
            elif x % 2 == 1 and y % 2 == 1:
        elif z == 1:
            # aaa
        elif z == 2:
            # www

        return neighbors

    def _get_z_dimension(self, x , y):
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

    def get_available(self, player):
        return list()

    @staticmethod
    def get_number_points():
        return 12 * 12 + 5 * 6 + 6 * 5

    def toString(self):
        return str(self.np_pieces)
