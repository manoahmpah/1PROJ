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
        self.__background = pygame.image.load('asset_plateau/background.png')

        self.__logic_obj = Logic('Luc', 'Jean-Marc')
        self.__createBoard = self.__logic_obj.CreateBoard()
        self.__logic_obj.Put(0, 8)
        self.__getBoard = self.__logic_obj.get_Board()

        self.__redRectangle = pygame.Rect(0, 0, self.__width, self.__height)
        self.__vertRectangle = pygame.Rect(self.__redRectangle.centerx - (self.__width / 1.2) / 2,
                                           self.__redRectangle.centery - (self.__height / 1.2) / 2, self.__width / 1.2,
                                           self.__height / 1.2)
        self.__halfDimension = 25
        self.__paddingRect = 30

    def createHitBox(self, pos_x, pos_y, hitBox):
        if pygame.mouse.get_pressed()[0]:
            mouse_pos = pygame.mouse.get_pos()
            if hitBox.collidepoint(mouse_pos):
                return int(((pos_x - (30 * ((pos_y // 51) - 2))) // 60) - 1), int(pos_y // 51) - 2

    def displayGui(self):
        for row in range(len(self.__getBoard)):
            dimension = self.__paddingRect * 2
            for col in range(len(self.__getBoard[row])):
                pos_x = self.__vertRectangle.left + col * dimension + row * self.__paddingRect
                pos_y = (self.__vertRectangle.top + row * self.__paddingRect) * 1.7

                # Création d'un rectangle
                rect_width = self.__halfDimension * 2 + 5
                rect_height = self.__halfDimension * 2

                hitBox = pygame.Rect(pos_x - self.__halfDimension, pos_y - self.__halfDimension,
                                          rect_width, rect_height)



                # Dessiner le cercle à l'intérieur du rectangle
                pygame.draw.rect(self.__screen, (255, 255, 255), hitBox, 1)

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

        # pygame.display.flip()

    def Run(self):
        while self.__running:
            # Appliquer l'arrière-plan
            self.__screen.blit(self.__background, (0, 0))

            self.displayGui()
            # Mise à jour de l'écran
            pygame.display.flip()

            # Si le joueur ferme cette fenêtre
            for event in pygame.event.get():

                # Que l'événement est la fermeture de fenêtre
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    print("Fermeture du jeu")
            pygame.draw.rect(self.__screen, (255, 0, 0), self.__redRectangle, 2)
            pygame.draw.rect(self.__screen, (0, 255, 0), self.__vertRectangle, 2)


if __name__ == "__main__":
    plateau = GUIPlateau()
    plateau.Run()
