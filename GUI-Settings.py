import pygame


class GUISettings:
    def __init__(self):

        # ------- Initialize ------- #
        self.__init = pygame.init()
        self.__screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Settings")

        self.__running = True

        # ------- Text ------- #
        self.__font = pygame.font.Font(None, 36)
        self.__Account = self.__font.render("Account", True, (0, 0, 0))
        self.__Languages = self.__font.render("Languages", True, (0, 0, 0))
        self.__Sound = self.__font.render("Sound", True, (0, 0, 0))
        self.__Customization = self.__font.render("Customization", True, (0, 0, 0))

        # ------- BackGround ------- #
        self.__BackGround = pygame.image.load("Assets-Setting/BackGround.png")

    def run(self):
        while self.__running:
            # ------- BackGround & Rectangle ------- #
            self.__screen.blit(self.__BackGround, (0, -200))
            pygame.draw.rect(self.__screen, (255, 255, 255),
                             (0, 0, self.__screen.get_width() / 4, self.__screen.get_height()))

            # pygame.draw.rect(self.__screen, (0, 0, 0), (self.__screen.get_width() / 4, 0, self.__screen.get_width()
            # , self.__screen.get_height()))

            # ------- Text ------- #
            self.__screen.blit(self.__Account, (10, 15))
            self.__screen.blit(self.__Languages, (10, 55))
            self.__screen.blit(self.__Sound, (10, 95))
            self.__screen.blit(self.__Customization, (10, 135))

            # ------- MaJ ------- #
            pygame.display.flip()

            # ------- Close windows ------- #
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()


if __name__ == "__main__":
    settings = GUISettings()
    settings.run()
