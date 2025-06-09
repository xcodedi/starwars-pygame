import os
import datetime
import pygame
import speech_recognition as sr

# Clears the console screen (compatible with Windows and Unix-based systems)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


# Initializes the database by creating the log file if it doesn't exist
def start_database():
    try:
        with open("log.dat", "r") as f:
            pass  # File exists, do nothing
    except:
        print("Creating database...")
        with open("log.dat", "w") as f:
            pass  # Create an empty file


# Draws a button on the screen using pygame
def draw_button(screen, rect, color, text, font, text_color, border_radius=12, padding=10):
    pygame.draw.rect(screen, color, rect, border_radius=border_radius)  # Draw button rectangle
    text_surface = font.render(text, True, text_color)  # Render button text
    text_rect = text_surface.get_rect(center=rect.center)  # Center text within the button
    screen.blit(text_surface, text_rect)  # Display the text on the screen
    return rect


# Saves a game log entry with player name, score, date, and time
def save_game_log(player_name, score):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    with open("log.dat", "a") as file:
        file.write(f"{player_name},{score},{date_str},{time_str}\n")


# Reads the log file and returns the top scores (default is top 5)
def get_top_scores(limit=5):
    try:
        with open("log.dat", "r") as file:
            games = []
            for line in file:
                if line.strip():  # Skip empty lines
                    parts = line.strip().split(',')
                    if len(parts) == 4:
                        try:
                            parts[1] = int(parts[1])  # Convert score to integer
                            games.append(parts)
                        except ValueError:
                            continue  # Skip invalid entries

            # Sort by highest score, then by date and time
            games.sort(key=lambda x: (-x[1], x[2], x[3]))

            # Convert score back to string for consistency
            for game in games:
                game[1] = str(game[1])

            return games[:limit]  # Return top N scores
    except Exception as e:
        print(f"Error reading leaderboard: {e}")
        return []


# Listens for voice command and returns True if any trigger phrase is recognized
def listen_voice(activator=("yes master", "try again"), timeout=3):
    recognizer = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print(f"Listening for: {activator}...")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=timeout)

        phrase = recognizer.recognize_google(audio, language="en").lower()
        print("You said:", phrase)

        for trigger in activator:
            if trigger in phrase:
                print("Voice command recognized!")
                return True

        print("Voice command not recognized.")
        return False

    except sr.WaitTimeoutError:
        print("No speech detected within timeout period.")
        return False
    except sr.UnknownValueError:
        print("Could not understand audio.")
        return False
    except Exception as e:
        print(f"Error in voice recognition: {e}")
        return False
