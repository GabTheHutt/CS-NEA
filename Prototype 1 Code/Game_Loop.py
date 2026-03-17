import pygame
from Map import load_test_map, WORLD_WIDTH
from Player import *


def draw_map(screen, tiles, camera_x):
    for tile in tiles:
        draw_rect = pygame.Rect( tile.x - camera_x, tile.y, tile.width, tile.height )
        pygame.draw.rect(screen, (140, 70, 20), draw_rect)
        #Map is drawn as brown rectangles.

def Play(screen,settings_manager):
    clock= pygame.time.Clock()
    running = True
    tiles = load_test_map()
    player = Player(100, 300)
    
    while running:
        dt = clock.tick(60) / 1000 # delta time for smooth movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
        
        # Handle player input and movement
        keys = pygame.key.get_pressed()
        player.handle_input(keys)
        player.apply_gravity(dt)
        player.move(dt, tiles)

        # CAMERA: centre on player 
        camera_x = player.rect.centerx - screen.get_width() // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - screen.get_width()))

        screen.fill((135, 206, 235))
        draw_map(screen, tiles, camera_x)
        player.draw(screen, camera_x)
        pygame.display.update()