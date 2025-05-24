import pygame
import random
import os
import tkinter as tk
from resources.functions import start_database
from tkinter import messagebox

pygame.init()
start_database()

size = (1000, 700)
clock = pygame.time.Clock()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("StarWars Game")

# Load the game icon
game_icon = pygame.image.load("assets/game-icon.jpg")
pygame.display.set_icon(game_icon)

# Set the background color
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
background_start = pygame.image.load("assets/background-start.jpg") 
background_battle = pygame.image.load("assets/background-battle.jpg")
death_star = pygame.image.load("assets/death-star.png")
galactic_empire_icon = pygame.image.load("assets/galactic-empire-icon.png")
rebel_alliance_icon = pygame.image.load("assets/rebel-alliance-icon.png")
jedi = pygame.image.load("assets/jedi.png")
villain = pygame.image.load("assets/ship-ti.png")
laser = pygame.image.load("assets/laser.png")
random_animation = pygame.image.load("assets/x-wing.png")
background_death = pygame.image.load("assets/background-death-2.jpg")

# Load sounds
start_sound = pygame.mixer.Sound("assets/march-of-the-troopers.mp3")  
battle_sound = pygame.mixer.Sound("assets/starwars-style.mp3")
laser_sound = pygame.mixer.Sound("assets/shot-ship.mp3")
shield_sound = pygame.mixer.Sound("assets/shield.mp3")
game_pause = pygame.mixer.Sound("assets/game-paused-darthvader.wav")
death_sound = pygame.mixer.Sound("assets/kylo.mp3")

# Load fonts
font_menu = pygame.font.SysFont("comicsansms", 30)
font_death = pygame.font.SysFont("comicsansms", 30)
font_intructions = pygame.font.SysFont("arial", 30)

# Background modification 
background_start = pygame.transform.scale(background_start, (size[0], size[1]))
background_battle = pygame.transform.scale(background_battle, (size[0], size[1]))
background_death = pygame.transform.scale(background_death, (size[0], size[1]))


# set name of player 
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

# Initial screen
def start_screen():
    while True:
        screen.blit(background_start, (0, 0))
        pygame.mixer.Sound.play(start_sound)

        # Box "Start Game"
        start_rect = pygame.Rect(90, 250, 300, 60)
        pygame.draw.rect(screen, (0, 255, 255), start_rect, border_radius=12)
        start_text = font_menu.render("Start Game", True, (255, 255, 255))
        screen.blit(start_text, (start_rect.x + 70, start_rect.y + 5))

        # Box "Exit"
        exit_rect = pygame.Rect(90, 350, 300, 60)
        pygame.draw.rect(screen, (0, 0, 0), exit_rect, border_radius=12)
        exit_text = font_menu.render("Exit Game", True, (255, 255, 255))
        screen.blit(exit_text, (exit_rect.x + 80, exit_rect.y + 5))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    jogar()             
                    show_instructions() 
                    return              
                elif exit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()

# Instructions screen
def show_instructions():
    while True:
        screen.blit(background_start, (0, 0))  

        instructions = [
            f"Welcome little Padawan, {player_name}!",
            "Press this buttons to move:",
            "← = Left",
            "→ = Right",
            "Press space bar to start the game.",
        ]

        for i, line in enumerate(instructions):
            text = font_intructions.render(line, True, (255, 255, 255))
            screen.blit(text, (50, 300 + i * 40))

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                return 


start_screen() 

# Set death star size (max)
death_star_width = 150
death_star_height = 100
death_star = pygame.transform.scale(death_star, (death_star_width, death_star_height))

# Death star animation scale
death_star_scale = 1.0
scale_direction = -0.005
death_star_min_scale = 0.8
death_star_max_scale = 1.0

# Set death star position
position_death_star_X = 860
position_death_star_Y = 5

# Set jedi size
jedi_width = 125  
jedi_height = 200
jedi = pygame.transform.scale(jedi, (jedi_width, jedi_height))

# Set jedi position
position_jedi_X = (size[0] // 2) - (jedi_width // 2)
position_jedi_Y = size[1] - jedi_height - 20
movement_jedi_X = 0

# Set villain size
villain_width = 200
villain_height = 300
villain = pygame.transform.scale(villain, (villain_width, villain_height))

# Set villain position
position_villain_X = (size[0] // 2) - (villain_width // 2)
position_villain_Y = -60
movement_villain_X = 0

# Set villain speed
villain_speed = 7

#Define laser size
laser_width = 10
laser_height = 130
laser = pygame.transform.scale(laser, (laser_width, laser_height))

# Define laser position  
position_laser_X = 400
position_laser_Y = 400

# Define random animation position 
position_random_animation_X = 800
position_random_animation_Y = 0

# Define shield position
position_shield_X = position_jedi_X + 20
position_shield_Y = position_jedi_Y - 50

score = 0

# Loop principal do jogo
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                movement_jedi_X = 5
            elif event.key == pygame.K_LEFT:
                movement_jedi_X = -5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                movement_jedi_X = 0


    # Atualiza escala da Death Star
    death_star_scale += scale_direction
    if death_star_scale <= death_star_min_scale or death_star_scale >= death_star_max_scale:
        scale_direction *= -1  

    current_width = int(death_star_width * death_star_scale)
    current_height = int(death_star_height * death_star_scale)
    scaled_death_star = pygame.transform.scale(death_star, (current_width, current_height))


    # Corrige posição para centralizar a Death Star ao escalar
    offset_x = (death_star_width - current_width) // 2
    offset_y = (death_star_height - current_height) // 2

    # Atualiza a posição do jedi
    position_jedi_X += movement_jedi_X

    if position_jedi_X > 895:
        position_jedi_X = 895
    elif position_jedi_X < -5:
        position_jedi_X = -5

    # Atualiza a posição do vilão
    position_villain_X += villain_speed
    if position_villain_X <= 0 or position_villain_X + villain_width >= size[0]:
     villain_speed *= -1

    #screen.fill(white) (precisa?)
    screen.blit(background_battle, (0, 0))
    screen.blit(scaled_death_star, (position_death_star_X + offset_x, position_death_star_Y + offset_y))
    screen.blit(jedi, (position_jedi_X, position_jedi_Y))
    screen.blit(villain, (position_villain_X, position_villain_Y))
    screen.blit(laser, (position_laser_X, position_laser_Y))

    pygame.display.update()
    clock.tick(60)