#CS Space Invadeers
"""
How do you set up pygame?

What is the purpose of the "While running" loop?

How do you create a screen in pygame?

How are objects placed on the screen in pygame?

What events can I listen for in pygame? What do those events do?

How can I detect collision with pygame?

How do you add sounds in pygame?

"""
import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

background = pygame.image.load('resources/background-1.jpg')
background = pygame.transform.scale(background, (800, 600))

# Score text
score_font = pygame.font.Font('resources/TimesNewBastard-Italic.ttf', 32)
font_color = (255, 255, 255)
font_location = (10, 10)

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
pygame_icon = pygame.image.load('resources/ufo.png')
# 32 x 32 px image
pygame.display.set_icon(pygame_icon)

class Bullet:
    def __init__(self,x=0,y=0):
        self.img = pygame.image.load('resources/bullet.png')
        self.x = x
        self.y = y
        self.change = -1
        self.state = "ready"
        self.rotated = pygame.transform.rotate(self.img, 90)
        

    def shoot(self):
        screen.blit(self.rotated,(self.x,self.y))
        

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "ready"

class Player:
    def __init__(self,x=0,change=0):
        self.img = pygame.image.load('resources/spaceship.png')
        self.x = x
        self.y = (600 - 70)  # Position at the bottom of the screen
        self.change = change
        self.score = 0
        
    def player_set(self):
        screen.blit(self.img,(self.x,self.y))
    
    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= 736:
            self.x = 736



class Enemy:
    def __init__(self,x=0,y=0):
        self.img = pygame.image.load('resources/alien.png')
        self.x = x
        self.y = y  # Position at the bottom of the screen
        self.change_x = 0.1
        self.change_y = 20
    def enemy_set(self):
        screen.blit(self.img,(self.x,self.y))
    
    def move(self):
        self.x += self.change_x
        # x boundary check
        if self.x <= 0:
            self.change_x= 0.1
            self.y += self.change_y

        elif self.x >= 736:
            self.change_x= -0.1
            self.y += self.change_y
        
        elif self.y >= 536:
            self.y = 0
    
    def is_hit(self,bullet):
        if math.sqrt((bullet.x-self.x)**2+(bullet.y-self.y)**2) < 48:
            return True
        else: return False

    def lose(self):
        if self.y >= 536-64:
            return True
        else: return False





player = Player(370)
#enemy = Enemy(random.randint(0,800-64), random.randint(0,300-64))
bullet = Bullet()

def spawn_enemies():
    enemies = []
    for i in range(6):
        x=random.randint(0,800-64)
        y=random.randint(0,300-64)
        enemies.append(Enemy(x, y))
    return enemies
enemies= spawn_enemies()
game_over = False


# Main game loop
running = True
while running:
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT: # Close the window
            running = False

        if event.type == pygame.KEYDOWN: # Key is pressed

            if keys[pygame.K_LEFT]:
                player.change = -0.3

            if keys[pygame.K_RIGHT]:
                player.change = 0.3

            if keys[pygame.K_UP]:
                
                if bullet.state == "ready":
                    bullet.state = "fire"
                    mixer.Sound('resources/laser.wav').play()
                    bullet.x = player.x + 16
                    bullet.y = player.y

        if event.type == pygame.KEYUP: # Key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    for i, enemy in enumerate(enemies) : # enemy handling
        enemy.move()
        if enemy.is_hit(bullet):
            mixer.Sound('resources/explosion.wav').play()
            player.score += 1
            bullet.state = "ready"
            bullet.y = player.y
            bullet.x = player.x + 16
            enemies.pop(i)
            if enemies == []:
                enemies = spawn_enemies()
        elif enemy.lose():
            enemies = []
            game_over = True

    if game_over == True:
        font_render = score_font.render(f"GAME OVER! Final Score: {player.score}", True, font_color)
        screen.fill((0, 0, 0))  # Clear screen with black   


    else:
        player.move()
        bullet.move() 
        # background handling
        screen.fill((0, 0, 0))  # Clear screen with black   
        screen.blit(background), (0, 0)  # Background

        #music
        mixer.music.load('resources/background.wav')
        mixer.music.play(-1) # -1 means loop indefinitely


        # Text
        font_render = score_font.render(f"Score: {player.score}", True, font_color)
        screen.blit(font_render, font_location)

        # Show Items
        player.player_set()

        for enemy in enemies:
            enemy.enemy_set()
        if bullet.state == "fire":
            bullet.shoot()
    
    
    pygame.display.flip()  # Update the display