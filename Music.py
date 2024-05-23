import pygame


class MusicPlayer:
    def __init__(self):
        pygame.mixer.init()
        self.background_music = pygame.mixer.Sound('background_music.mp3')
        self.background_music.set_volume(0.5)

    def play_background_music(self):
        self.background_music.play(-1)

    def pause_background_music(self):
        self.background_music.stop()

    def set_volume(self, volume):
        self.background_music.set_volume(volume)
