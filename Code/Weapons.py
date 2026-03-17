import pygame

# Weapon classes 
# The super class containing the base attributes for the melee and ranged weapons to inherit from.
# Contains the basic attack cooldown logic and equip/unequip methods.
class Weapon:
    def __init__(self, name, damage, cooldown):
        self.name = name
        self.damage = damage
        self.cooldown = cooldown        # milliseconds between attacks
        self.last_attack = 0
        self.equipped = False

    # Checks if enough time has passed since the last attack to allow attacking again
    def can_attack(self):
        return pygame.time.get_ticks() - self.last_attack > self.cooldown

    def attack(self):
        if self.can_attack():
            self.last_attack = pygame.time.get_ticks()
            return True
        return False  # on cooldown

    def equip(self):
        self.equipped = True

    def unequip(self):
        self.equipped = False

# Melee weapon class, inherits from Weapon and adds a reach attribute and hitbox calculation for melee attacks
class MeleeWeapon(Weapon):
    def __init__(self, name, damage, cooldown, reach):
        super().__init__(name, damage, cooldown)
        self.reach = reach  # how far in front of player the hitbox extends

    # Calculates the hitbox for a melee attack based on the player's position and facing direction
    def get_hitbox(self, player_rect, facing_right):
        if facing_right:
            return pygame.Rect(player_rect.right,player_rect.y,
                self.reach,player_rect.h)
        # If facing left, the hitbox extends to the left of the player
        else:
            return pygame.Rect(player_rect.left - self.reach,player_rect.y,
                self.reach,player_rect.h)
        
    # Overrides the attack method to also check for collisions with enemies and apply damage
    def attack(self, player_rect, facing_right, enemies):
        if super().attack():
            hitbox = self.get_hitbox(player_rect, facing_right)
            for enemy in enemies:
                if hitbox.colliderect(enemy.rect):
                    enemy.take_damage(self.damage)
            return hitbox  # return hitbox so it can be drawn briefly
        return None

# Ranged weapon class, inherits from Weapon 
# Adds attributes for bullet speed and ammo, as well as a method to spawn bullets when attacking
class RangedWeapon(Weapon):
    def __init__(self, name, damage, cooldown, bullet_speed, max_ammo):
        super().__init__(name, damage, cooldown)
        self.bullet_speed = bullet_speed
        self.max_ammo = max_ammo
        self.ammo = max_ammo

    def reload(self):
        self.ammo = self.max_ammo

    # Overrides the attack method to spawn a bullet if the weapon is not on cooldown and has ammo
    def attack(self, player_rect, facing_right, bullets):
        if super().attack() and self.ammo > 0:
            self.ammo -= 1
            # Spawn bullet at player centre
            bullet = Bullet(player_rect.centerx, player_rect.centery,
                self.bullet_speed,self.damage,facing_right)
            bullets.append(bullet)
            return True
        return False

# Bullet class for the projectiles fired by ranged weapons
# Contains attributes for position, speed, damage, direction, and active state
# Methods to update position and check for collisions with tiles and enemies.
class Bullet:
    def __init__(self, x, y, speed, damage, facing_right):
        self.rect = pygame.Rect(x, y, 10, 5)
        self.speed = speed
        self.damage = damage
        self.direction = 1 if facing_right else -1
        self.active = True

    def update(self, dt, tiles, enemies):
        self.rect.x += self.speed * self.direction * dt
        # Deactivate on tile collision
        for tile in tiles:
            if self.rect.colliderect(tile):
                self.active = False
                return
        # Deactivate and deal damage on enemy collision
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                enemy.take_damage(self.damage)
                self.active = False
                return

    def draw(self, screen, camera_x):
        if self.active:
            pygame.draw.rect(screen, (255, 255, 0),
                pygame.Rect(self.rect.x - camera_x, self.rect.y, self.rect.w, self.rect.h))