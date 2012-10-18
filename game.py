#! /usr/bin/env python

import argparse
import random
from abc import abstractmethod

class Player(object):
	def __init__(self, symbol):
		self._symbol = symbol

	def __repr__(self):
		return self._symbol

	def __str__(self):
		return self._symbol

	@abstractmethod
	def get_move(self):
		pass

class AIPlayer(Player):
	def __init__(self, *args, **kwargs):
		super(AIPlayer, self).__init__(*args)
		self._board = None
		self._algorithm = kwargs['algorithm']

	def _get_move_naive(self):
		legal_moves = self._board.legal_moves()
		# Return a random move picked from the list of legal moves
		random_move = legal_moves[
			random.randint(0, len(legal_moves) - 1)
			]
		row, column = random_move
		return row, column

	def _maxMove(self):
		print '_maxMove called, and state was '
		print self._board
		"""Return [x,y] pair that represents best move
			for the AI
		"""
		if self._board.game_over():
			return self._board.utility()

		best_move = 0
		legal_moves = self._board.legal_moves()
		for move in legal_moves:
			self._board.move(move[0], move[1])

			self._minMove()
			move_utility = self._board.utility()

			if move_utility > best_move:
				best_move = move

			self._board.undo_latest_move()

		if best_move == 0:
			return legal_moves[0]

		return best_move

	def _minMove(self):
		print '_minMove called, and state was '
		print self._board
		best_move = 0
		legal_moves = self._board.legal_moves()
		for move in legal_moves:
			self._board.move(move[0], move[1])

			self._maxMove()
			move_utility = self._board.utility()

			if move_utility > best_move:
				bestmove = move
			
			self._board.undo_latest_move()

		if best_move == 0:
			return legal_moves[0]

		return best_move

	def _get_move_minimax(self):
		# import pdb; pdb.set_trace
		return self._maxMove()

	def get_move(self, board):
		import copy
		self._board = copy.deepcopy(board)

		if self._algorithm == 'minimax':
			return self._get_move_minimax()
		else:
			return self._get_move_naive()

class HumanPlayer(Player):
	def get_move(self, board):
		self._board = board
		state = self._board.state
		legal_moves = self._board.legal_moves()
		while True:
			# If move was illegal, print error and allow user to
			# 	enter another move.
			try:
				row, column = raw_input(
					'Player {}: Enter a (row, column) pair from (0,1,2), or enter to skip:\n' \
					.format(self)) \
					.strip().split(',')
				row, column = int(row), int(column)
			except ValueError:
				print 'Please enter a valid (row,column) pair.'
			else:
				if [row,column] in legal_moves:
					return row, column
				else:
					print('Illegal move: Space already filled. Try again.')

class Board:
	def __init__(self):
		self._size = 3
		self.state = [[None for x in range(self._size)]
			for y in range(self._size)]
		self._player = self._players = None
		self._movestack = []

	AI = 'O'

	def __str__(self):
		buffer = ""
		for row in self.state:
			buffer += str(row) + '\n'
		return buffer

	def _win_horizontal(self):
		for row in self.state:
			if row[0] and row[0] == row[1] and row[0] == row[2]:
				return row[0]

	def _win_vertical(self):
		b = self.state
		for col in range(self._size):
			if b[0][col] and b[0][col] == b[1][col] and \
				b[0][col] == b[2][col]:
				return b[0][col]

	def _win_diagonals(self):
		b = self.state
		if (b[0][0] and b[0][0] == b[1][1] and b[0][0] == b[2][2]) \
			or \
			(b[2][0] and b[2][0] == b[1][1] and b[2][0] == b[0][2]):
			return b[0][0]

	def legal_moves(self):
		legal_moves = []
		for row in range(3):
			for col in range(3):
				if self.state[row][col] == None:
					legal_moves.append([row, col])
		return legal_moves

	def undo_latest_move(self):
		move_to_undo = self._movestack.pop()
		self.state[
			move_to_undo[0]][move_to_undo[1]
			] = None

	def draw(self):
		"""Return False if any board space has yet to be filled.
			and True if all spaces have been filled.
		"""
		for row in self.state:
			for col in row:
				if col == None:
					return False
		return True

	def winner(self):
		"""Return winner (string) if board in winning state,
			or None if not in winning state.
		"""
		return self._win_horizontal() or self._win_vertical() \
			or self._win_diagonals()

	def _is_legal_move(self, x, y):
		return not bool(self.state[x][y])

	def move(self, x, y):
		self.state[x][y] = self._player
		self._movestack.append([x,y])

	def change_player(self):
		if str(self._player) == 'O':
			self._player = self._players['X']
		else:
			self._player = self._players['O']

	def utility(self):
		if self.winner():
			return 1
		elif self.draw():
			return 0
		return -1

	def game_over(self):
		"""Return True if game is over and False if not.
		"""
		return bool(self.winner()) or self.draw()

	def play(self, firstplayer, ai):		
		self._players = {
			"X": HumanPlayer('X'),
			"O": AIPlayer('O', algorithm=ai) if ai else HumanPlayer('O')
			}

		self._player = self._players[firstplayer]

		while not self.game_over():
			print(self)
			row, column = self._player.get_move(self)
			self.move(row, column)
			self.change_player()

		if self.winner():
			print('{} won the game.'.format(
				self.winner()
				))
		elif self.draw():
			print('Draw')

if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description = 'Tic-tac-toe, optionally with AI'
		)
	parser.add_argument(
		'--firstplayer',
		'-f',
		type = str,
		help = 'Defaults to X.',
		choices = {'X', 'O'},
		default = 'X'
		)
	parser.add_argument(
		'--ai',
		type = str,
		help = 'Play against an AI (minimax|naive) player (AI always plays as O). Defaults to minimax.'
		)
	args = parser.parse_args()

	board = Board()
	board.play(args.firstplayer,args.ai)
