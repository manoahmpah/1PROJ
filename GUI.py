import pygame
from LogicGame import Logic


class GUIPlateau:

    def __init__(self):
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
        self.__getBoard = self.__logic_obj.get_Board()

        self.__redRectangle = pygame.Rect(0, 0, self.__width, self.__height)
        self.__vertRectangle = pygame.Rect(self.__redRectangle.centerx - (self.__width/1.2)/2, self.__redRectangle.centery - (self.__height/1.2)/2, self.__width/1.2, self.__height/1.2)

    def displayGui(self):
        X = self.__vertRectangle.x
        for row in range(len(self.__getBoard)):
            # print(" " * row, end=" ")
            for col in range(len(self.__getBoard[row])):
                if self.__getBoard[row][col] == 9:
                    print(" ", end=" ")
                elif self.__getBoard[row][col] == 1:
                    pygame.draw.circle(self.__screen, (0, 0, 233), (X + 10, self.__vertRectangle.y), 5)
                    print("0", end=" ")

            print("")

    def Run(self):
        color = (0, 0, 255)
        while self.__running:
            # Appliquer l'arrière-plan
            self.__screen.blit(self.__background, (0, 0))

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
