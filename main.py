import pygame
import random
import math


WIDTH, HEIGHT = 1000, 1000
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pouchy's Lore")
floorImage = pygame.image.load('floorImage1.png')
floorImage = pygame.transform.scale(floorImage, (WIDTH, HEIGHT))

PLAYER_WIDTH = 75
PLAYER_HEIGHT = 75
PLAYER_VEL = 4
playerImage = pygame.image.load('playerImage.jpg')
movDir = pygame.math.Vector2(0, 0)

enemyNumber = 3
enemyWidth = 100
enemyHeight = 100
enemyImage = pygame.image.load('enemyImage.jpg')

bulletWidth = 10
bulletHeight = 10

wallHeight = 200
wallWidth = 400

currentLevel = 0

borderLines = []
enemies = []
bullets = []
levels = []

class Level:
    def __init__(self,number,enemyCount,playerStartPos,roomType,enemyDiff,levels):
        levels.append(self)
        self.number = number
        self.playerStartPos = playerStartPos
        self.enemyCount = enemyCount
        self.roomType = roomType
        self.enemyDiff = enemyDiff
    

class Bullet:
    def __init__(self, x, y, width, height, dir, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = dir
        self.vel = vel
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


class Player:
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = pygame.math.Vector2(-1, 0)
        self.vel = vel
        self.image = pygame.transform.scale(
            playerImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def basicPlayerMov(self, keys, movDir):

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
        if keys[pygame.K_UP] and self.y - PLAYER_VEL >= 0:
            self.y -= PLAYER_VEL
            movDir[0] = 0
            movDir[1] = 1

        return movDir

    def orientation(self, movDir):
        if movDir != [0, 0]:
            angle = self.dir.angle_to(movDir)
            self.dir = movDir.copy()
            rotatedImage = pygame.transform.rotate(self.image, angle)
            self.image = rotatedImage
            self.rect = rotatedImage.get_rect(center=self.rect.center)

    def collision(self, enemies, wall, playerXPrev, playerYPrev, borderLines):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.x = WIDTH/2 - PLAYER_WIDTH/2
                self.y = HEIGHT/2 - PLAYER_HEIGHT
        if self.rect.colliderect(wall) or self.rect.collidelistall(borderLines):
            self.x = playerXPrev
            self.y = playerYPrev


class Enemy:
    def __init__(self, x, y, width, height, vel, enemies):
        enemies.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = pygame.math.Vector2(-1, 0)
        self.vel = vel
        self.image = pygame.transform.scale(
            enemyImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class BorderLine:

    def __init__(self, x, y, width, height, borderLines):
        borderLines.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)


def draw(player, wall, enemies, bullets, borderLines):  # dessine chaque element de la scene
    WIN.blit(floorImage, WIN.get_rect())
    for borderLine in borderLines:
        pygame.draw.rect(WIN, "red", borderLine.rect)
    pygame.draw.rect(WIN, "green", wall)
    WIN.blit(player.image, player.rect)
    for bullet in bullets:
        pygame.draw.rect(WIN, "yellow", bullet)
    for enemy in enemies:
        WIN.blit(enemy.image, enemy.rect)
    pygame.display.update()


def enemyDirection(self, player):  # vecteur de direction de l'enemy
    dirvect = pygame.math.Vector2(player.x - self.x,
                                  player.y - self.y)
    if dirvect != [0, 0]:
        dirvect.normalize()
        return dirvect


def enemyEnemyCollisionAndMov(self, enemies, dirvect, player):
    if dirvect != [0, 0] and dirvect is not None:
        for enemy in enemies:
            if abs((enemy.rect.x+enemyWidth)-(self.rect.x+enemyWidth)) < enemyWidth and abs((enemy.rect.y+enemyHeight)-(self.rect.y+enemyHeight)) < enemyHeight and self != enemy:
                if math.hypot(enemy.rect.x-player.x, enemy.rect.y-player.y) < math.hypot(self.rect.x-player.x, self.rect.y-player.y):
                    dirvect.scale_to_length(4)
                    self.rect.move_ip(-dirvect)
                else:
                    dirvect.scale_to_length(enemy.vel)
                    self.rect.move_ip(dirvect)
                    return
        dirvect.scale_to_length(enemy.vel)
        self.rect.move_ip(dirvect)
        return


def enemyWallCollision(enemy, wall, enemies, player):
    x, y = enemy.rect.center

    distMurGauche = abs(wall.x - (enemy.rect.x+enemy.width))
    distMurDroit = abs((wall.x+wallWidth) - enemy.rect.x)
    distMurHaut = abs(wall.y - (enemy.rect.y+enemy.height))
    distMurBas = abs((wall.y+wallHeight) - enemy.rect.y)

    enemyEnemyCollisionAndMov(
        enemy, enemies, enemyDirection(enemy, player), player)

    if enemy.rect.colliderect(wall):
        if distMurGauche < distMurBas and distMurGauche < distMurHaut:  # mur gauche
            enemy.rect.x -= distMurGauche
            if player.y > y:
                enemy.rect.y += enemy.vel/2
            else:
                enemy.rect.y -= enemy.vel/2

        elif distMurDroit < distMurBas and distMurDroit < distMurHaut:  # mur droit
            enemy.rect.x += abs(wall.x+wallWidth - enemy.rect.x)
            if player.y > y:
                enemy.rect.y += enemy.vel/2
            else:
                enemy.rect.y -= enemy.vel/2

        elif distMurHaut < distMurDroit and distMurHaut < distMurGauche:  # mur haut
            enemy.rect.y -= abs(wall.y - (enemy.rect.y+enemy.height))
            if player.x > x:
                enemy.rect.x += enemy.vel/2
            else:
                enemy.rect.x -= enemy.vel/2

        elif distMurBas < distMurDroit and distMurBas < distMurGauche:  # mur bas
            enemy.rect.y += abs(wall.y+wallHeight - enemy.rect.y)
            if player.x > x:
                enemy.rect.x += enemy.vel/2
            else:
                enemy.rect.x -= enemy.vel/2

def levelManager(levels,enemies):
    global gameOver,currentLevel,player
    if enemies == []:
        gameOver = True
        if currentLevel != len(levels)-1:
            currentLevel = currentLevel + 1
            enemySpawner(enemies,levels,currentLevel)
            player.x,player.y = levels[currentLevel].playerStartPos


def playerBulletsInit(player, bullets):
    global bullet
    bullet = Bullet(player.x+PLAYER_WIDTH/2-bulletWidth/2,
                    player.y+PLAYER_HEIGHT/2-bulletHeight/2, 10, 10, 0, 4)
    bullets.append(bullet)
    return bullets


def playerWeapon(player, bullets, enemies, wall, borderLines):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouseDir = pygame.math.Vector2(player.x - mouse_x,
                                   player.y - mouse_y)
    mouseDir.scale_to_length(7)
    for bullet in bullets:
        if bullet.rect.colliderect(wall) or bullet.rect.collidelistall(borderLines) or bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
            bullets.remove(bullet)
            print('uwu')
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


def enemyXYSync(enemy):
    enemy.x = enemy.rect.x
    enemy.y = enemy.rect.y

def enemySpawner(enemies,levels,currentLevel):
    for i in range(levels[currentLevel].enemyCount):
        enemyX = random.choice([i for i in range(WIDTH)])
        Enemy(enemyX, 0, enemyWidth, enemyHeight, 3, enemies)


def main():
    run = True

    clock = pygame.time.Clock()

    BorderLine(100, 101, 10, 786, borderLines)
    BorderLine(100, 887, 800, 10, borderLines)
    BorderLine(101, 101, 799, 10, borderLines)
    BorderLine(888, 102, 10, 796, borderLines)

    Level(0,5,(500,500),1,1,levels)
    Level(1,10,(400,400),1,2,levels)
    Level(2,15,(300,300),1,3,levels)

    global player
    player = Player(levels[currentLevel].playerStartPos[0], levels[currentLevel].playerStartPos[1],
            PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL)
        
    wall = pygame.Rect(1000, 2000, wallWidth, wallHeight)

    attackSpeed = 30
    attackSpeedIncrement = 0

    gameOver = True


    
    # fait spawn les noobies
    
    enemySpawner(enemies,levels,currentLevel)
    
    while run:  # --------------------------------------------------------------------------------------------------------------------------#
        
        # tick par seconde du gaming

        clock.tick(60)

        

        
                

        # variable qui definie la position du joueur

        playerXPrev = player.x
        playerYPrev = player.y

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # deplacement du joueur (voir class Player)

        keys = pygame.key.get_pressed()
        player.basicPlayerMov(keys, movDir)
        playerXYSync(player)

        # sync du sprite et de la hit box des enemies

        for enemy in enemies:
            enemyXYSync(enemy)

        # collision du mur avec le joueur UwU

        for enemy in enemies:
            enemyWallCollision(enemy, wall, enemies, player)

        # bullet firing

        if True:
            attackSpeedIncrement += clock.get_fps()/attackSpeed
            if attackSpeedIncrement >= clock.get_fps() and clock.get_fps() != 0:
                print(clock.get_fps())
                attackSpeedIncrement = 0
                playerBulletsInit(player, bullets)
            playerWeapon(player, bullets, enemies, wall, borderLines)

        # entity orientation

        player.collision(enemies, wall, playerXPrev, playerYPrev, borderLines)
        player.orientation(movDir)

        #level management

        levelManager(levels,enemies)

        # object rendering

        draw(player, wall, enemies, bullets, borderLines)

    pygame.quit()


if __name__ == "__main__":
    main()
