import pygame
from Boxes import *
from Game_Loop import Play
from Settings import Show_settings
from UI import Menu_screen, draw_title
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 600))
font = pygame.font.Font(None, 36)
small_font = pygame.font.SysFont(None, 32)
settings_manager = SettingsManager()

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

def Main():
    menu = Menu_screen(screen, ["Play", "Settings", "Instructions"], font) #Instantiates the menu with 3 options
    running = True
    clock = pygame.time.Clock()
    if settings_manager.get_music(): #Checks if music is enabled in settings before playing music
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
                # Turns the music on or off based on the new value in settings
                if settings_manager.get_music():
                    if not pygame.mixer.music.get_busy(): #If music isn't already playing, start it
                        pygame.mixer.music.load("Music/Menu_Music.mp3")
                        pygame.mixer.music.play(-1)
                else:
                    pygame.mixer.music.stop() #If music is disabled, stop it in case it was playing
                pygame.mixer.music.set_volume(settings_manager.get_volume() / 100)
            elif result == "Instructions":
                # Handles the instructions
                Show_instructions(screen)

        clock.tick(60)
        pygame.display.update()