#!/usr/bin/env python

import os
import sys
_i = os.path.dirname(os.path.abspath(__file__))
sys.path.extend([os.path.abspath(os.path.join(_i, os.pardir))])

print('Python %s on %s' % (sys.version, sys.platform))
print('Argument List:', str(sys.argv))

import websocket

try:
    import thread
except ImportError:
    import _thread as thread

from onyx.OnyxGame import OnyxGame
from onyx.pytorch.NNet import NNetWrapper as NNet
from MCTS import MCTS

import numpy as np
from utils import *
import time

websocket.enableTrace(False)


class GameClient:
    def __init__(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self.on_message,
                                         on_error=self.on_error,
                                         on_close=self.on_close)
        self.ws.on_open = self.on_open
        self.turn = False
        self.started = False

        self.game = OnyxGame()
        self.color = 1
        self.board = self.game.getInitBoard()

        n = NNet(self.game)
        n.load_checkpoint('./pretrained_models/onyx/pytorch/', '6x6_90.pth.tar')
        args = dotdict({'numMCTSSims': 50, 'cpuct': 1.0})
        mcts = MCTS(self.game, n, args)
        self.ai_player = lambda x: np.argmax(mcts.getActionProb(x, temp=0))

    def on_message(self, message):
        # COMMAND
        if message[0] == '$':
            if message[1:] == "AWAITING":
                self.turn = False
                print("En attente de l'autre joueur")
            if message[1:] == "START":
                self.started = True
            if message[1:] == "READY":
                self.turn = True
            if message[1:] == "WIN":
                print("Vous avez gagné !")
            if message[1:] == "LOOSE":
                print("Vous avez perdu !")
            if message[1:] == "DRAW":
                print("Match nul !")
                self.ws.close()
            if message[1:] == "END":
                print("Partie terminée.")
                self.ws.close()
        # ERROR
        if message[0] == '!':
            print("Erreur : ", message[1:])

        # INFO
        if message[0] == '#':
            if "OPPONENT" in message[1:]:
                print("L'aversaire à joué : ", message.split(" ")[1])
                action = self.game.convert_action_to_int(self.board, message.split(" ")[1])
                x, y = self.game.convert_action_to_coord(self.board, action)
                self.board[y, x] = self.color * -1
            elif message[1:] == "Room created":
                print("Partie créée")
                self.color = -1
            elif message[1:] == "Room joined":
                print("Partie rejointe")
                self.color = 1
            else:
                print("Information : ", message[1:])

        # RESULT
        if message[0] == '=':
            self.turn = False
            print("Capturé(s) : ", message[1:].split(" "))
            for captured in message[1:].split(" "):
                action = self.game.convert_action_to_int(self.board, captured)
                x, y = self.game.convert_action_to_coord(self.board, action)
                self.board[y, x] = 0

        if self.started and self.turn:
            self.play()

    def on_error(self, error):
        print(error)

    def on_close(self):
        print("### closed ###")

    def on_open(self):
        def run(*args):
            print("Connecté.")

        thread.start_new_thread(run, ())

    def run(self):
        self.ws.run_forever()

    def play(self):
        time.sleep(0.2)
        action = self.ai_player(self.game.getCanonicalForm(self.board, self.color))
        coord = self.game.convert_action_to_str(self.board, action)
        self.board, next_player = self.game.getNextState(self.board, self.color, action)
        print("put " + str(action) + " for player " + str(self.color) + "\nboard : " + str(
            self.game.base_board.with_np_pieces(self.board).string_test_js()) + "\n")
        self.ws.send(coord)


client = GameClient("ws://localhost:8889/room/" + str(sys.argv[1]))
client.run()
