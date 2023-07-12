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
playerImage = pygame.image.load('perso 2.png')
movDir = pygame.math.Vector2(0, 0)

enemyNumber = 3
enemyWidth = 100
enemyHeight = 100
enemyImage = pygame.image.load('enemyImage.jpg')
dashImage = pygame.image.load('sprite_image.png')

bulletWidth = 10
bulletHeight = 10
imagemur = pygame.image.load('mur test 2.jpg')
wallHeight = 500
wallWidth = 400

dash_distance = 35
cooldown = 3
can_dash = True
last_dash_time = pygame.time.get_ticks()


currentLevel = 0

borderLines = []
enemies = []
bullets = []
levels = []
walls = []
playerAnimations = []

currentAnim = 'idle'
playerRunAnimation = [pygame.image.load('frame1.png'), pygame.image.load('frame2.png'), pygame.image.load('frame3.png'), pygame.image.load('frame4.png'), pygame.image.load('frame5.png')
 ]

for i in range(0,len(playerRunAnimation)):
    playerRunAnimation[i] = pygame.transform.scale(playerRunAnimation[i],(PLAYER_WIDTH,PLAYER_HEIGHT))


playerAnimations.append(playerRunAnimation)

class Level:
    def __init__(self, number, enemyCount, playerStartPos, roomType, enemyDiff, levels):
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
        self.image = pygame.transform.scale(playerImage, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.currentSprite = 0
        self.anim = 'idle'
        self.animCooldown = 100
        self.animCooldownIncrement = 0

    def drawDashImage(self, surface):
        if not can_dash:
            surface.blit(dashImage, (self.x, self.y))

    def basicPlayerMov(self, keys, movDir):
        global can_dash
        global last_dash_time
        if keys[pygame.K_LEFT] and self.x - self.vel >= 0:
            tempRect = self.rect.copy()
            tempRect.x -= self.vel
            if tempRect.collidelistall(borderLines) == [] and tempRect.collidelistall(walls) == []:
                self.x -= self.vel
                movDir[0] = -1
                movDir[1] = 0
                self.anim = 'run left'
        if keys[pygame.K_RIGHT] and self.x + self.vel + self.width <= WIDTH:
            tempRect = self.rect.copy()
            tempRect.x += self.vel
            if tempRect.collidelistall(borderLines) == [] and tempRect.collidelistall(walls) == []:
                self.x += self.vel
                movDir[0] = 1
                movDir[1] = 0
                self.anim = 'run right'
        if keys[pygame.K_DOWN] and self.y + self.vel + self.height <= HEIGHT:
            tempRect = self.rect.copy()
            tempRect.y += self.vel
            if tempRect.collidelistall(borderLines) == [] and tempRect.collidelistall(walls) == []:
                self.y += self.vel
                movDir[0] = 0
                movDir[1] = 1
                self.anim = 'run down'
        if keys[pygame.K_UP] and self.y - self.vel >= 0:
            tempRect = self.rect.copy()
            tempRect.y -= self.vel
            if tempRect.collidelistall(borderLines) == [] and tempRect.collidelistall(walls) == []:
                self.y -= self.vel
                movDir[0] = 0
                movDir[1] = -1
                self.anim = 'run up'
        
        

        # DASH :3
        if False:
            if keys[pygame.K_SPACE] and can_dash:
                if pygame.time.get_ticks() - last_dash_time >= cooldown * 1000 and 0 < self.x + movDir[0] * self.vel * dash_distance < WIDTH and 0 < self.y + movDir[1] * self.vel * dash_distance < HEIGHT:
                    self.x += movDir[0] * self.vel * dash_distance
                    self.y += movDir[1] * self.vel * dash_distance
                    last_dash_time = pygame.time.get_ticks()
                    can_dash = False
                else:
                    can_dash = True


    def orientation(self, movDir):
        if movDir != [0, 0]:
            angle = self.dir.angle_to(movDir)
            self.dir = movDir.copy()
            rotatedImage = pygame.transform.rotate(self.image, angle)
            self.image = rotatedImage
            self.rect = rotatedImage.get_rect(center=self.rect.center)

    def collision(self, enemies):
        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.x = WIDTH/2 - PLAYER_WIDTH/2
                self.y = HEIGHT/2 - PLAYER_HEIGHT

    def animation(self,playerAnimations):
        self.animCooldownIncrement += 10

        if self.anim == 'idle' and self.animCooldownIncrement >= self.animCooldown:
            self.animCooldownIncrement = 0

            self.currentSprite += 1
            if self.currentSprite >= len(playerAnimations[0]):
                self.currentSprite = 0

            self.image = playerAnimations[0][self.currentSprite]

class Enemy:
    def __init__(self, x, y, width, height, vel, enemies):
        enemies.append(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.dir = pygame.math.Vector2(-1, 0)
        self.vel = vel
        self.image = pygame.transform.scale(enemyImage, (self.width, self.height))
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

def draw(player, walls, enemies, bullets, borderLines):
    WIN.blit(imagemur, WIN.get_rect())

    for wall in walls:
        pygame.draw.rect(WIN, "green", wall)

    WIN.blit(player.image, player.rect)

    for bullet in bullets:
        pygame.draw.rect(WIN,"yellow", bullet.rect)

    for enemy in enemies:
        WIN.blit(enemy.image, enemy.rect)

    if False:
        for borderLine in borderLines:
            pygame.draw.rect(WIN, "red", borderLine.rect)

    pygame.display.update()

def enemyDirection(self, player):
    dirvect = pygame.math.Vector2(player.x - self.x, player.y - self.y)
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

def enemyWallCollision(enemy, walls, enemies, player):
    x, y = enemy.rect.center
    for wall in walls:
        distMurGauche = abs(wall.x - (enemy.rect.x+enemy.width))
        distMurDroit = abs((wall.x+wallWidth) - enemy.rect.x)
        distMurHaut = abs(wall.y - (enemy.rect.y+enemy.height))
        distMurBas = abs((wall.y+wallHeight) - enemy.rect.y)
        enemyEnemyCollisionAndMov(enemy, enemies, enemyDirection(enemy, player), player)

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

def levelManager(levels, enemies):
    global gameOver, currentLevel, player
    if enemies == [] and player.x >700 and player.y >500:
        gameOver = True
        if currentLevel != len(levels)-1:
            currentLevel = currentLevel + 1
            enemySpawner(enemies, levels, currentLevel)

def playerBulletsInit(player, bullets):
    global bullet
    bullet = Bullet(player.x+PLAYER_WIDTH/2-bulletWidth/2, player.y+PLAYER_HEIGHT/2-bulletHeight/2, 10, 10, 0, 4)
    bullets.append(bullet)
    return bullets

# pipipi

def playerWeapon(player, bullets, enemies, walls, borderLines):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    mouseDir = pygame.math.Vector2(player.x - mouse_x, player.y - mouse_y)
    mouseDir.scale_to_length(7)
    for bullet in bullets:
        if bullet.rect.collidelistall(walls) or bullet.rect.collidelistall(borderLines) or bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:
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

def enemyXYSync(enemy):
    enemy.x = enemy.rect.x
    enemy.y = enemy.rect.y

def enemySpawner(enemies, levels, currentLevel):
    for i in range(levels[currentLevel].enemyCount):
        enemyX = random.choice([i for i in range(WIDTH)])
        Enemy(enemyX, 0, enemyWidth, enemyHeight, 3, enemies)

def main():
    run = True
    clock = pygame.time.Clock()
    
    BorderLine( 87 , 101 , 10 , 804 ,borderLines)
    BorderLine( 98 , 903 , 804 , 10 ,borderLines)
    BorderLine( 906 , 100 , 10 , 804 ,borderLines)
    BorderLine( 97 , 87 , 809 , 10 ,borderLines)

    Level(0, 5, (500, 500), 1, 1, levels)
    Level(1, 10, (400, 400), 1, 2, levels)
    Level(2, 15, (300, 300), 1, 3, levels)

    global player
    player = Player(levels[currentLevel].playerStartPos[0], levels[currentLevel].playerStartPos[1], PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_VEL)

    
    walls.append(pygame.Rect(1000, 2000, wallWidth, wallHeight))

    attackSpeed = 30
    attackSpeedIncrement = 0
    gameOver = True

    # fait spawn les noobies

    enemySpawner(enemies, levels, currentLevel)
    while run:
        
        # tick par seconde du gaming

        clock.tick(60)
        
        player.anim = 'idle'

        # variable qui definie la position du joueur

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
            enemyWallCollision(enemy, walls, enemies, player)

        # bullet firing

        if True:
            attackSpeedIncrement += clock.get_fps()/attackSpeed
            if attackSpeedIncrement >= clock.get_fps() and clock.get_fps() != 0:
                print(clock.get_fps())
                print(player.anim)
                attackSpeedIncrement = 0
                playerBulletsInit(player, bullets)
            playerWeapon(player, bullets, enemies, walls, borderLines)

        # entity orientation

        player.collision(enemies)
        player.orientation(movDir)

        # level management

        levelManager(levels, enemies)

        # object rendering
        player.animation(playerAnimations)
        draw(player, walls, enemies, bullets, borderLines)

    pygame.quit()


if __name__ == "__main__":
    main()
