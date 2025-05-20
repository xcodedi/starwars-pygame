import os

def clear_screen():
 os.system('cls' if os.name == 'nt' else 'clear')

def start_database():
 try: 
  base = open("log.dat", "r")
 except:
  print("Creating Database...")
  base = open("log.dat", "w")