import sqlite3
import pygame
import hashlib
from Boxes import InputBox
from Boxes import Button
clock = pygame.time.Clock()
pygame.init()
pygame.mixer.init()

def create_table():
    query = "CREATE TABLE IF NOT EXISTS login(Username VARCHAR UNIQUE, Password VARCHAR)" #Defines the structure of the table; Username field must be unique, passwords can be identical
    cursor.execute(query) 
    conn.commit() 

def enter(username, password):
    query = "INSERT INTO login (Username, Password) VALUES (?, ?)" #Inserts the new username and password into the database
    cursor.execute(query, (username, password))
    conn.commit()

def check(username, password):
    query = 'SELECT * FROM login WHERE Username = ? AND Password = ?' #Checks if the username and password combination exists within the database
    cursor.execute(query, (username, password)) 
    result = cursor.fetchone()
    return result

def user_exists(username):
    query = "SELECT 1 FROM login WHERE Username = ?" #Checks if username already exists within the database
    cursor.execute(query, (username,))
    return cursor.fetchone() is not None #Returns True if it exists, returns False otherwise

def valid_username(username):
    return len(username) >= 6 and len(username) <= 15 #Returns true if username is correct length
def valid_password(password):
    return len(password) >= 6 and len(password) <= 15 #Returns true if password is correct length

def login_screen(screen):
    pygame.mixer.music.load("Music/Login_Music.mp3")#Loads and plays the login music on a loop
    pygame.mixer.music.play(-1)
    font = pygame.font.Font(None, 32)
    title_font = pygame.font.Font(None, 64)
    username_box = InputBox(300, 200, 200, 40,15,font) #Creates the username and password input boxes
    password_box = InputBox(300, 260, 200, 40,15,font, is_password=True)
    message = ""
    mode = "Login" #Sets the screen the player is on to login by default
    Login_button = Button(350, 320, 100, 40, True, mode, font)
    Go_signup_button = Button(350, 380, 100, 40, True, "Sign Up", font)
    attempts = 0
    while attempts < 3:
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT:
                return False
            username_box.handle_event(event)
            password_box.handle_event(event)
            if Go_signup_button.action(event) == True: #If the player clicks the sign up button
                mode = "Signup"
                message = ""
                username_box.text = ""
                password_box.text = ""
                Go_signup_button.hide()
                Login_button.set_text("Sign Up")
            if Login_button.action(event) is True: #If the player clicks the login button
                username = username_box.text
                password = hashlib.sha256(password_box.text.encode()).hexdigest() #Hashes the password input for secure storage and comparison
                if mode == "Login":
                    if not valid_username(username) or not valid_password(password_box.text):  # validate original
                        message = "Username and passwords must be 6-15 characters."
                        attempts += 1
                        username_box.text = ""
                        password_box.text = ""
                        continue
                    if check(username, password):
                        message = "Login successful!"
                        return True
                    else:
                        message = "Invalid username or password."
                        attempts += 1
                elif mode == "Signup":
                    username = username_box.text
                    password = hashlib.sha256(password_box.text.encode()).hexdigest()  # hash the password
                    if not valid_username(username) or not valid_password(password_box.text):  # validate original
                        message = "Username and passwords must be 6-15 characters."
                        continue
                    if user_exists(username):
                        message = "That username already exists."
                    else:
                        enter(username, password)
                        message = "Account created! Please log in."
                        username_box.text = ""
                        password_box.text = ""
                        mode = "Login"
                        Login_button.set_text("Login")
                        Go_signup_button.visible = True
                        
        #----Drawing the login screen
        screen.fill((30, 30, 30)) 
        title = "Login" if mode == "Login" else "Sign Up"
        title_surface = title_font.render(title, True, (255,255,255))
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 80))
        screen.blit(title_surface, title_rect)
        username_box.draw(screen)
        password_box.draw(screen)
        screen.blit(font.render("Username:", True, (255,255,255)), (135, 207))
        screen.blit(font.render("Password:", True, (255,255,255)), (135, 267))
        screen.blit(font.render(message, True, (255,50,100)), (135, 150))
        Login_button.draw(screen)
        Go_signup_button.draw(screen)
        pygame.display.flip()
        clock.tick(30)
    return False #Exceeded maximum login attempts

conn = sqlite3.connect("Login.db") #Connects to the database file
cursor = conn.cursor()

create_table() #Creates the login table if it does not already exist