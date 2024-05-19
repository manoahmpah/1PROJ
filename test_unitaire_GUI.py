import unittest
from LogicGame import Logic, Pawn


class TestLogicMethods(unittest.TestCase):

	def setUp(self):
		self.logic_obj = Logic('Luc', 'Jean-Marc')
		self.logic_obj.create_board()

	def test_get_current_player(self):
		self.assertEqual(self.logic_obj.get_current_player(), 2)

	def test_get_player_to_play(self):
		self.assertEqual(self.logic_obj.get_player_to_play(), 2)

	def test_set_player_to_play(self):
		self.logic_obj.set_player_to_play(1)
		self.assertEqual(self.logic_obj.get_player_to_play(), 1)

	def test_get_pawn_number_on_board(self):
		self.assertEqual(self.logic_obj.get_pawn_number_on_board(), 0)

	def test_set_pawn_number_on_board(self):
		self.logic_obj.set_pawn_number_on_board(5)
		self.assertEqual(self.logic_obj.get_pawn_number_on_board(), 5)

	def test_get_name1(self):
		self.assertEqual(self.logic_obj.get_name1(), 'Luc')

	def test_get_name2(self):
		self.assertEqual(self.logic_obj.get_name2(), 'Jean-Marc')

	def test_create_board(self):
		self.assertEqual(len(self.logic_obj.get_board()), 11)
		self.assertEqual(len(self.logic_obj.get_board()[0]), 11)

	def test_possible_to_put(self):
		self.assertFalse(self.logic_obj.possible_to_put(0, 0))
		self.assertTrue(self.logic_obj.possible_to_put(6, 4))

	def test_put(self):
		self.logic_obj.put(0, 0)
		self.assertIsInstance(self.logic_obj.get_board()[0][0], Pawn)

	def test_move(self):
		self.logic_obj.put(0, 7)
		self.logic_obj.move(0, 7, 1, 7)
		self.assertIsInstance(self.logic_obj.get_board()[1][7], Pawn)


if __name__ == '__main__':
	unittest.main()
