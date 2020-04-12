import pygame
import random
import math
from pygame import mixer

# initialize the pygame
pygame.init()

# create the screen(width,height) 0,0 at the left top corner.
screen = pygame.display.set_mode((800,600))

# background image
background = pygame.image.load("space_background.jpg")
# background music
mixer.music.load("background.wav")
# -1 means in loop
# mixer.music.play(-1) 


# everything happends in the game are events
# Title and Icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("Title_icon.png")
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load("player_icon.png")
playerX = 370
playerY = 480
playerX_delta = 0
playerX_speed = 2

class enemy():
    
    def __init__(self,enemy_speed_x,enemy_speed_y):
        self.Img = pygame.image.load("enemy_alien_icon.png")
        self.X = random.randint(1,735)
        self.Y = random.randint(10,200)
        self.X_delta = enemy_speed_x
        self.Y_delta = enemy_speed_y
        self.lb =1
        self.ub = 734
    def show(self):
        screen.blit(self.Img,(self.X,self.Y))
    def move(self):
        self.X += self.X_delta
        if self.X <= self.lb or self.X >= self.ub:
            self.X_delta = -self.X_delta
            self.Ymove()
    
    def Ymove(self):
        self.Y += self.Y_delta


vx = 1
vy = 2
e1 = enemy(vx,vy)


# bullet
# ready - you cant see the bullet on the screen
# fire - bullet moving
bulletImg = pygame.image.load("bullet_icon.png")
bulletX = 0
bulletY = 480
bullet_speed_x = 0
bullet_speed_y = 5
bulletX_delta = bullet_speed_x
bulletY_delta = bullet_speed_y
bullet_state = "ready"

# score-text
score_value = 0
score_font = pygame.font.Font('freesansbold.ttf',32)
textX = 10
textY = 10 

# game-over-text
over_font = pygame.font.Font('freesansbold.ttf',64)


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (0xff,0xff,0xff))
    screen.blit(over_text,(200,250))

def show_score(x,y):
    score = score_font.render("Score: " + str(score_value),True, (0xff,0xff,0xff))
    screen.blit(score,(x,y))

def player(x,y):
    # drawing the player image on the screen windows
    screen.blit(playerImg,(x,y))

# def enemy(x,y):
#     screen.blit(enemyImg,(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    # x,y top left corner of spaceship
    # move it to the center of icon
    screen.blit(bulletImg,(x+16,y+10))

def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = (enemyX - bulletX)**2 + (enemyY - bulletY)**2
    if distance < 800:
        return True
    return False
    
# game loop
running = True
while running:
    # RGB color of scrren
    screen.fill((0x00,0,0))
    # background image
    screen.blit(background,(0,0))
    # loop throught all events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroke is pressed and find who it is
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                # print("left")
                playerX_delta = -playerX_speed
            if event.key == pygame.K_RIGHT:
                # print("right")
                playerX_delta = playerX_speed
            if event.key == pygame.K_SPACE and bullet_state == 'ready':
                # capture the current x coordinate of spaceship and store it as the x of bullet
                bullet_sound = mixer.Sound('laser.wav')
                bullet_sound.play()
                bulletX = playerX
                fire_bullet(bulletX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_delta = 0
    
    # boundary condition for spaceship
    playerX += playerX_delta
    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    e1.move()

    # game_over
    if e1.Y > 440:
        game_over_text()
        # break

    # bullet movement
    if bulletY <=0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state is "fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_delta

    collision = isCollision(e1.X, e1.Y, bulletX, bulletY)
    if collision:
        collision_sound = mixer.Sound("explosion.wav")
        collision_sound.play()
        bulletY = 480
        bullet_state = 'ready'
        score_value +=1
        e1 = enemy(vx,vy)
    # drawing the player
    player(playerX,playerY)
    e1.show()
    show_score(textX,textY)
    pygame.display.update()
