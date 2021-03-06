# A strategy that uses stockfish to play the worst moves possible
# Created by Terry Hearst on 2020/12/30

import os

import chess
import chess.engine

import strategy

class WorstfishStrategy(strategy.BaseStrategy):
	def __init__(self):
		try:
			stockfishPath = os.environ["STOCKFISH_PATH"]
		except KeyError:
			print("ERROR")
			print("Please set environment variable STOCKFISH_PATH to your stockfish executable")
			os._exit(1)
		self.engine = chess.engine.SimpleEngine.popen_uci(stockfishPath)

	def get_move(self, board: chess.Board) -> chess.Move:
		moves = list(board.legal_moves)

		worst_move = None
		worst_eval = chess.engine.MateGiven

		for move in moves:
			board.push(move)
			info = self.engine.analyse(board, chess.engine.Limit(nodes = 10000))
			board.pop()

			score = info["score"].pov(board.turn)
			if score < worst_eval:
				worst_move = move
				worst_eval = score

		return worst_move
