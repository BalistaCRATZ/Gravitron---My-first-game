import pygame
import math
import sys
import random
import time

pygame.init()
pygame.font.init()

width = 500
height = 500

#The player class
class Player():

    def _init_(self):
        self.x = 0
        self.y = 0
        self.y_speed = 0
        self.death_state = False
        self.lives = 0
        
class Bullet():

    def _init_(self):
        self.x = 0
        self.y = 0
        self.speed = 0
        self.state = False

    def draw(self, x, y, colour):
        pygame.draw.rect(screen, colour, [x, y, 10, 4], 5)

    def move(self, x, speed):
        self.x += self.speed

class Enemy():

    def _init_(self):
        self.x = 0
        self.y = 0
        self.death_state = False
        self.on = False
    
class Circle():

    def _init_(self):
        self.x = 0
        self.y = 0
        self.radius = 0
        self.state = False

    def draw(self, x, y, radius):
        pygame.draw.circle(screen, BLUE, (x, y), radius, 10)
        

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

clock = pygame.time.Clock()

size = (width, height)
screen = pygame.display.set_mode(size)

title = pygame.display.set_caption("Gravitron")

background = pygame.image.load("background.png").convert()
image_size = background.get_size()
image_width = image_size[0]

falcon = pygame.image.load("falcon.png").convert()
ninja = pygame.image.load("EnemyShip.png").convert()
explosion_image = pygame.image.load("explosion_image.jpg").convert()
heart = pygame.image.load("heart.png").convert()

laser = pygame.mixer.Sound("Laser.wav")
explosion = pygame.mixer.Sound("Explosion.wav")
emp = pygame.mixer.Sound("EMP.wav")

myfont = pygame.font.Font("ScoreFont.TTF", 16)
myfont2 = pygame.font.Font("ScoreFont.TTF", 50)

#Creating a player
player = Player()
player.x = 20
player.y = height / 2
player.y_speed = -15

#Creating a bullet
bullet = Bullet()
bullet.x = 0
bullet.y = 0
bullet.speed = 50
bullet.state = False

#Creating an enemy
enemy = Enemy()
enemy.x = 500
enemy.y = random.randint(20, height - 20)
enemy.x_speed = -1
enemy.death_state = False
enemy.on = True
enemy.bullet_state = False

#Creating another enemy
enemy2 = Enemy()
enemy2.x = 1000
enemy2.y = random.randint(20, height-20)
enemy2.x_speed = -1
enemy2.death_state = False
enemy2.on = False
enemy2.bullet_state = False

#Creating another enemy
enemy3 = Enemy()
enemy3.x = 2000
enemy3.y = random.randint(20, height - 20)
enemy3.x_speed = -1
enemy3.death_state = False
enemy3.on = False
enemy3.bullet_state = False

#Creating a circle
circle = Circle()
circle.x = player.x + 50
circle.y = player.y + 40
circle.radius = 1
circle.state = False

#Creating an enemy bullet
e_bullet = Bullet()
e_bullet.x = enemy3.x
e_bullet.y = enemy3.y
e_bullet.speed = -20
e_bullet.state = False

def distance(x1, y1, x2, y2):
    
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return dist

def speed_multiplier(total_score):

    multiplier = total_score / 100
    return multiplier

def main():

    pygame.init()

    player.lives = 3
    player.death_state = False

    #Score variable
    score = 0
    
    done = False

    bg_x = 0
    pressed_up = False
    pressed_down = False
    
    while done == False:

        #Player death sequence
        while player.death_state == True:
            screen.fill(WHITE)
            gameoversurface = myfont2.render("GAME OVER", False, BLACK)
            gameoverscoresurface = myfont2.render("YOUR SCORE    " + str(score), False, BLACK)
            textsurface = myfont.render("Type r to  restart", False, BLACK)
            screen.blit(gameoverscoresurface, [width/2 - 160, height/2])
            screen.blit(gameoversurface, [width/2 - 110, height/2 - 50])
            screen.blit(textsurface, [150, 400])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        main()
                elif event.type == pygame.QUIT:
                    done = True
                    player.death_state = False

        circle.y = player.y + 40

        multiplier = speed_multiplier(score)

        if bullet.state == False:
            bullet.x = player.x + 73
            bullet.y = player.y + 37
        
        #Event processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done  = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    pressed_up = True
                elif event.key == pygame.K_DOWN:
                    pressed_down = True
                elif event.key == pygame.K_SPACE:
                    bullet.state = True
                    laser.play()
                elif event.key == pygame.K_LSHIFT:
                    circle.state = True
                    emp.play()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pressed_up = False
                elif event.key == pygame.K_DOWN:
                    pressed_down = False
                elif event.key == pygame.K_LSHIFT:
                    circle.state = False
                 
        #Drawing
        screen.blit(background, [bg_x, 0])
        bg_x -= 5

        if circle.state == True:
            circle.draw(int(circle.x), int(circle.y), 300)

            if distance(player.x, player.y, enemy.x, enemy.y) <= 350:
                explosion.play()
                screen.blit(explosion_image, [enemy.x, enemy.y])
                enemy.death_state = True
                score += 10
                
            elif distance(player.x, player.y, enemy2.x, enemy2.y) <= 350 and enemy2.on == True:
                explosion.play()
                screen.blit(explosion_image, [enemy2.x, enemy2.y])
                enemy2.death_state = True
                score += 10

            elif distance(player.x, player.y, enemy3.x, enemy3.y) <= 350 and enemy3.on == True:
                explosion.play()
                screen.blit(explosion_image, [enemy3.x, enemy3.y])
                enemy3.death_state = True
                score += 10
            
                       
        #Score display
        scoresurface = myfont.render("Score   " + str(score), False, WHITE)
        screen.blit(scoresurface, (10,10))

        #Lives display
        if player.lives == 3:
            screen.blit(heart, (10, 30))
            screen.blit(heart, (30, 30))
            screen.blit(heart, (50, 30))
        elif player.lives == 2:
            screen.blit(heart, (10, 30))
            screen.blit(heart, (30, 30))
        elif player.lives == 1:
            screen.blit(heart, (10, 30))
        
        #Background 
        if bg_x < -(image_width - 500):
            bg_x = 0

        #Player movement handling

        if player.death_state == False:
            screen.blit(falcon, [player.x, player.y])
            
        if pressed_up == True:
            player.y += player.y_speed
 
        elif pressed_down == True:
            player.y -= player.y_speed

        if player.y > height - 65:
            player.y = height - 65
        elif player.y < 0:
            player.y = 0

        #Bullet movement handling
        if bullet.state == True:            
            bullet.draw(bullet.x, bullet.y, RED)
            bullet.move(bullet.x, bullet.speed)

        if bullet.x > width:
            bullet.state = False

        #Enemy movement handling

        if enemy.x < -10:
            enemy.x = 500

        if enemy2.x < -10:
            enemy2.x = 500

        if enemy3.x < -10:
            enemy3.x = 500

        if enemy.death_state == False:
            screen.blit(ninja, [enemy.x, enemy.y])
            enemy.x += enemy.x_speed

        if enemy.death_state == True:
            enemy.y = random.randint(50, height-20)
            enemy.x = 500
            enemy.death_state = False

        #Bullet collision detection
        dist = distance(bullet.x, bullet.y, enemy.x, enemy.y)
        if dist < 40 and bullet.state == True:
            explosion.play()
            screen.blit(explosion_image, [enemy.x, enemy.y])
            enemy.death_state = True
            score += 10

        dist2 = distance(bullet.x, bullet.y, enemy2.x, enemy2.y)
        if dist2 < 40 and bullet.state == True and enemy2.on == True:
            explosion.play()
            screen.blit(explosion_image, [enemy2.x, enemy2.y])
            enemy2.death_state = True
            score += 10

        dist3 = distance(bullet.x, bullet.y, enemy3.x, enemy3.y)
        if dist3 < 40 and bullet.state == True and enemy3.on == True:
            explosion.play()
            screen.blit(explosion_image, [enemy3.x, enemy3.y])
            enemy3.death_state = True
            score += 10

        #Player collison detection
        player_dist = distance(player.x, player.y, enemy.x, enemy.y)
        if player_dist <= 60:
            explosion.play()
            screen.blit(explosion_image, [player.x, player.y])
            enemy.death_state = True
            player.lives -= 1
            bullet.state = False

        player_dist2 = distance(player.x, player.y, enemy2.x, enemy2.y)
        if player_dist2 <= 60 and enemy2.on == True:
            explosion.play()
            screen.blit(explosion_image, [player.x, player.y])
            enemy2.death_state = True
            player.lives -= 1
            bullet.state = False
            
        player_dist3 = distance(player.x, player.y, enemy3.x, enemy3.y)
        if player_dist3 <= 60 and enemy3.on == True:
            explosion.play()
            screen.blit(explosion_image, [player.x, player.y])
            enemy3.death_state = True
            player.lives -= 1
            bullet.state = False

        playerBulletDist = distance(player.x, player.y, e_bullet.x, e_bullet.y)
        if playerBulletDist <= 40 and e_bullet.state == True:
            explosion.play()
            screen.blit(explosion_image, [player.x, player.y])
            player.lives -= 1
            bullet.state = False

        if player.lives == 0:
            player.death_state = True

        #New enemy handling
        if score >= 100:

            enemy2.on = True
            
            if enemy2.death_state == False:
                screen.blit(ninja, [enemy2.x, enemy2.y])
                enemy2.x += enemy2.x_speed

            if enemy2.death_state == True:
                enemy2.y = random.randint(20, height-20)
                enemy2.x = 500
                enemy2.death_state = False

        if score >= 150:

            enemy3.on = True

            e_bullet.state = True

            if e_bullet.state == True:
                e_bullet.draw(e_bullet.x, e_bullet.y, BLUE)
                e_bullet.move(e_bullet.x, e_bullet.speed)

            if e_bullet.x < -500:
                e_bullet.state = False
                e_bullet.x = enemy3.x - 10
                e_bullet.y = enemy3.y + 25
            
            if enemy3.death_state == False:
                screen.blit(ninja, [enemy3.x, enemy3.y])
                enemy3.x += enemy3.x_speed

            if enemy3.death_state == True:
                enemy3.y = random.randint(20, height-20)
                enemy3.x = 700
                enemy3.death_state = False


            
        #Increasing speed
        if score >= 10:
            enemy.x += multiplier * enemy.x_speed
            enemy2.x += multiplier * enemy2.x_speed
            enemy3.x += multiplier * enemy3.x_speed

        if score >= 1500:
            enemy.x += 1 * enemy.x_speed
            enemy2.x += 1 * enemy2.x_speed
            enemy3.x += 1 * enemy3.x_speed
            
        pygame.display.update()


        clock.tick(30)
                    
    pygame.quit()
    sys.exit
    pygame.font.quit()


main()  

                
        
