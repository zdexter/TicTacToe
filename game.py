#! /usr/bin/env python

import argparse

class Board:
	def __init__(self):
		self._size = 3
		self._board = [[None for x in range(self._size)]
			for y in range(self._size)]

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

	def _move(self, x, y, player):
		self._board[x][y] = player

	def _update_player(self, current_player):
		return 'X' if current_player == 'O' else 'O'

	def _game_over(self):
		"""Return True if game is over and False if not.
		"""
		return bool(self.winner()) or self.draw()

	def play(self, firstplayer, ai):
		player = firstplayer

		while not self._game_over():
			print(self)

			legal_move = False
			while not legal_move:
				# If move was illegal, print error and allow user to
				# 	enter another move.
				try:
					row, column = raw_input(
						'Player {}: Enter a (row, column) pair from (0,1,2), or enter to skip:\n' \
						.format(player)) \
						.strip().split(',')
					row, column = int(row), int(column)
				except ValueError:
					print 'Please enter a valid (row,column) pair.'
				else:
					if self._is_legal_move(row, column):
						legal_move = True

						self._move(row, column, player)
						player = self._update_player(player)
					else:
						print('Illegal move: Space already filled. Try again.')

		if self.winner():
			print(self.winner() + ' won the game.')
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
