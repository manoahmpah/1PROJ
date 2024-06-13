import pygame
import sys
import subprocess

class Rules:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1080, 730))
        self.clock = pygame.time.Clock()
        self.images = [pygame.image.load(f'./asset_rules/{i}.png') for i in range(1, 23)]  # Assurez-vous que vos images sont nommées image_1.png, image_2.png, ..., image_22.png
        self.images = [pygame.transform.smoothscale(image, (1080, 730)) for image in self.images]
        self.current_image_index = 0
        self.change_button_rect = pygame.Rect(950, 20, 100, 50)
        self.font = pygame.font.Font(None, 36)
        self.change_button_text = self.font.render("Changer", True, (255, 255, 255))

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.change_button_rect.collidepoint(event.pos):
                            self.current_image_index = (self.current_image_index + 1) % len(self.images)
                            if self.current_image_index == 21:  # Si c'est la 22ème image
                                self.launch_next_script()
                                return  # Terminer la boucle pour fermer la fenêtre Pygame

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.images[self.current_image_index], (0, 0))
            pygame.draw.rect(self.screen, (0, 0, 0), self.change_button_rect)
            self.screen.blit(self.change_button_text, (960, 30))

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def launch_next_script(self):
        pygame.quit()
        subprocess.run(["python", "menuMain.py"])

if __name__ == "__main__":
    rules_display = Rules()
    rules_display.run()