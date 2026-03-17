import sqlite3
from Login import *
from Boxes import *

def login_screen(screen):
    font = pygame.font.Font(None, 32)

    # Input boxes
    username_box = InputBox(300, 200, 200, 40, 15, font)
    password_box = InputBox(300, 260, 200, 40, 15, font, is_password=True)

    # Buttons (created outside the loop to not reset their state every frame)
    login_button = Button(350, 320, 100, 40, True, "Login", font)
    signup_button = Button(350, 380, 100, 40, True, "Sign Up", font)

    mode = "login"   # or "signup"
    message = ""
    attempts = 0
    # Main loop for login/signup screen
    while attempts < 3:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            username_box.handle_event(event)
            password_box.handle_event(event)

            # --- BUTTON CLICKS ---
            if signup_button.action(event):
                mode = "signup"
                message = ""
                username_box.text = ""
                password_box.text = ""

            if login_button.action(event):
                username = username_box.text
                password = password_box.text

                # LOGIN MODE
                if mode == "login":
                    if not valid_username(username) or not valid_password(password):
                        message = "Username and passwords must be 6-15 characters."
                        attempts += 1
                        username_box.text = ""
                        password_box.text = ""
                        continue

                    if check(username, password): #Checks the username and password against the database
                        message = "Login successful!"
                        return True
                    else:
                        message = "Invalid username or password."
                        attempts += 1

                # SIGNUP MODE
                elif mode == "signup":
                    if not valid_username(username) or not valid_password(password):
                        message = "Username and passwords must be 6-15 characters."
                        continue

                    if user_exists(username):
                        message = "That username already exists."
                    else:
                        enter(username, password)
                        message = "Account created! Please log in."
                        username_box.text = ""
                        password_box.text = ""
                        mode = "login"

        # --- DRAWING ---
        screen.fill((30, 30, 30))

        title = "Login" if mode == "login" else "Sign Up"
        screen.blit(font.render(title, True, (255,255,255)), (260, 80))

        username_box.draw(screen)
        password_box.draw(screen)
        
        # Draw labels and messages for the buttons.
        screen.blit(font.render("Username:", True, (255,255,255)), (120, 150))
        screen.blit(font.render("Password:", True, (255,255,255)), (120, 210))
        screen.blit(font.render(message, True, (255,100,100)), (220, 260))

        # Update login button text depending on mode
        login_button.text = "Login" if mode == "login" else "Create"

        login_button.draw(screen)
        signup_button.draw(screen)

        pygame.display.flip()
        clock.tick(30)

    return False

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.knob_rect = pygame.Rect(x, y - 5, 15, h + 10)
         #Separate rect for the knob with padding
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.dragging = False

        # Position knob based on start_val
        ratio = (start_val - min_val) / (max_val - min_val)
        self.knob_rect.x = x + ratio * w

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob_rect.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            # Move knob but clamp inside slider
            self.knob_rect.x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w))
            # Convert knob position → value
            ratio = (self.knob_rect.x - self.rect.x) / self.rect.w
            self.value = self.min_val + ratio * (self.max_val - self.min_val)

    def draw(self, screen):
        pygame.draw.rect(screen, (180,180,180), self.rect)
        pygame.draw.rect(screen, (255,120,0), self.knob_rect)

# KeyBindBox class for rebinding keys in settings menu
class KeyBindBox:
    def __init__(self, x, y, w, h, action, settings_manager, font):
        self.base_y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.settings = settings_manager
        self.font = font
        self.active = False

    # Update the box's position based on scroll offset;
    # Only implemented within a scroll area.
    # Box moves up and down as the user scrolls.
    # elative to the player's position in the settings menu.
    def update_position(self, scroll_offset):
        self.rect.y = self.base_y + scroll_offset

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            new_key = pygame.key.name(event.key) #Convert key code to human-readable name (e.g., "a", "space", "left ctrl")
            self.settings.set_key(self.action, new_key) #update the key binding in the settings manager
            self.active = False

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.rect, 2)
        key_text = self.settings.get_key(self.action)
        text_surface = self.font.render(key_text, True, (255,255,255))
        screen.blit(text_surface, (self.rect.x + 5, self.rect.y + 5))


class ScrollArea:
    def __init__(self, x, y, w, h, content_height):
        self.rect = pygame.Rect(x, y, w, h)
        self.offset = 0
        self.content_height = content_height
    
    #Handles the mouse wheel event to scroll the content within the scroll area.
    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.offset += event.y * 25
            self.offset = max(min(self.offset, 0), -(self.content_height - self.rect.h))
        # Adjusts the offset while ensuring it stays within the bounds of the content height and the visible area.

    def apply(self, y):
        return y + self.offset

import json, os

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.settings = {
            "difficulty": 1,
            "volume": 75,
            "keybinds": {
                "shoot": "space",
                "dash": "lshift",
                "walk": "w",
                "jump": "space",
                "melee": "e",
                "interact": "f"}}
        self.load()
    
    #Stores the settings in a JSON file, allowing for easy retrieval and modification of user preferences which will persist across sessions.
    def load(self): 
        #Checks if the settings file exists and loads it into the settings dictionary; if not, it will use the default settings defined in the constructor.
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                self.settings = json.load(f)

    def save(self):
        with open(self.filename, "w") as f:
            json.dump(self.settings, f, indent=4) #Save the settings dictionary to a JSON file with indentation for readability

    def get_key(self, action):
        return self.settings["keybinds"].get(action, "") #Retrieves the key binding specifically

    def set_key(self, action, key):
        self.settings["keybinds"][action] = key #Update the key binding for the specified action in the settings dictionary

    def set_volume(self, vol):
        self.settings["volume"] = int(vol) #Update the volume setting in the settings dictionary, ensuring it's stored as an integer

    def get_volume(self):
        return self.settings["volume"]
