import IA

class ring:
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
	def __init__(self, name1: str, name2: str, IA: bool = False, gameMode = 2, Network = False, Server = True):
		"""
		:param name1: Name of the players 1
		:param name2: Name of the players 2
		"""

		self.__gameMode = gameMode
		self.__n: int = 11
		self._board = []
		self._player_to_play: int = 2
		self.__name1, self.__name2 = name1, name2
		self._ring_number_on_board: int = 0
		self._list_alignment = [[], [], []]
		self._list_possibilities_to_move = []
		self.list_mark_in_the_way = []
		self._IA = IA
		self._network = Network
		self.__server = Server

	def get_server(self):
		return self.__server

	def get_list_possibilities(self):
		return self._list_possibilities_to_move

	def get_server(self):
		return self.__server

	def is_server_mode(self):
		return self._network

	def get_gameMode(self):
		return self.__gameMode

	def set_list_possibilities(self, new_list_possibilities: list):
		self._list_possibilities_to_move = new_list_possibilities

	def get_IA(self):
		return self._IA

	def set_IA(self, new_IA: bool):
		self._IA = new_IA

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

	def get_ring_number_on_board(self):
		return self._ring_number_on_board

	def set_ring_number_on_board(self, new_ring_number_on_board: int):
		self._ring_number_on_board = new_ring_number_on_board

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
				elif isinstance(self._board[row][col], ring) and self._player_to_play == 1:
					print("*", end=" ")
				elif isinstance(self._board[row][col], ring) and self._player_to_play == 2:
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
			self._board[i][j] = ring(self._player_to_play, self.__name1)
		elif self._player_to_play == 2:
			self._board[i][j] = ring(self._player_to_play, self.__name2)

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

	def separate_the_rings_from_the_marks(self, position_y: int, position_x: int, vector_y: int, vector_x: int):
		if 0 <= position_x < self.__n and 0 <= position_y < self.__n:
			if self._board[position_y][position_x] == 1:
				self._list_possibilities_to_move.append((position_y, position_x))
				return self.separate_the_rings_from_the_marks(position_y + vector_y, position_x + vector_x, vector_y, vector_x)
			elif position_y + vector_y < self.__n and position_x + vector_x < self.__n and self._board[position_y][position_x] in [-1, -2]:
				self.list_mark_in_the_way.append((position_y, position_x))
				if self._board[position_y + vector_y][position_x + vector_x] == 1:
					self._list_possibilities_to_move.append((position_y + vector_y, position_x + vector_x))
				elif self._board[position_y + vector_y][position_x + vector_x] in [-1, -2]:
					return self.separate_the_rings_from_the_marks(position_y + vector_y, position_x + vector_x, vector_y, vector_x)

	def create_all_list_of_possibilities(self, position_y: int, position_x: int):
		for index, (i, j) in enumerate([(0, -1), (0, 1), (-1, 0), (1, 0), (-1, 1), (1, -1)]):

			if index < 2:
				self.separate_the_rings_from_the_marks(position_y + i, position_x + j, i, j)
			elif 2 <= index < 4:
				self.separate_the_rings_from_the_marks(position_y + i, position_x + j, i, j)
			else:
				self.separate_the_rings_from_the_marks(position_y + i, position_x + j, i, j)

	def delete_preview(self):
		for possibility in self._list_possibilities_to_move:
			if self._board[possibility[0]][possibility[1]] == -3:
				self._board[possibility[0]][possibility[1]] = 1
		self._list_possibilities_to_move = []

	def preview(self):
		for possibility in self._list_possibilities_to_move:
			self._board[possibility[0]][possibility[1]] = -3

	def move(self, start_position_x: int, start_position_y: int, end_position_x: int, end_position_y: int,
	         wining_move: bool = False):
		if 0 <= start_position_x < 11 and 0 <= start_position_y < 11 and 0 <= end_position_x < 11 and 0 <= end_position_y < 11:
			if self._board[end_position_x][end_position_y] in [-3, 1] and not wining_move:
				if isinstance(self._board[start_position_x][start_position_y], ring):
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
	def get_vectors(start_position_x: int, start_position_y: int, end_position_x: int, end_position_y: int) -> tuple[
		int, int]:
		vector_x = 0
		vector_y = 0

		if start_position_x < end_position_x:
			vector_x = 1
		elif start_position_x > end_position_x:
			vector_x = -1

		if start_position_y < end_position_y:
			vector_y = 1
		elif start_position_y > end_position_y:
			vector_y = -1

		return vector_x, vector_y

	def verify_not_ring_in_lign(self, start_position_x: int, start_position_y: int, end_position_x: int,
	                            end_position_y: int) -> bool:

		vector_x, vector_y = self.get_vectors(start_position_x, start_position_y, end_position_x, end_position_y)

		if start_position_x + vector_x == end_position_x and start_position_y + vector_y == end_position_y:
			return True
		if isinstance(self._board[start_position_x + vector_x][start_position_y + vector_y], ring):
			return False
		else:
			return self.verify_not_ring_in_lign(start_position_x + vector_x, start_position_y + vector_y,
			                                    end_position_x, end_position_y)

	def check_valid_jumps(self, start_position_x: int, start_position_y: int, end_position_x: int,
	                      end_position_y: int) -> bool:
		vector_x, vector_y = self.get_vectors(start_position_x, start_position_y, end_position_x, end_position_y)

		current_position_x, current_position_y = start_position_x, start_position_y

		while current_position_x != end_position_x or current_position_y != end_position_y:
			if self._board[current_position_x + vector_x][current_position_y + vector_y] in [-1, -2]:
				if current_position_x + vector_x * 2 == end_position_x and current_position_y + vector_y * 2 == end_position_y:
					return True
				elif self._board[current_position_x + vector_x * 2][current_position_y + vector_y * 2] not in [-1, -2]:
					return False
			current_position_x += vector_x
			current_position_y += vector_y

		return True

	def possible_to_move(self, start_position_x: int, start_position_y: int, end_position_x: int,
	                     end_position_y: int) -> tuple[bool, None | str]:

		"""
		:param start_position_x: The X coordinate of the start position.
		:param start_position_y: The Y coordinate of the start position.
		:param end_position_x: The X coordinate of the end position.
		:param end_position_y: The Y coordinate of the end position.
		:return: True if the move is possible, False otherwise.
		"""
		if 0 <= start_position_x < 11 and 0 <= start_position_y < 11 and 0 <= end_position_x < 11 and 0 <= end_position_y < 11:
			coefficient_diagonal_x = (end_position_x - start_position_x) / 1
			coefficient_diagonal_y = (end_position_y - start_position_y) / -1
			if isinstance(self._board[end_position_x][end_position_y], ring) or self._board[end_position_x][
				end_position_y] in [-1, -2]:
				return False, "Tu ne peux pas te déplacer sur une anneau ou une marque !"
			elif not (start_position_x == end_position_x and start_position_y != end_position_y or start_position_x != end_position_x and start_position_y == end_position_y or coefficient_diagonal_x == coefficient_diagonal_y):
				return False, "Mouvemnt impossible !"
			elif not self.check_valid_jumps(start_position_x, start_position_y, end_position_x, end_position_y):
				return False, "Vous devez vous arrêter avant un anneau !"
			elif not self.verify_not_ring_in_lign(start_position_x, start_position_y, end_position_x, end_position_y):
				return False, 'You can not move on a ring !'
			elif start_position_x == end_position_x and start_position_y != end_position_y:
				return True, None
			elif start_position_x != end_position_x and start_position_y == end_position_y:
				return True, None
			elif coefficient_diagonal_x == coefficient_diagonal_y:
				return True, None
			else:
				return False, "Mouvemnt impossible !"

	def change_mark_on_move(self, start_position_x: int, start_position_y: int, end_position_x: int,
	                        end_position_y: int):
		vector_x, vector_y = self.get_vectors(start_position_x, start_position_y, end_position_x, end_position_y)

		new_x = start_position_x + vector_x
		new_y = start_position_y + vector_y
		current_value = self._board[new_x][new_y]

		if start_position_x == end_position_x and start_position_y == end_position_y:
			return 0

		elif current_value in (-1, -2):
			self._board[new_x][new_y] = -2 if current_value == -1 else -1
			return 1 + self.change_mark_on_move(new_x, new_y, end_position_x, end_position_y)

		else:
			return self.change_mark_on_move(start_position_x + vector_x, start_position_y + vector_y, end_position_x,
			                                end_position_y)

	def check_all_win(self, start_position_x: int, start_position_y: int, end_position_x: int,
	                        end_position_y: int):
		vector_x, vector_y = self.get_vectors(start_position_x, start_position_y, end_position_x, end_position_y)

		new_x = start_position_x + vector_x
		new_y = start_position_y + vector_y
		current_value = self._board[new_x][new_y]

		if start_position_x == end_position_x and start_position_y == end_position_y:
			return 0

		elif current_value in (-1, -2):
			if self.check_win(new_x, new_y):
				self._board[new_x][new_y] = 1
				return True
			else:
				return self.check_all_win(new_x, new_y, end_position_x, end_position_y)

	def win_game(self, number_of_ring_win_player_one: int, number_of_ring_win_player_two: int):
		if self.__gameMode == 1 and( number_of_ring_win_player_one == 3 or number_of_ring_win_player_two == 3):
			return True
		elif self.__gameMode == 2 and (number_of_ring_win_player_one == 1 or number_of_ring_win_player_two == 1):
			return True
		else:
			return False

if __name__ == '__main__':
	logic_obj = Logic('Luc', 'Jean-Marc')
	logic_obj.create_board()
	logic_obj.put(0, 7)
	logic_obj.display()
