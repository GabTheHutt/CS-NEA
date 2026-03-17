import pygame
from Login import *
from Boxes import *
from Menu import *

#----Pygame setup
pygame.init()
pygame.key.set_repeat(300, 80) #Sets delay from holding key to repeat and the speed of repeating
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("The Cowboy Knight")
running= True #Returns True once the player logs in successfully
font= pygame.font.Font(None, 36)

#----Main loop
while running is True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    Main()

pygame.quit()
cursor.close()
conn.close()
