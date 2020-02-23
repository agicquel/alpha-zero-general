from __future__ import print_function
import sys

sys.path.append('..')
from Game import Game
from .OnyxLogic import Board
import numpy as np

class OnyxGame(Game):
    def __init__(self):

    def getInitBoard(self):
        return super().getInitBoard()

    def getBoardSize(self):
        return super().getBoardSize()

    def getActionSize(self):
        return super().getActionSize()

    def getNextState(self, board, player, action):
        return super().getNextState(board, player, action)

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