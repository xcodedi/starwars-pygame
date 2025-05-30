import pygame
import random
import math
import tkinter as tk
import os
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
font_score = pygame.font.SysFont("comicsansms", 36)

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
    pygame.mixer.Sound.play(start_sound)
    while True:
        screen.blit(background_start, (0, 0)) 
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
             
def check_collision(laser_pos, jedi_rect):
    laser_rect = pygame.Rect(laser_pos[0], laser_pos[1], laser_width, laser_height)
    return laser_rect.colliderect(jedi_rect)

def show_death_screen():
    pygame.mixer.Sound.play(death_sound)
    screen.blit(background_death, (0, 0))
    
    # Texto de Game Over
    death_text = font_death.render("GAME OVER", True, (255, 0, 0))
    screen.blit(death_text, (size[0]//2 - death_text.get_width()//2, 200))
    
    # Pontuação
    score_text = font_score.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (size[0]//2 - score_text.get_width()//2, 300))
    
    # Botão de Tentar Novamente
    retry_rect = pygame.Rect(size[0]//2 - 100, 400, 200, 50)
    pygame.draw.rect(screen, (0, 255, 0), retry_rect, border_radius=10)
    retry_text = font_menu.render("Try Again", True, (0, 0, 0))
    screen.blit(retry_text, (retry_rect.x + 50, retry_rect.y + 15))
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    waiting = False
                    return True
    return False

start_screen() 
pygame.mixer.stop()
pygame.mixer.Sound.play(battle_sound, loops=-1)
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

# Random villain movement
villain_direction_change_timer = 0

# Set laser size
laser_width = 10
laser_height = 130
laser = pygame.transform.scale(laser, (laser_width, laser_height))

# Set laser position  
position_laser_X = position_villain_X
position_laser_Y = position_villain_Y

# set laser feature
laser_villain = []
last_shot_time = pygame.time.get_ticks()
laser_speed = 15

# Set random animation position 
position_random_animation_X = 800
position_random_animation_Y = 0

# Set shield position
position_shield_X = position_jedi_X + 20
position_shield_Y = position_jedi_Y - 50

score = 0

# Main game loop
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

    # Updates Death Star scale
    death_star_scale += scale_direction
    if death_star_scale <= death_star_min_scale or death_star_scale >= death_star_max_scale:
        scale_direction *= -1  

    current_width = int(death_star_width * death_star_scale)
    current_height = int(death_star_height * death_star_scale)
    scaled_death_star = pygame.transform.scale(death_star, (current_width, current_height))

    # Fix position to center the Death Star when scaling
    offset_x = (death_star_width - current_width) // 2
    offset_y = (death_star_height - current_height) // 2

    # Updates Jedi position
    position_jedi_X += movement_jedi_X

    if position_jedi_X > 895:
        position_jedi_X = 895
    elif position_jedi_X < -5:
        position_jedi_X = -5

    # Random villain movement
    villain_direction_change_timer += 1
    if villain_direction_change_timer > 60:
        villain_speed = random.choice([-15, -10, -5, 5, 10, 15])
        villain_direction_change_timer = 0

    position_villain_X += villain_speed

    # Keep the villain on screen
    if position_villain_X < 0:
        position_villain_X = 0
        villain_speed *= -1
    elif position_villain_X + villain_width > size[0]:
        position_villain_X = size[0] - villain_width
        villain_speed *= -1

    # verif if 1,5 seconds have passed to shoot again 
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time > 1500:
        position_laser_X = position_villain_X + villain_width // 2 - laser_width // 2
        position_laser_Y = position_villain_Y + villain_height - 100
        angle = random.uniform(-0.5, 0.5)  # em radianos, ~ -28° a +28°
        dx = laser_speed * math.sin(angle)
        dy = laser_speed * math.cos(angle)
        laser_villain.append([position_laser_X, position_laser_Y, dx, dy])
        pygame.mixer.Sound.play(laser_sound)
        last_shot_time = current_time 

    screen.blit(background_battle, (0, 0))
    screen.blit(scaled_death_star, (position_death_star_X + offset_x, position_death_star_Y + offset_y))
    screen.blit(jedi, (position_jedi_X, position_jedi_Y))
    screen.blit(villain, (position_villain_X, position_villain_Y))

    # Create jedi_rect for collision detection
    jedi_rect = pygame.Rect(position_jedi_X, position_jedi_Y, jedi_width, jedi_height)

    # Update and draw lasers
    for laser_pos in laser_villain[:]:
        laser_pos[0] += laser_pos[2]  
        laser_pos[1] += laser_pos[3] 
        screen.blit(laser, (laser_pos[0], laser_pos[1]))

        # Check collision
        if check_collision(laser_pos, jedi_rect):
            pygame.mixer.stop()
            if show_death_screen():
                position_jedi_X = (size[0] // 2) - (jedi_width // 2)
                position_villain_X = (size[0] // 2) - (villain_width // 2)
                laser_villain = []
                score = 0
                pygame.mixer.Sound.play(battle_sound, loops=-1)
                break 
            else:
                pygame.quit()
                quit()
        if laser_pos[1] > size[1]:
            laser_villain.remove(laser_pos)
            score += 1  

    pygame.display.update()
    clock.tick(60)