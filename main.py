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
try:
    game_icon = pygame.image.load("assets/game-icon.jpg")
    pygame.display.set_icon(game_icon)
except:
    print("Could not load game icon")

# Colors
white = (255, 255, 255)
black = (0, 0, 0)

# Load images
try:
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
    
    # Scale images
    background_start = pygame.transform.scale(background_start, size)
    background_battle = pygame.transform.scale(background_battle, size)
    background_death = pygame.transform.scale(background_death, size)
except Exception as e:
    print(f"Error loading images: {e}")
    pygame.quit()
    exit()

# Load sounds
try:
    start_sound = pygame.mixer.Sound("assets/march-of-the-troopers.mp3")  
    battle_sound = pygame.mixer.Sound("assets/starwars-style.mp3")
    laser_sound = pygame.mixer.Sound("assets/shot-ship.mp3")
    shield_sound = pygame.mixer.Sound("assets/shield.mp3")
    game_pause = pygame.mixer.Sound("assets/game-paused-darthvader.wav")
    death_sound = pygame.mixer.Sound("assets/kylo.mp3")
except:
    print("Could not load some sounds")

# Load fonts
try:
    font_menu = pygame.font.SysFont("comicsansms", 30)
    font_death = pygame.font.SysFont("comicsansms", 40)
    font_intructions = pygame.font.SysFont("arial", 30)
    font_score = pygame.font.SysFont("comicsansms", 36)
    font_pause_mensage = pygame.font.SysFont("comicsansms", 13)
except:
    print("Could not load fonts")

# Game variables
score = 0
player_name = "Player"  # Default name
paused = False

# set name of player 
def jogar():
    global player_name
    
    def get_name():
        global player_name
        player_name = entry_player_name.get()
        if not player_name:
            messagebox.showwarning("Error", "Please enter a name.")
        else:
            root.destroy()

    root = tk.Tk()
    root.title("Enter with your name")
    
    # Center window
    window_width = 300
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    position_x = (screen_width // 2) - (window_width // 2)
    position_y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{position_x}+{position_y}")
    
    tk.Label(root, text="Enter your name:").pack(pady=10)
    entry_player_name = tk.Entry(root)
    entry_player_name.pack(pady=5)
    
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="OK", command=get_name).pack(side=tk.LEFT, padx=10)
    tk.Button(button_frame, text="Cancel", command=root.destroy).pack(side=tk.RIGHT, padx=10)
    
    root.mainloop()

# Initial screen
def start_screen():
    pygame.mixer.Sound.play(start_sound,loops=-1)
    while True:
        screen.blit(background_start, (0, 0)) 
        
        # Box "Start Game"
        start_rect = pygame.Rect(90, 250, 300, 60)
        pygame.draw.rect(screen, (0, 255, 255), start_rect, border_radius=12)
        start_text = font_menu.render("Start Game", True, white)
        screen.blit(start_text, (start_rect.x + 70, start_rect.y + 10))

        # Box "Exit"
        exit_rect = pygame.Rect(90, 350, 300, 60)
        pygame.draw.rect(screen, black, exit_rect, border_radius=12)
        exit_text = font_menu.render("Exit Game", True, white)
        screen.blit(exit_text, (exit_rect.x + 80, exit_rect.y + 10))

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
            "Controls:",
            "← = Move Left",
            "→ = Move Right",
            "SPACE = Pause Game",
            "Press SPACE to start the game",
        ]

        for i, line in enumerate(instructions):
            text = font_intructions.render(line, True, white)
            screen.blit(text, (50, 250 + i * 40))

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
    
    waiting = True
    while waiting:
        screen.blit(background_death, (0, 0))
        
        # Render "GAME OVER" text with black border 
        death_text = font_death.render("GAME OVER", True, (255, 10, 0))
        text_rect = death_text.get_rect(center=(size[0]//2, 250))
        
        # Draw black outline 
        for offset in [(-1,-1), (1,-1), (-1,1), (1,1)]:
            screen.blit(font_death.render("GAME OVER", True, black), 
                       (text_rect.x + offset[0], text_rect.y + offset[1]))
        
        screen.blit(death_text, text_rect)
        
        # Score text
        score_text = font_score.render(f"Score: {score}", True, white)
        screen.blit(score_text, (size[0]//2 - score_text.get_width()//2, 300))
        
        # Retry button with border
        retry_rect = pygame.Rect(size[0]//2 - 100, 400, 200, 50)
        
        # Draw border 
        pygame.draw.rect(screen, black, retry_rect.inflate(10, 10), border_radius=15)
        # Draw main button
        pygame.draw.rect(screen, (0, 255, 255), retry_rect, border_radius=10)
        
        retry_text = font_menu.render("TRY AGAIN", True, white)
        screen.blit(retry_text, (retry_rect.x + 18, retry_rect.y + 5))
        
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_rect.collidepoint(event.pos):
                    return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

    return False

# Initialize game objects
death_star_width = 150
death_star_height = 100
death_star = pygame.transform.scale(death_star, (death_star_width, death_star_height))

death_star_scale = 1.0
scale_direction = -0.005
death_star_min_scale = 0.8
death_star_max_scale = 1.0
position_death_star_X = 860
position_death_star_Y = 5

jedi_width = 125  
jedi_height = 200
jedi = pygame.transform.scale(jedi, (jedi_width, jedi_height))
position_jedi_X = (size[0] // 2) - (jedi_width // 2)
position_jedi_Y = size[1] - jedi_height - 20
movement_jedi_X = 0

villain_width = 200
villain_height = 300
villain = pygame.transform.scale(villain, (villain_width, villain_height))
position_villain_X = (size[0] // 2) - (villain_width // 2)
position_villain_Y = -60
villain_speed = 7
villain_direction_change_timer = 0

laser_width = 10
laser_height = 130
laser = pygame.transform.scale(laser, (laser_width, laser_height))
laser_villain = []
laser_speed = 15

position_random_animation_X = 800
position_random_animation_Y = 0

position_shield_X = position_jedi_X + 20
position_shield_Y = position_jedi_Y - 50

# Start the game
start_screen() 
pygame.mixer.stop()
pygame.mixer.Sound.play(battle_sound, loops=-1)

last_shot_time = pygame.time.get_ticks() + 3000  

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                movement_jedi_X = 5
            elif event.key == pygame.K_LEFT:
                movement_jedi_X = -5
            elif event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    pygame.mixer.Sound.stop(battle_sound)
                    pygame.mixer.Sound.play(game_pause)
                else:
                    pygame.mixer.Sound.stop(game_pause)
                    pygame.mixer.Sound.play(battle_sound, loops=-1)        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT and movement_jedi_X > 0:
                movement_jedi_X = 0
            elif event.key == pygame.K_LEFT and movement_jedi_X < 0:
                movement_jedi_X = 0
    
    if paused:
        pause_text = font_menu.render("GAME PAUSED", True, (0, 255, 255))
        screen.blit(pause_text, (size[0]//2 - pause_text.get_width()//2, size[1]//2))
        pygame.display.update()
        clock.tick(10)
        continue

    # Game logic
    # Update Death Star animation
    death_star_scale += scale_direction
    if death_star_scale <= death_star_min_scale or death_star_scale >= death_star_max_scale:
        scale_direction *= -1  

    current_width = int(death_star_width * death_star_scale)
    current_height = int(death_star_height * death_star_scale)
    scaled_death_star = pygame.transform.scale(death_star, (current_width, current_height))
    offset_x = (death_star_width - current_width) // 2
    offset_y = (death_star_height - current_height) // 2

    # Update Jedi position
    position_jedi_X += movement_jedi_X
    position_jedi_X = max(-5, min(895, position_jedi_X))

    # Update Villain movement
    villain_direction_change_timer += 1
    if villain_direction_change_timer > 60:
        villain_speed = random.choice([-15, -10, -5, 5, 10, 15])
        villain_direction_change_timer = 0

    position_villain_X += villain_speed
    if position_villain_X < 0:
        position_villain_X = 0
        villain_speed *= -1
    elif position_villain_X + villain_width > size[0]:
        position_villain_X = size[0] - villain_width
        villain_speed *= -1

    # Villain shooting
    current_time = pygame.time.get_ticks()
    if current_time - last_shot_time > 1500:
        position_laser_X = position_villain_X + villain_width // 2 - laser_width // 2
        position_laser_Y = position_villain_Y + villain_height - 100
        angle = random.uniform(-0.5, 0.5)  
        dx = laser_speed * math.sin(angle)
        dy = laser_speed * math.cos(angle)
        laser_villain.append([position_laser_X, position_laser_Y, dx, dy])
        pygame.mixer.Sound.play(laser_sound)
        last_shot_time = current_time 

    # Drawing
    screen.blit(background_battle, (0, 0))
    screen.blit(scaled_death_star, (position_death_star_X + offset_x, position_death_star_Y + offset_y))
    screen.blit(jedi, (position_jedi_X, position_jedi_Y))
    screen.blit(villain, (position_villain_X, position_villain_Y))

    # Collision detection
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
                # Reset game state
                position_jedi_X = (size[0] // 2) - (jedi_width // 2)
                position_villain_X = (size[0] // 2) - (villain_width // 2)
                laser_villain = []
                score = 0
                last_shot_time = pygame.time.get_ticks() + 3000
                pygame.mixer.Sound.play(battle_sound, loops=-1)
            else:
                running = False
            break
        
        # Remove lasers that go off screen
        if laser_pos[1] > size[1]:
            laser_villain.remove(laser_pos)
            score += 1

    # Display score
    score_text = font_score.render(f"Score: {score}", True, white)
    screen.blit(score_text, (10, 10))
    #Display pause message
    pause_mensage = font_pause_mensage.render("Press SPACE to pause GAME", True, (128, 128, 128))
    screen.blit(pause_mensage, (10, 50))

    pygame.display.update()
    clock.tick(60)

pygame.quit()