import pygame
from Boxes import Button

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


class Menu_screen:
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