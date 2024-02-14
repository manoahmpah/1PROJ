import pygame

pygame.init()

# ------- generer la fenetre de notre jeu ------- #
pygame.display.set_caption("Settings")
screen = pygame.display.set_mode((1080, 720))

backgroud = pygame.image.load("Assets-Setting/BackGround.png")

# ------- mettre du text ------- #
font = pygame.font.Font(None, 36)
Account = font.render("Account", True, (0, 0, 0))
Languages = font.render("Languages", True, (0, 0, 0))
Sound = font.render("Sound", True, (0, 0, 0))
Customization = font.render("Customization", True, (0, 0, 0))

running = True
# ------- boucle tant que cette conditiojn est vrai ------- #
while running:
    # appliquer l'arrière plan de notre Jeu
    screen.blit(backgroud, (0, -200))
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, screen.get_width()/4, screen.get_height()))

    # affichage du texte
    screen.blit(Account, (10, 15))
    screen.blit(Languages, (10, 55))
    screen.blit(Sound, (10, 95))
    screen.blit(Customization, (10, 135))

    # mettre à jour notre ecran
    pygame.display.flip()

    # si le joueur ferme cette fenetre
    for event in pygame.event.get():
        # Que l'evenement est fermeture de fenetre
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()


