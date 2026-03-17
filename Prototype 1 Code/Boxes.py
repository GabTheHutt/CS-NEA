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
    def __init__(self, x, y, w, h,visible, text, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.visible = visible
        self.font = font


    def draw(self, screen):
        if self.visible:
            pygame.draw.rect(screen, self.rect) #Draws the button as a rectangle
            txt_surface = self.font.render(self.text, True)
            text_rect = txt_surface.get_rect(center=self.rect.center) #Centers the text on the button
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
            self.offset = max(min(self.offset, 0), -(self.content_height - self.rect.h)) 
            #Limits the scroll offset to prevent scrolling past the content

    def apply(self, y):
        return y + self.offset #Applies the scroll offset to a given y-coordinate

class SettingsManager:
    def __init__(self, filename="settings.json"):
        self.filename = filename
        self.settings = {
            "difficulty": 5,
            "volume": 75,
            "keybinds": { 
                "shoot": "r", 
                "dash": "lshift", 
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
    
    def reset_keybinds(self):
        self.settings = {
            "difficulty": 5,
            "volume": 75,
            "keybinds": {
                "shoot": "r",
                "dash": "lshift",
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

    def update_position(self, scroll_offset):
        self.rect.y = self.base_y + scroll_offset
        self.rect.x = self.base_x
        #Updates the position to keep it in line with the hitbox when the scroll area is scrolled


    def handle_event(self, event, scroll_x, scroll_y):
        if event.type == pygame.MOUSEBUTTONDOWN:
            local_x = event.pos[0] - scroll_x
            local_y = event.pos[1] - scroll_y #Creates a local position for the mouse click
            hitbox = pygame.Rect( self.rect.x - scroll_x, self.rect.y - scroll_y, self.rect.w, self.rect.h)
            self.active = hitbox.collidepoint(local_x, local_y)
            #The position of the mouse click is adjusted to account for the scroll area

        if event.type == pygame.KEYDOWN and self.active:
            new_key = pygame.key.name(event.key)
            self.settings.set_key(self.action, new_key)
            self.active = False
            #Updates to the new key

    def draw(self, surface, offset_x=0, offset_y=0):
        colour = (0,0,255) if self.active else (255,255,255) #Changes colour to blue if the box is active
        pygame.draw.rect(surface, colour,(self.rect.x - offset_x, self.rect.y - offset_y, self.rect.w, self.rect.h), 2)
        key_text = self.settings.get_key(self.action)
        text_surface = self.font.render(key_text, True, (255,255,255))
        surface.blit(text_surface, (self.rect.x - offset_x + 5, self.rect.y - offset_y + 5))

class text_box:
    def __init__(self, x, y, text, font, colour=(255, 255, 255)):
        self.x = x
        self.y = y
        self.text = text
        self.font = font
        self.colour = colour

    def draw(self, screen):
        txt_surface = self.font.render(self.text, True, self.colour)
        screen.blit(txt_surface, (self.x, self.y))
    def set_text(self, new_text):
        self.text = new_text
    def set_colour(self, new_colour):
        self.colour = new_colour   
    def set_position(self, new_x, new_y):
        self.x = new_x
        self.y = new_y

class Heading(text_box):
    def __init__(self, x, y, text, font, colour=(255, 255, 255)):
        super().__init__(x, y, text, font, colour)
        