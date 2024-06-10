import pygame
import sys
from Music import MusicPlayer
from Settings import Settings
from GUI import GUIBoard


pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialiser le lecteur de musique
music_player = MusicPlayer()
music_player.play_background_music()

class MainController:
    def __init__(self):
        self.screen = pygame.display.set_mode((1080,  730))
        pygame.display.set_caption("Menu")
        self.current_screen = "menu"
        self.running = True
        self.player1_name = ""
        self.player2_name = ""
        self.active_input = None  # To track which input box is active

        self.__background_image = pygame.image.load('asset_plateau/img_4.png').convert()
        self.__background_image = pygame.transform.smoothscale(self.__background_image,
                                                               (self.screen.get_width(), self.screen.get_height()))

        # Charger les images du menu
        self.load_images()

    def load_images(self):
        self.images = {
            "title": pygame.transform.scale(pygame.image.load("asset_menu/logo.png"), (500, 500)),
            "help": pygame.transform.scale(pygame.image.load("asset_menu/help.png"), (300, 300)),
            "quit": pygame.transform.scale(pygame.image.load("asset_menu/quit.png"), (300, 300)),
            "play": pygame.transform.scale(pygame.image.load("asset_menu/play.png"), (300, 100)),
            "settings": pygame.transform.scale(pygame.image.load("asset_menu/settings.png"), (100, 100)),
            "local": pygame.transform.scale(pygame.image.load("asset_menu/local.png"), (200, 100)),
            "online": pygame.transform.scale(pygame.image.load("asset_menu/online.png"), (200, 100)),
            "create_game": pygame.transform.scale(pygame.image.load("asset_menu/create.png"), (200, 100)),
            "join_game": pygame.transform.scale(pygame.image.load("asset_menu/join.png"), (200, 100)),
        }

    def run(self):
        while self.running:
            if self.current_screen == "menu":
                self.menu()
            elif self.current_screen == "choose_mode":
                self.choose_mode()
            elif self.current_screen == "enter_names":
                self.enter_names()
            elif self.current_screen == "create_game":
                self.create_game()
            elif self.current_screen == "join_game":
                self.join_game()
            elif self.current_screen == "create_or_join":
                self.create_or_join()
            elif self.current_screen == "settings":
                self.settings()
            elif self.current_screen == "game":
                self.game()

    def menu(self):
        # self.screen.fill(WHITE)
        self.screen.blit(self.__background_image, (0, 0))

        self.screen.blit(self.images["title"], ((self.screen.get_width() // 2 - self.images["title"].get_width() // 2),
                                                self.screen.get_height() // 2 - self.images["title"].get_height() // 2))

        button_spacing = 20
        total_width = self.images["play"].get_width() + button_spacing + self.images["settings"].get_width()
        start_x = (self.screen.get_width()) // 2 - total_width // 2
        play_button_pos = (start_x, self.screen.get_height() - 120)
        setting_button_pos = (start_x + self.images["play"].get_width() + button_spacing, self.screen.get_height() - 120)

        self.screen.blit(self.images["help"], (20, 20))
        self.screen.blit(self.images["quit"], (self.screen.get_width() - self.images["quit"].get_width() - 20, 20))
        self.screen.blit(self.images["play"], play_button_pos)
        self.screen.blit(self.images["settings"], setting_button_pos)

        pygame.display.update()
        self.handle_events(
            buttons=[
                {"rect": self.images["help"].get_rect(topleft=(20, 20)), "action": self.show_help},
                {"rect": self.images["quit"].get_rect(topleft=(self.screen.get_width() - self.images["quit"].get_width() - 20, 20)), "action": self.quit_game},
                {"rect": pygame.Rect(play_button_pos, self.images["play"].get_size()), "action": lambda: self.set_screen("choose_mode")},
                {"rect": pygame.Rect(setting_button_pos, self.images["settings"].get_size()), "action": lambda: self.set_screen("settings")}
            ]
        )

    def choose_mode(self):
        self.screen.blit(self.__background_image, (0, 0))
        # self.screen.fill(WHITE)
        button_spacing = 20
        total_width = self.images["local"].get_width() + button_spacing + self.images["online"].get_width()
        start_x = (self.screen.get_height() - total_width) // 2
        local_button_pos = (start_x, self.screen.get_height() // 2 - 60)
        online_button_pos = (start_x + self.images["local"].get_width() + button_spacing, self.screen.get_height() // 2 - 60)

        self.screen.blit(self.images["local"], local_button_pos)
        self.screen.blit(self.images["online"], online_button_pos)

        pygame.display.update()
        self.handle_events(
            buttons=[
                {"rect": pygame.Rect(local_button_pos, self.images["local"].get_size()), "action": lambda: self.set_screen("enter_names")},
                {"rect": pygame.Rect(online_button_pos, self.images["online"].get_size()), "action": lambda: self.set_screen("create_or_join")}
            ]
        )

    def enter_names(self):
        # self.screen.fill(WHITE)
        self.screen.blit(self.__background_image, (0, 0))

        font = pygame.font.Font(None, 36)

        # Define input boxes and labels
        player1_label_box = pygame.Rect(self.screen.get_width() // 2 - 300, self.screen.get_height() // 2 - 80, 100, 40)
        player1_box = pygame.Rect(self.screen.get_width() // 2 - 180, self.screen.get_height() // 2 - 80, 200, 40)
        player2_label_box = pygame.Rect(self.screen.get_width() // 2 - 300, self.screen.get_height() // 2, 100, 40)
        player2_box = pygame.Rect(self.screen.get_width() // 2 - 180, self.screen.get_height() // 2, 200, 40)
        start_button = pygame.Rect(self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 + 80, 100, 40)

        running = True
        while running:
            # self.screen.fill(WHITE)
            self.screen.blit(self.__background_image, (0, 0))

            pygame.draw.rect(self.screen, BLACK, player1_label_box, 2)
            pygame.draw.rect(self.screen, BLACK, player1_box, 2)
            pygame.draw.rect(self.screen, BLACK, player2_label_box, 2)
            pygame.draw.rect(self.screen, BLACK, player2_box, 2)
            pygame.draw.rect(self.screen, BLACK, start_button, 2)

            player1_label = font.render("Player 1:", True, BLACK)
            player2_label = font.render("Player 2:", True, BLACK)
            player1_text = font.render(self.player1_name, True, BLACK)
            player2_text = font.render(self.player2_name, True, BLACK)
            start_text = font.render("Start", True, BLACK)

            self.screen.blit(player1_label, (player1_label_box.x + 5, player1_label_box.y + 5))
            self.screen.blit(player1_text, (player1_box.x + 5, player1_box.y + 5))
            self.screen.blit(player2_label, (player2_label_box.x + 5, player2_label_box.y + 5))
            self.screen.blit(player2_text, (player2_box.x + 5, player2_box.y + 5))
            self.screen.blit(start_text, (start_button.x + 15, start_button.y + 5))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if player1_box.collidepoint(event.pos):
                        self.active_input = "player1"
                    elif player2_box.collidepoint(event.pos):
                        self.active_input = "player2"
                    elif start_button.collidepoint(event.pos):
                        self.set_screen("game")
                        running = False
                elif event.type == pygame.KEYDOWN:
                    if self.active_input == "player1":
                        if event.key == pygame.K_RETURN:
                            self.active_input = None
                        elif event.key == pygame.K_BACKSPACE:
                            self.player1_name = self.player1_name[:-1]
                        else:
                            self.player1_name += event.unicode
                    elif self.active_input == "player2":
                        if event.key == pygame.K_RETURN:
                            self.active_input = None
                        elif event.key == pygame.K_BACKSPACE:
                            self.player2_name = self.player2_name[:-1]
                        else:
                            self.player2_name += event.unicode

    def create_or_join(self):
        # self.screen.fill(WHITE)
        self.screen.blit(self.__background_image, (0, 0))

        button_spacing = 20
        total_width = self.images["create_game"].get_width() + button_spacing + self.images["join_game"].get_width()
        start_x = (self.screen.get_width() - total_width) // 2
        create_game_button_pos = (start_x, self.screen.get_height() // 2 - 60)
        join_game_button_pos = (start_x + self.images["create_game"].get_width() + button_spacing, self.screen.get_height() // 2 - 60)

        self.screen.blit(self.images["create_game"], create_game_button_pos)
        self.screen.blit(self.images["join_game"], join_game_button_pos)

        pygame.display.update()
        self.handle_events(
            buttons=[
                {"rect": pygame.Rect(create_game_button_pos, self.images["create_game"].get_size()), "action": lambda: self.set_screen("create_game")},
                {"rect": pygame.Rect(join_game_button_pos, self.images["join_game"].get_size()), "action": lambda: self.set_screen("join_game")}
            ]
        )

    def create_game(self):
        # Afficher un message à l'utilisateur pendant la création de la partie
        self.display_message("Creating Game...", duration=2000)

        # Mettre en œuvre la création de la session de jeu en réseau
        # Cela peut inclure l'initialisation d'un serveur, la génération d'un code unique pour la session, etc.

        # Après la création de la partie, revenir au menu principal
        self.set_screen("menu")

    def join_game(self, game_code_is_valid):
        # self.screen.fill(WHITE)
        self.screen.blit(self.__background_image, (0, 0))
        # Affichage du texte pour demander le code du jeu
        font = pygame.font.Font(None, 36)
        text = font.render("Enter Game Code:", True, BLACK)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 50))
        self.screen.blit(text, text_rect)

        # Affichage de la zone de texte pour entrer le code
        input_box = pygame.Rect(self.screen.get_width() // 2 - 100, self.screen.get_height() // 2, 200, 40)
        pygame.draw.rect(self.screen, BLACK, input_box, 2)

        # Affichage du bouton pour rejoindre le jeu
        join_button = pygame.Rect(self.screen.get_width() // 2 - 50, self.screen.get_height() // 2 + 60, 100, 40)
        pygame.draw.rect(self.screen, BLACK, join_button, 2)
        join_text = font.render("Join", True, BLACK)
        join_text_rect = join_text.get_rect(center=join_button.center)
        self.screen.blit(join_text, join_text_rect)

        pygame.display.update()

        # Variable pour stocker le code du jeu entré par l'utilisateur
        game_code = ""

        while True:
            self.screen.blit(self.__background_image, (0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Démarrez le jeu en réseau avec le code entré si le code est valide
                        if game_code_is_valid(game_code):
                            self.start_network_game(game_code)
                            return
                    elif event.key == pygame.K_BACKSPACE:
                        game_code = game_code[:-1]
                    else:
                        game_code += event.unicode
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if join_button.collidepoint(event.pos):
                        # Démarrez le jeu en réseau avec le code entré si le code est valide
                        if game_code_is_valid(game_code):
                            self.start_network_game(game_code)
                            return

            # Effacer la zone de texte avant de rendre à nouveau le texte saisi par l'utilisateur
            self.screen.fill(WHITE, input_box)

            # Afficher le texte entré par l'utilisateur dans la zone de texte
            entered_text = font.render(game_code, True, BLACK)
            entered_text_rect = entered_text.get_rect(center=input_box.center)
            self.screen.blit(entered_text, entered_text_rect)

            pygame.display.update()

            # Condition pour démarrer le jeu en réseau avec le code entré
            if game_code_is_valid(game_code):
                self.start_network_game(game_code)
                return

    def game_code_valid(self, code):
        # Implémentez la logique pour vérifier si le code est valide ou non
        # Par exemple, vérifiez si le code existe dans une base de données, ou s'il correspond à un jeu en attente, etc.
        # Retournez True si le code est valide, False sinon
        return True  # Exemple de réponse, remplacez par votre propre logique de validation

    def settings(self):
        settings = Settings(self.screen)
        settings.show_settings()
        self.set_screen("menu")

    def show_help(self): # à modifier pour les regles du jeu
        self.display_message("Help Instructions")

    def quit_game(self):
        self.running = False
        pygame.quit()
        sys.exit()

    def display_message(self, message, duration=1000):
        font = pygame.font.Font(None, 36)
        text = font.render(message, True, BLACK)
        text_rect = text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(text, text_rect)
        pygame.display.update()
        pygame.time.delay(duration)

    def handle_events(self, buttons):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button["rect"].collidepoint(event.pos):
                        button["action"]()

    def set_screen(self, screen_name):
        self.current_screen = screen_name

    def game(self):
        game_board = GUIBoard(self.player1_name, self.player2_name)
        game_board.run()

    def start_network_game(self, game_code):
        #Implementez le jeu en reseau
        pass


if __name__ == "__main__":
    controller = MainController()
    controller.run()
