import pygame
import sys

class Settings:
    def __init__(self, screen, music_player):
        self.screen = screen
        self.music_player = music_player
        self.running = True

        # Chargez les icônes de sourdine
        self.mute_button = pygame.image.load("asset-Setting/volume_off_icon.png")
        self.unmute_button = pygame.image.load("asset-Setting/volume_on_icon.png")
        self.is_muted = False

        # Dimensions du curseur de volume
        self.slider_rect = pygame.Rect(150, 300, 300, 20)
        self.knob_rect = pygame.Rect(0, 0, 20, 40)
        self.knob_rect.center = (self.slider_rect.x + int(self.slider_rect.width * self.music_player.background_music.get_volume()), self.slider_rect.centery)
        self.dragging = False

    def run(self):
        while self.running:
            self.screen.fill((200, 200, 200))

            # Affichage du curseur de volume
            pygame.draw.rect(self.screen, (100, 100, 100), self.slider_rect)
            pygame.draw.rect(self.screen, (255, 0, 0), self.knob_rect)

            # Affichage de l'icône de sourdine
            if self.is_muted:
                self.screen.blit(self.mute_button, (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))
            else:
                self.screen.blit(self.unmute_button, (self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.knob_rect.collidepoint(event.pos):
                        self.dragging = True
                    elif self.is_muted_button_clicked(event.pos):
                        self.toggle_mute()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        self.knob_rect.centerx = min(max(event.pos[0], self.slider_rect.x), self.slider_rect.x + self.slider_rect.width)
                        volume = (self.knob_rect.centerx - self.slider_rect.x) / self.slider_rect.width
                        self.music_player.set_volume(volume)

    def is_muted_button_clicked(self, pos):
        icon_rect = self.mute_button.get_rect(topleft=(self.slider_rect.x + self.slider_rect.width + 20, self.slider_rect.y - 10))
        return icon_rect.collidepoint(pos)

    def toggle_mute(self):
        if self.is_muted:
            self.music_player.play_background_music()
            self.is_muted = False
        else:
            self.music_player.pause_background_music()
            self.is_muted = True
