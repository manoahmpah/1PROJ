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
        # self.__logic_obj.Put(0, 7)
        self.__getBoard = self.__logic_obj.get_Board()

        self.__redRectangle = pygame.Rect(0, 0, self.__width, self.__height)
        self.__vertRectangle = pygame.Rect(self.__redRectangle.centerx - (self.__width / 1.2) / 2,
                                           self.__redRectangle.centery - (self.__height / 1.2) / 2, self.__width / 1.2,
                                           self.__height / 1.2)
        self.__circle_radius = 30
        self.__circle_spacing = 30

    def displayGui(self):
        for row in range(len(self.__getBoard)):
            circle_spacing = self.__circle_spacing * 2  # Espacement entre les cercles, ajusté pour chaque ligne
            for col in range(len(self.__getBoard[row])):
                circle_x = self.__vertRectangle.left + col * circle_spacing + row * self.__circle_spacing
                circle_y = (self.__vertRectangle.top + row * self.__circle_spacing) * 1.7

                # Création d'une surface transparente
                circle_surface = pygame.Surface((self.__circle_radius * 2, self.__circle_radius * 2),
                                                pygame.SRCALPHA)

                if self.__getBoard[row][col] == 1:
                    if col + 1 < len(self.__getBoard[row]) and self.__getBoard[row][col + 1] == 1:
                        pygame.draw.line(self.__screen, (0, 0, 0), (circle_x, circle_y), (
                            (self.__vertRectangle.left + (col + 1) * circle_spacing + row * self.__circle_spacing),
                            ((self.__vertRectangle.top + row * self.__circle_spacing) * 1.7)), 2)

                    if row + 1 < len(self.__getBoard[row]) and self.__getBoard[row + 1][col] == 1:
                        pygame.draw.line(self.__screen, (0, 0, 0), (circle_x, circle_y),
                                         (
                                             (self.__vertRectangle.left + (col + 1) * circle_spacing + (
                                                     row - 1) * self.__circle_spacing),
                                             ((self.__vertRectangle.top + (row + 1) * self.__circle_spacing) * 1.7)
                                         )
                                         , 2)
                    if row + 1 < len(self.__getBoard) and col - 1 < len(self.__getBoard) and self.__getBoard[row + 1][col - 1] == 1:
                        pygame.draw.line(self.__screen, (0, 0, 0), (circle_x, circle_y),
                                         (
                            (self.__vertRectangle.left + (col + 1) * circle_spacing + (row - 3) * self.__circle_spacing),
                            ((self.__vertRectangle.top + (row + 1) * self.__circle_spacing) * 1.7)
                                         ), 2)

                    pygame.draw.circle(circle_surface, (0, 0, 0, 0), (circle_x, circle_y), self.__circle_radius, 1)
                elif isinstance(self.__getBoard[row][col], Pawn) and self.__PlayerToPlay == 1:
                    pygame.draw.circle(circle_surface, (255, 0, 0, 0), (circle_x, circle_y), self.__circle_radius, 1)
                elif isinstance(self.__getBoard[row][col], Pawn) and self.__PlayerToPlay == 2:
                    pygame.draw.circle(circle_surface, (0, 255, 0, 0), (circle_x, circle_y), self.__circle_radius, 1)
                else:

                    pygame.draw.circle(circle_surface, (255, 255, 0, 0), (self.__circle_radius, self.__circle_radius),
                                       self.__circle_radius, 0)


        pygame.display.flip()

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
