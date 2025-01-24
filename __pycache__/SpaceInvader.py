import cv2
import numpy as np
from Vaisseau import vaisseau
from Ennemis import ennemi
from Projectile import projectile
from Jeu import jeu
from Constant import *
import random
import time
import os

import cv2

from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *




class spaceInvader : 
    def __init__(self):
        pass

    def initialiser_sprites(self):
        """
        Initialise les sprites utilisés dans le jeu.
        :return: Les sprites pour les projectiles, le vaisseau et les ennemis.
        """
        projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
        cv2.circle(projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

        vaisseau_sprite = np.ones((VAISSEAU_HEIGHT, VAISSEAU_WIDTH, 3), dtype=np.uint8) * 255
        ennemi_sprite = np.ones((ENNEMI_HEIGHT, ENNEMI_WIDTH, 3), dtype=np.uint8) * 255

        return projectile_sprite, vaisseau_sprite, ennemi_sprite


    def initialiser_objets(self,vaisseau_sprite, ennemi_sprite):
        """
        Initialise les objets principaux du jeu (vaisseau, ennemis).
        :param vaisseau_sprite: Sprite du vaisseau.
        :param ennemi_sprite: Sprite des ennemis.
        :return: Le vaisseau et la liste d'ennemis.
        """
        Vaisseau = vaisseau(
            position=[270, 500],
            graphic=vaisseau_sprite,
            vitesse_vaisseau=VITESSE_VAISSEAU,
            largeur=VAISSEAU_WIDTH,
            hauteur=VAISSEAU_HEIGHT,
            point_de_vie=10
        )

        ennemis = [
            ennemi(
                position=[100 + i * 100, 100],
                graphic=ennemi_sprite,
                vitesse_ennemi=VITESSE_ENNEMI,
                largeur=ENNEMI_WIDTH,
                hauteur=ENNEMI_HEIGHT,
                point_de_vie=1
            )
            for i in range(5)
        ]
        Jeu = jeu(
            joueur = "j1",
            score=0
        )
        return Vaisseau, ennemis, Jeu

    def create_vaisseau_proj(self,projectile_sprite,Vaisseau):
        return projectile(
                        graphic=projectile_sprite,
                        vitesse_projectile=VITESSE_PROJECTILES,
                        direction=-1,  # Monte
                        degat=1,
                        rayon=PROJECTILE_RADIUS,
                        position=[Vaisseau.position[0] + VAISSEAU_WIDTH // 2, Vaisseau.position[1]]
                    )

    def create_ennemi_proj(self,projectile_sprite,Ennemi):
        return projectile(
                        graphic=projectile_sprite,
                        vitesse_projectile=VITESSE_PROJECTILES_ENNEMI,
                        direction=1,  # Descend
                        degat=1,
                        rayon=PROJECTILE_RADIUS,
                        position=[Ennemi.position[0] + ENNEMI_WIDTH // 2, Ennemi.position[1] + ENNEMI_HEIGHT]
                    )

    