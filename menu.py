import pygame
import sys
from GUI import GUIBoard


# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Création de la fenêtre
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Menu")

# Charger et redimensionner les images
game_title_image = pygame.transform.scale(pygame.image.load("asset_menu/title.png"), (600, 200))
help_button_image = pygame.transform.scale(pygame.image.load("asset_menu/help_button.png"), (100, 100))
quit_button_image = pygame.transform.scale(pygame.image.load("asset_menu/quit_button.png"), (100, 100))
play_button_image = pygame.transform.scale(pygame.image.load("asset_menu/play_button.png"), (200, 100))
setting_button_image = pygame.transform.scale(pygame.image.load("asset_menu/setting_button.png"), (100, 100))

# Fonction principale du menu
def menu():
    running = True

    while running:
        window.fill(WHITE)

        # Affichage du titre du jeu au centre
        window.blit(game_title_image, (WINDOW_WIDTH // 2 - game_title_image.get_width() // 2, WINDOW_HEIGHT // 2 - game_title_image.get_height() // 2))

        # Affichage des boutons
        # Bouton "Help"
        window.blit(help_button_image, (20, 20))

        # Bouton "Quit Game"
        window.blit(quit_button_image, (WINDOW_WIDTH - quit_button_image.get_width() - 20, 20))

        # Bouton "Play"
        window.blit(play_button_image, (WINDOW_WIDTH // 2 - play_button_image.get_width() // 2, WINDOW_HEIGHT - 120))

        # Bouton "Setting"
        window.blit(setting_button_image, (WINDOW_WIDTH // 2 - setting_button_image.get_width() // 2, WINDOW_HEIGHT - 60))

        # Actualisation de l'affichage
        pygame.display.update()

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                # Si le bouton "Help" est cliqué
                if 20 <= mouse_pos[0] <= 20 + help_button_image.get_width() and \
                   20 <= mouse_pos[1] <= 20 + help_button_image.get_height():
                    # Mettez ici le code pour afficher la page d'aide
                    pass

                # Si le bouton "Quit Game" est cliqué
                elif WINDOW_WIDTH - quit_button_image.get_width() - 20 <= mouse_pos[0] <= WINDOW_WIDTH - 20 and \
                     20 <= mouse_pos[1] <= 20 + quit_button_image.get_height():
                    running = False
                    pygame.quit()
                    sys.exit()

                # Si le bouton "Play" est cliqué
                elif WINDOW_WIDTH // 2 - play_button_image.get_width() // 2 <= mouse_pos[0] <= \
                     WINDOW_WIDTH // 2 + play_button_image.get_width() // 2 and \
                     WINDOW_HEIGHT - 120 <= mouse_pos[1] <= WINDOW_HEIGHT - 70:
                    # Ouvrir "Gui.py" en utilisant subprocess.call()
                    plateau = GUIBoard()
                    plateau.run()
                    # subprocess.call(["python", "Gui.py"])
                    pygame.quit()  # Quitter Pygame après le lancement de "Gui.py"
                    sys.exit()     # Quitter le script actuel après le lancement de "Gui.py"

                # Si le bouton "Setting" est cliqué
                elif WINDOW_WIDTH // 2 - setting_button_image.get_width() // 2 <= mouse_pos[0] <= \
                     WINDOW_WIDTH // 2 + setting_button_image.get_width() // 2 and \
                     WINDOW_HEIGHT - 60 <= mouse_pos[1] <= WINDOW_HEIGHT - 10:
                    # Mettez ici le code pour passer à la page de paramètres
                    pass

# Lancement du menu
menu()
