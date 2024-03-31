class Pawn:
	def __init__(self, player, name):
		"""
		:param player: player number 1 or 2
		:param name: The name of the players
		"""
		self.__player = player
		self._name = name

	def get_player(self):
		return self.__player


class Logic:
	def __init__(self, name1, name2):
		"""
		:param name1: Name of the players 1
		:param name2: Name of the players 2
		"""
		self.__n = 11
		self._board = []
		self._player_to_play = 1
		self.__name1, self.__name2 = name1, name2

	def get_current_player(self) -> int:
		return self._player_to_play

	def get_board(self):
		return self._board

	def get_player_to_play(self) -> int:
		return self._player_to_play

	def set_player_to_play(self, new_payer_to_play: int):
		self._player_to_play = new_payer_to_play

	def create_board(self):
		for (a, b, c) in [(6, 4, 1), (4, 7, 0), (3, 8, 0), (2, 9, 0), (1, 10, 0), (1, 9, 1), (0, 10, 1), (0, 9, 2),
		                  (0, 8, 3), (0, 7, 4), (1, 4, 6)]:
			# nine is a null box & one is an empty box
			board_anex = [9 for _ in range(a)] + [1 for _ in range(b)] + [9 for _ in range(c)]
			self._board.append(board_anex)

	def display(self):
		self.create_board()
		for row in range(self.__n):
			print(" " * row, end=" ")
			for col in range(self.__n):
				if self._board[row][col] == 9:
					print(" ", end=" ")
				elif self._board[row][col] == 1:
					print("0", end=" ")
				elif isinstance(self._board[row][col], Pawn) and self._player_to_play == 1:
					print("*", end=" ")
				elif isinstance(self._board[row][col], Pawn) and self._player_to_play == 2:
					print("_", end=" ")
			print("")

	def possible_to_put(self, i: int, j: int):
		"""
		:param i: Coordinate X of player
		:param j: Coordinate Y of player
		:return: boolean True or False
		"""
		return True if 0 <= i < self.__n and 0 <= j < self.__n and self._board[i][j] == 1 else False

	def put(self, i, j):
		if self.possible_to_put(i, j):
			if self._player_to_play == 1:
				self._board[i][j] = Pawn(self._player_to_play, self.__name1)
			elif self._player_to_play == 2:
				self._board[i][j] = Pawn(self._player_to_play, self.__name2)

		else:
			print("Cette position est impossible !")

	def one_direction(self, position_y, position_x, i, j):
		"""
			Calculate the length of a sequence of opponent's pieces in one direction.

			:param position_y: The Y coordinate of the current position.
			:param position_x: The X coordinate of the current position.
			:param i: The change in X direction (vector).
			:param j: The change in Y direction (vector).
			:return: The number of marks of the current player on the liners of the player's position.
	"""
		return 1 + self.one_direction(position_y + i, position_x + j, i, j) \
			if (0 <= position_x + j < self.__n
			    and 0 <= position_y + i < self.__n
			    and self._board[position_y + i][position_x + j] == (-self._player_to_play)) else 0

	def all_direction(self, position_y, position_x):
		"""
			Check if there is a winning sequence in any direction.

			:param position_y: The Y coordinate of the current position.
			:param position_x: The X coordinate of the current position.
			:return: True if there's a winning sequence in any direction, False otherwise.
		"""
		column, line, slash, = 0, 0, 0
		for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

			if index < 2:
				column += self.one_direction(position_y, position_x, i, j)
			elif 2 <= index < 4:
				line += self.one_direction(position_y, position_x, i, j)
			else:
				slash += self.one_direction(position_y, position_x, i, j)

		return True if column + 1 >= 5 or line + 1 >= 5 or slash + 1 >= 5 else False


if __name__ == '__main__':
	logic_obj = Logic('Luc', 'Jean-Marc')
	logic_obj.create_board()
	logic_obj.put(0, 7)
	logic_obj.display()
