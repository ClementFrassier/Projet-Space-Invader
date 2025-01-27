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
        self.input_text = ""  # Stocke le texte entré
        self.confirmed_text = ""  # Stocke le texte confirmé
        self.is_typing = False  # Flag pour détecter si on est en train de taper
            

    def mouse_callback(self, event, x, y, flags, param):
        """Handles mouse clicks for text input and OK button."""
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if the click is inside the text input box
            if 50 <= x <= 300 and 50 <= y <= 100:  # Text input area
                self.is_typing = True  # Start typing
            # Check if the click is on the OK button
            elif 350 <= x <= 450 and 50 <= y <= 100:  # OK button
                self.is_typing = False  # Stop typing
                self.confirmed_text = self.input_text  # Confirm the text

    def menu_princiapl(self):
        """Displays the main menu, allowing the player to enter their name."""
        cv2.namedWindow("Menu principal")
        cv2.setMouseCallback("Menu principal", self.mouse_callback)  # Link the mouse callback

        while True:
            # Create the menu background
            menu_principal = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

            # Draw the text input box
            cv2.rectangle(menu_principal, (50, 50), (300, 100), (200, 200, 200), -1)
            cv2.rectangle(menu_principal, (50, 50), (300, 100), (0, 0, 0), 2)

            # Display the current input text
            cv2.putText(menu_principal, self.input_text, (60, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

            # Draw the OK button
            cv2.rectangle(menu_principal, (350, 50), (450, 100), (100, 200, 100), -1)
            cv2.putText(menu_principal, "OK", (370, 85), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

            # Display the confirmed name
            cv2.putText(menu_principal, f"Confirmed: {self.confirmed_text}", (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

            # Show the menu
            cv2.imshow("Menu principal", menu_principal)
            key = cv2.waitKey(1) & 0xFF

            # Handle keyboard input while typing
            if self.is_typing:
                if key == 8:  # Backspace
                    self.input_text = self.input_text[:-1]
                elif key == 13:  # Enter key
                    self.confirmed_text = self.input_text  # Confirm the input
                    self.is_typing = False
                    break  # Exit the menu to start the game
                elif key != 255:  # Any other key (avoid unprintable keys)
                    self.input_text += chr(key)

            # Allow exiting the menu with the Escape key
            if key == 27:  # Escape key
                cv2.destroyAllWindows()
                exit()  # Exit the program

        cv2.destroyAllWindows()
        return self.confirmed_text  # Return the player's name









    def initialiser_sprites(self):
        """
        Initialise les sprites utilisés dans le jeu.
        :return: Les sprites pour les projectiles, le vaisseau et les ennemis.
        """
        # Sprite des projectiles du vaisseau (bleu)
        projectile_vaisseau_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
        cv2.circle(projectile_vaisseau_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

        # Sprite des projectiles ennemis (rouge)
        projectile_ennemi_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
        cv2.circle(projectile_ennemi_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (0, 0, 255), -1)


        vaisseau_sprite = cv2.imread("image/vaisseau.png", cv2.IMREAD_UNCHANGED)
        ennemi_sprite = cv2.imread("image/ennemi.png", cv2.IMREAD_UNCHANGED)

        if vaisseau_sprite is None or ennemi_sprite is None:
            raise FileNotFoundError("Un ou plusieurs fichiers d'image sont introuvables.")
        
        return projectile_vaisseau_sprite, projectile_ennemi_sprite, vaisseau_sprite, ennemi_sprite



    def initialiser_objets(self,vaisseau_sprite, ennemi_sprite, nombreEnnemis,nom):
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
            point_de_vie=2
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
            for i in range(nombreEnnemis)
        ]
        Jeu = jeu(
            joueur = nom,
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

    def gerer_deplacement_ennemis(self,ennemis, ennemis_direction, jeu, game_graphic, game_window):
        """
        Gère le déplacement des ennemis et leur interaction avec le jeu.
        """
        if ennemis:
            # Vérification des limites de l'écran
            ennemis_bounds = [min(e.position[0] for e in ennemis), max(e.position[0] + ENNEMI_WIDTH for e in ennemis)]
            if ennemis_bounds[0] <= 0 or ennemis_bounds[1] >= WINDOW_WIDTH:
                ennemis_direction[0] = -ennemis_direction[0]

        if not ennemis:  # Si aucun ennemi n'est présent
            return None

        for Ennemi in ennemis[:]:
            Ennemi.position[0] += ennemis_direction[0]
            # Affichage des ennemis
            game_graphic.dessiner_ennemi(game_window, Ennemi)

            if Ennemi.point_de_vie <= 0:
                ennemis.remove(Ennemi)
                jeu.score += 1

        return ennemis


    def gerer_projectiles_vaisseau(self,vaisseau_proj, ennemis, game_graphic, game_window):
        """
        Gère le déplacement des projectiles du vaisseau et leurs interactions.
        """
        if not ennemis:  # Vérifie si ennemis est vide ou None
            return vaisseau_proj  # Pas d'ennemis à gérer, retourne juste les projectiles


        for proj in vaisseau_proj[:]:
            proj.move_projectile(1)  # Déplacement vers le haut
            if proj.is_out_of_bounds(WINDOW_HEIGHT):
                vaisseau_proj.remove(proj)
            else:
                game_graphic.dessiner_projectile_vaisseau(game_window, proj)
                for Ennemi in ennemis[:]:
                    if Ennemi.ennemi_projectile_interaction(proj):
                        vaisseau_proj.remove(proj)

        return vaisseau_proj


    def gerer_projectiles_ennemi(self, ennemi_proj, Vaisseau, ennemis, projectile_sprite, game_graphic, game_window):
        """
        Gère le déplacement des projectiles des ennemis et leurs interactions avec le vaisseau.
        """
        import random

        # Gestion du tir des ennemis
        for Ennemi in ennemis:
            if random.random() < PROBA_TIR_ENNEMI: #Gener un tire entre 0 et 1 si il est inferieur a la proba il tire
                nouveau_proj = self.create_ennemi_proj(projectile_sprite, Ennemi)
                ennemi_proj.append(nouveau_proj)

        # Déplacement des projectiles existants
        for proj in ennemi_proj[:]:
            proj.move_projectile(1)  # Déplacement vers le bas
            if proj.is_out_of_bounds(WINDOW_HEIGHT):
                ennemi_proj.remove(proj)
            else:
                game_graphic.dessiner_projectile_ennemi(game_window, proj)
                if Vaisseau.vaisseau_projectile_interaction(proj):
                    ennemi_proj.remove(proj)

        return ennemi_proj
