import pygame
import json
import os
pygame.font.init()

class InputBox:
    def __init__(self, x, y, w, h,upper,font, is_password=False, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""
        self.upper = upper #Sets a maximum character amount
        self.font = font
        self.is_password = is_password #Determines if the input box is for a password
        self.active = False
        self.colour_inactive = pygame.Color('lightskyblue3')
        self.colour_active = pygame.Color('dodgerblue2')
        self.colour = self.colour_inactive #Changes colour if it is in use

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos): #Whenever the player clicks on the input box
                self.active = not self.active
            else:
                self.active = False
            self.colour = self.colour_active if self.active else self.colour_inactive
        if event.type == pygame.KEYDOWN and self.active: #Triggers when the box has been selected and the player types.
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1] #Deletes the last character if backspace is pressed
            elif len(self.text) <= self.upper: 
                self.text += event.unicode #Adds the character pressed to the input box

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect, 2)
        font = pygame.font.Font(None, 32)
        display_text = "*" * len(self.text) if self.is_password else self.text
        txt_surface = font.render(display_text, True, self.colour)
        screen.blit(txt_surface, (self.rect.x+5, self.rect.y+5))
        self.rect.w = max(200, txt_surface.get_width()+10)

class Button:
    def __init__(self, x, y, w, h,visible, text, font, bg_colour=(60,60,60), text_colour=(255,255,255), border_colour=(255,255,255)):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.visible = visible
        self.font = font
        self.bg_colour = bg_colour #Defaults the colour to the specified background colour
        self.text_colour = text_colour
        self.border_colour = border_colour

    def draw(self, screen):
        if self.visible:
            mouse_pos = pygame.mouse.get_pos()
            colour = (100,100,100) if self.rect.collidepoint(mouse_pos) else self.bg_colour #Hover effects
            pygame.draw.rect(screen, colour, self.rect)
            pygame.draw.rect(screen, self.border_colour, self.rect, 3)  # border
            txt_surface = self.font.render(self.text, True, self.text_colour)
            text_rect = txt_surface.get_rect(center=self.rect.center)
            screen.blit(txt_surface, text_rect)

    def action(self, event):
        if not self.visible:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN: #Checks if the button is clicked only while it is visible
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def hide(self): 
        self.visible = False 
    
    def show(self): 
        self.visible = True
    
    def set_text(self, new_text):
        self.text = new_text

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.base_y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.knob = pygame.Rect(x, y - 6, 20, h + 12) #The knob is set larger than the slider bar
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.dragging = False

        ratio = (start_val - min_val) / (max_val - min_val)
        self.knob.x = x + ratio * w  #Positions the knob according to the starting value

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.knob.collidepoint(event.pos):
                self.dragging = True

        if event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False

        if event.type == pygame.MOUSEMOTION and self.dragging:
            self.knob.x = max(self.rect.x, min(event.pos[0], self.rect.x + self.rect.w)) #Keeps the knob within the slider bar
            ratio = (self.knob.x - self.rect.x) / self.rect.w
            self.value = int(self.min_val + ratio * (self.max_val - self.min_val)) #Updates the value according to the position of the knob

    def draw(self, surface, offset_x=0, offset_y=0): 
        pygame.draw.rect(surface, (180,180,180), (self.rect.x - offset_x, self.rect.y - offset_y, self.rect.w, self.rect.h)) #Draws the slider bar
        pygame.draw.rect(surface, (255,120,0), (self.knob.x - offset_x, self.knob.y - offset_y, self.knob.w, self.knob.h)) #Draws the knob

    def update_position(self, scroll_offset):
        self.rect.y = self.base_y + scroll_offset
        self.knob.y = self.rect.y - 6
    
    def reset(self, value):
        self.value = value
        ratio = (value - self.min_val) / (self.max_val - self.min_val)
        self.knob.x = self.rect.x + ratio * self.rect.w

class ScrollArea:
    def __init__(self, x, y, w, h, content_height):
        self.rect = pygame.Rect(x, y, w, h)
        self.offset = 0
        self.content_height = content_height

    def handle_event(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.offset += event.y * 25
            self.offset = max(min(self.offset, 0), -(self.content_height - self.rect.h)) #Limits the scroll offset to prevent scrolling past the content

    def apply(self, y):
        return y + self.offset #Applies the scroll offset to a given y-coordinate

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.settings = {
            "difficulty": 5,
            "volume": 75,
            "show_enemy_health": True,
            "music": True,
            "sfx": True,
            "keybinds": { 
                "shoot": "r", 
                "dash": "left shift", 
                "left": "a",
                "right": "d",
                "jump": "space", 
                "melee": "e", 
                "interact": "f"  
            } #Default keybinds, can be changed by the player and will be saved to the settings file
        }
        self.load()

    def load(self): 
        if os.path.exists(self.filename): 
            with open(self.filename, "r") as f:
                self.settings = json.load(f) #Loads the settings from the file if it exists, otherwise uses the default settings
    
    def save(self): 
        with open(self.filename, "w") as f:
            json.dump(self.settings, f, indent=4) #Saves the current settings to the file in a readable format
        
    
    def get_key(self, action):
        return self.settings["keybinds"].get(action, "")

    def set_key(self, action, key):
        self.settings["keybinds"][action] = key
    
    def get_volume(self):
        return self.settings["volume"]
    
    def set_volume(self, volume):
        self.settings["volume"] = volume
    
    def get_difficulty(self):
        return self.settings["difficulty"]
    
    def set_difficulty(self, difficulty):
        self.settings["difficulty"] = difficulty
    
    def get_pygame_key(settings_manager, action):
        key_name = settings_manager.get_key(action).replace(" ", "_")
        return getattr(pygame, f"K_{key_name}", None)
    
    # Get and set methods for the show enemy health settings;
    # When enabled, health bars appear over the enemy.
    def get_show_enemy_health(self):
        return self.settings.get("show_enemy_health", True)

    def set_show_enemy_health(self, value):
        self.settings["show_enemy_health"] = value
    
    # Get and set methods for the music and sfx settings; 
    # When enabled, the respective audio will play in the game.
    def get_music(self):
        return self.settings.get("music", True)
    
    def set_music(self, value):
        self.settings["music"] = value
    
    def get_sfx(self):
        return self.settings.get("sfx", True)
    
    def set_sfx(self, value):
        self.settings["sfx"] = value
    
    # Stores the default values of the settings;
    # Writes over the JSON file when the button is pressed and saves changes
    def reset_keybinds(self):
        self.settings = {
            "difficulty": 5,
            "volume": 75,
            "show_enemy_health": True,
            "music": True,
            "sfx": True,
            "keybinds": {
                "shoot": "r",
                "dash": "left shift",
                "left": "a",
                "right": "d",
                "jump": "space",
                "melee": "e",
                "interact": "f"
            }
        }
        self.save()

class KeyBindBox:
    def __init__(self, x, y, w, h, action, settings_manager, font):
        self.base_y = y
        self.base_x = x
        self.rect = pygame.Rect(x, y, w, h)
        self.action = action
        self.settings = settings_manager
        self.font = font
        self.active = False
        self.duplicate = False

    def update_position(self, scroll_offset):
        self.rect.y = self.base_y + scroll_offset
        self.rect.x = self.base_x
        #Updates the position to keep it in line with the hitbox when the scroll area is scrolled


    def handle_event(self, event, scroll_x, scroll_y):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #Checks for left mouse clicks
            local_x = event.pos[0] - scroll_x
            local_y = event.pos[1] - scroll_y #Creates a local position for the mouse click
            hitbox = pygame.Rect( self.rect.x - scroll_x, self.rect.y - scroll_y, self.rect.w, self.rect.h)
            self.active = hitbox.collidepoint(local_x, local_y)
            #The position of the mouse click is adjusted to account for the scroll area

        if event.type == pygame.KEYDOWN and self.active:
            new_key = pygame.key.name(event.key)
            current_keybinds = self.settings.settings["keybinds"].values()
            if new_key not in current_keybinds: #Prevents duplicate keybinds
                self.settings.set_key(self.action, new_key)
                self.duplicate = False
            else:
                self.duplicate = True
            self.active = False #De-selects the box after a key has been pressed

    def draw(self, surface, offset_x=0, offset_y=0):
        colour = (0,0,255) if self.active else (255,255,255)
        draw_rect = pygame.Rect(self.rect.x - offset_x,
                                self.rect.y - offset_y, self.rect.w, self.rect.h)
        pygame.draw.rect(surface, colour, draw_rect, 2)
        key_text = self.settings.get_key(self.action)
        text_surface = self.font.render(key_text.capitalize(), True, (255,255,255))
        text_rect = text_surface.get_rect(center=draw_rect.center)  # centre within box
        surface.blit(text_surface, text_rect)

class text_box:
    def __init__(self, x, y, text, font, colour=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.colour = colour

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.colour)
        screen.blit(txt_surface, (self.x, self.y)) #Draws the text at the specified position
    def set_text(self, new_text):
        self.text = new_text #Allows the text to be changed after the box has been created
    def set_colour(self, new_colour):
        self.colour = new_colour   
    def set_position(self, new_x, new_y): #Allows the position to be changed after the box has been created
        self.x = new_x
        self.y = new_y

class Heading(text_box):
    def __init__(self, x, y, text, font, colour=(255, 255, 255)):
        super().__init__(x, y, text, font, colour) 

class HealthBar:
    def __init__(self, x, y, w, h, max_health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.max_health = max_health

    def draw(self, screen, current_health):
        # Background bar (red)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.w, self.h))
        # Health bar (green)
        health_ratio = current_health / self.max_health
        current_width = int(self.w * health_ratio)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y, current_width, self.h))
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (self.x, self.y, self.w, self.h), 2)
        # Health text
        font = pygame.font.SysFont(None, 28)
        text = font.render(f"{current_health} / {self.max_health}", True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.x + self.w // 2, self.y + self.h // 2))
        screen.blit(text, text_rect)

class Toggle:
    def __init__(self, x, y, w, h, initial_value, settings_manager, setting_getter, setting_setter):
        self.base_x = x
        self.base_y = y
        self.rect = pygame.Rect(x, y, w, h)
        self.value = initial_value
        self.settings_manager = settings_manager
        self.setting_getter = setting_getter  # function to get value
        self.setting_setter = setting_setter  # function to set value
        # Knob starts on left (OFF) or right (ON)
        self.knob_rect = pygame.Rect(x, y, h, h)  # knob is square
        self.knob_x = x + (w - h) if initial_value else x  # position based on value
        self.knob_rect.x = self.knob_x
        self.animating = False

    def update_position(self, scroll_offset):
        self.rect.y = self.base_y + scroll_offset
        self.knob_rect.y = self.rect.y

    def handle_event(self, event, scroll_x, scroll_y):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            local_x = event.pos[0] - scroll_x
            local_y = event.pos[1] - scroll_y
            hitbox = pygame.Rect(
                self.rect.x - scroll_x,
                self.rect.y - scroll_y,
                self.rect.w, self.rect.h
            )
            if hitbox.collidepoint(local_x, local_y):
                self.value = not self.value
                self.setting_setter(self.value)
                # Snap knob to new position
                self.knob_rect.x = self.rect.x + (self.rect.w - self.rect.h) if self.value else self.rect.x

    def draw(self, surface, offset_x=0, offset_y=0):
        draw_rect = pygame.Rect(
            self.rect.x - offset_x,
            self.rect.y - offset_y,
            self.rect.w, self.rect.h
        )
        knob_draw_rect = pygame.Rect(
            self.knob_rect.x - offset_x,
            self.rect.y - offset_y,
            self.rect.h, self.rect.h
        )
        # Background colour changes based on state
        bg_colour = (0, 180, 0) if self.value else (100, 100, 100)
        pygame.draw.rect(surface, bg_colour, draw_rect, border_radius=self.rect.h // 2)
        # ON/OFF text
        font = pygame.font.SysFont(None, 28)
        if self.value:
            label = font.render("ON", True, (255, 255, 255))
            surface.blit(label, (draw_rect.x + 8, draw_rect.y + draw_rect.h // 2 - label.get_height() // 2))
        else:
            label = font.render("OFF", True, (255, 255, 255))
            surface.blit(label, (draw_rect.right - label.get_width() - 8 - self.rect.h,
                                  draw_rect.y + draw_rect.h // 2 - label.get_height() // 2))
        # Knob
        pygame.draw.circle(surface, (255, 255, 255),
                           knob_draw_rect.center, self.rect.h // 2 - 2)