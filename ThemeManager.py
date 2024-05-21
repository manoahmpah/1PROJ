import pygame
import os


class ThemeManager:
    def __init__(self, theme="light"):
        self.theme = theme
        self.load_images()

    def load_images(self):
        theme_path = f"assets/{self.theme}/"
        self.images = {
            "title": pygame.transform.scale(pygame.image.load(os.path.join(theme_path, "title_settings.png")),
                                            (400, 200)),
            "volume_off": pygame.transform.scale(pygame.image.load(os.path.join(theme_path, "volume_off_icon.png")),
                                                 (50, 50)),
            "volume_on": pygame.transform.scale(pygame.image.load(os.path.join(theme_path, "volume_on_icon.png")),
                                                (50, 50)),
            "checkmark": pygame.transform.scale(pygame.image.load(os.path.join(theme_path, "checkmark_icon.png")),
                                                (20, 20))
        }
        self.colors = {
            "background": (255, 255, 255) if self.theme == "light" else (0, 0, 0),
            "text": (0, 0, 0) if self.theme == "light" else (255, 255, 255)
        }

    def toggle_theme(self):
        self.theme = "dark" if self.theme == "light" else "light"
        self.load_images()
