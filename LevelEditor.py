import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pouchy's Lore Level Editor")

def draw():
    WIN.fill("white")
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("mousPos: " + str(pygame.mouse.get_pos()), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=WIN.get_width()/2)
        WIN.blit(text, textpos)
    pygame.display.update()

while True:

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                print("")


    
    draw()
