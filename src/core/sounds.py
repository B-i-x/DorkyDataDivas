import pygame

# Initialize Pygame mixer
pygame.mixer.init()

def found_word_sound():
    sound = pygame.mixer.Sound("src/assets/mixkit-instant-win-2021.wav")
    sound.play()

def game_won_sound():
    sound = pygame.mixer.Sound("src/assets/mixkit-ethereal-fairy-win-sound-2019.wav")
    sound.play()