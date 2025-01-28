from Constant import *
import cv2

class Graphic:
    def __init__(self):
        pass
    
    def draw_health_bar(self, window, position, width, height, health, max_health, background_color=(50, 50, 50), health_color=(0, 255, 0)):
        """
        Draws a health bar on the screen.

        :param window: The game window.
        :param position: Position (x, y) of the health bar.
        :param width: Width of the health bar.
        :param height: Height of the health bar.
        :param health: Current health.
        :param max_health: Maximum health.
        :param background_color: Background color of the bar.
        :param health_color: Color of the remaining health.
        """
        health = max(0, min(health, max_health))
        health_width = int((health / max_health) * width)
        cv2.rectangle(window, position, (position[0] + width, position[1] + height), background_color, -1)
        if health > 0:
            cv2.rectangle(window, position, (position[0] + health_width, position[1] + height), health_color, -1)

    def draw_enemy(self, window, enemy):
        """
        Draws an enemy on the game window.

        :param window: The game window.
        :param enemy: Enemy object with attributes position, graphic, width, height, health, max_health.
        """
        if enemy.health_points > 0:
            # Draw the enemy
            window[
                enemy.position[1]:enemy.position[1] + ENEMY_HEIGHT,
                enemy.position[0]:enemy.position[0] + ENEMY_WIDTH
            ] = enemy.sprite

        # Draw the enemy's health bar
        self.draw_health_bar(
            window,
            position=(enemy.position[0], enemy.position[1] - 10),
            width=ENEMY_WIDTH,
            height=5,
            health=enemy.health_points,
            max_health=enemy.max_health_points
        )

    def draw_ship(self, window, ship):
        """
        Draws the ship on the game window.

        :param window: The game window.
        :param ship: Ship object with attributes position, graphic, width, height, health, max_health.
        """
        if ship.health_points > 0:
            # Draw the ship
            window[
                ship.position[1]:ship.position[1] + SHIP_HEIGHT,
                ship.position[0]:ship.position[0] + SHIP_WIDTH
            ] = ship.graphic

            # Draw the ship's health bar
            self.draw_health_bar(
                window,
                position=(ship.position[0], ship.position[1] - 10),
                width=SHIP_WIDTH,
                height=5,
                health=ship.health_points,
                max_health=ship.max_health_points
            )

    def draw_ship_projectile(self, window, projectile):
        """
        Draws a ship's projectile on the game window.
        
        :param window: The game window.
        :param projectile: Ship's projectile object with attributes position and graphic.
        """
        if projectile is not None:
            y_start = max(0, projectile.position[1])
            y_end = min(WINDOW_HEIGHT, projectile.position[1] + PROJECTILE_RADIUS * 2)
            x_start = max(0, projectile.position[0])
            x_end = min(WINDOW_WIDTH, projectile.position[0] + PROJECTILE_RADIUS * 2)
            
            if y_end > y_start and x_end > x_start:
                graphic_part = projectile.graphic[:y_end - y_start, :x_end - x_start]
                window[y_start:y_end, x_start:x_end] = graphic_part

    def draw_enemy_projectile(self, window, projectile):
        """
        Draws an enemy's projectile on the game window.
        
        :param window: The game window.
        :param projectile: Enemy's projectile object with attributes position and graphic.
        """
        if projectile is not None:
            y_start = max(0, projectile.position[1])
            y_end = min(WINDOW_HEIGHT, projectile.position[1] + PROJECTILE_RADIUS * 2)
            x_start = max(0, projectile.position[0])
            x_end = min(WINDOW_WIDTH, projectile.position[0] + PROJECTILE_RADIUS * 2)
            
            if y_end > y_start and x_end > x_start:
                graphic_part = projectile.graphic[:y_end - y_start, :x_end - x_start]
                window[y_start:y_end, x_start:x_end] = graphic_part
