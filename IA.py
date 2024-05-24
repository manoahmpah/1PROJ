import random
import time

from LogicGame import Logic


class IA:
<<<<<<< HEAD
    def __init__(self, logic):
        self._object_logic = logic
        self._put = []

    def put_random(self):
        """Put a random piece on the board."""
        while True:
            x = random.randint(0, 10)
            y = random.randint(0, 10)
            if self._object_logic.possible_to_put(x, y):
                self._object_logic.put(x, y)
                self._put.append((x, y))
                break

    def move_random(self):
        """Move randomly a piece on the board"""
        if not self._put:
            return

        random_index_ring = random.randint(0, len(self._put) - 1)
        position_to_move_x, position_to_move_y = self._put[random_index_ring]
        self._object_logic.create_all_list_of_possibilities(position_to_move_x, position_to_move_y)
        possibilities = self._object_logic.get_list_possibilities()

        if possibilities:
            arrival_position = possibilities[random.randint(0, len(possibilities) - 1)]

            self._object_logic.change_mark_on_move(position_to_move_x, position_to_move_y, arrival_position[0], arrival_position[1])

            self._object_logic.move(position_to_move_x, position_to_move_y, arrival_position[0], arrival_position[1])

            self._put[random_index_ring] = (arrival_position[0], arrival_position[1])

            if self._object_logic.check_win(arrival_position[0], arrival_position[1]):
                self._object_logic.delete_on_alignment()
        self._object_logic.set_list_possibilities([])

if __name__ == '__main__':
    logic_obj = Logic('Luc', 'Jean-Marc')
    logic_obj.create_board()
    ia = IA(logic_obj)
=======
	def __init__(self, logic):
		self._object_logic = logic
		self._put = []
		self._number_of_ring = 5

	def put_random(self):
		"""Put a random piece on the board."""
		x = random.randint(0, 10)
		y = random.randint(0, 10)
		if self._object_logic.possible_to_put(x, y):
			self._object_logic.put(x, y)
			self._put.append((x, y))
			# self._object_logic.set_ring_number_on_board(self._object_logic.get_ring_number_on_board() + 1)
		else:
			self.put_random()

	def move_random(self):
		"""Move randomly a piece on the board"""
		random_index_ring = random.randint(0, self._number_of_ring - 1)
		position_to_move_x, position_to_move_y = self._put[random_index_ring]
		self._object_logic.create_all_list_of_possibilities(position_to_move_x, position_to_move_y)

		if self._object_logic.check_win(position_to_move_x, position_to_move_y):
			ring_index_to_delete = random.randint(0, self._number_of_ring - 1)
			ring_index_to_delete_x, ring_index_to_delete_y = self._put[ring_index_to_delete]
			self._object_logic.get_board()[ring_index_to_delete_x][ring_index_to_delete_y] = 1
			self._object_logic.delete_on_alignment()

			self._number_of_ring -= 1
			self._put.pop(random_index_ring)


		arrival_position = self._object_logic.get_list_possibilities()[random.randint(0, len(self._object_logic.get_list_possibilities()) - 1)]
>>>>>>> 772da56eff3f9166f91b73db60ad58b9eb84674c


