import cv2
import numpy as np
from Starship import spaceship
from Enemies import enemy
from Projectile import projectile
from Player import player
from SpaceInvader import spaceInvader
from Graphic import *
from Camera import *
import time
from FPSCounter import *
from SkeletonTracker import *
from Parsers import *
from models import *
from BDD import *
from Constant import *
from Sound import *

def main():
    pygame.init()
    init_sound()
    explosion_sound = load_sound_effect("son/sonExplosion.mp3")
    explosion_sound.set_volume(0.1)  # Explosion at 10% volume
    # Load sound effects
    tir_sound = load_sound_effect("son/sonTir.mp3")
    tir_sound.set_volume(0.01)  # Shot at 1% volume
    # Load and play background music
    load_music("son/MusiqueFondJeu.mp3") 
    play_music(volume=1.0)

    game = spaceInvader(explosion_sound)
    game_graphic = Graphic()
    nombre_ennemi = 1
    name = game.menu_principal()

    while True:
        # Initialize the game window
        cv2.namedWindow("Space Invader")
        game_window = np.zeros((WINDOW_HEIGHT, WINDOW_WIDTH, 3), dtype=np.uint8)

        # Initialize sprites and objects
        projectile_vaisseau_sprite, projectile_ennemi_sprite, vaisseau_sprite, ennemi_sprite = game.initialize_sprites()
        Vaisseau, ennemis, Jeu = game.initialize_objects(vaisseau_sprite, ennemi_sprite, nombre_ennemi, name)

        # Game variables
        ennemis_direction = [ENEMY_SPEED, 0]
        vaisseau_proj = []
        ennemi_proj = []
        last_shoot_time = time.time()

        # Camera parameters
        EPSILON = 1
        video_path = 0
        cap = cv2.VideoCapture(video_path)
        fps = FPSCounter()

        params = SkeletonTrackerParameters()
        params.use_yolo = False
        params.use_body = False
        params.max_bodies = 1
        params.use_hands = True
        params.use_face = False
        params.hand_skip_frames = 1
        params.models_paths = "PoseEstimation/models"
        tracking = SkeletonTracker(params)

        previous_x = None
        game_camera = camera(cap, tir_sound)

        # Main loop
        game_over = False
        while not game_over and cap.isOpened():

            game_window.fill(0)
            game.add_starfield(game_window)
            # Camera handling
            previous_x, last_shoot_time, vaisseau_proj = game_camera.handle_camera(previous_x, last_shoot_time, Vaisseau, game, tracking, projectile_vaisseau_sprite, vaisseau_proj)

            # Keyboard event handling to exit
            key = cv2.waitKey(EPSILON) & 0xFF
            if key == 27:  # ESC to quit
                cv2.destroyAllWindows()
                return

            # Enemy movement
            ennemis = game.handle_enemy_movement(ennemis, ennemis_direction, Jeu, game_graphic, game_window)

            # If all enemies are destroyed:
            if not ennemis:
                if nombre_ennemi <= 5:
                    nombre_ennemi += 1
                _ , ennemis, _ = game.initialize_objects(vaisseau_sprite, ennemi_sprite, nombre_ennemi, name)

            # Movement and display of spaceship projectiles
            vaisseau_proj = game.handle_spaceship_projectiles(vaisseau_proj, ennemis, game_graphic, game_window)

            # Movement and display of enemy projectiles
            ennemi_proj = game.manage_enemy_projectiles(ennemi_proj, Vaisseau, ennemis, projectile_ennemi_sprite, game_graphic, game_window)

            # Display the spaceship
            game_graphic.draw_ship(game_window, Vaisseau)

            cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # If lost
            if Vaisseau.health_points <= 0:
                game_over = True
                break

            # Display the window
            cv2.imshow("Space Invader", game_window)

        # Handling if lost
        while game_over:

            nombre_ennemi = 1
            game_window.fill(0)
            cv2.putText(game_window, "Lost", (WINDOW_WIDTH // 2 - 50, WINDOW_HEIGHT // 7), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 2)
            cv2.putText(game_window, f"Score: {Jeu.score}", (WINDOW_WIDTH - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            game.add_starfield(game_window)
            cv2.putText(game_window, "Leaderboard :", (1, WINDOW_HEIGHT // 4), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            """
            games = get_games()
            if "error" in games:
                cv2.putText(game_window, "Error retrieving scores: {game_data['error']}", (WINDOW_WIDTH //2 - 50, WINDOW_HEIGHT // 4+10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            else:
                for i, game_data in enumerate(games[:10], start=1):  # Limit to 10 rows
                    cv2.putText(game_window, f"{i}. ID: {game_data['id']}, Player: {game_data['player_name']}, Score: {game_data['score']}, Date: {game_data['timestamp']}", (1, WINDOW_HEIGHT // 4+10+i*30 ), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            """
            cv2.imshow("Space Invader", game_window)
            key = cv2.waitKey(1) & 0xFF
            if cv2.getWindowProperty("Camera Feed", cv2.WND_PROP_VISIBLE) >= 1:
                cv2.destroyWindow("Camera Feed")

            if key == 27:
                # Call the function to update the database
                result = save_game(name, Jeu.score)
                if "error" in result:
                    print(f"Error during saving: {result['error']}")
                else:
                    print(f"Game successfully saved for {name} with a score of {Jeu.score}.")

                return

            elif key == 32:  # Spacebar to restart
                # Call the function to update the database
                result = save_game(name, Jeu.score)
                if "error" in result:
                    print(f"Error during saving: {result['error']}")
                else:
                    print(f"Game successfully saved for {name} with a score of {Jeu.score}.")
                cv2.destroyWindow("Space Invader")
                main()
        cv2.destroyWindow("Space Invader")  

if __name__ == "__main__":
    main()
