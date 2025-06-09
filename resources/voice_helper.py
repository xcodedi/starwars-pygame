import pyttsx3  # Imports the offline speech synthesis library
import threading

def speak_instructions(player_name):  # Function that receives the player's name to personalize the message
    def speak():  # Internal function that does the speaking (will be executed in a thread)
        engine = pyttsx3.init()  # Initializes the voice engine
        voices = engine.getProperty('voices')  # Gets the voices available in the system
        for index, voice in enumerate(voices):  # (Optional) Lists the voices available in the console
            print(f"Index: {index}, Name: {voice.name}, ID: {voice.id}")
        engine.setProperty('rate', 150)  # Sets the speech rate
        engine.setProperty('volume', 1.0)  # Sets the speech volume (1.0 = maximum)
        engine.setProperty('voice', voices[1].id)  # Select a voice
        engine.say(f"Welcome little Padawan, {player_name}! Press SPACE to start the game.")  # Set the text to be spoken
        engine.runAndWait()  # Execute the speech
    t = threading.Thread(target=speak)  # Create a thread to run the speak function
    t.start()  # Start the thread, allowing the speech to happen while the game continues

# Why use it like this?
# - pyttsx3.runAndWait() blocks the program until it finishes speaking.
# - Using threading, the speech happens in parallel to the Pygame loop, keeping the instructions screen interactive.
# - This way, the player can see the instructions and press the SPACE key while listening to the message, without crashing the game.