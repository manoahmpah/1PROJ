import pygame
from Music import MusicPlayer
#from rules import Rules


class Settings:
    def __init__(self, screen, music_player):
        self.screen = screen
        self.music_player = music_player
        self.running = True

        # Chargez les icônes de sourdine en ajustant leur taille
        self.mute_button = pygame.transform.scale(pygame.image.load(
            "asset_settings/volume_off_icon.png"), (50, 50))
        self.unmute_button = pygame.transform.scale(pygame.image.load(
            "asset_settings/volume_on_icon.png"), (50, 50))
        self.is_muted = False

        # Dimensions du curseur de volume
        self.slider_rect = pygame.Rect(450, 300, 300, 20)
        if self.music_player.background_music is not None:
            self.knob_rect = pygame.Rect(0, 0, 20, 40)
            self.knob_rect.center = (
                self.slider_rect.x + int(self.slider_rect.width * self.music_player.background_music.get_volume()),
                self.slider_rect.centery)
        else:
            self.knob_rect = None
        self.dragging = False

        # Charger l'image du titre
        self.title_image = pygame.transform.scale(pygame.image.load("asset_settings/title_settings.png"), (400, 200))

        # Initialiser les options du thème
        self.light_theme_checkbox = pygame.Rect(450, 400, 20, 20)
        self.dark_theme_checkbox = pygame.Rect(450, 430, 20, 20)

        # Charger l'image du checkmark
        self.checkmark_image = pygame.transform.scale(pygame.image.load("asset_settings/checkmark_icon.png"), (20, 20))

        # Boolean pour indiquer si les options du thème sont sélectionnées
        self.light_theme_selected = False
        self.dark_theme_selected = False

    def run(self):
        while self.running:
            # Remplir l'écran avec la couleur blanche
            self.screen.fill((255, 255, 255))

            # Affichage du titre centré en haut de l'écran
            self.screen.blit(self.title_image, ((WINDOW_WIDTH - self.title_image.get_width()) // 2, 50))

            # Affichage du curseur de volume si le lecteur de musique est initialisé
            if self.knob_rect is not None:
                pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
                pygame.draw.rect(self.screen, (0, 0, 0), self.knob_rect)

            # Affichage du texte "Music" à gauche du curseur
            font = pygame.font.Font(None, 48)
            music_text = font.render("Music", True, (0, 0, 0))
            self.screen.blit(music_text, (300, 290))

            # Affichage de l'icône de sourdine
            if self.is_muted:
                self.screen.blit(self.mute_button,
                                 (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))
            else:
                self.screen.blit(self.unmute_button,
                                 (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))

            # Affichage des options de thème
            pygame.draw.rect(self.screen, (0, 0, 0), self.light_theme_checkbox, 2)
            pygame.draw.rect(self.screen, (0, 0, 0), self.dark_theme_checkbox, 2)

            # Affichage du texte des options de thème
            light_theme_text = font.render("Light", True, (0, 0, 0))
            dark_theme_text = font.render("Dark", True, (0, 0, 0))
            self.screen.blit(light_theme_text, (300, 395))
            self.screen.blit(dark_theme_text, (300, 425))

            # Affichage des checkmarks si les options sont sélectionnées
            if self.light_theme_selected:
                self.screen.blit(self.checkmark_image, self.light_theme_checkbox.topleft)
            if self.dark_theme_selected:
                self.screen.blit(self.checkmark_image, self.dark_theme_checkbox.topleft)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.knob_rect is not None and self.knob_rect.collidepoint(event.pos):
                        self.dragging = True
                    elif self.is_muted_button_clicked(event.pos):
                        self.toggle_mute()
                    elif self.light_theme_checkbox.collidepoint(event.pos):
                        self.light_theme_selected = not self.light_theme_selected
                    elif self.dark_theme_checkbox.collidepoint(event.pos):
                        self.dark_theme_selected = not self.dark_theme_selected
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging and self.knob_rect is not None:
                        self.knob_rect.centerx = min(max(event.pos[0], self.slider_rect.x),
                                                     self.slider_rect.x + self.slider_rect.width)
                        volume = (self.knob_rect.centerx - self.slider_rect.x) / self.slider_rect.width
                        self.music_player.set_volume(volume)
                elif event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()

    def is_muted_button_clicked(self, pos):
        icon_rect = self.mute_button.get_rect(
            topleft=(self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))
        return icon_rect.collidepoint(pos)

    def toggle_mute(self):
        if self.is_muted:
            self.music_player.play_background_music()
            self.is_muted = False
        else:
            self.music_player.pause_background_music()
            self.is_muted = True


# Initialisation de Pygame
pygame.init()

# Dimensions de la fenêtre
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720
WINDOW_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

# Création de la fenêtre
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Settings")

# Initialisation du lecteur de musique en utilisant la classe MusicPlayer
music_player = MusicPlayer()

# Lancement de la page des paramètres
if __name__ == "__main__":
    settings_page = Settings(screen, music_player)
    settings_page.run()
