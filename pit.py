import Arena
from MCTS import MCTS
from onyx.OnyxGame import OnyxGame
from onyx.pytorch.NNet import NNetWrapper as NNet
from onyx.OnyxPlayers import *


import numpy as np
from utils import *

"""
use this script to play any two agents against each other, or play manually with
any agent.
"""

"""
mini_othello = False  # Play in 6x6 instead of the normal 8x8.

if mini_othello:
    g = OthelloGame(6)
else:
    g = OthelloGame(8)

# all players
"""
g = OnyxGame()
human_vs_cpu = True

rp = RandomPlayer(g).play
#rp2 = RandomPlayer(g).play
hp = HumanOnyxPlayer(g).play
"""
gp = GreedyOthelloPlayer(g).play

"""



# nnet players
n1 = NNet(g)
n1.load_checkpoint('./pretrained_models/onyx/pytorch/', '6x6_best.pth.tar')
args1 = dotdict({'numMCTSSims': 50, 'cpuct':1.0})
mcts1 = MCTS(g, n1, args1)
n1p = lambda x: np.argmax(mcts1.getActionProb(x, temp=0))


n2 = NNet(g)
n2.load_checkpoint('./temp/', 'best.pth.tar')
args2 = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
mcts2 = MCTS(g, n2, args2)
n2p = lambda x: np.argmax(mcts2.getActionProb(x, temp=0))

player2 = rp #n2p  # Player 2 is neural network if it's cpu vs cpu.

arena = Arena.Arena(rp, n2p, g, g.display)

print(arena.playGames(1000, verbose=False))
