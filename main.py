import pygame
import random
import math



WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UwU")

list_sec = list(range(1, 301))



x = random.choice(list_sec)
y = random.choice(list_sec)
z = random.choice(list_sec)
v = random.choice(list_sec)

print(x)
print(y)
print(z)
print(v)


AXE_4 = int(v)
AXE_3 = int(z)
AXE_2 = int(y)
AXE_1 = int(x)

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_VEL = 5

enemyNumber = 100
enemyWidth = 30
enemyHeight = 30

def draw(player, wall, enemies, bullets):
    WIN.fill('black')
    pygame.draw.rect(WIN, "green", wall)
    pygame.draw.rect(WIN, "red", player)
    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)
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

def playerBulletsLogic (player,bullets):
     global bullet
     bullet = pygame.Rect(player.x,player.y,10,10)
     bullets.append(bullet)
     return bullets


def playerWeapon (player,bullets,enemy):
    playerDir = pygame.math.Vector2(player.x - (player.x+PLAYER_WIDTH),
                                    player.y - (player.y+PLAYER_HEIGHT))
    playerDir.scale_to_length(7)
    for bullet in bullets:
        print(bullet)
        #for enemy in enemies:
        if bullet.colliderect(enemy) or bullet.colliderect(player) or bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y <0 :
            del bullet
        bullet.move_ip(playerDir)

     
    
                     

def main():
    run = True

    player = pygame.Rect(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    wall = pygame.Rect(AXE_1,AXE_2,AXE_3,AXE_4)
    enemy = pygame.Rect(0,0,30,30)
    enemies = []
    bullets = []
    clock = pygame.time.Clock()

    for i in range(enemyNumber):
             enemyX = random.choice([i for i in range(WIDTH)])
             enemy = pygame.Rect(enemyX,0,enemyWidth,enemyHeight)
             enemies.append(enemy)

    while run:
        clock.tick(40)

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
        playerBulletsLogic(player,bullets)
        playerWeapon(player,bullets,enemy)
        draw(player, wall, enemies, bullets)
        
    
    pygame.quit()

if __name__ == "__main__":
    main()
