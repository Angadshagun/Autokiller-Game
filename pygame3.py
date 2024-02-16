# Import modules
import pygame
import random
import math
from pygame import mixer

# Initialize the  pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((1000, 750))

# Title and Icon
pygame.display.set_caption('Space Bastered')
icon = pygame.image.load('logo png.png')
pygame.display.set_icon(icon)

# Background Image
back = pygame.image.load('space_b.png')

# Set width and height of background image
background = pygame.transform.scale(back, (1000, 750))

# Music Load (Background,shooting and explosion)
mixer.music.load('background.wav')
mixer.music.play(-1)

# Plane Image
playerImg = pygame.image.load('Spaceship.png')
playerx = 390
playery = 350

# Player Lifeline
Lifeline = 4


def player(x, y):
    # drawing an image on screen
    screen.blit(resized_image, (x, y),)


# Resize the image
resized_image = pygame.transform.scale(playerImg, (170, 170))

# More enemies images
enemyImg = []
enemy_x = []
enemy_y = []
num_of_enemies = 6
enemy_dir = []

for i in range(num_of_enemies):
    ene = pygame.image.load('enemy1.png')
    # Resized enemy image
    enemy = pygame.transform.scale(ene, (100, 100))
    enemyImg.append(enemy)
    enemy_x.append(random.randint(0, 900))
    enemy_y.append(random.randint(50, 100))
    enemy_dir.append('Right')

# drawing enemy on screen


def enemyph(x, y, i):
    screen.blit(enemyImg[i], (x, y))

# Bullet
# Ready :- You can't see the bullet on the screen
# Fired :- The bullet is moving


bullets = pygame.image.load('Bullets.png')
bullet_x = playerx + 70
bullet_y = playery + 2
bullet_state = 'Ready'

# Resize the bullet
bullet = pygame.transform.scale(bullets, (30, 40))

# Fire function


def Fire(x, y):
    global bullet_state
    bullet_state = 'Fire'
    screen.blit(bullet, (x, y))

# Collision Function


def isCollision(bullet_x, bullet_y, enemyx, enemyy):
    distance = math.sqrt(math.pow(enemyx - bullet_x, 2) +
                         math.pow(enemyy-bullet_y, 2))
    if (distance < 50 or enemyy > 700):
        return True
    else:
        return False

# Lifeline Function


def life():
    x, y = 920, 10
    i = Lifeline
    lifeline_image = pygame.image.load(
        'lifeline_image.png')
    lifeline_image = pygame.transform.scale(lifeline_image, (50, 50))

    while (i > 0):
        screen.blit(lifeline_image, (x, y))
        x -= 50
        i -= 1


# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

# Game Over Text
over = pygame.font.Font('freesansbold.ttf', 64)

# Show Score


def show_score():
    score = font.render("Score :-"+str(score_value), True, (255, 255, 255))
    screen.blit(score, (10, 10))


# Screen Content
start_Screen = 0
game_Screen = 1
game_over_Screen = 2
curr_Screen = start_Screen

running = True
pressed = None
while running:
    # RGB Value in this tuple
    # screen.fill((0, 10, 40))

    # Background image
    screen.blit(background, (0, 0))

    if (curr_Screen == start_Screen):
        # Draw start screen
        # (You can add a start button here)

        start_text = font.render("Start Game", True, (0, 155, 0))
        start_button_rect = start_text.get_rect(center=(500, 400))
        screen.blit(start_text, start_button_rect.topleft)

        # Check for button click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (start_button_rect.collidepoint(mouse_x, mouse_y)):
                    curr_Screen = game_Screen
            elif event.type == pygame.QUIT:
                running = False

        # for restart the game give the position of player
        playerx = 390
        playery = 350

        # for restart the game give the position of enemies
        for i in range(num_of_enemies):
            enemy_x[i] = (random.randint(0, 900))
            enemy_y[i] = (random.randint(50, 100))
            enemy_dir[i] = 'Right'

        # Restart moving player
        pressed = None
        Lifeline = 3

    elif (curr_Screen == game_Screen):

        # Screen change situation
        for i in range(num_of_enemies):
            if enemy_y[i] > 650:
                curr_Screen = game_over_Screen

            coll = math.sqrt((enemy_x[i]-playerx)**2 + (enemy_y[i]-playery)**2)
            if coll < 100 and Lifeline == 0:
                curr_Screen = game_over_Screen
            if coll < 100:
                Lifeline -= 1
                enemy_x[i] = random .randint(0, 900)
                enemy_y[i] = random .randint(50, 100)
                enemy_dir[i] = 'Right'

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # key stroke event
            # if keystroke is pressed check whether its right or left
            elif (event.type == pygame.KEYDOWN):
                if (event.key == pygame.K_LEFT):
                    pressed = 'Left'
                elif (event.key == pygame.K_RIGHT):
                    pressed = 'Right'
                elif (event.key == pygame.K_UP):
                    pressed = 'Up'
                elif (event.key == pygame.K_DOWN):
                    pressed = 'Down'
                elif (event.key == pygame.K_SPACE):
                    if (bullet_state == 'Ready'):
                        bullet_x = playerx + 70
                        bullet_y = playery
                        bullet_sound = mixer.Sound('laser.wav')
                        bullet_sound.play()
                        Fire(bullet_x, bullet_y)
            elif event.type == pygame.KEYUP:
                pressed = None

        if (pressed == 'Left'):
            if (playerx >= 0.5):
                playerx -= 2.5
        elif (pressed == 'Right'):
            if (playerx <= 830):
                playerx += 2.5
        elif (pressed == 'Up'):
            if (playery >= 50):
                playery -= 2.5
        elif (pressed == 'Down'):
            if (playery <= 570):
                playery += 2.5

        # Enemy movement
        # x-direction change

        for i in range(num_of_enemies):

            if enemy_dir[i] == 'Right':
                if enemy_x[i] < 897:
                    enemy_x[i] += 2
                else:
                    enemy_dir[i] = 'Left'
            elif enemy_dir[i] == 'Left':
                if enemy_x[i] >= 20:
                    enemy_x[i] -= 2
                else:
                    enemy_dir[i] = 'Right'

        # Enemy y-direction change
            if (enemy_y[i] <= 650):
                enemy_y[i] += 0.2

            # Collision
            collision = isCollision(bullet_x, bullet_y, enemy_x[i], enemy_y[i])
            if collision:
                explosion_sound = mixer.Sound('explosion.wav')
                explosion_sound.play()
                bullet_y = playery + 2
                bullet_state = 'Ready'
                score_value += 1
                enemy_x[i] = random.randint(0, 900)
                enemy_y[i] = random.randint(50, 100)

        # update enemy position
            enemyph(enemy_x[i], enemy_y[i], i)

        # Bullet Movement
        if (bullet_y <= 0):
            bullet_state = 'Ready'
            bullet_y = playery+2
        if bullet_state == 'Fire':
            bullet_y -= 4
            bullet_sound = mixer.Sound('laser.wav')
            bullet_sound.play()
            Fire(bullet_x, bullet_y)

        # update player
        player(playerx, playery)

        # update lifeline
        life()

        # Show score
        show_score()

    elif (curr_Screen == game_over_Screen):
        # Draw game over screen
        # game_over(350, 350)

        # Draw score text
        score_text = font.render(
            "Score: " + str(score_value), True, (0, 130, 0))
        screen.blit(score_text, (420, 350))

        # Draw start again button
        start_text = font.render("Start Again", True, (0, 0, 155))
        start_button_rect = start_text.get_rect(center=(510, 420))
        screen.blit(start_text, start_button_rect.topleft)

        # Check for button click
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if (start_button_rect.collidepoint(mouse_x, mouse_y)):
                    # Reset game variables
                    score_value = 0
                    curr_Screen = start_Screen
            elif event.type == pygame.QUIT:
                running = False

    # Update the display
    pygame.display.update()

pygame.quit()
