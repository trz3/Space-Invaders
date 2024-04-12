import pygame
from pygame import mixer
import random
import math

# Initialize pygame package (mandatory)
pygame.init()

# Create the screen using the set_mode with width x height
screenWidth = 800
screenHeight = 600
screen = pygame.display.set_mode((screenWidth, screenHeight))

# Title and Icon
pygame.display.set_caption('Space Invaders')

shipWidth = 64

# background



speed = 1.5
enemySpeed = 1
bulletSpeed = 10

# Player
playerImg = pygame.image.load('images/player.png')
playerX = 368  # (800 / 2) - (64 / 2) = 368 (half of the screen)
playerY = 480
playerX_change = 0

# Enemies Create several enemies inside a list
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('images/enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 200))
    enemyX_change.append(enemySpeed)
    enemyY_change.append(40)

# Bullet
bulletImg = pygame.image.load('images/bullet.png')
bulletX = 0
bulletY = playerY
bulletY_change = bulletSpeed
# ready - No bullet on screen
# fire - Bullet is moving
bulletState = "ready"

boundaryLeft = 0
boundaryRight = 800

# score
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

# game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


# player coordinates
def player(x, y):
    screen.blit(playerImg, (x, y))


# enemy coordinates
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bulletState
    bulletState = "fire"
    # start from the middle of the player ship
    screen.blit(bulletImg, (x + 16, y + 10))


def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    # distance = math.hypot(enemy_x - bullet_x, enemy_y - bullet_y)
    if distance < 27:
        return True
    else:
        return False


def show_score():
    # First render the test and then draw it on the screen
    score_render = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_render, (textX, textY))


def game_over_text():
    # First render the test and then draw it on the screen
    over_render = game_over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_render, (200, 250))


# listen for the QUIT event on the screen - infinite loop
running = True
while running:
    # screen background with a RGB value
    screen.fill((0, 128, 128))  # teal color
    # background image
    screen.blit(background, (0, 0))

    # everything that happens inside the game window, should be inside this infinite loop
    for event in pygame.event.get():
        # quit event
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed
        if event.type == pygame.KEYDOWN:
            # player spaceship: check whether is right or left
            if event.key == pygame.K_LEFT:
                playerX_change = -speed
            if event.key == pygame.K_RIGHT:
                playerX_change = speed
            if event.key == pygame.K_SPACE:
                if bulletState == "ready":
                    # get the current X coordinate of the player
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    # Player: boundary control for X axis
    if playerX < boundaryLeft:
        playerX = 0
    elif playerX > boundaryRight - shipWidth:
        playerX = boundaryRight - shipWidth

    # Bullet movement
    if bulletState == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    # Bullet reset on boundary
    if bulletY <= 0:
        bulletY = playerY
        bulletState = "ready"

    # detect which enemy
    for i in range(num_of_enemies):
        # Game over on enemy crossing boundary
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                # move all enemies outside of the screen
                enemyY[j] = 2000
            game_over_text()
            break

        # Enemy movement
        enemyX[i] += enemyX_change[i]

        # Enemy: boundary control for X and Y axis
        if enemyX[i] <= boundaryLeft:
            enemyX_change[i] = enemySpeed
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= boundaryRight - shipWidth:
            enemyX_change[i] = -enemySpeed
            enemyY[i] += enemyY_change[i]

        # collision
        collision = is_collision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            # reset bullet
            bulletY = playerY
            bulletState = "ready"
            # add score
            score += 1
            # reset enemy
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 200)

        # placement of enemy
        enemy(enemyX[i], enemyY[i], i)

    # placement of objects
    player(playerX, playerY)
    show_score()
    pygame.display.update()
