import pygame
import random
import math


WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("UwU")

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_VEL = 5
playerImage = pygame.image.load('Trollface.jpg')
movDir = pygame.math.Vector2(0,0)

enemyNumber = 3
enemyWidth = 60
enemyHeight = 60
enemyImage = pygame.image.load('axel.jpg')

bulletWidth = 10
bulletHeight = 10



class Bullet:
    def __init__(self,x,y,width,height,dir,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = dir
        self.vel = vel
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)

class Player:
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = pygame.math.Vector2(-1,0)
        self.vel = vel
        self.image = pygame.transform.scale(playerImage,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        
    
    def basicPlayerMov(self,keys,movDir):    

        if keys[pygame.K_LEFT] and self.x - PLAYER_VEL >= 0:
            self.x -= PLAYER_VEL
            movDir[0] = -1
            movDir[1] = 0
        if keys[pygame.K_RIGHT] and self.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH:
            self.x += PLAYER_VEL
            movDir[0] = 1
            movDir[1] = 0
        if keys[pygame.K_DOWN] and self.y + PLAYER_VEL + PLAYER_HEIGHT <= HEIGHT:
            self.y += PLAYER_VEL
            movDir[0] = 0
            movDir[1] = -1
        if keys[pygame.K_UP]  and self.y - PLAYER_VEL >= 0:
            self.y -= PLAYER_VEL
            movDir[0] = 0
            movDir[1] = 1

        return movDir
         
    def orientation(self,movDir):
        if movDir != [0,0]:
            angle = self.dir.angle_to(movDir)
            self.dir = movDir.copy()
            rotatedImage = pygame.transform.rotate(self.image,angle)
            self.image = rotatedImage
            self.rect = rotatedImage.get_rect(center=self.rect.center)

class Enemy:
    def __init__(self,x,y,width,height,vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = pygame.math.Vector2(-1,0)
        self.vel = vel
        self.image = pygame.transform.scale(enemyImage,(self.width,self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
    

def draw(player, wall, enemies, bullets):   #dessine chaque element de la scene
    WIN.fill('black')
    pygame.draw.rect(WIN, "green", wall)
    WIN.blit(player.image,player.rect)
    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)
    for enemy in enemies:
        WIN.blit(enemy.image,enemy.rect)
    pygame.display.update()

def enemyDirection(self, player):                               #vecteur de direction de l'enemy
            dirvect = pygame.math.Vector2(player.x - self.x,
                                        player.y - self.y)
            if dirvect != [0,0]:
                dirvect.normalize()
                return dirvect
            

def enemyCollision(self,enemies,dirvect,player):        
    if dirvect != [0,0] and dirvect is not None :
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                    player.x = WIDTH/2 - PLAYER_WIDTH/2
                    player.y = HEIGHT/2 - PLAYER_HEIGHT
            if abs((enemy.x+enemyWidth)-(self.x+enemyWidth))<30 and abs((enemy.y+enemyHeight)-(self.y+enemyHeight))<30 and self != enemy:
                if math.hypot(enemy.x-player.x, enemy.y-player.y) < math.hypot(self.x-player.x, self.y-player.y):
                    dirvect.scale_to_length(4)
                    self.rect.move_ip(-dirvect)
                    print("collision")
                else:
                    dirvect.scale_to_length(3)
                    self.rect.move_ip(dirvect)
                    return
        dirvect.scale_to_length(3)
        self.rect.move_ip(dirvect)
        return
    

def playerBulletsInit (player,bullets):            
     global bullet
     bullet = Bullet(player.x+PLAYER_WIDTH/2-bulletWidth/2,player.y+PLAYER_HEIGHT/2-bulletHeight/2,10,10,0,4)
     bullets.append(bullet)
     return bullets


def playerWeapon (player,bullets,enemies,wall):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouseDir = pygame.math.Vector2(player.x - mouse_x,
                                    player.y - mouse_y)
    mouseDir.scale_to_length(7)
    for bullet in bullets:
        if bullet.rect.colliderect(wall) or bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y <0:
                bullets.remove(bullet)
        for enemy in enemies:
            if bullet.rect.colliderect(enemy.rect) and bullet in bullets:
                bullets.remove(bullet)
                enemies.remove(enemy)
        if bullet.dir == 0:
             bullet.dir = -mouseDir
        bullet.rect.move_ip(bullet.dir)

def playerXYSync(player):
     player.rect.x = player.x
     player.rect.y = player.y

     
    
                     

def main():
    run = True

    player = Player(WIDTH/2 - PLAYER_WIDTH/2, HEIGHT/2 - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT,PLAYER_VEL)   #taille de chaque objet de la scene
    wall = pygame.Rect(100,100,100,100)
    #enemy = pygame.Rect(0,0,30,30)
    enemies = []
    bullets = []

    clock = pygame.time.Clock()

    attackSpeed = 60
    attackSpeedIncrement = 0

    enemySpawnIncrement = 0
    enemySpawnRate = 4

    while run: #--------------------------------------------------------------------------------------------------------------------------#

        #tick par seconde du gaming

        clock.tick(60)          

        #fait spawn les noobies

        enemySpawnIncrement += enemySpawnRate
        if enemySpawnIncrement >= 1000:
            enemySpawnRate += 0.01
            enemySpawnIncrement = 0
            for i in range(enemyNumber):               
                    enemyX = random.choice([i for i in range(WIDTH)])
                    enemy = Enemy(enemyX,0,enemyWidth,enemyHeight,3)
                    enemies.append(enemy)

        #variable qui definie la position du joueur 

        playerXPrev = player.x  
        playerXPrev = playerXPrev    
        playerYPrev = player.x
        playerYPrev = playerYPrev

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        
        #deplacement du joueur (voir class Player)
        keys = pygame.key.get_pressed()
        player.basicPlayerMov(keys,movDir)
        playerXYSync(player)

        #collision du mur avec le joueur UwU
        
        if player.rect.colliderect(wall):
            player.x = playerXPrev
            player.y = playerYPrev    

        for enemy in enemies:
            enemyCollision(enemy,enemies,enemyDirection(enemy,player),player)
            
        #bullet firing

        attackSpeedIncrement += clock.get_fps()/attackSpeed
        if attackSpeedIncrement >= clock.get_fps() and clock.get_fps() != 0:
            print(clock.get_fps())
            attackSpeedIncrement = 0
            playerBulletsInit(player,bullets)
        playerWeapon(player,bullets,enemies,wall)

        #entity orientation

        player.orientation(movDir)

        #object rendering

        draw(player, wall, enemies, bullets)
    
    pygame.quit()

if __name__ == "__main__":
    main()