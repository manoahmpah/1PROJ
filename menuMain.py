import pygame
import sys
from GUI import GUIBoard  # Importer la classe GUIBoard depuis le fichier Gui.py
from rules import Rules

class GameMenu:
    def __init__(self):
        pygame.init()
        self.screen_width, self.screen_height = 1080, 730
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Menu")

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)

        self.font = pygame.font.Font(None, 36)

        # Charger l'image de fond et la redimensionner à la taille de la fenêtre
        try:
            self.background_img = pygame.image.load("asset_plateau/img.png")
            self.background_img = pygame.transform.smoothscale(self.background_img, (self.screen_width, self.screen_height))
        except pygame.error as e:
            print(f"Unable to load background image: {e}")
            sys.exit()

        # Charger et redimensionner les images pour les boutons
        try:
            self.play_img = pygame.image.load("asset_menu/asset_first_btn/play.png")
            self.help_img = pygame.image.load("asset_menu/asset_first_btn/help.png")
        except pygame.error as e:
            print(f"Unable to load image: {e}")
            sys.exit()

        # Définir les nouvelles dimensions pour les boutons
        new_width, new_height = 150, 150  # Vous pouvez ajuster ces valeurs

        # Redimensionner les images des boutons
        self.play_img = pygame.transform.scale(self.play_img, (new_width, new_height))
        self.help_img = pygame.transform.scale(self.help_img, (new_width, new_height))

        # Positions des boutons
        play_button_x = (self.screen_width // 2) - (new_width // 2)
        play_button_y = self.screen_height - new_height - 50

        help_button_x = self.screen_width - new_width
        help_button_y = 0


        self.buttons = [
            {"image": self.play_img, "rect": self.play_img.get_rect(topleft=(play_button_x, play_button_y))},
            {"image": self.help_img, "rect": self.help_img.get_rect(topleft=(help_button_x, 0))},
        ]

        try:
            self.logo_img = pygame.image.load("asset_menu/logo.png")
            self.logo_img = pygame.transform.scale(self.logo_img, (400, 400))
        except pygame.error as e:
            print(f"Unable to load logo image: {e}")
            sys.exit()

        try:
            self.questions_images = [
                pygame.transform.scale(pygame.image.load("asset_menu/asset_questions/choose_game_type.png"), (500, 350)),
                pygame.transform.scale(pygame.image.load("asset_menu/asset_questions/choose_game_type.png"), (500, 350)),
                pygame.transform.scale(pygame.image.load("asset_menu/asset_questions/network_game.png"), (500, 350))
            ]
            self.options_images = {
                "Blitz": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/blitz.png"), (150, 150)),
                "Normal": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/normal.png"), (150, 150)),
                "1vs1": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/1vs1.png"), (150, 150)),
                "1vsIA": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/1vsAI.png"), (150, 150)),
                "Yes": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/online.png"), (150, 150)),
                "No": pygame.transform.scale(pygame.image.load("asset_menu/asset_options/local.png"), (150, 150)),
            }
        except pygame.error as e:
            print(f"Unable to load question or option image: {e}")
            sys.exit()

        self.play_steps = [
            {"question": self.questions_images[0], "options": ["Blitz", "Normal"]},
            {"question": self.questions_images[1], "options": ["1vs1", "1vsIA"]},
            {"question": self.questions_images[2], "options": ["Yes", "No"]}
        ]
        self.play_answers = []

        self.current_step = 0
        self.play_mode = False
        self.network_message_shown = False

        option_width, option_height = 150, 150
        space_between_options = 20
        total_options_width = 2 * option_width + space_between_options

        option_area_x = (self.screen_width - total_options_width) // 2
        option_area_y = (self.screen_height - option_height) // 2

        self.option_buttons = [
            {"label": "", "rect": pygame.Rect(option_area_x, option_area_y, option_width, option_height)},
            {"label": "", "rect": pygame.Rect(option_area_x + option_width + space_between_options, option_area_y, option_width, option_height)}
        ]

        self.back_button = {"label": "Back", "rect": pygame.Rect(self.screen_width - 200, self.screen_height - 100, 150, 50)}

    def draw_buttons(self):
        for button in self.buttons:
            self.screen.blit(button["image"], button["rect"])

    def draw_question(self):
        if self.network_message_shown:
            message = "The game Yinsh is not available in network version."
            message_text = self.font.render(message, True, self.RED)
            self.screen.blit(message_text, (50, 100))
        else:
            step = self.play_steps[self.current_step]
            question_image = step["question"]
            options = step["options"]

            self.screen.blit(question_image, (290, 100))

            for i, option in enumerate(options):
                self.option_buttons[i]["label"] = option
                self.screen.blit(self.options_images[option], self.option_buttons[i]["rect"])

            pygame.draw.rect(self.screen, self.GRAY, self.back_button["rect"])
            back_text = self.font.render(self.back_button["label"], True, self.BLACK)
            back_text_rect = back_text.get_rect(center=self.back_button["rect"].center)
            self.screen.blit(back_text, back_text_rect)

    def play_action(self):
        self.play_mode = True
        self.current_step = 0
        self.play_answers.clear()
        self.network_message_shown = False

    def help_action(self):
        Rules().run()

    def handle_answer(self, answer):
        self.play_answers.append(answer)

        if self.current_step == 1 and answer == "1vsIA":
            self.current_step += 3
        elif self.current_step == 2 and answer == "No":
            self.current_step += 2
        elif self.current_step == 2 and answer == "Yes":
            self.network_message_shown = True
            self.play_mode = False
            self.show_error_message("Network game is not available yet.")
        else:
            self.current_step += 1

        if self.current_step >= len(self.play_steps) or self.network_message_shown:
            self.play_mode = False
            if not self.network_message_shown:
                if self.current_step >= len(self.play_steps):
                    self.launch_gui_board()

    def handle_back(self):
        if self.current_step > 0:
            self.current_step -= 1
            if self.play_answers:
                self.play_answers.pop()

    def show_error_message(self, message):
        error_font = pygame.font.Font(None, 30)
        error_text = error_font.render(message, True, self.RED)
        error_rect = error_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
        self.screen.blit(error_text, error_rect)
        pygame.display.flip()
        pygame.time.wait(3000)

    def launch_gui_board(self):
        ia = False
        gameMode = 1
        if self.play_answers[1] == "1vsIA":
            ia = True
        if self.play_answers[0] == "Blitz":
            gameMode = 2

        plateau = GUIBoard('player1', 'player2', ia=ia, game_mode=gameMode)
        plateau.run()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.play_mode:
                        if self.network_message_shown:
                            self.play_mode = False
                        else:
                            if self.back_button["rect"].collidepoint(event.pos):
                                self.handle_back()
                            else:
                                for button in self.option_buttons:
                                    if button["rect"].collidepoint(event.pos):
                                        self.handle_answer(button["label"])
                    else:
                        for button in self.buttons:
                            if button["rect"].collidepoint(event.pos):
                                if button["rect"] == self.buttons[0]["rect"]:
                                    self.play_action()
                                elif button["rect"] == self.buttons[1]["rect"]:
                                    self.help_action()

            self.screen.blit(self.background_img, (0, 0))

            if self.play_mode:
                self.draw_question()
            else:
                self.draw_buttons()
                self.logo_rect = self.logo_img.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
                self.screen.blit(self.logo_img, self.logo_rect)

            pygame.display.flip()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game_menu = GameMenu()
    game_menu.run()
