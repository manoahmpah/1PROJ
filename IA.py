import random
import time


class IA:
	def __init__(self, logic):
		self._object_logic = logic
		self._put = []
		self._number_of_rings = 5

	def put_random(self):
		"""Put a random piece on the board."""
		x = random.randint(0, 10)
		y = random.randint(0, 10)
		if self._object_logic.get_board()[y][x] == 1:
			self._object_logic.put(x, y)
			self._put.append((x, y))
			# self._object_logic.set_ring_number_on_board(self._object_logic.get_ring_number_on_board() + 1)
		else:
			self.put_random()

	def move_random(self):
		"""Move randomly a piece on the board"""
		random_index_ring = random.randint(0, self._number_of_rings - 1)
		position_to_move_x, position_to_move_y = self._put[random_index_ring]
		self._object_logic.create_all_list_of_possibilities(position_to_move_x, position_to_move_y)
		if self._object_logic.check_win(position_to_move_x, position_to_move_y):
			self._object_logic.delete_on_alignment()
			self._put.pop(random_index_ring)
			self._number_of_rings -= 1

		arrival_position = self._object_logic.get_list_possibilities()[random.randint(0, len(self._object_logic.get_list_possibilities()) - 1)]

		self._object_logic.change_mark_on_move(position_to_move_x, position_to_move_y, arrival_position[0], arrival_position[1])

		self._object_logic.move(position_to_move_x, position_to_move_y, arrival_position[0], arrival_position[1])
		self._put[random_index_ring] = (arrival_position[0], arrival_position[1])
		self._object_logic.set_list_possibilities([])