import pygame

pygame.mixer.init()

UI_BUTTON_SOUND_PATH = ""
PADDLE_HIT_SOUND_PATH = ""
WALL_HIT_SOUND_PATH = ""
SCORE_SOUND_PATH = ""
BACKGROUND_MUSIC_PATH = ""

button_select_sound = pygame.mixer.Sound(UI_BUTTON_SOUND_PATH)
paddle_hit_sound = pygame.mixer.Sound(PADDLE_HIT_SOUND_PATH)
wall_hit_sound = pygame.mixer.Sound(WALL_HIT_SOUND_PATH)
score_sound = pygame.mixer.Sound(SCORE_SOUND_PATH)

button_select_sound.set_volume(0.5)
paddle_hit_sound.set_volume(0.5)
wall_hit_sound.set_volume(0.5)
score_sound.set_volume(0.5)

def play_sound(sound):
    sound.play()

def play_background_music():
    pygame.mixer.music.load(BACKGROUND_MUSIC_PATH)
    pygame.mixer.music.set_volume(0.25)
    pygame.mixer.music.play(-1) 

def stop_background_music():
    pygame.mixer.music.stop()
    