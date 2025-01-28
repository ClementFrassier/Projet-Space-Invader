from Enemies import *  # Ensure that enemies are defined somewhere in this module

class projectile:
    def __init__(self, graphic, projectile_speed, direction, damage, radius, position):
        """
        Initializes a projectile with the given attributes.

        :param graphic: The visual representation of the projectile (e.g., an image or a NumPy array).
        :param projectile_speed: The speed of the projectile (positive value).
        :param direction: The direction of the projectile (-1 for upward, 1 for downward).
        :param damage: The damage dealt by the projectile upon impact.
        :param radius: The radius of the projectile used for collision detection.
        :param position: The initial position of the projectile as a tuple (x, y).
        """
        # Assigning attributes
        self.graphic = graphic
        self.projectile_speed = projectile_speed  # Positive speed
        self.direction = direction  # -1 for upward, 1 for downward
        self.damage = damage
        self.radius = radius
        self.position = list(position)  # Copy to avoid external references

    def move_projectile(self, dt):
        """
        Moves the projectile based on its direction and the elapsed time (dt).

        :param dt: The elapsed time (delta time) between updates, used for consistent speed regardless of framerate.
        """
        # Movement is influenced by direction (-1 or 1)
        self.position[1] += dt * self.projectile_speed * self.direction

    def is_out_of_bounds(self, screen_height):
        """
        Checks if the projectile has gone out of bounds of the screen.

        :param screen_height: The height of the screen, used to check if the projectile is above or below the screen.
        :return: True if the projectile is out of bounds, False otherwise.
        """
        return self.position[1] < 0 or self.position[1] >= screen_height