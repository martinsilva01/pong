import pygame

pygame.mixer.init()

UI_BUTTON_SOUND_PATH = "assets/selection.wav"
PADDLE_HIT_SOUND_PATH = "assets/collision.wav"
WALL_HIT_SOUND_PATH = "assets/wallcollision.wav"
SCORE_SOUND_PATH = "assets/score.wav"
POWER_UP_SOUND_PATH = "assets/powerUp.wav"
BACKGROUND_MUSIC_PATH = "assets/ponggameBGM.wav"

button_select_sound = pygame.mixer.Sound(UI_BUTTON_SOUND_PATH)
paddle_hit_sound = pygame.mixer.Sound(PADDLE_HIT_SOUND_PATH)
wall_hit_sound = pygame.mixer.Sound(WALL_HIT_SOUND_PATH)
score_sound = pygame.mixer.Sound(SCORE_SOUND_PATH)
power_up_sound = pygame.mixer.Sound(POWER_UP_SOUND_PATH)

button_select_sound.set_volume(0.15)
paddle_hit_sound.set_volume(0.2)
wall_hit_sound.set_volume(0.2)
score_sound.set_volume(0.2)
power_up_sound.set_volume(0.2)

def play_sound(sound):
    sound.play()

def play_background_music():
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1) 

def stop_background_music():
    pygame.mixer.music.stop()
    