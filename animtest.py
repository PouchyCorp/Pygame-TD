import pygame, sys

pygame.init()
clock = pygame.time.Clock()


screen_width = 800
screnn_height = 800
screen = pygame.display.set_mode((screen_width,screnn_height))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            

    pyagme.display.flip()
    clock.tick(60)
