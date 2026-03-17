import pygame

class Entity:
    def __init__(self, x, y, width, height, health, speed):
        # Basic properties for all entities, including position, size, health, speed, and movement variables.
        self.rect = pygame.Rect(x, y, width, height)
        self.health = health
        self.max_health = health
        self.speed = speed
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
        self.gravity = 1500
        self.on_ground = False
    
    # Applies gravity to the entity's vertical velocity.
    def apply_gravity(self, dt):
        self.vel_y += self.gravity * dt
    
    # Handles movement and collision with tiles.
    # Separates horizontal and vertical movement to ensure proper collision handling.
    def move(self, dt, tiles):
        self.rect.x += self.vel_x * dt
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.rect.right = tile.left
                elif self.vel_x < 0:
                    self.rect.left = tile.right

        self.rect.y += self.vel_y * dt
        self.on_ground = False
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_y > 0:
                    self.rect.bottom = tile.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:
                    self.rect.top = tile.bottom
                    self.vel_y = 0
    
    # Method to apply damage to the entity, reducing health and checking for death.
    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.health = 0
            self.alive = False

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def draw(self, screen, camera_x, colour):
        pygame.draw.rect(screen, colour,
            pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h))

class NPC(Entity):
    def __init__(self, x, y, width, height, health, speed, dialogue):
        super().__init__(x, y, width, height, health, speed)
        self.dialogue = dialogue  # list of strings
        self.dialogue_index = 0
        self.talking = False

    def interact(self):
        self.talking = True
        line = self.dialogue[self.dialogue_index]
        self.dialogue_index = (self.dialogue_index + 1) % len(self.dialogue)
        return line  # return the line to be displayed on screen

    def draw(self, screen, camera_x):
        super().draw(screen, camera_x, (0, 200, 0))  # green for NPCs

class Enemy(Entity):
    def __init__(self, x, y, width, height, health, speed, damage, currency_amount):
        super().__init__(x, y, width, height, health, speed)
        self.damage = damage
        self.attack_cd = 1000       # milliseconds between attacks
        self.last_attack = 0
        self.currency_amount = currency_amount
        self.is_aggro = False
        self.aggro_range = 300      # distance at which enemy notices player
        self.patrol_direction = 1   # 1 for right, -1 for left
    
    # Check if the player is within aggro range and update the enemy's aggro status accordingly.
    def check_aggro(self, player):
        distance = abs(self.rect.centerx - player.rect.centerx)
        self.is_aggro = distance < self.aggro_range

    # Simple patrol behaviour: moves in one direction until it hits a wall, then turns around.
    # Default movement until the player is in aggro range.
    def patrol(self, tiles):
        self.vel_x = self.speed * self.patrol_direction
        # Reverse direction on wall collision
        for tile in tiles:
            if self.rect.colliderect(tile):
                if self.vel_x > 0:
                    self.patrol_direction = -1
                elif self.vel_x < 0:
                    self.patrol_direction = 1

    # Simple chase behaviour: moves towards the player when they are in aggro range.
    def chase(self, player):
        if player.rect.centerx < self.rect.centerx:
            self.vel_x = -self.speed
        else:
            self.vel_x = self.speed
    
    # Checks if the enemy can attack the player, based on collision and attack cooldowns.
    # Applies damage to the player if the attack is successful.
    def attack(self, player):
        now = pygame.time.get_ticks()
        if self.rect.colliderect(player.rect):
            if now - self.last_attack > self.attack_cd:
                player.take_damage(self.damage)
                self.last_attack = now
    
    def drop_currency(self):
        return self.currency_amount  # return amount to add to player's total
    
    # Method to be called within the main game loop to update the enemy's behaviour and state.
    # Checks for aggro, updates movement based on patrol or chase behaviour and attacks the player if in range.
    def update(self, dt, tiles, player):
        self.check_aggro(player)
        if self.is_aggro:
            self.chase(player)
        else:
            self.patrol(tiles)
        self.apply_gravity(dt)
        self.move(dt, tiles)
        self.attack(player)

    def draw(self, screen, camera_x, show_health=False):
        super().draw(screen, camera_x, (255, 0, 0))  # red for enemies
        if show_health:
            bar_width = self.rect.w
            bar_x = self.rect.x - camera_x
            bar_y = self.rect.y - 12
            # Background
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, 8))
            # Health
            health_ratio = self.health / self.max_health
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, int(bar_width * health_ratio), 8))
            # Border
            pygame.draw.rect(screen, (255, 255, 255), (bar_x, bar_y, bar_width, 8), 1)
