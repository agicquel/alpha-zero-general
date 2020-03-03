from __future__ import print_function
import sys

sys.path.append('..')
from Game import Game
from .OnyxLogic import Board
import numpy as np

class OnyxGame(Game):
    def __init__(self, height=None, np_pieces=None):
        Game.__init__(self)
        self._base_board = Board(height, np_pieces)

    def getInitBoard(self):
        return self._base_board.np_pieces

    def getBoardSize(self):
        return self._base_board.np_pieces.shape()

    def getActionSize(self):
        return self._base_board.np_pieces.size()

    def getNextState(self, board, player, action):
        b = self._base_board.with_np_pieces(np_pieces=np.copy(board))
        b.add_stone(action, player)
        return b.np_pieces, -player

    def getValidMoves(self, board, player):
        return super().getValidMoves(board, player)

    def getGameEnded(self, board, player):
        return super().getGameEnded(board, player)

    def getCanonicalForm(self, board, player):
        return super().getCanonicalForm(board, player)

    def getSymmetries(self, board, pi):
        return super().getSymmetries(board, pi)

    def stringRepresentation(self, board):
        return board.toString()