import pygame

class Player: 
    def __init__(self, x, y): 
        self.rect = pygame.Rect(x, y, 40, 60)
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 200
        self.jump_strength= -600
        self.gravity = 1500
        self.on_ground = False

    def handle_input(self, keys):
        self.vel_x = 0
        if keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_d]:
            self.vel_x = self.speed

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_strength
            #Player can only jump if they are on the ground.
    
    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
        #Gravity is applied to the vertical velocity each frame.

    def move(self, dt, tiles):
    # Horizontal velocity
        self.rect.x += self.vel_x * dt
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.rect.right = tile.left
                elif self.vel_x < 0:
                    self.rect.left = tile.right

        # Vertical
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
        pygame.draw.rect( screen, (255, 255, 0), pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h) )