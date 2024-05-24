import random
import time

from LogicGame import Logic


class IA:
    def __init__(self, logic):
        self._object_logic = logic
        self._put = []
        self._number_of_ring = 5

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
                # Adjust the number of rings
                self._number_of_ring -= 1
                if self._number_of_ring < len(self._put):
                    self._put.pop(random_index_ring)

        self._object_logic.set_list_possibilities([])


if __name__ == '__main__':
    logic_obj = Logic('Luc', 'Jean-Marc')
    logic_obj.create_board()
    ia = IA(logic_obj)

