import pygame
from Boxes import *
from Game_Loop import Play
pygame.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
small_font = pygame.font.SysFont(None, 32)
settings_manager = SettingsManager()
pygame.mixer.init()

class Menu:
    def __init__(self, screen, options, font):
        self.screen = screen
        self.buttons = []
        start_y = int(screen.get_height() * 0.60)
        base_x = int(screen.get_width() * 0.15)
        for i, option in enumerate(options):
            btn = Button(
                x=base_x,
                y=start_y + i * 70,
                w=100 + i * 50,  # Vary width as the list goes down
                h=50,
                visible=True,
                text=option,
                font=font,
                bg_colour=(60, 60, 60),
                text_colour=(255, 255, 255),
                border_colour=(255, 255, 255))
            self.buttons.append(btn)

    def draw(self):
        for btn in self.buttons:
            btn.draw(self.screen)

    def handle_event(self, event):
        for btn in self.buttons:
            if btn.action(event):
                return btn.text
        return None

def Show_instructions(screen):
        running = True 
        clock = pygame.time.Clock()
        # Heading 
        heading = Heading(0, 80, "INSTRUCTIONS", pygame.font.SysFont(None, 70))
        heading.set_position((screen.get_width() - heading.font.size(heading.text)[0]) // 2, 80)

        # Instructions text (split into lines) 
        lines = [ "Welcome! This is the Cowboy Knight, an RPG based on Hollow Knight.", "Explore the dangers of the Wild West and defeat mafia groups", "in neighbouring outposts using your revolver and dagger.", "Visit the settings page to check the controls." ]
        text_boxes = []
        y_offset = 180
        for line in lines:
            tb = text_box(40, y_offset, line, pygame.font.SysFont(None, 32)) #Prints each line as a separate text box
            text_boxes.append(tb)
            y_offset += 40 # Space between lines
        
        # Back to Menu Button 
        back_button = Button( x=(screen.get_width() // 2) - 125, y=screen.get_height() - 120, w=250, h=60, visible=True, text="BACK TO MENU", font=pygame.font.SysFont(None, 40) )

        while running:
            screen.fill((0, 0, 0)) #Clears screen each frame
            heading.draw(screen)
            for tb in text_boxes: tb.draw(screen) #Draws each line of instructions
            back_button.draw(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if back_button.action(event): 
                    running = False #Exits instructions screen if the back button is clicked

            pygame.display.update()
            clock.tick(60)

def Show_settings(screen, font, settings_manager):

    in_settings = True
    clock = pygame.time.Clock()

    heading = Heading(0, 80, "SETTINGS", pygame.font.SysFont(None, 70))
    heading.set_position((screen.get_width() - heading.font.size(heading.text)[0]) // 2, 80) #Centers the heading at the top of the screen

    # Volume slider
    volume_slider = Slider(320, 200, 300, 8, 0, 100, settings_manager.get_volume())
    volume_slider.base_y = 200

    #Difficulty slider
    difficulty_slider = Slider(320, 260, 300, 8, 1, 10, settings_manager.get_difficulty())
    difficulty_slider.base_y = 260

    # Scroll area for keybinds
    actions = ["shoot", "dash", "left", "right", "jump", "melee", "interact"]
    keybind_font = pygame.font.SysFont(None, 32)

    scroll_area = ScrollArea((screen.get_width() - 500) // 2, 150, 500, 300, content_height=200 + len(actions) * 70)
    LEFT_MARGIN = 40 #Margin for text inside the scroll area

    #Scroll Surface
    scroll_surface = pygame.Surface((scroll_area.rect.w, scroll_area.rect.height)) #Creates a separate surface for the scroll area content, which allows for smoother scrolling and prevents artifacts when scrolling
    scroll_surface.set_colorkey((0,0,0))

    keybind_boxes = []
    y = 340
    for action in actions:
        keybind_boxes.append(KeyBindBox(320, y, 150, 40, action, settings_manager, keybind_font)) 
        y += 70 #Creates a keybind box for each action, which allows the player to change the keybinds

    back_button = Button(x=50,y=screen.get_height() - 120,w=250,h=60,visible=True,text="BACK TO MENU",font=small_font)
    reset_button = Button(x=screen.get_width() - 50 - 250,y=screen.get_height() - 120,w=250,h=60,visible=True,text="RESET TO DEFAULT",font=small_font)

    while in_settings:
        screen.fill((0,0,0))
        heading.draw(screen)

        volume_slider.update_position(scroll_area.offset) #Updates the position of the sliders based on the scroll offset, so they will scroll with the keybind boxes
        difficulty_slider.update_position(scroll_area.offset)
        # Scroll area background
        scroll_surface.fill((40,40,40))

        pygame.draw.rect(screen, (40,40,40), scroll_area.rect)

        visible_top = scroll_area.rect.top
        visible_bottom = scroll_area.rect.bottom
        #Calculates the visible area of the scroll content
        
        # Draw volume slider
        if volume_slider.rect.bottom >= visible_top and volume_slider.rect.top <= visible_bottom:
            vol_label = font.render("Volume:", True, (255,255,255))
            scroll_surface.blit(vol_label, (LEFT_MARGIN, volume_slider.rect.y - scroll_area.rect.y - 10))
            volume_slider.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)
        
        # Draw difficulty slider
        if difficulty_slider.rect.bottom >= visible_top and difficulty_slider.rect.top <= visible_bottom:
            diff_label = font.render("Difficulty:", True, (255,255,255))
            scroll_surface.blit(diff_label,(LEFT_MARGIN, difficulty_slider.rect.y - scroll_area.rect.y - 10))
            difficulty_slider.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)

        # Draw keybinds inside scroll area
        for kb in keybind_boxes:
            kb.update_position(scroll_area.offset)
            if kb.rect.bottom >= visible_top and kb.rect.top <= visible_bottom:
                label = keybind_font.render(kb.action.upper(), True, (255,255,255))
                scroll_surface.blit(label, (LEFT_MARGIN, kb.rect.y - scroll_area.rect.y + 10))
                kb.draw(scroll_surface, scroll_area.rect.x, scroll_area.rect.y)

        screen.blit(scroll_surface, scroll_area.rect.topleft) #Draws the scroll surface onto the main screen at the position of the scroll area

        back_button.draw(screen)
        reset_button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # Handle events for sliders, scroll area, and keybind boxes
            volume_slider.handle_event(event)
            difficulty_slider.handle_event(event)
            scroll_area.handle_event(event)
            if reset_button.action(event):
                settings_manager.reset_keybinds() #Resets settings to default values
                # Reset sliders to default values
                volume_slider.reset(settings_manager.get_volume())
                difficulty_slider.reset(settings_manager.get_difficulty())

                # Update all keybind boxes to reflect new defaults
                for kb in keybind_boxes:
                    kb.active = False  # ensure none stay selected

            for kb in keybind_boxes:
                kb.handle_event(event, scroll_area.rect.x, scroll_area.rect.y)  

            # Save the settings and return to the main menu
            if back_button.action(event):
                settings_manager.set_volume(volume_slider.value)
                settings_manager.set_difficulty(difficulty_slider.value)
                settings_manager.save()
                in_settings = False

        pygame.display.update()
        clock.tick(60)

def draw_title(screen):
    font = pygame.font.Font(None, 120)  # choose your font + size

    line1 = font.render("The", True, (255, 255, 255))
    line2 = font.render("Cowboy", True, (255, 255, 255))
    line3 = font.render("Knight", True, (255, 255, 255))

    # Center horizontally
    screen_width = screen.get_width()

    line1_rect = line1.get_rect(center=(screen_width // 2, 80))
    line2_rect = line2.get_rect(center=(screen_width // 2, 170))
    line3_rect = line3.get_rect(center=(screen_width // 2, 260))

    screen.blit(line1, line1_rect)
    screen.blit(line2, line2_rect)
    screen.blit(line3, line3_rect)

def Main():
    menu = Menu(screen, ["Play", "Settings", "Instructions"], font) #Instantiates the menu with 3 options
    running = True
    clock = pygame.time.Clock()
    pygame.mixer.music.load("Music/Menu_Music.mp3")
    pygame.mixer.music.play(-1) #Plays menu music on a loop
    pygame.mixer.music.set_volume(settings_manager.get_volume() / 100) #Adjusts for the volume setting
    while running:
        screen.fill((0, 0, 0))
        draw_title(screen)  #Draws the game title at the top of the menu
        menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            result = menu.handle_event(event)
            if result == "Play":
                pygame.mixer.music.stop()
                Play(screen, settings_manager) #Starts the game loop
            elif result == "Settings":
                # Handles the settings loop
                Show_settings(screen, font, settings_manager)
                # Changes the volume to the new value after returning from the settings menu
                pygame.mixer.music.set_volume(settings_manager.get_volume() / 100)
            elif result == "Instructions":
                # Handles the instructions
                Show_instructions(screen)

        clock.tick(60)
        pygame.display.update()