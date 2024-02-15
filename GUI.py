import pygame


class GUIPlateau:

    def __init__(self):
        pygame.init()
        # Générer la fenêtre du jeu
        self.__screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption('yinsh')
        self.__running = True

        self.__background = pygame.image.load('asset_plateau/background.png')

    def hexagone(self):
        pygame.draw.polygon(self.__screen, (255, 255, 255), [(500, 620), (600, 520), (600, 300), (500, 100), (400, 300), (400, 520)])
        # Boucle tant que la condition est vraie
        while self.__running:
            # Appliquer l'arrière-plan
            # self.__screen.blit(self.__background, (0, 100))
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
