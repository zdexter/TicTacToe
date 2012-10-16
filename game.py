#! /usr/bin/env python

import argparse

class TicTacToe:
	def __init__(self):
		self._board_pieces = {
			"X": "X",
			"O": "O",
			"skip": "skip"
		}

		self._board_size = 3
		self._board = [[None for x in range(self._board_size)]
			for y in range(self._board_size)]
		self._num_moves = 0

	def _check_win(self, i):
		if i == self._board_size - 1:
			self._render_board()
			print('Win')
			return True
		return False

	def _render_board(self):
		for row in self._board:
			print row

	def _move(self, x, y, board_piece):
		if self._board[x][y] == None:
			self._board[x][y] = board_piece
			self._num_moves += 1

		for i in range(self._board_size):
			if self._board[x][i] != board_piece:
				break

			if self._check_win(i):
				return True

		for i in range(self._board_size):
			if self._board[i][y] != board_piece:
				break

			if self._check_win(i):
				 return True

		if x == y:
			for i in range(self._board_size):
				if self._board[i][i] != board_piece:
					break

				if self._check_win(i):
					 return True

		for i in range(self._board_size):
			if self._board[i][(self._board_size - 1) - i] != board_piece:
				break

			if self._check_win(i):
				 return True

		if self._num_moves == (self._board_size ** 2 - 1):
			print 'Draw.'
			return True

		return False

	def _get_move(self, last_move):
		print last_move
		if last_move == 'O':
			return 'X'
		return 'O'

	def play(self, firstmove):
		win = False
		move = firstmove
		while not win:
			self._render_board()
			try:
				column, row = raw_input(
					'Player {}: Enter a (row, column) pair from (0,1,2), or enter to skip:\n' \
					.format(move)) \
					.strip().split(',')
				column, row = int(column), int(row)
			except ValueError:
				print 'Skipped turn.'
			else:
				win = self._move(column, row, move)
			move = self._get_move(move)

if __name__ == "__main__":
	game = TicTacToe()

	parser = argparse.ArgumentParser(
		description = 'Tic-tac-toe, optionally with AI'
		)
	parser.add_argument(
		'--firstmove',
		'-f',
		type = str,
		help = 'If not specified, defaults to X.',
		choices = {'X', 'O'},
		default = 'X'
		)

	args = parser.parse_args()
	game.play(args.firstmove)
