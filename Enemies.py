from Sound import *

class enemy:
    """
    Represents an enemy in the Space Invaders game. Handles position, movement, 
    interactions with projectiles, and health management.
    """
    def __init__(self, position, height, width, sprite, velocity, health_points):
        """
        Initializes the enemy object.

        Parameters:
            position (list or tuple): Initial position of the enemy [x, y].
            height (int): Height of the enemy.
            width (int): Width of the enemy.
            sprite: Graphical representation or sprite of the enemy.
            velocity (list or tuple): Velocity vector [vx, vy] of the enemy.
            health_points (int): Initial health points of the enemy.
        """
        self.position = position
        self.height = height
        self.width = width
        self.sprite = sprite
        self.velocity = velocity
        self.health_points = health_points
        self.max_health_points = health_points

    def move_enemy(self, dt):
        """
        Moves the enemy based on its velocity and the time delta (dt).

        Parameters:
            dt (float): Time delta used to scale the movement.
        """
        self.position[0] += dt * self.velocity[0]  # Move horizontally
        self.position[1] += dt * self.velocity[1]  # Move vertically

    def enemy_projectile_interaction(self, projectile, explosion_sound=None):
        """
        Handles interactions between the enemy and a projectile.

        Parameters:
            projectile (Projectile): The projectile object that may collide with the enemy.
            explosion_sound (Sound, optional): Sound effect to play on collision.

        Returns:
            bool: True if the projectile hits the enemy, False otherwise.
        """
        # Check if the projectile is within the enemy's bounding box
        if (self.position[0] < projectile.position[0] < self.position[0] + self.width and
                self.position[1] < projectile.position[1] < self.position[1] + self.height):
            # Reduce the enemy's health by the projectile's damage
            self.health_points -= projectile.degat()

            # Play explosion sound if provided
            if explosion_sound:
                explosion_sound.play()

            return True  # Projectile hit the enemy
        return False  # No collision
