import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pouchy's Lore Level Editor")
grid = pygame.image.load('Frame_4casequadril.png')

def draw(rects):
    WIN.blit(grid,WIN.get_rect())
    for rect in rects:
        pygame.draw.rect(WIN,"red",rect)
    if pygame.font:
        font = pygame.font.Font(None, 36)
        text = font.render("mousPos: " + str(pygame.mouse.get_pos()), 1, (10, 10, 10))
        textpos = text.get_rect(centerx=WIN.get_width()/2)
        WIN.blit(text, textpos)
    pygame.display.update()

x_1 = 0
y_1 = 0

rects = []

def levelEditor(mouseXY):
    global x_1
    global y_1
    if x_1 != 0 and y_1 != 0:
            print('Uwu')
            if abs(mouseXY[0]-x_1) > abs(mouseXY[1]-y_1):
                rect = pygame.Rect(x_1,y_1,abs(mouseXY[0]-x_1),10)
                rects.append(rect)
                print(rects)
                x_1 = 0
                y_1 = 0
                return rects
            else:
                rect = pygame.Rect(x_1,y_1,10,abs(mouseXY[1]-y_1))
                rects.append(rect)
                print(rects)
                x_1 = 0
                y_1 = 0
                return rects

    if x_1 == 0 and y_1 == 0:
        x_1 = mouseXY[0]
        y_1 = mouseXY[1]
        print(x_1,y_1)
        return x_1,y_1
    
run = True
while run:

    mouseXY = pygame.mouse.get_pos()

    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                for rect in rects:
                    print("BorderLine(",str(rect.x),',',str(rect.y),',',str(rect.width),',',str(rect.height),',borderLines)')

            if event.type == pygame.MOUSEBUTTONDOWN:
                levelEditor(mouseXY)
                
                


    
    draw(rects)
pygame.quit()