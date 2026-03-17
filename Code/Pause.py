import pygame
from Boxes import *
from Settings import Show_settings
from UI import draw_title, Menu_screen

def Show_pause(screen, font, settings_manager):
    pause_menu = Menu_screen(screen,["Resume", "Settings", "Main Menu"],font) #Creates the pause menu
    paused = True
    clock = pygame.time.Clock()

    while paused:
        screen.fill((0, 0, 0))
        draw_title(screen)
        pause_menu.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            result = pause_menu.handle_event(event)
            if result == "Resume":
                paused = False #Unpauses the game and returns to the game loop
            elif result == "Settings":
                Show_settings(screen, font, settings_manager)
            elif result == "Main Menu":
                return "main_menu"  # signal to game loop to return to main menu

        clock.tick(60)
        pygame.display.update()