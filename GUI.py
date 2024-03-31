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

		self.__logic_obj = Logic('Luc', 'Jean-Marc')
		self._create_board = self.__logic_obj.CreateBoard()
		self._get_board = self.__logic_obj.get_Board()

		self._rect_all = pygame.Rect(0, 0, self.__width, self.__height)
		self._rect_board = pygame.Rect(self._rect_all.centerx - self.__width / 2.4, self._rect_all.centery - self.__height / 2.4, self.__width / 1.2, self.__height / 1.2)
		self._half_dim_hit_box = 25
		self._padding_rect = 30

		self._position_points = []

		self._rect_width = self._half_dim_hit_box * 2 + 4
		self._rect_height = self._half_dim_hit_box * 2

		self._position_click_x, self._position_click_y = -1, -1

	def hit_box(self):
		x, y = pygame.mouse.get_pos()
		for point in self._position_points:
			if (point['pos_x'] - 30 < x < point['pos_x'] + 30) and (point['pos_y'] - 25 < y < point['pos_y'] + 25):

				if self._position_click_y == -1 and self._position_click_x == -1:
					self._position_click_y = int(((point['pos_x'] - (30 * ((point['pos_y'] // 51) - 2))) // 60) - 1)
					self._position_click_x = int(point['pos_y'] // 51) - 2
					self.__logic_obj.Put(self._position_click_x, self._position_click_y)

		# print(self._position_click_x, self._position_click_y)

		# initialise click
		self._position_click_x, self._position_click_y = -1, -1

		self.__logic_obj.set_PlayerToPlay((self.__logic_obj.get_PlayerToPlay() % 2) + 1)

	def display_gui(self):
		for row in range(len(self._get_board)):
			for col in range(len(self._get_board[row])):
				pos_x, pos_y = self.calculate_position(row, col)
				self.draw_circles_and_lines(row, col, pos_x, pos_y)

	def calculate_position(self, row, col):
		dimension = self._padding_rect * 2
		pos_x = self._rect_board.left + col * dimension + row * self._padding_rect
		pos_y = (self._rect_board.top + row * self._padding_rect) * 1.7
		return pos_x, pos_y

	def draw_circles_and_lines(self, row, col, pos_x, pos_y):
		if self._get_board[row][col] != 9:
			self._position_points.append({'pos_x': pos_x, 'pos_y': pos_y})

		# Draw lines
		if self._get_board[row][col] != 9:
			self.draw_adjacent_lines(row, col, pos_x, pos_y)

		# Draw circles of pawns
		if isinstance(self._get_board[row][col], Pawn):
			player = self._get_board[row][col].getPlayer()
			color = (255, 255, 255) if player == 1 else (0, 0, 0)
			pygame.draw.circle(self.__screen, color, (pos_x, pos_y), 25, 7)

	def draw_adjacent_lines(self, row, col, pos_x, pos_y):
		dimension = self._padding_rect * 2
		board = self._get_board
		screen = self.__screen
		rect_board = self._rect_board

		if col + 1 < len(board[row]) and board[row][col + 1] != 9:
			col_pos_x = rect_board.left + (col + 1) * dimension + row * self._padding_rect
			col_pos_y = (rect_board.top + row * self._padding_rect) * 1.7

			pygame.draw.line(screen, (0, 0, 0), (pos_x, pos_y), (col_pos_x, col_pos_y), 2)

		if row + 1 < len(board):
			if col - 1 < len(board) and board[row + 1][col - 1] != 9:
				diag_col_pos_x = rect_board.left + (col - 1) * dimension + (row + 1) * self._padding_rect
				diag_col_pos_y = (rect_board.top + (row + 1) * self._padding_rect) * 1.7

				pygame.draw.line(screen, (0, 0, 0), (pos_x, pos_y), (diag_col_pos_x, diag_col_pos_y), 2)

			if board[row + 1][col] != 9:
				next_row_pos_x = rect_board.left + col * dimension + (row + 1) * self._padding_rect
				next_row_pos_y = (rect_board.top + (row + 1) * self._padding_rect) * 1.7

				pygame.draw.line(screen, (0, 0, 0), (pos_x, pos_y), (next_row_pos_x, next_row_pos_y), 2)

	def run(self):
		while self.__running:
			self.__screen.fill(self.__background)

			self.display_gui()
			pygame.display.flip()

			# if player close windows
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.hit_box()
				if event.type == pygame.QUIT:
					self.__running = False
					pygame.quit()


if __name__ == "__main__":
	plateau = GUIPlateau()
	plateau.run()
