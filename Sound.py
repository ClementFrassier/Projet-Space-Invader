import pygame

def init_sound():
    """
    Initializes the Pygame audio module.
    This function must be called before using any sound functions.
    """
    pygame.mixer.init()

def load_music(file_path):
    """
    Loads a background music file.
    
    :param file_path: Path to the music file (str)
    """
    pygame.mixer.music.load(file_path)

def play_music(volume=1, loop=True):
    """
    Plays the loaded background music.
    
    :param volume: Volume of the music (float, between 0.0 and 1.0)
    :param loop: If True, the music will loop indefinitely. If False, it will play once.
    """
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.play(-1 if loop else 0)

def stop_music():
    """
    Stops the currently playing background music.
    """
    pygame.mixer.music.stop()

def load_sound_effect(file_path):
    """
    Loads a sound effect file.
    
    :param file_path: Path to the sound effect file (str)
    :return: pygame.mixer.Sound object for the loaded sound effect
    """
    return pygame.mixer.Sound(file_path)

def play_sound_effect(sound_effect, volume=0.2):
    """
    Plays a sound effect.
    
    :param sound_effect: pygame.mixer.Sound object representing the sound effect
    :param volume: Volume of the sound effect (float, between 0.0 and 1.0)
    """
    sound_effect.set_volume(volume)
    sound_effect.play()
