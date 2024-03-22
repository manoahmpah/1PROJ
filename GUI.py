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

    def hexagone(self):
        """
        creation of hexagonal
        :return:nothing
        """

        logic_obj = Logic('Luc', 'Jean-Marc')
        logic_obj.CreateBoard()
        logic_obj.Put(0, 7)
        logic_obj.Display()

        color = (0, 0, 255)
        while self.__running:

            # Appliquer l'arrière-plan
            self.__screen.blit(self.__background, (0, 0))
            # creation de hexagone

            pygame.draw.polygon(self.__screen, (255, 255, 255),
             [(500, 720), (600, 520), (600, 300), (500, 100), (400, 300), (400, 520)])

            pygame.draw.circle(self.__screen, color, (self.__width//20, 200), (self.__height//30))

        # Mise à jour de l'écran
            pygame.display.flip()
        # Si le joueur ferme cette fenêtre
            for event in pygame.event.get():
            # Que l'événement est la fermeture de fenêtre
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    print("Fermeture du jeu")


if __name__ == "__main__":
    plateau = GUIPlateau()
    plateau.hexagone()
