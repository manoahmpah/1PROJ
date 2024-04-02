import pygame
from LogicGame import Logic, Pawn
import cProfile


class GUIPlateau:
	def __init__(self):
		pygame.init()
		# Windows game
		self.__width = 1080
		self.__height = 720
		self.__screen = pygame.display.set_mode((self.__width, self.__height))
		pygame.display.set_caption('yinsh')
		self.__running = True
		self.__background = (170, 184, 197)

		self.__logic_obj = Logic('Maëlys', 'Léa')
		self._create_board = self.__logic_obj.create_board()
		self._get_board = self.__logic_obj.get_board()

		self._rect_all = pygame.Rect(0, 0, self.__width, self.__height)
		self._rect_board = pygame.Rect(self._rect_all.centerx - self.__width / 2.4,
		                               self._rect_all.centery - self.__height / 2.4, self.__width / 1.2,
		                               self.__height / 1.2)
		self._rect_name1 = pygame.Rect(self._rect_all.left + 10, self._rect_all.centery - 120, 100, 50)

		self._rect_name2 = pygame.Rect(self._rect_all.left + 10, self._rect_all.centery - 20, 100, 50)
		self._half_dim_hit_box = 25
		self._padding_rect = 30

		self._position_points = []

		self._rect_width = self._half_dim_hit_box * 2 + 4
		self._rect_height = self._half_dim_hit_box * 2

		self._number_click = 1
		self._position_click_x, self._position_click_y = -1, -1
		self._click_x_p1, self._click_y_p1 = None, None
		self._click_x_p2, self._click_y_p2 = None, None

	def transform_cord_to_pos(self, x, y) -> tuple:
		return int(y // 51) - 2, int(((x - (30 * ((y // 51) - 2))) // 60) - 1)

	def exact_position(self, x: int, y: int) -> tuple:
		for point in self._position_points:
			if (point['pos_x'] - 30 < x < point['pos_x'] + 30) and (point['pos_y'] - 25 < y < point['pos_y'] + 25):
				return self.transform_cord_to_pos(point['pos_x'], point['pos_y'])

	def hit_box(self) -> tuple:
		x, y = pygame.mouse.get_pos()
		if self._position_click_y == -1 and self._position_click_x == -1:
			self._position_click_x, self._position_click_y = self.exact_position(x, y) if self.exact_position(x,
			                                                                                                  y) else (
				-1, -1)

			if self.__logic_obj.possible_to_put(self._position_click_x, self._position_click_y):
				self.__logic_obj.put(self._position_click_x, self._position_click_y)
				self.__logic_obj.set_player_to_play((self.__logic_obj.get_player_to_play() % 2) + 1)
				self.__logic_obj.set_pawn_number_on_board(self.__logic_obj.get_pawn_number_on_board() + 1)

			else:
				print('Impossible to put')

		return self._position_click_x, self._position_click_y

	def reinitialise_click(self):
		self._position_click_x, self._position_click_y = -1, -1

	def display_gui(self):
		for row in range(len(self._get_board)):
			for col in range(len(self._get_board[row])):
				pos_x, pos_y = self.calculate_position(row, col)
				self.draw_circles_and_lines(row, col, pos_x, pos_y)

	def calculate_position(self, row: int, col: int) -> tuple:
		dimension = self._padding_rect * 2
		pos_x = self._rect_board.left + col * dimension + row * self._padding_rect
		pos_y = (self._rect_board.top + row * self._padding_rect) * 1.7
		return pos_x, pos_y

	# problem
	def draw_circles_and_lines(self, row: int, col: int, pos_x: int, pos_y: int):
		if self._get_board[row][col] != 9:
			self._position_points.append({'pos_x': pos_x, 'pos_y': pos_y})
			self.draw_adjacent_lines(row, col, pos_x, pos_y)

		if isinstance(self._get_board[row][col], Pawn):
			player = self._get_board[row][col].get_player()
			color = (255, 255, 255) if player == 1 else (0, 0, 0)
			pygame.draw.circle(self.__screen, color, (pos_x, pos_y), 25, 7)
			if self._get_board[row][col].get_selected():
				pygame.draw.circle(self.__screen, color, (pos_x, pos_y), 15)

		if self._get_board[row][col] == -1:
			pygame.draw.circle(self.__screen, (255, 255, 255), (pos_x, pos_y), 15)
		elif self._get_board[row][col] == -2:
			pygame.draw.circle(self.__screen, (0, 0, 0), (pos_x, pos_y), 15)

	def draw_adjacent_lines(self, row, col, pos_x, pos_y):
		board = self._get_board
		if col + 1 < len(board[row]) and board[row][col + 1] != 9:
			col_pos = self.calculate_position(row, col + 1)
			pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y), col_pos, 2)

		if row + 1 < len(board):
			if col - 1 < len(board) and board[row + 1][col - 1] != 9:
				diag_col_pos = self.calculate_position(row + 1, col - 1)
				pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y), diag_col_pos, 2)

			if board[row + 1][col] != 9:
				next_row_pos = self.calculate_position(row + 1, col)
				pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y), next_row_pos, 2)

	def move_gui(self):
		x, y = pygame.mouse.get_pos()
		exact_pos = self.exact_position(x, y)
		if exact_pos is None:
			print('Please press a pawn !')
			return

		x, y = exact_pos
		board_piece = self._get_board[x][y]
		current_player = self.__logic_obj.get_player_to_play()

		if (self._number_click == 1 and isinstance(board_piece, Pawn)
				and board_piece.get_player() == current_player):
			self._click_x_p1, self._click_y_p1 = x, y
			board_piece.set_selected(True)
			self._number_click = 2

		elif self._number_click == 2:
			if x == self._click_x_p1 and y == self._click_y_p1:
				self._get_board[x][y].set_selected(False)

				self._number_click = 1
			else:
				self._click_x_p2, self._click_y_p2 = x, y
				self._number_click = 1
				self.__logic_obj.move(self._click_x_p1, self._click_y_p1, self._click_x_p2, self._click_y_p2)
				self._get_board[x][y].set_selected(False)

				self.__logic_obj.set_player_to_play(current_player % 2 + 1)

		else:
			print('please press a pawn !')

		self.player_name_display()
		self.display_gui()
		pygame.display.flip()

	def create_text_name(self, text: str, rect, color: tuple, color_bg: tuple, font_size: int):
		pygame.draw.rect(self.__screen, color_bg, rect)
		font = pygame.font.Font(None, font_size)
		name = font.render(text, True, color)
		text_rect = name.get_rect()
		text_rect.center = rect.center
		self.__screen.blit(name, text_rect)

	def player_name_display(self):
		color_bg_name1 = (255, 255, 255) if self.__logic_obj.get_player_to_play() == 1 else (170, 184, 197)
		if self.__logic_obj.get_player_to_play() == 2:
			color_font_name2 = (255, 255, 255)
			color_bg_name2 = (0, 0, 0)
		else:
			color_font_name2 = (0, 0, 0)
			color_bg_name2 = (170, 184, 197)

		self.create_text_name(self.__logic_obj.get_name1(), self._rect_name1, (0, 0, 0), color_bg_name1, 29)
		self.create_text_name(self.__logic_obj.get_name2(), self._rect_name2, color_font_name2, color_bg_name2, 29)

	def run(self):
		self.__screen.fill(self.__background)
		self.player_name_display()
		self.display_gui()
		pygame.display.flip()

		while self.__running:
			event = pygame.event.poll()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.__logic_obj.get_pawn_number_on_board() < 10:
					self.hit_box()
					self.reinitialise_click()
					self.player_name_display()
					self.display_gui()
					pygame.display.flip()
				else:
					self.move_gui()
			elif event.type == pygame.QUIT:
				self.__running = False
				pygame.quit()


if __name__ == "__main__":
	plateau = GUIPlateau()
	plateau.run()

# Importez le module cProfile


# # Fonction pour exécuter le script avec cProfile
# def profile_code():
# 	plateau = GUIPlateau()
# 	plateau.run()
#
#
# # Exécutez le script avec cProfile
# cProfile.run('profile_code()', 'profile_stats')
#
# # Importez le module pstats pour analyser les résultats
# import pstats
#
# # Chargez les statistiques de profilage à partir du fichier profile_stats
# stats = pstats.Stats('profile_stats')
#
# # Affichez les statistiques triées par temps cumulé
# stats.strip_dirs().sort_stats('cumulative').print_stats()
