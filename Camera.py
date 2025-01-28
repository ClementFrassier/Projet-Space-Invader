from Constant import *
import cv2
from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *
import time
from Sound import *

class camera :
    """
    Class to handle camera interactions for the Space Invaders game, including hand tracking
    and gesture recognition for controlling the spaceship and shooting projectiles.
    """

    def __init__(self, cap, tir_sound=None):
        """
        Initializes the Camera object.

        Parameters:
            cap (cv2.VideoCapture): Video capture object to read frames from the camera.
            tir_sound (Sound, optional): Sound object for playing the shooting sound effect.
        """
        self.cap = cap
        self.previous_x = None
        self.last_shoot_time = time.time()
        self.tir_sound = tir_sound


    def is_hand_closed(self,y1, y2, x1, x2):
        """
        Checks if the hand is closed by verifying if two points are within a small threshold.

        Parameters:
            y1, y2 (float): Y-coordinates of two hand points (e.g., palm and middle finger).
            x1, x2 (float): X-coordinates of two hand points.

        Returns:
            bool: True if the points are within ±0.1, indicating a closed hand. False otherwise.
        """
        if y1 is not None and y2 is not None and x1 is not None and x2 is not None:
            if abs(y2 - y1) <= 0.1 and abs(x2 - x1) <= 0.1:
                return True
        return False


    def detect_hand_movement(self,current_x, previous_x):
        """
        Detects horizontal movement of the hand.

        Parameters:
            current_x (float): Current x-coordinate of the hand.
            previous_x (float): Previous x-coordinate of the hand.

        Returns:
            bool: 
                - True if the hand moved to the right.
                - False if the hand moved to the left.
        """
        # 0.01 acts as a margin of error for detection

        if current_x > previous_x + 0.01:
            return True                #Right
                            
        elif current_x < previous_x - 0.01:
            return False              #Left
        

    def handle_camera(self, previous_x, last_shoot_time, vaisseau, game, tracking, projectile_sprite,vaisseau_proj):
        """
        Manages the camera feed and interprets hand gestures for controlling the game.
        Parameters:
            previous_x (float): Previous x-coordinate of the hand.
            last_shoot_time (float): Timestamp of the last shot fired.
            spaceship (Spaceship): Player's spaceship object.
            game (Game): Game object managing the overall game state.
            tracking (SkeletonTracker): Object for hand tracking and skeleton detection.
            projectile_sprite (Sprite): Sprite for projectiles fired by the spaceship.
            spaceship_projectiles (list): List of active projectiles fired by the spaceship.

        Returns:
            tuple: Updated (previous_x, last_shoot_time, spaceship_projectiles).
        """
        ret, img = self.cap.read()
        if not ret:
            return previous_x, last_shoot_time, []

        img = cv2.resize(img, (300, 240))
        img = cv2.flip(img, 1)

        tracking.update(img)

        # Process detected hands
        for hand in tracking.hands:
            img = hand.displaySkeleton(img)
            articulation_paume = hand.skeleton()[0]
            articulation_Middle = hand.skeleton()[12]

            paume_x = articulation_paume[1]
            paume_y = articulation_paume[0]
            middle_x = articulation_Middle[1]
            middle_y = articulation_Middle[0]
            
            if not np.isnan(articulation_paume).any():
                current_x = articulation_paume[1]
                # Handle horizontal hand movement
                if previous_x is not None:
                    if self.detect_hand_movement(current_x, previous_x):
                        # Move spaceship to the right
                        vaisseau.position[0] = min(WINDOW_WIDTH - SHIP_WIDTH, vaisseau.position[0] + SHIP_SPEED * 3)
                    elif self.detect_hand_movement(current_x, previous_x) == False:
                        # Move spaceship to the left
                        vaisseau.position[0] = max(0, vaisseau.position[0] - SHIP_SPEED * 3)

                if self.is_hand_closed(paume_y, middle_y, paume_x, middle_x):
                    current_time = time.time()
                    if current_time - last_shoot_time >= 0.25:  # 4 shots per second
                        # Create a new projectile
                        dernier_projectile = game.create_spaceship_projectile(projectile_sprite, vaisseau)
                        vaisseau_proj.append(dernier_projectile)
                        last_shoot_time = current_time

                        # Play shooting sound
                        if self.tir_sound:
                            self.tir_sound.play()

                previous_x = current_x

        cv2.imshow("Camera Feed", img) # Display the camera feed in a separate window
        return previous_x, last_shoot_time, vaisseau_proj
