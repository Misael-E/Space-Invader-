import random
import math
from pygame import mixer
import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('spaceship.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerXChanged = 0
playerYChanged = 0

background = pygame.image.load('background.jpg')
mixer.music.load('backgroundSong.mp3')
mixer.music.play(-1)

enemyImg = []
enemyX = []
enemyY = []
enemyXChanged = []
enemyYChanged = []
numOfEnemies = 6

for i in range(numOfEnemies):
    enemyImg.append(pygame.image.load('ufo.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyXChanged.append(2)
    enemyYChanged.append(40)

bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletYChanged = 5
bulletState = "ready"

score = 0
font = pygame.font.Font('freesansbold.ttf', 20)

textX = 10
textY = 10

gameOverFont = pygame.font.Font('freesansbold.ttf', 64)


def gameOverText():
    gameOverText = gameOverFont.render("GAME OVER!", True, (255, 0, 0))
    screen.blit(gameOverText, (200, 250))


def scoreView(x, y):
    scoreShow = font.render("Score : " + str(score), True, (255, 0, 0))
    screen.blit(scoreShow, (x, y))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


# Bullet shot
def fire(x, y):
    global bulletState
    bulletState = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


# Checks for collision
def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2) + math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    # Player movement
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerXChanged = -3
            if event.key == pygame.K_RIGHT:
                playerXChanged = 3
            if event.key == pygame.K_SPACE:
                if bulletState is "ready":
                    bulletSound = mixer.Sound("pew.wav")
                    bulletSound.play()
                    bulletX = playerX
                    fire(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerXChanged = 0

    # Player bounds
    playerX += playerXChanged
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy movement and spawn
    for i in range(numOfEnemies):

        if enemyY[i] > 440:
            for j in range(numOfEnemies):
                enemyY[j] = 2000
            gameOverText()
            break

        enemyX[i] += enemyXChanged[i]
        if enemyX[i] <= 0:
            enemyXChanged[i] = 2
            enemyY[i] += enemyYChanged[i]
        elif enemyX[i] >= 736:
            enemyXChanged[i] = -2
            enemyY[i] += enemyYChanged[i]

        # Collisions
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explodeSound = mixer.Sound("explode.wav")
            explodeSound.play()
            bulletY = 480
            bulletState = "ready"
            score += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    # Bullet movement
    if bulletY <= 0:
        bulletY = 480
        bulletState = "ready"

    if bulletState is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletYChanged

    player(playerX, playerY)
    scoreView(textX, textY)
    pygame.display.update()
