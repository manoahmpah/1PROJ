import pygame
from LogicGame import Logic, ring


class GUIBoard:
	def __init__(self, player1_name, player2_name):
		pygame.init()
		# Windows game
		self.__width = 1080
		self.__height = 720
		self.__screen = pygame.display.set_mode((self.__width, self.__height), pygame.SRCALPHA)
		pygame.display.set_caption('yinsh')
		self.__running = True
		self.__background = (170, 184, 197)
		self.__background_image = pygame.image.load('asset_plateau/bg1.png').convert()
		self.__background_image = pygame.transform.scale(self.__background_image, (self.__width, self.__height))

		self.__logic_obj = Logic(player1_name, player2_name)
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

		self._board_color = (255, 255, 255)

		self._refresh = True

		self._rect_error = pygame.Rect(self._rect_all.centerx - 100, self._rect_all.bottom - 100, 200, 50)
		self._error_message = ""

		self._winning_move_player_one, self._winning_move_player_two = 0, 0
		self._react_rings_win_player_one = pygame.Rect(self._rect_all.left + 200, self._rect_all.top + 20, 130, 70)
		self._color_ring_win_player_one = [(50,50,50) for _ in range(3)]
		self._react_rings_win_player_two = 5

	def rectangle_ring_win_player_one(self):
		# print(self._color_ring_win_player_one)
		pygame.draw.circle(self.__screen, self._color_ring_win_player_one[0], (self._react_rings_win_player_one.centerx + 20, self._react_rings_win_player_one.centery), 25, 7)
		pygame.draw.circle(self.__screen, self.__background, (self._react_rings_win_player_one.centerx - 10, self._react_rings_win_player_one.centery), 25)
		pygame.draw.circle(self.__screen, self._color_ring_win_player_one[1], (self._react_rings_win_player_one.centerx - 10, self._react_rings_win_player_one.centery), 25, 7)
		pygame.draw.circle(self.__screen, self.__background, (self._react_rings_win_player_one.centerx - 40, self._react_rings_win_player_one.centery), 25)
		pygame.draw.circle(self.__screen, self._color_ring_win_player_one[2], (self._react_rings_win_player_one.centerx - 40, self._react_rings_win_player_one.centery), 25, 7)

	@staticmethod
	def __transform_cord_to_pos(x, y) -> tuple:
		return int(y // 51) - 2, int(((x - (30 * ((y // 51) - 2))) // 60) - 1)

	def __pixel_to_coordinate_transformation(self, x: int, y: int) -> tuple:
		for point in self._position_points:
			if (point['pos_x'] - 30 < x < point['pos_x'] + 30) and (point['pos_y'] - 25 < y < point['pos_y'] + 25):
				return self.__transform_cord_to_pos(point['pos_x'], point['pos_y'])

	def __put_on_click(self) -> tuple:
		pixel_x, pixel_y = pygame.mouse.get_pos()

		if self._position_click_y == -1 and self._position_click_x == -1:
			self._position_click_x, self._position_click_y = self.__pixel_to_coordinate_transformation(pixel_x, pixel_y) if self.__pixel_to_coordinate_transformation(pixel_x, pixel_y) else (-1, -1)

			if self.__logic_obj.possible_to_put(self._position_click_x, self._position_click_y):
				self.__logic_obj.put(self._position_click_x, self._position_click_y)
				self.__logic_obj.set_player_to_play((self.__logic_obj.get_player_to_play() % 2) + 1)
				self.__logic_obj.set_ring_number_on_board(self.__logic_obj.get_ring_number_on_board() + 1)

				self._error_message = ''
			else:
				if self._error_message == '':
					self._error_message = 'Impossible to put your ring here !'

		return self._position_click_x, self._position_click_y

	def __reinitialise_click(self):
		self._position_click_x, self._position_click_y = -1, -1

	def __display_board_gui(self):
		self.__create_text_error((0, 0, 0), 20)
		for row in range(len(self._get_board)):
			for col in range(len(self._get_board[row])):
				pos_x, pos_y = self.__collision_area(row, col)
				self.__draw_circles_and_lines(row, col, pos_x, pos_y)

	def __collision_area(self, row: int, col: int) -> tuple:
		dimension = self._padding_rect * 2
		pos_x = self._rect_board.left + col * dimension + row * self._padding_rect
		pos_y = (self._rect_board.top + row * self._padding_rect) * 1.7
		return pos_x, pos_y

	# problem
	def __draw_circles_and_lines(self, row: int, col: int, pos_x: int, pos_y: int):
		if self._get_board[row][col] != 9:
			self._position_points.append({'pos_x': pos_x, 'pos_y': pos_y})
			self.__draw_line_to_create_board(row, col, pos_x, pos_y)

			if isinstance(self._get_board[row][col], ring):
				player = self._get_board[row][col].get_player()
				color = (255, 255, 255) if player == 1 else (0, 0, 0)
				pygame.draw.circle(self.__screen, color, (pos_x, pos_y), 25, 7)
				if self._get_board[row][col].get_selected():
					pygame.draw.circle(self.__screen, color, (pos_x, pos_y), 15)

			if self._get_board[row][col] == -1:
				pygame.draw.circle(self.__screen, (255, 255, 255), (pos_x, pos_y), 15)
			elif self._get_board[row][col] == -2:
				pygame.draw.circle(self.__screen, (0, 0, 0), (pos_x, pos_y), 15)

	def __draw_line_to_create_board(self, row, col, pos_x, pos_y):
		board = self._get_board
		if col + 1 < len(board[row]) and board[row][col + 1] != 9:
			col_pos = self.__collision_area(row, col + 1)
			pygame.draw.line(self.__screen, self._board_color, (pos_x, pos_y), col_pos, 4)

		if row + 1 < len(board):
			if col - 1 < len(board) and board[row + 1][col - 1] != 9:
				diag_col_pos = self.__collision_area(row + 1, col - 1)
				pygame.draw.line(self.__screen, self._board_color, (pos_x, pos_y), diag_col_pos, 4)

			if board[row + 1][col] != 9:
				next_row_pos = self.__collision_area(row + 1, col)
				pygame.draw.line(self.__screen, self._board_color, (pos_x, pos_y), next_row_pos, 4)

	def __handle_first_click_move(self, mouse_coordinate_x, mouse_coordinate_y, board_piece):
		board_piece.set_selected(True)
		self._click_x_p1, self._click_y_p1 = mouse_coordinate_x, mouse_coordinate_y
		self._move_click = 2
		self._error_message = ''

	def __handle_second_click_move(self, mouse_coordinate_x, mouse_coordinate_y):
		winning_move = False

		self.__logic_obj.set_list_alignment([[], [], []])

		if mouse_coordinate_x == self._click_x_p1 and mouse_coordinate_y == self._click_y_p1:
			self._get_board[mouse_coordinate_x][mouse_coordinate_y].set_selected(False)
			self._refresh = True
			self.__refresh()
			self._move_click = 1

		elif self.__logic_obj.possible_to_move(self._click_x_p1, self._click_y_p1, mouse_coordinate_x, mouse_coordinate_y)[0]:
			self.__logic_obj.change_mark_on_move(self._click_x_p1, self._click_y_p1, mouse_coordinate_x, mouse_coordinate_y)
			if self.__logic_obj.check_win(self._click_x_p1, self._click_y_p1):
				self.__logic_obj.delete_on_alignment()
				winning_move = True
				if self.__logic_obj.get_player_to_play() == 1:
					self._winning_move_player_one += 1

				else:
					self._color_ring_win_player_one[self._winning_move_player_one-1] = (0, 0, 0)
					self._winning_move_player_two += 1

			self._click_x_p2, self._click_y_p2 = mouse_coordinate_x, mouse_coordinate_y
			self._move_click = 1
			self.__logic_obj.move(self._click_x_p1, self._click_y_p1, self._click_x_p2, self._click_y_p2, winning_move)
			self._get_board[mouse_coordinate_x][mouse_coordinate_y].set_selected(False) if not winning_move else None
			self._refresh = True
			self.__refresh()
			if winning_move:
				self.choose_a_ring_to_delete_if_win()

			self._error_message = ''
			self.__logic_obj.set_player_to_play(self.__logic_obj.get_player_to_play() % 2 + 1)

		else:
			self._error_message = self.__logic_obj.possible_to_move(self._click_x_p1, self._click_y_p1, mouse_coordinate_x, mouse_coordinate_y)[1]

	def choose_a_ring_to_delete_if_win(self):
		valid_selection = False
		while not valid_selection:
			# Implement the logic for the player to select a ring to remove
			event = pygame.event.poll()
			if event.type == pygame.MOUSEBUTTONDOWN:
				# Get the mouse coordinates
				mouse_x, mouse_y = pygame.mouse.get_pos()
				# Calculate the row and column based on mouse coordinates
				if self.__pixel_to_coordinate_transformation(mouse_x, mouse_y) is not None:
					row, column = self.__pixel_to_coordinate_transformation(mouse_x, mouse_y)
				else:
					row, column = -1, -1
				if 0 <= row < 11 and 0 <= column < 11 and isinstance(self._get_board[row][column], ring):
					if self._get_board[row][column].get_player() == self.__logic_obj.get_player_to_play():
						self.__logic_obj.get_board()[row][column] = 1
						valid_selection = True
					else:
						self._error_message = 'Please select a white ring' if self.__logic_obj.get_player_to_play() == 1 else 'Please select a black ring'
						self._refresh = True
						self.__refresh()
				else:
					self._error_message = 'Please select a ring to remove'
					self._refresh = True
					self.__refresh()

	def __move_rings(self):
		mouse_coordinate = self.__pixel_to_coordinate_transformation(*pygame.mouse.get_pos())

		if mouse_coordinate is None:
			return

		mouse_coordinate_x, mouse_coordinate_y = mouse_coordinate
		board_piece = self._get_board[mouse_coordinate_x][mouse_coordinate_y]
		current_player = self.__logic_obj.get_player_to_play()

		if self._move_click == 1 and isinstance(board_piece, ring) and board_piece.get_player() == current_player:
			self.__handle_first_click_move(mouse_coordinate_x, mouse_coordinate_y, board_piece)
		elif self._move_click == 2:
			self.__handle_second_click_move(mouse_coordinate_x, mouse_coordinate_y)
		else:
			self._error_message = 'please press a white ring !' if current_player == 1 and self._error_message == '' else 'please press a black ring !'

	def __create_text_name(self, text: str, rect, color, color_bg: tuple, font_size: int):
		if color_bg is not None:
			pygame.draw.rect(self.__screen, color_bg, rect)
		font = pygame.font.Font(None, font_size)
		name = font.render(text, True, color)
		text_rect = name.get_rect()
		text_rect.center = rect.center
		self.__screen.blit(name, text_rect)

	def __create_text_error(self, color: tuple, font_size: int):
		font = pygame.font.Font(None, font_size)
		name = font.render(self._error_message, True, color)
		text_rect = name.get_rect()
		text_rect.center = (self._rect_error.centerx, self._rect_error.centery)
		self.__screen.blit(name, text_rect)

	def __player_name_display(self):
		color_bg_name1 = (255, 255, 255) if self.__logic_obj.get_player_to_play() == 1 else None
		if self.__logic_obj.get_player_to_play() == 2:
			color_font_name2 = (255, 255, 255)
			color_bg_name2 = (0, 0, 0)
		else:
			color_font_name2 = (0, 0, 0)
			color_bg_name2 = None

		self.__create_text_name(self.__logic_obj.get_name1(), self._rect_name1, (0, 0, 0), color_bg_name1, 29)
		self.__create_text_name(self.__logic_obj.get_name2(), self._rect_name2, color_font_name2, color_bg_name2, 29)

	def __refresh(self):
		if self._refresh:
			self.__screen.blit(self.__background_image, (0, 0))
			# self.__screen.fill(self.__background)
			self.__display_board_gui()
			self.__player_name_display()
			self.rectangle_ring_win_player_one()
			pygame.display.flip()
			self._refresh = False

	def run(self):
		while self.__running:
			self.__refresh()
			event = pygame.event.poll()

			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.__logic_obj.get_ring_number_on_board() < 10:
					self.__put_on_click()
					self.__reinitialise_click()
				else:
					self.__move_rings()

				self._refresh = True

			elif event.type == pygame.QUIT:
				self.__running = False
				pygame.quit()


if __name__ == "__main__":
	plateau = GUIBoard('player1', 'player2')
	plateau.run()
