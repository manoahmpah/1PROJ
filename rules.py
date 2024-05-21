import pygame
import os
import re

class Rules:
    def __init__(self, rect):
        pygame.init()
        self.__screen = pygame.display.set_mode((1080, 720))
        pygame.display.set_caption("rules")
        self.__running = True
        self.__rect = rect
        self.__font = pygame.font.Font(None, 36)
        self.__NOIR = (0, 0, 0)
        self.__scroll_y = 0  # Position de défilement initiale

        self.__long_text = (
            "Salut Lina ! Bienvenue dans le monde fascinant de YINSH, prête à apprendre comment jouer ? "
            "Salut Max ! Oui, je suis prête. Le plateau a l'air intéressant, par où commencer ? "
            "Commençons par les bases, YINSH est un jeu de stratégie abstrait où le but est de retirer trois de vos anneaux du plateau, mais avant ça, il faut comprendre comment placer et déplacer les anneaux et les marqueurs. "
            "D'accord, comment placer les anneaux ? "
            "Chaque joueur commence avec cinq anneaux, on les place chacun à son tour sur les points d'intersection du plateau. "
            "(fait glisser un anneau sur un point d'intersection) Comme ça ? "
            "Parfait ! On continue à placer les anneaux jusqu'à ce que tous les dix soient sur le plateau. "
            "Tous les anneaux sont placés. Que fait-on maintenant ? "
            "Maintenant, chaque tour consiste à déplacer un de tes anneaux, mais avant de le déplacer, tu dois placer un marqueur à l'intérieur de l'anneau que tu veux déplacer. "
            "(place un marqueur dans un anneau) C'est fait. Et ensuite ? "
            "Ensuite, tu fais glisser l'anneau le long des lignes jusqu'à un point d'intersection libre, l'anneau peut sauter par-dessus des marqueurs, mais il ne peut pas s'arrêter sur eux ni sauter par-dessus d'autres anneaux. "
            "(fait glisser l'anneau jusqu'à un point libre) Comme ça ? "
            "Exactement ! Chaque fois que tu te déplaces, tu laisses un marqueur derrière toi. "
            "Les marqueurs s'accumulent sur le plateau, quel est l'objectif ? "
            "L'objectif est de créer des lignes de cinq marqueurs de ta couleur, horizontalement, verticalement ou en diagonale. Lorsque tu en formes une, tu retires cette ligne et l'un de tes anneaux. "
            "(fait une ligne de cinq marqueurs) Comme ça ? "
            "Oui, retire les marqueurs de la ligne et un de tes anneaux, le premier joueur à retirer trois de ses anneaux gagne la partie. "
            "J'ai retiré trois anneaux ! J'ai gagné ? "
            "Félicitations, Lina ! Tu as bien compris les règles de base de YINSH, avec la pratique, tu développeras des stratégies encore plus efficaces. "
            "Merci, Max ! J'ai hâte de jouer plus de parties et de m'améliorer. "
            "Super ! N'oublie pas que chaque partie est différente, alors amuse-toi bien en découvrant toutes les possibilités stratégiques de YINSH. "
        )

        # Séparer les phrases avec ponctuation
        self.phrases = re.findall(r'[^.?]+[.?]', self.__long_text)
        self.current_phrase_index = 0

        # Charger les images
        self.images = [
            pygame.image.load('asset_rules/feuille.png'),
            pygame.image.load('asset_rules/fleur.png')  # Remplacer par le chemin de votre deuxième image
        ]
        self.images = [pygame.transform.scale(img, (150, 150)) for img in self.images]  # Redimensionner les images si nécessaire
        self.current_image_index = 0

        # Créer les canvases
        self.canvases = [self.create_canvas(phrase) for phrase in self.phrases]

    def create_canvas(self, text):
        screen_width, screen_height = 1080, 720
        canvas_surface = pygame.Surface((screen_width, screen_height))
        canvas_surface.fill((255, 255, 255))

        # Diviser le texte en lignes si nécessaire
        wrapped_text = self.wrap_text(text, screen_width - 40)  # Marge de 20 pixels de chaque côté
        y_offset = 140  # Position initiale du texte

        # Ajouter du texte au canvas
        font = pygame.font.SysFont(None, 72)
        for line in wrapped_text:
            text_rendered = font.render(line, True, self.__NOIR)
            text_rect = text_rendered.get_rect(center=(screen_width // 2, y_offset))
            canvas_surface.blit(text_rendered, text_rect)
            y_offset += font.get_height() + 10  # Espacement entre les lignes

        # Ajouter une image au canvas
        current_image = self.images[self.current_image_index]
        image_rect = current_image.get_rect(center=(screen_width // 2, screen_height - 100))  # Positionner l'image vers le bas
        canvas_surface.blit(current_image, image_rect)

        return canvas_surface

    def wrap_text(self, text, max_width):
        """ Divise le texte en lignes de manière à ce qu'il tienne dans la largeur maximale spécifiée. """
        words = text.split(' ')
        lines = []
        current_line = ""
        font = pygame.font.SysFont(None, 72)

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.strip())
                current_line = word + " "

        lines.append(current_line.strip())
        return lines

    def Button(self):
        while self.__running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.__running = False
                    pygame.quit()
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        x, y = event.pos
                        if self.__rect.collidepoint(x, y):
                            self.current_phrase_index += 1
                            if self.current_phrase_index >= len(self.canvases):
                                self.__running = False  # Arrêter la boucle principale
                                os.system("python menu.py")
                            self.current_image_index = (self.current_image_index + 1) % len(self.images)
                            self.canvases = [self.create_canvas(phrase) for phrase in self.phrases]

            if not self.__running:
                break

            self.__screen.fill((255, 255, 255))  # Effacer l'écran

            # Dessiner le canvas actuel
            self.__screen.blit(self.canvases[self.current_phrase_index], (0, 0))

            # Dessiner le bouton
            pygame.draw.rect(self.__screen, (0, 0, 0), self.__rect)
            texte_surface = self.__font.render("Suivant", True, (255, 255, 255))
            texte_rect = texte_surface.get_rect(center=self.__rect.center)
            self.__screen.blit(texte_surface, texte_rect)

            pygame.display.flip()  # Mettre à jour l'affichage

if __name__ == "__main__":
    regle = Rules(pygame.Rect(950, 50, 100, 50))
    regle.Button()
