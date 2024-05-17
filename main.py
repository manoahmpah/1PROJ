import pygame
import sys
from GUI import GUIPlateau
from Music import MusicPlayer
from Settings import Settings

# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialiser le lecteur de musique
music_player = MusicPlayer()
music_player.play_background_music()

class MainController:
    def __init__(self):
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        pygame.display.set_caption("Menu")
        self.current_screen = "menu"
        self.running = True

        # Charger les images du menu
        self.game_title_image = pygame.transform.scale(pygame.image.load("asset_menu/title.png"), (600, 200))
        self.help_button_image = pygame.transform.scale(pygame.image.load("asset_menu/help_button.png"), (100, 100))
        self.quit_button_image = pygame.transform.scale(pygame.image.load("asset_menu/quit_button.png"), (100, 100))
        self.play_button_image = pygame.transform.scale(pygame.image.load("asset_menu/play_button.png"), (200, 100))
        self.setting_button_image = pygame.transform.scale(pygame.image.load("asset_menu/setting_button.png"), (100, 100))

    def run(self):
        while self.running:
            if self.current_screen == "menu":
                self.menu()
            elif self.current_screen == "game":
                self.game()
            elif self.current_screen == "settings":
                self.settings()

    def menu(self):
        self.screen.fill(WHITE)

        # Affichage du titre du jeu au centre
        self.screen.blit(self.game_title_image, (WINDOW_WIDTH // 2 - self.game_title_image.get_width() // 2, WINDOW_HEIGHT // 2 - self.game_title_image.get_height() // 2))

        # Affichage des boutons
        self.screen.blit(self.help_button_image, (20, 20))  # Bouton "Help"
        self.screen.blit(self.quit_button_image, (WINDOW_WIDTH - self.quit_button_image.get_width() - 20, 20))  # Bouton "Quit Game"
        self.screen.blit(self.play_button_image, (WINDOW_WIDTH // 2 - self.play_button_image.get_width() // 2, WINDOW_HEIGHT - 120))  # Bouton "Play"
        self.screen.blit(self.setting_button_image, (WINDOW_WIDTH // 2 - self.setting_button_image.get_width() // 2, WINDOW_HEIGHT - 60))  # Bouton "Setting"

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Si le bouton "Help" est cliqué
                if 20 <= mouse_pos[0] <= 20 + self.help_button_image.get_width() and \
                   20 <= mouse_pos[1] <= 20 + self.help_button_image.get_height():
                    # Code pour afficher les règles du jeu
                    pass

                # Si le bouton "Quit Game" est cliqué
                elif WINDOW_WIDTH - self.quit_button_image.get_width() - 20 <= mouse_pos[0] <= WINDOW_WIDTH - 20 and \
                     20 <= mouse_pos[1] <= 20 + self.quit_button_image.get_height():
                    self.running = False
                    pygame.quit()
                    sys.exit()

                # Si le bouton "Play" est cliqué
                elif WINDOW_WIDTH // 2 - self.play_button_image.get_width() // 2 <= mouse_pos[0] <= \
                     WINDOW_WIDTH // 2 + self.play_button_image.get_width() // 2 and \
                     WINDOW_HEIGHT - 120 <= mouse_pos[1] <= WINDOW_HEIGHT - 70:
                    self.current_screen = "game"

                # Si le bouton "Setting" est cliqué
                elif WINDOW_WIDTH // 2 - self.setting_button_image.get_width() // 2 <= mouse_pos[0] <= \
                     WINDOW_WIDTH // 2 + self.setting_button_image.get_width() // 2 and \
                     WINDOW_HEIGHT - 60 <= mouse_pos[1] <= WINDOW_HEIGHT - 10:
                    self.current_screen = "settings"

    def game(self):
        plateau = GUIPlateau()
        plateau.run()
        self.current_screen = "menu"

    def settings(self):
        settings = Settings(self.screen, music_player)
        settings.run()
        self.current_screen = "menu"

# Lancement du menu
if __name__ == "__main__":
    controller = MainController()
    controller.run()
