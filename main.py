import pygame
import random
import math
import time



WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UwU")

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_VEL = 5

enemyNumber = 300
enemyWidth = 30
enemyHeight = 30

def draw(player, wall, enemies):
    WIN.fill('black')
    pygame.draw.rect(WIN, "green", wall)
    pygame.draw.rect(WIN, "red", player)
    for enemy in enemies:
        pygame.draw.rect(WIN, "blue", enemy)
    pygame.display.update()

def enemyDirection(self, player):
            dirvect = pygame.math.Vector2(player.x - self.x,
                                        player.y - self.y)
            if dirvect != [0,0]:
                dirvect.normalize()
                return dirvect

def enemyCollision(self,enemies,dirvect,player):
    if dirvect != [0,0] and dirvect is not None :
        for enemy in enemies:
                    if player.colliderect(enemy):
                         player.x = WIDTH/2 - PLAYER_WIDTH/2
                         player.y = HEIGHT/2 - PLAYER_HEIGHT
                    if abs((enemy.x+enemyWidth)-(self.x+enemyWidth))<30 and abs((enemy.y+enemyHeight)-(self.y+enemyHeight))<30 and self != enemy:
                        if math.hypot(enemy.x-player.x, enemy.y-player.y) < math.hypot(self.x-player.x, self.y-player.y):
                            print("collision")
                            dirvect.scale_to_length(4)
                            self.move_ip(-dirvect)
                        else:
                            dirvect.scale_to_length(3)
                            self.move_ip(dirvect)
                            return
        dirvect.scale_to_length(3)
        self.move_ip(dirvect)
        return
    
                     

def main():
    run = True

    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    wall = pygame.Rect(200,200,50,500)
    enemy = pygame.Rect(0,0,30,30)
    enemies = []
    clock = pygame.time.Clock()

    for i in range(enemyNumber):
             enemyX = random.choice([i for i in range(WIDTH)])
             enemy = pygame.Rect(enemyX,0,enemyWidth,enemyHeight)
             enemies.append(enemy)

    while run:
        clock.tick(60)

        playerXPrev = player.x
        playerYPrev = player.x
#        enemyXPrev  = enemy.x
#        enemyXPrev  = enemy.x

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break\
                
        #collision du mur avec le joueur 
        if player.colliderect(wall):
            player.x = playerXPrev
            player.y = playeryPrev
    
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            player.x += PLAYER_VEL
        if keys[pygame.K_DOWN] and player.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            player.y += PLAYER_VEL
        if keys[pygame.K_UP]  and player.y - PLAYER_VEL >= 0:
            player.y -= PLAYER_VEL

        print("----")
        for enemy in enemies:
            enemyCollision(enemy,enemies,enemyDirection(enemy,player),player)
        draw(player, wall, enemies)
        
    
    pygame.quit()

if __name__ == "__main__":
    main()
