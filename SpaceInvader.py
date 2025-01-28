import cv2
import numpy as np
from Starship import spaceship
from Enemies import enemy
from Projectile import projectile
from Player import player
from Constant import *
import random
import time
import os

import cv2

from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *

class spaceInvader:
    
    def __init__(self, explosion_sound):
        """
        Initializes the Space Invaders game class.

        :param explosion_sound: Sound to play during explosions.
        """
        self.input_text = ""  # Stores the text entered by the player
        self.confirmed_text = ""  # Stores the confirmed text
        self.is_typing = False  # Flag to detect if the player is typing
        self.explosion_sound = explosion_sound  # Explosion sound
        self.font = cv2.FONT_HERSHEY_SIMPLEX  # Font used for text rendering

    def mouse_callback(self, event, x, y, flags, param):
        """
        Handles mouse click events for text input and the OK button.

        :param event: Mouse event type
        :param x, y: Mouse position
        :param flags: Event flags
        :param param: Additional parameters passed to the callback
        """
        if event == cv2.EVENT_LBUTTONDOWN:
            # Check if the click is inside the text input box
            if WINDOW_WIDTH // 2 - 125 <= x <= WINDOW_WIDTH // 2 + 125 and WINDOW_HEIGHT // 2 - 25 <= y <= WINDOW_HEIGHT // 2 + 25:
                self.is_typing = True  # Start typing

    def menu_principal(self):
        """
        Displays the main menu where the player can enter their name.

        :return: The player's confirmed name
        """
        cv2.namedWindow("Main Menu")
        cv2.setMouseCallback("Main Menu", self.mouse_callback)  # Link mouse callback

        while True:
            # Create the menu background (space theme)
            main_menu = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

            # Add space background (stars field)
            self.add_starfield(main_menu)

            # Centering calculations for text input box
            text_box_width = 250
            text_box_height = 50
            center_x = WINDOW_WIDTH // 2
            center_y = WINDOW_HEIGHT // 2

            # Draw the text input box at the center
            top_left_x = center_x - text_box_width // 2
            top_left_y = center_y - text_box_height // 2
            bottom_right_x = center_x + text_box_width // 2
            bottom_right_y = center_y + text_box_height // 2

            cv2.rectangle(main_menu, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (200, 200, 200), -1)
            cv2.rectangle(main_menu, (top_left_x, top_left_y), (bottom_right_x, bottom_right_y), (255, 255, 255), 2)

            # Display the current input text inside the centered box
            text_position_x = top_left_x + 10
            text_position_y = top_left_y + 30
            cv2.putText(main_menu, self.input_text, (text_position_x, text_position_y), self.font, 0.7, (0, 0, 0), 2)

            # Add instruction text
            instruction_text = "Press enter to play"
            instruction_text2 = "Click the box below to enter your name"

            # Calculate positions for instruction text
            text_size = cv2.getTextSize(instruction_text, self.font, 0.7, 2)[0]
            text_size2 = cv2.getTextSize(instruction_text2, self.font, 0.7, 2)[0]

            instruction_x = center_x - text_size[0] // 2
            instruction_y = bottom_right_y + 40
            instruction_x2 = center_x - text_size2[0] // 2
            instruction_y2 = bottom_right_y - 75

            # Display instructions
            cv2.putText(main_menu, instruction_text, (instruction_x, instruction_y), self.font, 0.7, (255, 0, 255), 2)
            cv2.putText(main_menu, instruction_text2, (instruction_x2, instruction_y2), self.font, 0.7, (255, 0, 255), 2)

            # Show the menu
            cv2.imshow("Main Menu", main_menu)
            key = cv2.waitKey(1) & 0xFF

            # Handle keyboard input while typing
            if self.is_typing:
                if key == 8:  # Backspace
                    self.input_text = self.input_text[:-1]
                elif key == 13:  # Enter key
                    self.confirmed_text = self.input_text  # Confirm input
                    self.is_typing = False
                    break  # Exit menu to start the game
                elif key != 255:  # Any other key
                    self.input_text += chr(key)

            # Allow exiting the menu with the Escape key
            if key == 27:  # Escape key
                cv2.destroyAllWindows()
                exit()  # Exit the program

        cv2.destroyAllWindows()
        return self.confirmed_text  # Return the player's name

    def add_starfield(self, image):
        """
        Adds a field of stars to simulate space background.

        :param image: Image to modify
        """
        for _ in range(200):  # Number of stars
            x = random.randint(0, image.shape[1] - 1)
            y = random.randint(0, image.shape[0] - 1)
            brightness = random.randint(0, 255)
            image[y, x] = [brightness, brightness, brightness]

    def draw_input_box(self, image):
        """
        Draws the text input box with glowing edges.

        :param image: Image to modify
        """
        cv2.rectangle(image, (50, 50), (300, 100), (200, 200, 200), -1)
        cv2.rectangle(image, (50, 50), (300, 100), (255, 255, 255), 2)  # White border

    def draw_input_text(self, image):
        """
        Displays the current input text.

        :param image: Image to render text on
        """
        cv2.putText(image, self.input_text, (60, 85), self.font, 0.7, (0, 0, 0), 2)

    def initialize_sprites(self):
        """
        Initializes the sprites used in the game (projectiles, spaceship, enemies).

        :return: Sprites for the projectiles, spaceship, and enemies.
        """
        # Spaceship projectile sprite (blue)
        spaceship_projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
        cv2.circle(spaceship_projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (255, 0, 0), -1)

        # Enemy projectile sprite (red)
        enemy_projectile_sprite = np.zeros((PROJECTILE_RADIUS * 2, PROJECTILE_RADIUS * 2, 3), dtype=np.uint8)
        cv2.circle(enemy_projectile_sprite, (PROJECTILE_RADIUS, PROJECTILE_RADIUS), PROJECTILE_RADIUS, (0, 0, 255), -1)

        spaceship_sprite = cv2.imread("image/vaisseau.png", cv2.IMREAD_UNCHANGED)
        enemy_sprite = cv2.imread("image/ennemi.png", cv2.IMREAD_UNCHANGED)

        if spaceship_sprite is None or enemy_sprite is None:
            raise FileNotFoundError("One or more image files are missing.")
        
        return spaceship_projectile_sprite, enemy_projectile_sprite, spaceship_sprite, enemy_sprite

    def initialize_objects(self, spaceship_sprite, enemy_sprite, enemy_count, name):
        """
        Initializes the main objects in the game (spaceship, enemies).

        :param spaceship_sprite: Sprite for the spaceship
        :param enemy_sprite: Sprite for the enemies
        :param enemy_count: Number of enemies to spawn
        :param name: Player's name
        :return: Spaceship, list of enemies, and the game object
        """
        Spaceship = spaceship(
            position=[270, 500],
            graphic=spaceship_sprite,
            spaceship_speed=SHIP_SPEED,
            width=SHIP_WIDTH,
            height=SHIP_HEIGHT,
            health_points=2
        )

        enemies = [
            enemy(
                position=[100 + i * 100, 100],
                sprite=enemy_sprite,
                velocity=ENEMY_SPEED,
                width=ENEMY_WIDTH,
                height=ENEMY_HEIGHT,
                health_points=1
            )
            for i in range(enemy_count)
        ]
        Player = player(
            player_name=name,
            score=0
        )
        return Spaceship, enemies, Player

    def create_spaceship_projectile(self, projectile_sprite, spaceship):
        """
        Creates a new spaceship projectile.

        :param projectile_sprite: Sprite for the projectile
        :param spaceship: The spaceship object
        :return: New spaceship projectile
        """

        return projectile(
            graphic=projectile_sprite,
            projectile_speed=PROJECTILE_SPEED,
            direction=-1,  # Moves upwards
            damage=1,
            radius=PROJECTILE_RADIUS,
            position=[spaceship.position[0] + SHIP_WIDTH // 2, spaceship.position[1]]
        )

    def create_enemy_projectile(self, projectile_sprite, enemy):
        """
        Creates a new enemy projectile.

        :param projectile_sprite: Sprite for the projectile
        :param enemy: The enemy object
        :return: New enemy projectile
        """
        return projectile(
            graphic=projectile_sprite,
            projectile_speed=ENEMY_PROJECTILE_SPEED,
            direction=1,  # Moves downwards
            damage=1,
            radius=PROJECTILE_RADIUS,
            position=[enemy.position[0] + ENEMY_WIDTH // 2, enemy.position[1] + ENEMY_HEIGHT]
        )

    def handle_enemy_movement(self, enemies, enemy_direction, game, game_graphics, game_window):
        """
        Handles the movement of enemies and their interaction with the game.

        :param enemies: List of enemy objects
        :param enemy_direction: Direction of enemy movement
        :param game: Game object
        :param game_graphics: Game graphics object
        :param game_window: Game window to render
        :return: Updated list of enemies
        """
        if enemies:
            # Check the screen bounds for enemies
            enemy_bounds = [min(e.position[0] for e in enemies), max(e.position[0] + ENEMY_WIDTH for e in enemies)]
            if enemy_bounds[0] <= 0 or enemy_bounds[1] >= WINDOW_WIDTH:
                enemy_direction[0] = -enemy_direction[0]

        if not enemies:  # If no enemies are present
            return None

        for enemy in enemies[:]:
            enemy.position[0] += enemy_direction[0]
            # Render the enemies
            game_graphics.draw_enemy(game_window, enemy)
            print("OKKKKK")
            if enemy.health_points <= 0:
                print("OKKKKK ENEMI")
                game.score += 1
                enemies.remove(enemy)
        return enemies

    def handle_spaceship_projectiles(self, spaceship_projectiles, enemies, game_graphics, game_window):
        """
        Handles the movement of spaceship projectiles and their interactions with enemies.

        :param spaceship_projectiles: List of spaceship projectiles
        :param enemies: List of enemies
        :param game_graphics: Game graphics object
        :param game_window: Game window to render
        :return: Updated list of spaceship projectiles
        """
        for projectile in spaceship_projectiles[:]:
            projectile.position[1] += projectile.direction * projectile.projectile_speed
            if projectile.position[1] < 0 or projectile.position[1] > WINDOW_HEIGHT:
                spaceship_projectiles.remove(projectile)
                continue

            for enemy in enemies[:]:
                if self.check_collision(projectile, enemy):
                    spaceship_projectiles.remove(projectile)
                    enemy.health_points -= projectile.damage
                 
                    break

            game_graphics.draw_ship_projectile(game_window, projectile)
        
        return spaceship_projectiles

    def check_collision(self, projectile, enemy):
        """
        Checks if a projectile has collided with an enemy.

        :param projectile: The projectile object
        :param enemy: The enemy object
        :return: True if collision occurs, False otherwise
        """
        return (
            projectile.position[0] > enemy.position[0] and
            projectile.position[0] < enemy.position[0] + ENEMY_WIDTH and
            projectile.position[1] > enemy.position[1] and
            projectile.position[1] < enemy.position[1] + ENEMY_HEIGHT
        )
    
    def manage_enemy_projectiles(self, enemy_projectiles, ship, enemies, projectile_sprite, game_graphic, game_window):
        """
        Manages the movement of enemy projectiles and their interactions with the ship.
        """
        import random

        # Handling enemy firing
        for enemy in enemies:
            if random.random() < ENEMY_FIRE_PROBABILITY:  # Generate a shot between 0 and 1; if it’s less than the probability, it fires
                new_proj = self.create_enemy_projectile(projectile_sprite, enemy)
                enemy_projectiles.append(new_proj)

        # Moving existing projectiles
        for proj in enemy_projectiles[:]:
            proj.move_projectile(1)  # Moving downwards
            if proj.is_out_of_bounds(WINDOW_HEIGHT):
                enemy_projectiles.remove(proj)
            else:
                game_graphic.draw_enemy_projectile(game_window, proj)
                if ship.spaceship_projectile_interaction(proj):
                    enemy_projectiles.remove(proj)

        return enemy_projectiles

