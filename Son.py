import pygame

# Initialisation de Pygame
pygame.init()

# Initialisation du mixer pour le son
pygame.mixer.init()

# Charger la musique de fond
pygame.mixer.music.load("MusiqueFondJeu.mp3")  # Remplace "musique_fond.mp3" par le nom de ton fichier

# Démarrer la musique en boucle
pygame.mixer.music.play(-1)  # -1 signifie répétition infinie

# Exemple : Afficher une fenêtre simple pour tester
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders avec musique")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

pygame.quit()
