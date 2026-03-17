import pygame
from Weapons import MeleeWeapon, RangedWeapon, Bullet

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 60)
        # Spawn position is stored to allow for respawning after death
        self.spawn_x = x
        self.spawn_y = y
        self.vel_x = 0
        self.vel_y = 0

        #Horizontal movement parameters
        self.speed = 200        # max horizontal speed
        self.acceleration = 1000 # how fast the player reaches max speed
        self.friction = 800     # how fast the player slows down

        #Vertical movement parameters
        self.jump_strength = -600
        self.gravity = 1500
        self.on_ground = False

        #Health and damage system
        self.max_health = 100
        self.health = self.max_health
        self.alive = True

        # Death effect
        self.dying = False
        self.death_timer = 0
        self.death_duration = 2000  # 2 seconds before respawn

        # Invincibility frames to prevent taking damage every frame
        self.invincible = False
        self.invincible_timer = 0
        self.invincible_duration = 1500  # milliseconds

        # Weapons
        self.facing_right = True
        self.dagger = MeleeWeapon("Dagger", damage=20, cooldown=500, reach=50)
        self.revolver = RangedWeapon("Revolver", damage=30, cooldown=800,
                                      bullet_speed=600, max_ammo=6)
        self.bullets = []
    
    #Damage and healing methods
    def take_damage(self, amount):
        if self.invincible:
            return
        self.health -= amount
        self.invincible = True
        self.invincible_timer = pygame.time.get_ticks()
        if self.health <= 0:
            self.health = 0
            self.alive = False
            self.dying = True
            self.death_timer = pygame.time.get_ticks()
        # The player becomes invincible after taking damage;
        # Same method is used to calculate player death status.
        # Invincibilty timer tracks and limits the player's invincibility status.

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)
        # Healing method to restore player health, ensuring it does not exceed max health.
    
    def set_spawn(self, x, y):
        self.spawn_x = x  # updates spawn point when resting at a location
        self.spawn_y = y
    
    
    def respawn(self):
        self.rect.x = self.spawn_x
        self.rect.y = self.spawn_y
        self.health = self.max_health
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
        self.dying = False
    # Respawn method to reset player position and health after death.

    def update_invincibility(self):
        if self.invincible:
            if pygame.time.get_ticks() - self.invincible_timer > self.invincible_duration:
                self.invincible = False
        # This method should be called in the main game loop to update the player's invincibility status


    # Updates the player's death status and respawns them after the death duration has passed.
    def update_death(self):
        if self.dying:
            if pygame.time.get_ticks() - self.death_timer > self.death_duration:
                self.respawn()
    
    def handle_input(self, keys, settings_manager, dt):
        if self.dying:  # lock movement during death animation
            self.vel_x = 0
            return
        
        try:
            left_key = pygame.key.key_code(settings_manager.get_key('left'))
            right_key = pygame.key.key_code(settings_manager.get_key('right'))
            jump_key = pygame.key.key_code(settings_manager.get_key('jump'))
        except ValueError:
            return

        moving = False
        if keys[left_key]:
            self.vel_x -= self.acceleration * dt
            moving = True
        if keys[right_key]:
            self.vel_x += self.acceleration * dt
            moving = True
        
        # Update facing direction based on horizontal velocity
        if self.vel_x > 0:
            self.facing_right = True
        elif self.vel_x < 0:
            self.facing_right = False

        # Apply friction when no key is pressed
        # Slows down the player's movement while they are not accelerating
        # Allows for more precise control
        if not moving:
            if self.vel_x > 0:
                self.vel_x = max(0, self.vel_x - self.friction * dt)
            elif self.vel_x < 0:
                self.vel_x = min(0, self.vel_x + self.friction * dt)

        # Sets the terminal velocity of the player.
        # Prevents reaching infinite speeds
        self.vel_x = max(-self.speed, min(self.speed, self.vel_x))

        if keys[jump_key] and self.on_ground:
            self.vel_y = self.jump_strength
    
    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
        #Gravity is applied to the vertical velocity each frame.

    def move(self, dt, tiles):
    # Horizontal velocity and collisions
        self.rect.x += self.vel_x * dt
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.rect.right = tile.left
                elif self.vel_x < 0:
                    self.rect.left = tile.right

        # Vertical velocities and collisions
        self.rect.y += self.vel_y * dt
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top #Moving downwards
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0: #Moving upwards
                    self.rect.top = tile.bottom
                    self.vel_y = 0


    def draw(self, screen, camera_x):
        if self.dying:
            # Flash red during death animation
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                colour = (255, 0, 0)
            else:
                colour = (255, 255, 0)
        else:
            colour = (255, 255, 0)
        pygame.draw.rect(screen, colour,
            pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h))