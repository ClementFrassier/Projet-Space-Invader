from Projectile import projectile  
from Sound import * 

class spaceship:
    def __init__(self, position, graphic, spaceship_speed, height, width, health_points):
        """
        Constructor for the Spaceship class. Initializes the attributes of the spaceship.

        Parameters:
            position (list): A list representing the [x, y] position of the spaceship.
            graphic (str): A graphic (image or icon) representing the spaceship.
            spaceship_speed (float): The speed at which the spaceship moves.
            height (int): The height of the spaceship (used for collision detection).
            width (int): The width of the spaceship (used for collision detection).
            health_points (int): The number of health points the spaceship starts with.
        """
        self.position = position  
        self.graphic = graphic  
        self.spaceship_speed = spaceship_speed  
        self.width = width  
        self.height = height  
        self.health_points = health_points  
        self.max_health_points = health_points 

    def move_spaceship(self, dt):
        """
        Moves the spaceship based on its speed and the time step (dt).

        Parameters:
            dt (float): The delta time, which represents the time elapsed since the last update.
        """
        # Update the position based on the spaceship's speed and the elapsed time (dt)
        self.position[0] += dt * self.spaceship_speed  # Update the x-coordinate (horizontal movement)

    def spaceship_projectile(self, projectile_speed, radius, graphic):
        """
        Creates a new projectile fired from the spaceship.

        Parameters:
            projectile_speed (float): The speed at which the projectile moves.
            radius (int): The radius (size) of the projectile.
            graphic (str): The graphic (image or icon) representing the projectile.

        Returns:
            Projectile: A new instance of the Projectile class.
        """
        new_projectile = projectile(
            position=[  
                self.position[0] + self.width // 2 - 5,  
                self.position[1] - 10  
            ],
            damage=1, 
            graphic=graphic,  
            projectile_speed=projectile_speed,  
            radius=radius  
        )
        return new_projectile  

    def spaceship_projectile_interaction(self, projectile, explosion_sound=None):
        """
        Checks if the spaceship is hit by a projectile. If it is, reduces health points.

        Parameters:
            projectile (Projectile): The projectile that may have hit the spaceship.
            explosion_sound (Sound or None): A sound that plays if the spaceship is hit.

        Returns:
            bool: True if the spaceship is hit, False otherwise.
        """
        if (projectile.position[0] > self.position[0] and
            projectile.position[0] < self.position[0] + self.width and
            projectile.position[1] > self.position[1] and
            projectile.position[1] < self.position[1] + self.height):
            
            self.health_points -= projectile.damage

            if explosion_sound:
                explosion_sound.play()

            # Return True because the spaceship was hit
            return True
        
        # Return False because the spaceship was not hit
        return False