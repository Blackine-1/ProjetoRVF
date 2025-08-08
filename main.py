
import pygame

pygame.init()
screen = pygame.display.set_mode((600, 500))
clock = pygame.time.Clock()
running = True

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    
    screen.fill("black")

    pygame.display.flip()

    clock.tick(15)  

pygame.quit()