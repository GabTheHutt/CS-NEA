import pygame

WORLD_WIDTH = 5000 #sets the width of the world for camera limits
GROUND_Y = 500 #sets the y position of the ground level, which is used for player and tile placement

def load_test_map():
    tiles = [] #Creates a list of tiles for the test map

    tiles.append(pygame.Rect(0, GROUND_Y, WORLD_WIDTH, 60))

    tiles.append(pygame.Rect(300, 400, 200, 30))
    tiles.append(pygame.Rect(700, 350, 200, 30))
    tiles.append(pygame.Rect(1200, 300, 200, 30))
    tiles.append(pygame.Rect(1800, 420, 250, 30))
    tiles.append(pygame.Rect(2500, 380, 200, 30))
    tiles.append(pygame.Rect(3200, 340, 200, 30))
    tiles.append(pygame.Rect(4000, 300, 250, 30))

    return tiles