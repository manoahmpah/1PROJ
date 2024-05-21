import pygame
from Music import MusicPlayer
from ThemeManager import ThemeManager


class Settings:
    def __init__(self, screen, music_player, theme_manager):
        self.screen = screen
        self.music_player = music_player
        self.theme_manager = ThemeManager()
        self.running = True

        # Charger les icônes de sourdine en ajustant leur taille
        self.mute_button = pygame.transform.scale(pygame.image.load(
            f"assets/{self.theme_manager.theme}/volume_off_icon.png"), (50, 50))
        self.unmute_button = pygame.transform.scale(pygame.image.load(
            f"assets/{self.theme_manager.theme}/volume_on_icon.png"), (50, 50))
        self.is_muted = False

        # Dimensions du curseur de volume
        self.slider_rect = pygame.Rect(150, 300, 300, 20)
        if self.music_player.background_music is not None:
            self.knob_rect = pygame.Rect(0, 0, 20, 40)
            self.knob_rect.center = (
            self.slider_rect.x + int(self.slider_rect.width * self.music_player.background_music.get_volume()),
            self.slider_rect.centery)
        else:
            self.knob_rect = None
        self.dragging = False

    def run(self):
        while self.running:
            self.screen.fill((200, 200, 200))

            # Affichage du curseur de volume si le lecteur de musique est initialisé
            if self.knob_rect is not None:
                pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
                pygame.draw.rect(self.screen, (255, 0, 0), self.knob_rect)

            # Affichage de l'icône de sourdine
            if self.is_muted:
                self.screen.blit(self.mute_button,
                                 (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))
            else:
                self.screen.blit(self.unmute_button,
                                 (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.knob_rect is not None and self.knob_rect.collidepoint(event.pos):
                        self.dragging = True
                    elif self.is_muted_button_clicked(event.pos):
                        self.toggle_mute()
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

# Couleur de l'écran
WHITE = (255, 255, 255)

# Création de la fenêtre
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Settings")

# Initialisation du lecteur de musique en utilisant la classe MusicPlayer
music_player = MusicPlayer()

# Lancement de la page des paramètres
if __name__ == "__main__":
    settings_page = Settings(screen, music_player)
    settings_page.run()
