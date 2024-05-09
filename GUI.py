import pygame
from LogicGame import Logic, Pawn


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

		self._move_click = 1
		self._position_click_x, self._position_click_y = -1, -1
		self._click_x_p1, self._click_y_p1 = None, None
		self._click_x_p2, self._click_y_p2 = None, None

		self._refresh = True

		self._rect_error = pygame.Rect(self._rect_all.centerx - 100, self._rect_all.bottom - 100, 200, 50)
		self._error_message = ""

	def transform_cord_to_pos(self, x, y) -> tuple:
		return int(y // 51) - 2, int(((x - (30 * ((y // 51) - 2))) // 60) - 1)

	def pixel_to_coordinate_transformation(self, x: int, y: int) -> tuple:
		for point in self._position_points:
			if (point['pos_x'] - 30 < x < point['pos_x'] + 30) and (point['pos_y'] - 25 < y < point['pos_y'] + 25):
				return self.transform_cord_to_pos(point['pos_x'], point['pos_y'])

	def hit_box(self) -> tuple:
		pixel_x, pixel_y = pygame.mouse.get_pos()

		if self._position_click_y == -1 and self._position_click_x == -1:
			self._position_click_x, self._position_click_y = self.pixel_to_coordinate_transformation(pixel_x, pixel_y) if self.pixel_to_coordinate_transformation(pixel_x, pixel_y) else (-1, -1)

			if self.__logic_obj.possible_to_put(self._position_click_x, self._position_click_y):
				self.__logic_obj.put(self._position_click_x, self._position_click_y)
				self.__logic_obj.set_player_to_play((self.__logic_obj.get_player_to_play() % 2) + 1)
				self.__logic_obj.set_pawn_number_on_board(self.__logic_obj.get_pawn_number_on_board() + 1)

				self._error_message = ''
			else:
				if self._error_message == '':
					self._error_message = 'Impossible to put your pawn here !'

		return self._position_click_x, self._position_click_y

	def reinitialise_click(self):
		self._position_click_x, self._position_click_y = -1, -1

	def display_gui(self):
		self.create_text_error((0, 0, 0), 20)
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

	def handle_first_click_move(self, mouse_coordinate_x, mouse_coordinate_y, board_piece):
		board_piece.set_selected(True)
		self._click_x_p1, self._click_y_p1 = mouse_coordinate_x, mouse_coordinate_y
		self._move_click = 2
		self._error_message = ''

	def handle_second_click_move(self, mouse_coordinate_x, mouse_coordinate_y):
		winning_move = False

		self.__logic_obj.set_list_alignment([[], [], []])

		if mouse_coordinate_x == self._click_x_p1 and mouse_coordinate_y == self._click_y_p1:
			self._get_board[mouse_coordinate_x][mouse_coordinate_y].set_selected(False)
			self._refresh = True
			self.refresh()
			self._move_click = 1
		elif isinstance(self._get_board[mouse_coordinate_x][mouse_coordinate_y], Pawn) or \
			self._get_board[mouse_coordinate_x][mouse_coordinate_y] in [-1, -2]:
			if self._error_message == '':
				self._error_message = 'You can not move on a pawn or a mark !'
				self._refresh = True
				self.refresh()
		else:
			if self.__logic_obj.check_win(self._click_x_p1, self._click_y_p1):
				self.__logic_obj.delete_on_alignment()
				winning_move = True

			self._click_x_p2, self._click_y_p2 = mouse_coordinate_x, mouse_coordinate_y
			self._move_click = 1
			self.__logic_obj.move(self._click_x_p1, self._click_y_p1, self._click_x_p2, self._click_y_p2, winning_move)
			self._get_board[mouse_coordinate_x][mouse_coordinate_y].set_selected(False) if not winning_move else None
			self.refresh()
			self._error_message = ''
			self.__logic_obj.set_player_to_play(self.__logic_obj.get_player_to_play() % 2 + 1)

	def move_pawns(self):
		mouse_coordinate = self.pixel_to_coordinate_transformation(*pygame.mouse.get_pos())

		if mouse_coordinate is None:
			return

		mouse_coordinate_x, mouse_coordinate_y = mouse_coordinate
		board_piece = self._get_board[mouse_coordinate_x][mouse_coordinate_y]
		current_player = self.__logic_obj.get_player_to_play()

		if self._move_click == 1 and isinstance(board_piece, Pawn) and board_piece.get_player() == current_player:
			self.handle_first_click_move(mouse_coordinate_x, mouse_coordinate_y, board_piece)
		elif self._move_click == 2:
			self.handle_second_click_move(mouse_coordinate_x, mouse_coordinate_y)
		else:
			self._error_message = 'please press a white pawn !' if current_player == 1 and self._error_message == '' else 'please press a black pawn !'

	def create_text_name(self, text: str, rect, color: tuple, color_bg: tuple, font_size: int):
		pygame.draw.rect(self.__screen, color_bg, rect)
		font = pygame.font.Font(None, font_size)
		name = font.render(text, True, color)
		text_rect = name.get_rect()
		text_rect.center = rect.center
		self.__screen.blit(name, text_rect)

	def create_text_error(self, color: tuple, font_size: int):
		pygame.draw.rect(self.__screen, (170, 184, 197), self._rect_error)
		font = pygame.font.Font(None, font_size)
		name = font.render(self._error_message, True, color)
		text_rect = name.get_rect()
		text_rect.center = (self._rect_error.centerx, self._rect_error.centery)
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

	def refresh(self):
		if self._refresh:
			self.__screen.fill(self.__background)
			self.display_gui()
			self.player_name_display()
			pygame.display.flip()
			self._refresh = False

	def run(self):
		while self.__running:
			self.refresh()

			event = pygame.event.poll()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.__logic_obj.get_pawn_number_on_board() < 10:
					self.hit_box()
					self.reinitialise_click()
				else:
					self.move_pawns()

				self._refresh = True

			elif event.type == pygame.QUIT:
				self.__running = False
				pygame.quit()


if __name__ == "__main__":
	plateau = GUIPlateau()
	plateau.run()
