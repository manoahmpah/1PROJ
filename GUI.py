import pygame
from LogicGame import Logic, Pawn


class GUIPlateau:
	def __init__(self):
		self.__PlayerToPlay = 2
		pygame.init()
		# Générer la fenêtre du jeu
		self.__width = 1080
		self.__height = 720
		self.__screen = pygame.display.set_mode((self.__width, self.__height))
		pygame.display.set_caption('yinsh')
		self.__running = True
		self.__background = (170, 184, 197)

		self.__logic_obj = Logic('Luc', 'Jean-Marc')
		self.__createBoard = self.__logic_obj.CreateBoard()
		self.__getBoard = self.__logic_obj.get_Board()

		self.__redRectangle = pygame.Rect(0, 0, self.__width, self.__height)
		self.__vertRectangle = pygame.Rect(self.__redRectangle.centerx - (self.__width / 1.2) / 2,
		                                   self.__redRectangle.centery - (self.__height / 1.2) / 2, self.__width / 1.2,
		                                   self.__height / 1.2)
		self.__halfDimension = 25
		self.__paddingRect = 30

		self.__positionPoints = []

		self.__rect_width = self.__halfDimension * 2 + 4
		self.__rect_height = self.__halfDimension * 2

		self.__position_clickX, self.__position_clickY = -1, -1

	def transformCordIntoIndex(self, Cord_x, Cord_y):
		return int(((Cord_x - (30 * ((Cord_y // 51) - 2))) // 60) - 1), int(Cord_y // 51) - 2

	def createHitBox(self):
		x, y = pygame.mouse.get_pos()
		for Point in self.__positionPoints:
			if (Point['pos_x'] - 30 < x < Point['pos_x'] + 30) and (Point['pos_y'] - 25 < y < Point['pos_y'] + 25):
				if self.__position_clickY == -1 and self.__position_clickX == -1:
					self.__position_clickY, self.__position_clickX = self.transformCordIntoIndex(Point['pos_x'],
					                                                                             Point['pos_y'])
					self.__logic_obj.Put(self.__position_clickX, self.__position_clickY)

			# print(self.__position_clickX, self.__position_clickY)

		self.__position_clickX, self.__position_clickY = -1, -1

		self.__logic_obj.set_PlayerToPlay((self.__logic_obj.get_PlayerToPlay() % 2) + 1)

	def displayGui(self):
		for row in range(len(self.__getBoard)):
			dimension = self.__paddingRect * 2
			for col in range(len(self.__getBoard[row])):
				pos_x = self.__vertRectangle.left + col * dimension + row * self.__paddingRect
				pos_y = (self.__vertRectangle.top + row * self.__paddingRect) * 1.7
				if self.__getBoard[row][col] != 9:
					self.__positionPoints.append({'pos_x': pos_x, 'pos_y': pos_y})

				# Dessiner les lignes pour les cercles adjacents
				if self.__getBoard[row][col] != 9:
					if col + 1 < len(self.__getBoard[row]) and self.__getBoard[row][col + 1] != 9:
						pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y),
						                 ((self.__vertRectangle.left + (
								                 col + 1) * dimension + row * self.__paddingRect),
						                  ((self.__vertRectangle.top + row * self.__paddingRect) * 1.7)), 2)

					if row + 1 < len(self.__getBoard[row]) and self.__getBoard[row + 1][col] != 9:
						pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y),
						                 ((self.__vertRectangle.left + col * dimension + (
								                 row + 1) * self.__paddingRect),
						                  ((self.__vertRectangle.top + (row + 1) * self.__paddingRect) * 1.7)), 2)

					if row + 1 < len(self.__getBoard) and col - 1 < len(self.__getBoard) and self.__getBoard[row + 1][
						col - 1] != 9:
						pygame.draw.line(self.__screen, (0, 0, 0), (pos_x, pos_y),
						                 ((self.__vertRectangle.left + (col - 1) * dimension + (
								                 row + 1) * self.__paddingRect),
						                  ((self.__vertRectangle.top + (row + 1) * self.__paddingRect) * 1.7)), 2)
					if isinstance(self.__getBoard[row][col], Pawn) and self.__getBoard[row][col].getPlayer() == 1:
						pygame.draw.circle(self.__screen, (255, 255, 255), (pos_x, pos_y), 25, 7)
					if isinstance(self.__getBoard[row][col], Pawn) and self.__getBoard[row][col].getPlayer() == 2:
						pygame.draw.circle(self.__screen, (255, 0, 0), (pos_x, pos_y), 25, 7)


	def Run(self):
		while self.__running:
			self.__screen.fill(self.__background)

			self.displayGui()

			pygame.display.flip()

			# Si le joueur ferme cette fenêtre
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN:
					self.createHitBox()
				# Que l'événement est la fermeture de fenêtre
				if event.type == pygame.QUIT:
					self.__running = False
					pygame.quit()
					print("Fermeture du jeu")


if __name__ == "__main__":
	plateau = GUIPlateau()
	plateau.Run()
