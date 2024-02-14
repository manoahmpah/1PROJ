import pygame


class GUISettings:
    def __init__(self):

        # ------- Initialize ------- #

        self.__init = pygame.init()
        self.__screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("Settings")

        self.__running = True

        self.__name1Boolean, self.__name2Boolean = False, False

        # ------- Text ------- #
        self.__font = pygame.font.Font(None, 36)
        self.__Account = self.__font.render("Account", True, (0, 0, 0))
        self.__Languages = self.__font.render("Languages", True, (0, 0, 0))
        self.__Sound = self.__font.render("Sound", True, (0, 0, 0))

        self.__Customization = self.__font.render("Customization", True, (0, 0, 0))
        self.__name1 = ''
        self.__input_text_surface = None
        self.__input_rect = pygame.Rect(self.__screen.get_width() / 4 + 50, 0, 200, 50)

        # ------- BackGround ------- #
        self.__BackGround = pygame.image.load("Assets-Setting/BackGround.png")

    def run(self):
        while self.__running:
            # ------- BackGround & Rectangle ------- #
            self.__screen.blit(self.__BackGround, (0, -200))
            pygame.draw.rect(self.__screen, (255, 255, 255),
                             (0, 0, self.__screen.get_width() / 4, self.__screen.get_height()))

            pygame.draw.rect(self.__screen, (255, 255, 255), self.__input_rect, 2)

            # ------- Text ------- #
            self.__screen.blit(self.__Account, (10, 15))
            self.__screen.blit(self.__Languages, (10, 55))
            self.__screen.blit(self.__Sound, (10, 95))
            self.__screen.blit(self.__Customization, (10, 135))

            # ------- Input Text ------- #
            self.__input_text_surface = self.__font.render(self.__name1, True, (255, 255, 255))
            self.__screen.blit(self.__input_text_surface, (self.__input_rect.x + 15, self.__input_rect.y + 15))
            self.__input_rect.w = max(100, self.__input_text_surface.get_width() + 30)

            # ------- MaJ ------- #
            pygame.display.flip()

            for event in pygame.event.get():
                self.CloseWindow(event)
                self.collisionRect1(event)
                self.KeyBoardEvent(event)

    def collisionRect1(self, event):
        # ------- Collision ------- #
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.__input_rect.collidepoint(event.pos):
                self.__name1Boolean = True
            else:
                self.__name1Boolean = False

    def CloseWindow(self, event):
        # ------- Close windows ------- #
        if event.type == pygame.QUIT:
            self.__running = False
            pygame.quit()

    def KeyBoardEvent(self, event):
        # ------- KeyBoard Event ------- #
        if event.type == pygame.KEYDOWN and self.__name1Boolean:
            if event.key == pygame.K_BACKSPACE:
                self.__name1 = self.__name1[:-1]
            else:
                self.__name1 += event.unicode


if __name__ == "__main__":
    settings = GUISettings()
    settings.run()
