import pygame
import random
import math

#initialize the module pygame
pygame.init()

#title and icon
screen = pygame.display.set_mode((800,600))
icon = pygame.image.load('grid.png')
pygame.display.set_icon(icon)
bg_image = pygame.image.load('background.jpg')
pygame.display.set_caption("Akash le dhalyo sab lai!!")

#player module
playerimg = pygame.image.load('playerimg.jpg')
playerX=368
playerY=538
playerX_change = 0

#enemies module 1st
enemyimg = []
enemyX = []
enemyY = []
enemyX_change = []

number_of_enemies=4
for i in range(number_of_enemies):
    enemyimg.append(pygame.image.load('enemyimg'+str(i)+'.jpg'))
    enemyX.append(float(random.randint(0,736)))
    enemyY.append(random.randint(50,150))
    enemyX_change.append(random.uniform(0.5,2))

#bullet module 1st
bulletimg = pygame.image.load('bullet.png')
bulletX= 0
bulletY=538
bulletY_change= 2
bullet_state = "ready"

#score calc
score_value = 0
scoreX=10
scoreY=10
font= pygame.font.Font('freesansbold.ttf',32)

#game over
over_font= pygame.font.Font('freesansbold.ttf',64)
over_image = pygame.image.load('over.jpg')

#functions
def player(x,y):
    screen.blit(playerimg,(x,y))
 
def enemy(x,y,i):
    screen.blit(enemyimg[i],(x,y))

def bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg,(x+16,y+10))

def is_collision(enX,enY,buX,buY):
    distance = math.sqrt((math.pow((enX-buX),2))+(math.pow((enY-buY),2)))
    if distance<30:
        return True
    else: return False

def show_score(x,y):
    score = font.render("Score:" + str(score_value), True, (155,200,155))
    screen.blit(score,(x,y))

def game_over():
    over = over_font.render("GAME OVER", True, (255,0,0))
    screen.blit(over,(200,100))
    screen.blit(over_image,(200,200))


#Game module
running = True
while running:
    screen.fill((132,125,94))
    screen.blit(bg_image,(0,0))
    for event in pygame.event.get() :
        if event.type == pygame.QUIT :
            running = False
        
        if event.type == pygame.KEYDOWN :
            if event.key == pygame.K_LEFT :
               playerX_change = -2
            if event.key == pygame.K_RIGHT :
                playerX_change = 2

            if event.key == pygame.K_SPACE and bullet_state is "ready":
                bulletX = playerX
                bullet(bulletX,bulletY)
        
        if event.type == pygame.KEYUP :
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                playerX_change = 0
            
    playerX += playerX_change


    #bound player to the screen
    if playerX>=736:
        playerX=736
    elif playerX<=0:
        playerX = 0

# bullet module starts
    if bullet_state is "fire":
        bullet(bulletX,bulletY)
        bulletY -= bulletY_change
        if bulletY == 0:
            bullet_state="ready"
            bulletY = 538


    #modifying the number of enemies
    for i in range(number_of_enemies):
        if enemyY[i] >=500:
            for j in range(number_of_enemies):
                enemyY[j] = 2000
            game_over()
            break
        #Enemy module starts
        enemyX[i] += enemyX_change[i]
        if enemyX[i]>=736:
            enemyX[i]=736
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] += 50
        elif enemyX[i]<=0:
            enemyX[i] = 0
            enemyX_change[i] = -enemyX_change[i]
            enemyY[i] +=50

        #Collosion calling
        collision = is_collision(enemyX[i],enemyY[i],bulletX,bulletY)

        if collision:
            bullet_state="ready"
            bulletY = 538
            enemyX[i]= float(random.randint(0,736))
            enemyY[i]=random.randint(50,150)
            score_value +=1

        enemy(enemyX[i],enemyY[i],i)



    player(playerX,playerY)
    #score must be displaced here only!!!
    show_score(scoreX,scoreY)
    pygame.display.update()
