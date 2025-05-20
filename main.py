import pygame
import random
import os
import tkinter as tk
from resources.functions import 
from tkinter import messagebox

pygame.init()
size = (100, 700)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("StarWars Game")
game_icon = pygame.image.load("assets/game-icon.jpg")
pygame.display.set_icon(game_icon)
white = (255, 255, 255)
black = (0, 0, 0)
background_start = pygame.image.load("assets/background-start.jpg") 
background_battle = pygame.image.load("assets/background-battle.jpg")
death_star = pygame.image.load("assets/death-star.png")
galactic_empire_icon = pygame.image.load("assets/galactic-empire-icon.png")
rebel_alliance_icon = pygame.image.load("assets/rebel-alliance-icon.png")
jedi= pygame.image.load("assets/jedi.png")
villain = pygame.image.load("assets/ship-ti.png")
laser = pygame.image.load("assets/laser.png")
random_animation = pygame.image.load("assets/x-wing.png")
background_death = pygame.image.load("assets/background-death-2.jpg")
start_sound = pygame.mixer.Sound("assets/march-of-the-troopers.mp3")  
battle_sound = pygame.mixer.Sound("assets/starwars-style.mp3")
laser_sound = pygame.mixer.Sound("assets/shot-ship.mp3")
shield_sound = pygame.mixer.Sound("assets/shield.mp3")
game_pause = pygame.mixer.Sound("assets/game-paused-darthvader.wav")
death_sound = pygame.mixer.Sound("assets/kylo.mp3")
font_menu = pygame.font.SysFont("comicsansms", 18)
font_death = pygame.font.SysFont("comicsansms", 30)

def jogar():
  window_width = 300
  window_height = 50
  def get_name():
    global player_name
    player_name = entry_player_name.get()
    if not player_name:
      messagebox.showwarning("Error", "Please enter a name.")
    else:
      root.destroy()
  root = tk.Tk()
  screen_width = root.winfo_screenwidth()
  screen_height = root.winfo_screenheight()
  position_x = (screen_width // 2) - (window_width // 2)
  position_y = (screen_height // 2) - (window_height // 2)
  root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
  root.title("Enter your name")
  root.protocol("WM_DELETE_WINDOW", get_name)

  entry_player_name = tk.Entry(root)
  entry_player_name.pack()
  button = tk.Button(root, text="OK", command=get_name)
  button.pack()
  root.mainloop()

  #define jedi position
position_jedi_X = 500
position_jedi_Y = 15
movimentXjedi = 0
movimentYjedi = 0


  #define villain position
position_villain_X = 500
position_villain_Y = 650

  #define laser position  

position_laser_X = position_villain_X + 20
position_laser_Y = position_villain_Y - 50

  #define random animation position 
position_random_animation_X = 800
position_random_animation_Y = 0

  #define shield position
position_shield_X = position_jedi_X + 20
position_shield_Y = position_jedi_Y - 50

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      quit()
      elif event.type == pygame.K_right:
        position_jedi_X += 5
      elif event.type == pygame.K_LEFT:
        position_jedi_X -= 5

   newposition_jedi_X += moviment_jedi_X
    newposition_jedi_Y += moviment_jedi_Y    
  
    screen.fill(white)
  screen.blit(background_start, (0, 0))
  screen.blit(death_star, (0, 0))
  screen.blit(jedi, (position_jedi_X, position_jedi_Y))
