import os
import datetime
import speech_recognition as sr

def clear_screen():
 os.system('cls' if os.name == 'nt' else 'clear')

def start_database():
    try: 
        with open("log.dat", "r") as f:
            pass
    except:
        print("Criando banco de dados...")
        with open("log.dat", "w") as f:
            pass

def save_game_log(player_name, score):
    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    
    with open("log.dat", "a") as file:
        file.write(f"{player_name},{score},{date_str},{time_str}\n")

def get_top_scores(limit=5):
    try:
        with open("log.dat", "r") as file:
            games = []
            for line in file:
                if line.strip():
                    parts = line.strip().split(',')
                    if len(parts) == 4:  
                        try:
                            parts[1] = int(parts[1])
                            games.append(parts)
                        except ValueError:
                            continue
            
            games.sort(key=lambda x: (-x[1], x[2], x[3]))
            
            for game in games:
                game[1] = str(game[1])
                
            return games[:limit]
    except Exception as e:
        print(f"Erro ao ler ranking: {e}")
        return []
    
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
                return True
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