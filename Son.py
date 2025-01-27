import pygame

def init_son():
    """
    Initialise le module audio de Pygame.
    """
    pygame.mixer.init()

def charger_musique(fichier):
    """
    Charge une musique de fond.
    :param fichier: Chemin du fichier de musique (str)
    """
    pygame.mixer.music.load(fichier)

def jouer_musique(volume=1, boucle=True):
    """
    Joue la musique chargée.
    :param volume: Volume de la musique (float, entre 0.0 et 1.0)
    :param boucle: True pour jouer en boucle, False pour jouer une fois
    """
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if boucle else 0)

def arreter_musique():
    """
    Arrête la musique en cours.
    """
    pygame.mixer.music.stop()

def charger_effet_sonore(fichier):
    """
    Charge un effet sonore.
    :param fichier: Chemin du fichier audio (str)
    :return: Objet pygame.mixer.Sound
    """
    return pygame.mixer.Sound(fichier)

def jouer_effet_sonore(effet, volume=0.2):
    """
    Joue un effet sonore.
    :param effet: Objet pygame.mixer.Sound
    :param volume: Volume du son (float, entre 0.0 et 1.0)
    """
    effet.set_volume(volume)
    effet.play()
