#! /usr/bin/env python

import argparse
import random
from abc import abstractmethod

class Player:
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
	def get_move(self, legal_moves):
		random_move = legal_moves[
			random.randint(0, len(legal_moves) - 1)
			]
		row, column = random_move
		return row, column

class HumanPlayer(Player):
	def get_move(self, legal_moves):
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
		self._board = [[None for x in range(self._size)]
			for y in range(self._size)]
		self._player = self._players = None

	AI = 'O'

	def __str__(self):
		buffer = ""
		for row in self._board:
			buffer += str(row) + '\n'
		return buffer

	def _win_horizontal(self):
		for row in self._board:
			if row[0] and row[0] == row[1] and row[0] == row[2]:
				return row[0]

	def _win_vertical(self):
		b = self._board
		for col in range(self._size):
			if b[0][col] and b[0][col] == b[1][col] and \
				b[0][col] == b[2][col]:
				return b[0][col]

	def _win_diagonals(self):
		b = self._board
		if (b[0][0] and b[0][0] == b[1][1] and b[0][0] == b[2][2]) \
			or \
			(b[2][0] and b[2][0] == b[1][1] and b[2][0] == b[0][2]):
			return b[0][0]

	def draw(self):
		"""Return False if any board space has yet to be filled.
			and True if all spaces have been filled.
		"""
		for row in self._board:
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
		return not bool(self._board[x][y])

	def _move(self, x, y):
		self._board[x][y] = self._player

	def _change_player(self):
		if str(self._player) == 'O':
			self._player = self._players['X']
		else:
			self._player = self._players['O']

	def _game_over(self):
		"""Return True if game is over and False if not.
		"""
		return bool(self.winner()) or self.draw()

	def _legal_moves(self):
		legal_moves = []
		for row in range(self._size):
			for col in range(self._size):
				if self._board[row][col] == None:
					legal_moves.append([row, col])
		return legal_moves

	def play(self, firstplayer, ai):		
		self._players = {
			"X": HumanPlayer('X'),
			"O": AIPlayer('O') if ai else HumanPlayer('O')
			}

		self._player = self._players[firstplayer]

		while not self._game_over():
			print(self)
			row, column = self._player.get_move(
				self._legal_moves()
				)
			self._move(row, column)
			self._change_player()

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
		help = 'If not specified, defaults to X.',
		choices = {'X', 'O'},
		default = 'X'
		)
	parser.add_argument(
		'--ai',
		action = 'store_true',
		help = 'Play against an AI player (AI always plays as O). Defaults to human-vs-human.'
		)
	args = parser.parse_args()

	board = Board()
	board.play(args.firstplayer,args.ai)
