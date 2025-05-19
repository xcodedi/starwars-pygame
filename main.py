import pygame
import random
import os
from resources import functions 

pygame.init()
size = (100, 700)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("StarWars Game")
icon = pygame.image.load("assets/game-icon.jpg")
pygame.display.set_icon(icon)
white = (255, 255, 255)
black = (0, 0, 0)
background_start = pygame.image.load("assets/background-start.jpg") 
background_battle = pygame.image.load("assets/background-battle.jpg")
background_death = pygame.image.load("assets/background-death.jpg")
jedi= pygame.image.load("assets/jedi.png")
villain = pygame.image.load("assets/ship-ti.png")
laser = pygame.image.load("assets/laser.png")