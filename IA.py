import random
import time


class IA:
	def __init__(self, logic):
		self._object_logic = logic
		self._put = []

	def put_random(self):
		"""Put a random piece on the board."""
		x = random.randint(0, 10)
		y = random.randint(0, 10)
		if self._object_logic.get_board()[y][x] == 1:
			self._object_logic.put(x, y)
			self._object_logic.set_ring_number_on_board(self._object_logic.get_ring_number_on_board() + 1)
			self._put.append((x, y))
		else:
			self.put_random()

	def move_random(self):
		"""Move randomly a piece on the board"""

		random_index_ring = random.randint(0, 5)
		position_to_move_x, position_to_move_y = self._put[random_index_ring]
		self._object_logic.create_possible_moves(position_to_move_x, position_to_move_y)
		print(self._object_logic.get_possible_moves())
