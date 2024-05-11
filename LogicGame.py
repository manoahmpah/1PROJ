from typing import List, Any


class Pawn:
	def __init__(self, player: int, name: str):
		"""
		:param player: player number 1 or 2
		:param name: The name of the players
		"""
		self.__player = player
		self._name = name
		self._selected = False

	def get_player(self) -> int:
		return self.__player

	def get_selected(self) -> bool:
		return self._selected

	def set_selected(self, new_selected: bool):
		self._selected = new_selected


class Logic:
	def __init__(self, name1: str, name2: str):
		"""
		:param name1: Name of the players 1
		:param name2: Name of the players 2
		"""
		self.__n: int = 11
		self._board = []
		self._player_to_play: int = 2
		self.__name1, self.__name2 = name1, name2
		self._pawn_number_on_board: int = 0
		self._list_alignment = [[], [], []]

	def set_list_alignment(self, new_list_alignment: list):
		self._list_alignment = new_list_alignment

	def get_list_alignment(self):
		return self._list_alignment

	def get_current_player(self) -> int:
		return self._player_to_play

	def get_board(self):
		return self._board

	def set_coord_board(self, x, y, value):
		self._board[x][y] = value

	def get_player_to_play(self) -> int:
		return self._player_to_play

	def set_player_to_play(self, new_payer_to_play: int):
		self._player_to_play = new_payer_to_play

	def get_pawn_number_on_board(self):
		return self._pawn_number_on_board

	def set_pawn_number_on_board(self, new_pawn_number_on_board: int):
		self._pawn_number_on_board = new_pawn_number_on_board

	def get_name1(self):
		return self.__name1

	def get_name2(self):
		return self.__name2

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
					print("+", end=" ")
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

	def put(self, i: int, j: int):
		if self._player_to_play == 1:
			self._board[i][j] = Pawn(self._player_to_play, self.__name1)
		elif self._player_to_play == 2:
			self._board[i][j] = Pawn(self._player_to_play, self.__name2)

	def append_alignment_in_list(self, position_y: int, position_x: int, i: int, j: int, index_list_alignment: int):
		if 0 <= position_x + j < self.__n and 0 <= position_y + i < self.__n:
			if self._board[position_y + i][position_x + j] == (-self._player_to_play):
				self._list_alignment[index_list_alignment].append((position_y + i, position_x + j))

	def aligned_mark_number(self, position_y: int, position_x: int, i: int, j: int, index_list_alignment: int) -> int:
		"""
		Calculate the length of a sequence of opponent's pieces in one direction.

		:param index_list_alignment:
		:param position_y: The Y coordinate of the current position.
		:param position_x: The X coordinate of the current position.
		:param i: The change in X direction (vector).
		:param j: The change in Y direction (vector).
		:return: The number of marks of the current player on the liners of the player's position.
		"""
		self.append_alignment_in_list(position_y, position_x, i, j, index_list_alignment)

		if 0 <= position_x + j < self.__n and 0 <= position_y + i < self.__n:
			if self._board[position_y + i][position_x + j] == (-self._player_to_play):
				return 1 + self.aligned_mark_number(position_y + i, position_x + j, i, j, index_list_alignment)
			else:
				return 0
		else:
			return 0

	def check_win(self, position_y: int, position_x: int) -> bool:
		column, line, slash, = 0, 0, 0
		for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

			if index < 2:
				column += self.aligned_mark_number(position_y, position_x, i, j, 0)
			elif 2 <= index < 4:
				line += self.aligned_mark_number(position_y, position_x, i, j, 1)
			else:
				slash += self.aligned_mark_number(position_y, position_x, i, j, 2)

		return True if column + 1 >= 5 or line + 1 >= 5 or slash + 1 >= 5 else False

	def move(self, start_position_x: int, start_position_y: int, end_position_x: int, end_position_y: int, wining_move: bool = False):
		if 0 <= start_position_x < 11 and 0 <= start_position_y < 11 and 0 <= end_position_x < 11 and 0 <= end_position_y < 11 :
			if self._board[end_position_x][end_position_y] == 1 and not wining_move:
				if isinstance(self._board[start_position_x][start_position_y], Pawn):
					self.put(end_position_x, end_position_y)
					self._board[start_position_x][start_position_y] = -self._player_to_play
				else:
					print("not the good player to player")
			elif wining_move:
				self.put(end_position_x, end_position_y)
				self._board[start_position_x][start_position_y] = 1
		else:
			print("impossible to move !")

	def delete_on_alignment(self):
		for list_coord_alignment in self._list_alignment:
			if len(list_coord_alignment) >= 4:
				for index_coord_to_delete in range(4):
					self._board[list_coord_alignment[index_coord_to_delete][0]][
						list_coord_alignment[index_coord_to_delete][1]] = 1

	@staticmethod
	def possible_to_move(start_position_x: int, start_position_y: int, end_position_x: int,
						 end_position_y: int) -> bool:
		"""
		:param start_position_x: The X coordinate of the start position.
        :param start_position_y: The Y coordinate of the start position.
        :param end_position_x: The X coordinate of the end position.
        :param end_position_y: The Y coordinate of the end position.
        :return: True if the move is possible, False otherwise.
        """
		if 0 <= start_position_x < 11 and 0 <= start_position_y < 11 and 0 <= end_position_x < 11 and 0 <= end_position_y < 11:
			if start_position_x == end_position_x or start_position_y == end_position_y:
				return True
			elif (end_position_x - start_position_x) == -(end_position_y - start_position_y):
				return True
			else:
				return False
		else:
			return False


if __name__ == '__main__':
	logic_obj = Logic('Luc', 'Jean-Marc')
	logic_obj.create_board()
	logic_obj.put(0, 7)
	logic_obj.display()