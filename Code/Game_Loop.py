import pygame
from Boxes import HealthBar
from Map import load_test_map, WORLD_WIDTH
from Player import *
from Pause import Show_pause
from Entities import Enemy, NPC
font = pygame.font.Font(None, 36)


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
    currency = 0
    enemies = [Enemy(400, 300, 40, 60, 50, 100, 10, 25)]
    health_bar = HealthBar(20, 20, 200, 25, player.max_health)
    
    while running:
        dt = clock.tick(60) / 1000 # delta time for smooth movement
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()
            # Pause menu
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                result = Show_pause(screen, font, settings_manager)
                if result == "main_menu":
                    return  # Exit to main menu
                clock.tick()  # discard the time spent in the pause menu
            if event.type == pygame.KEYDOWN:
                melee_key = pygame.key.key_code(settings_manager.get_key('melee'))
                shoot_key = pygame.key.key_code(settings_manager.get_key('shoot'))
                if event.key == melee_key:
                    player.dagger.attack(player.rect, player.facing_right, enemies)
                if event.key == shoot_key:
                    player.revolver.attack(player.rect, player.facing_right, player.bullets)
        
        # Handle player input and movement
        # Keys take the player's inputs and pass them to the player object.
        # This updates their velocity, which then allows for movement, jumping, and other actions.
        # Gravity must be updated separately to ensure it applies even when no keys are pressed.
        keys = pygame.key.get_pressed()
        player.handle_input(keys,settings_manager,dt)
        player.apply_gravity(dt)
        player.move(dt, tiles)
        player.update_invincibility()
        player.update_death()

        # CAMERA: centre on player 
        camera_x = player.rect.centerx - screen.get_width() // 2
        camera_x = max(0, min(camera_x, WORLD_WIDTH - screen.get_width()))

        screen.fill((135, 206, 235))
        draw_map(screen, tiles, camera_x)

        # Update and draw enemies
        for enemy in enemies:
            enemy.update(dt, tiles, player)
            if not enemy.alive:
                currency += enemy.drop_currency()  # add dropped currency to player's total
            enemy.draw(screen, camera_x, settings_manager.get_show_enemy_health())  # draw before filtering out dead enemies
        enemies = [enemy for enemy in enemies if enemy.alive]

        # Update and draw bullets
        for bullet in player.bullets:
            bullet.update(dt, tiles, enemies)
        player.bullets = [b for b in player.bullets if b.active]

        # In drawing section
        for bullet in player.bullets:
            bullet.draw(screen, camera_x)

        player.draw(screen, camera_x)
        health_bar.draw(screen, player.health)  # drawn last so it sits on top
        pygame.display.update()