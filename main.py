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

# Initialize Pygame
pygame.init()

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
        if math.sqrt((bullet.x-self.x)**2+(bullet.y-self.y)**2) < 27:
            return True




player = Player(370)
enemny = Enemy(random.randint(0,800-64), random.randint(0,300-64))
bullet = Bullet()




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
                    bullet.x = player.x + 16
                    bullet.y = player.y

        if event.type == pygame.KEYUP: # Key is released
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0

    # Movement

    player.move()
    enemny.move()
   
    bullet.move()    

    # Show Items

    screen.fill((0, 0, 0))  # Clear screen with black   
    #screen.blit(pygame.image.load('resources/background-1.jpg'), (0, 0))  # Background
    player.player_set()
    enemny.enemy_set()
    if bullet.state == "fire":
        bullet.shoot()
    

    
    pygame.display.flip()  # Update the display