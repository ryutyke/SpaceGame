import pygame
import random
import time
import math

display_width = 700
display_height = 500

globalangle = 0

me_x= 332.5
me_y= 232.5
me_angle=0

gray = (160,161,157)
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
purple = (153,50,204)
lightred = (200,0,0)
lightgreen = (0,200,0)
lightpurple = (150,123,220)
score = 0

pygame.init()

screen = pygame.display.set_mode([display_width,display_height])
pygame.display.set_caption('SpaceGame')
clock = pygame.time.Clock()

pygame.time.set_timer(31,1000)
pygame.time.set_timer(29,260)
pygame.time.set_timer(30,600)

menueffect = pygame.mixer.Sound('menubgm.wav')
nosound = pygame.mixer.Sound('nosound.wav')
explosioneffect = pygame.mixer.Sound('explosionbgm.wav')
shooteffect1 = pygame.mixer.Sound('shootbgm1.wav')

class team(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, player_position):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(green)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        c = math.sqrt((player_position.x - self.rect.x) ** 2 + (player_position.y - self.rect.y) ** 2)
        self.dX = ((player_position.x - self.rect.x) / c) * 2
        self.dY = ((player_position.y  - self.rect.y) / c) *2

    def update(self):
        self.rect.x += self.dX
        self.rect.y += self.dY

class enemy(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, player_position):

        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(red)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        c = math.sqrt((player_position.x - self.rect.x) ** 2 + (player_position.y - self.rect.y) ** 2)
        self.dX = ((player_position.x - self.rect.x) / c) * 2.5
        self.dY = ((player_position.y  - self.rect.y) / c) *2.5

    def update(self):
        self.rect.x += self.dX
        self.rect.y += self.dY

class Player(pygame.sprite.Sprite):

    anglechange=0
    change_x = 0
    change_y = 0

    def __init__(self, x, y, angle):

        super().__init__()

        self.angle= angle

        self.tankImg = pygame.image.load('tank.png')
        tankL = pygame.transform.scale(self.tankImg, (25,25))
        rottank = pygame.transform.rotate(tankL, self.angle)
        self.image = rottank

        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x


    def changespeed(self, x, y):
        self.change_x += x
        self.change_y += y

    def changeangle(self,anglespeed):
        self.anglechange += anglespeed

    def move(self, enemys, teams):
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        oldCenter = self.rect.center
        self.angle += self.anglechange
        self.image = pygame.transform.rotate(self.tankImg, self.angle)
        self.image = pygame.transform.scale(self.image, (25,25))
        self.rect = self.image.get_rect()
        self.rect.center = oldCenter

        global globalangle
        globalangle = self.angle

        enemy_hit_list = pygame.sprite.spritecollide(self, enemys, False)
        team_hit_list = pygame.sprite.spritecollide(self, teams, False )
        if len(enemy_hit_list) > 0 or len(team_hit_list) > 0:
            pygame.mixer.music.load('gameoverbgm.wav')
            pygame.mixer.music.play(0)
            gameoverscreen()

        if self.rect.x > display_width - 25:
            self.rect.x = display_width - 25
        if self.rect.x < 0:
            self.rect.x = 0
        if self.rect.y > display_height - 25:
            self.rect.y = display_height - 25
        if self.rect.y < 0:
            self.rect.y = 0


class Bullet(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

        self.image = pygame.Surface([10, 10])
        self.image.fill(white)

        self.rect = self.image.get_rect()
        self.angle = globalangle % 360
        self.dX = math.cos(self.angle / 180 * math.pi) * 10
        self.dY = math.sin(self.angle / 180 * math.pi) * 10
    def update(self):
        
        self.rect.x += self.dX
        self.rect.y -= self.dY

def gamequit():
    pygame.quit()
    quit()

def text_objects(text,font, color):
    textSurface = font.render(text, True , color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText= pygame.font.Font('freesansbold.ttf',20)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        textSurf, textRect = text_objects(msg, smallText, purple)
        textRect.center = ( x+(w/2), y+(h/2))
        screen.blit(textSurf, textRect)
        if click[0] == 1 and action !=None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        textSurf, textRect = text_objects(msg, smallText, lightpurple)
        textRect.center = ( x+(w/2), y+(h/2))
        screen.blit(textSurf, textRect)

def storyscreen():

    storyimg1 = pygame.image.load("story1.png")
    storyimg1 = pygame.transform.scale(storyimg1, (700,500))
    storyimg2 = pygame.image.load("story2.png")
    storyimg2 = pygame.transform.scale(storyimg2, (700,500))
    storyimg3 = pygame.image.load("story3.png")
    storyimg3 = pygame.transform.scale(storyimg3, (700,500))
    screen.fill(black)
    story = True
    story1 = False
    story2 = False

    while True:
        while story:
            screen.blit(storyimg1, (0,0))
            pygame.display.update()
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamequit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screen.blit(storyimg2,(0,0))
                        story = False
                        story1 = True
        while story1:
            pygame.display.update()
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamequit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        screen.blit(storyimg3,(0,0))
                        story1 = False
                        story2 = True
        while story2:
            pygame.display.update()
            clock.tick(15)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gamequit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        introscreen()

        pygame.display.update()
        clock.tick(15)

def introscreen():
    
    pygame.mixer.music.load('introbgm.wav')
    pygame.mixer.music.play(-1)

    key = pygame.image.load("key.png")
    key = pygame.transform.scale(key, (250,250))
    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (400,150))
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)
        #largeText = pygame.font.Font('freesansbold.ttf',40)
        #TextSurf, TextRect = text_objects("SpaceGame",largeText, lightpurple)
        #TextRect.center = ((display_width/2),(display_height/5))
        #screen.blit(TextSurf, TextRect)
        screen.blit(key, (20,200))
        screen.blit(logo, (150, 20))

        button("Easymode",300,300,105,30,black,black,easymain)
        button("Hardmode",300,420,105,30,black,black,hardmain)
        button("Quit",500,360,55,30,black,black,gamequit)
        button("Rule",500,200,55,30,black,black,rulescreen)
       
        pygame.display.update()
        clock.tick(15)

def rulescreen():
     rule = pygame.image.load("rule.png")
     rule = pygame.transform.scale(rule, (500,300))
     intro = True
     while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)
        screen.blit(rule, (50,10))

        button("Back",220,430,55,30,black,black,introscreen)
        
        pygame.display.update()
        clock.tick(15)

def gameoverscreen():

    global score

    gameover=True
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf',40)
        TextSurf, TextRect = text_objects("GameOver",largeText, lightpurple)
        TextRect.center = ((display_width/2),(display_height/5))
        screen.blit(TextSurf, TextRect)
        
        smallText = pygame.font.Font('freesansbold.ttf',20)
        TextSurf1, TextRect1 = text_objects("Your score is " + str(score) ,smallText, lightpurple)
        TextRect1.center = ((display_width/2),(display_height/3))
        screen.blit(TextSurf1, TextRect1)

        button("Easymode",30,240,105,30,black,black,easymain)
        button("Hardmode",30,360,105,30,black,black,hardmain)
        button("Intro",400,240,55,30,black,black,introscreen)
        button("Quit",400,360,55,30,black,black,gamequit)
    
        pygame.display.update()
        clock.tick(15)



def easymain():

    global score
    global globalangle

    pygame.mixer.music.stop()
    pygame.mixer.music.load('mainbgm.wav')
    pygame.mixer.music.play(-1)

    player = Player(me_x, me_y,me_angle)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    team_list = pygame.sprite.Group()

    clock = pygame.time.Clock()
    score = 0
    done = False

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == 31:
                Teamlist=[]

                Teamlist.append(team(random_x,-100, 15,15,player.rect))
                Teamlist.append(team(random_x, 600, 15,15,player.rect))
                Teamlist.append(team(-100,random_y, 15,15,player.rect))
                Teamlist.append(team(800,random_y, 15,15,player.rect))
                
                Team = Teamlist[random.randint(0,3)]
                movingsprites.add(Team)
                team_list.add(Team)

            if event.type == 30:
                Enemylist=[]

                Enemylist.append(enemy(random_x,-100, 15,15,player.rect))
                Enemylist.append(enemy(random_x, 600, 15,15,player.rect))
                Enemylist.append(enemy(-100,random_y, 15,15,player.rect))
                Enemylist.append(enemy(800,random_y, 15,15,player.rect))
                
                Enemy = Enemylist[random.randint(0,3)]
                movingsprites.add(Enemy)
                enemy_list.add(Enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.changespeed(-4, 0)
                if event.key == pygame.K_d:
                    player.changespeed(4, 0)
                if event.key == pygame.K_w:
                    player.changespeed(0, -4)
                if event.key == pygame.K_s:
                    player.changespeed(0, 4)
                if event.key == pygame.K_SPACE:
                    shooteffect1.play()
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x +12.5
                    bullet.rect.y = player.rect.y +9
                    
                    movingsprites.add(bullet)
                    bullet_list.add(bullet)
                if event.key == pygame.K_LEFT:
                    player.changeangle(5)
                if event.key == pygame.K_RIGHT:
                    player.changeangle(-5)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.changespeed(4, 0)
                if event.key == pygame.K_d:
                    player.changespeed(-4, 0)
                if event.key == pygame.K_w:
                    player.changespeed(0, 4)
                if event.key == pygame.K_s:
                    player.changespeed(0, -4)
                if event.key == pygame.K_LEFT:
                    player.changeangle(-5)
                if event.key == pygame.K_RIGHT:
                    player.changeangle(5)
        
        # --- Game logic
        random_x = random.randint(-100,800)
        random_y = random.randint(-100,600)

        player.move(enemy_list,team_list)
   
        for Enemy in enemy_list:
            Enemy.update()

        for Team in team_list:
            Team.update()     

        for bullet in bullet_list:
            bullet.update()

            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
            team_hit_list = pygame.sprite.spritecollide(bullet, team_list, True)

            for Enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
                explosioneffect.play()
                score += 1
            if len(team_hit_list) > 0:
                pygame.mixer.music.load('gameoverbgm.wav')
                pygame.mixer.music.play(0)
                gameoverscreen()
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.y > 510:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.x < -10:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.x > 710:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)

        # --- Draw a frame

        screen.fill(black)

        movingsprites.draw(screen)

        font = pygame.font.SysFont(None, 25)
        text = font.render("Score "+str(score),True, white)
        screen.blit(text, (0,0))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

def hardmain():

    global score
    global globalangle
    score = 0

    pygame.mixer.music.stop()
    pygame.mixer.music.load('mainbgm.wav')
    pygame.mixer.music.play(-1)

    player = Player(me_x, me_y,me_angle)
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)

    enemy_list = pygame.sprite.Group()
    bullet_list = pygame.sprite.Group()
    team_list = pygame.sprite.Group()

    clock = pygame.time.Clock()
    score = 0
    done = False

    # -------- Main Program Loop -----------
    while not done:
        # --- Event Processing
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            
            if event.type == 29:
                Teamlist=[]

                Teamlist.append(team(random_x,-100, 15,15,player.rect))
                Teamlist.append(team(random_x, 600, 15,15,player.rect))
                Teamlist.append(team(-100,random_y, 15,15,player.rect))
                Teamlist.append(team(800,random_y, 15,15,player.rect))
                
                Team = Teamlist[random.randint(0,3)]
                movingsprites.add(Team)
                team_list.add(Team)

            if event.type == 30:
                Enemylist=[]

                Enemylist.append(enemy(random_x,-100, 15,15,player.rect))
                Enemylist.append(enemy(random_x, 600, 15,15,player.rect))
                Enemylist.append(enemy(-100,random_y, 15,15,player.rect))
                Enemylist.append(enemy(800,random_y, 15,15,player.rect))
                
                Enemy = Enemylist[random.randint(0,3)]
                movingsprites.add(Enemy)
                enemy_list.add(Enemy)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_d:
                    player.changespeed(5, 0)
                if event.key == pygame.K_w:
                    player.changespeed(0, -5)
                if event.key == pygame.K_s:
                    player.changespeed(0, 5)
                if event.key == pygame.K_SPACE:
                    shooteffect1.play()
                    bullet = Bullet()
                    bullet.rect.x = player.rect.x +12.5
                    bullet.rect.y = player.rect.y +9
                    
                    movingsprites.add(bullet)
                    bullet_list.add(bullet)
                if event.key == pygame.K_LEFT:
                    player.changeangle(5)
                if event.key == pygame.K_RIGHT:
                    player.changeangle(-5)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    player.changespeed(5, 0)
                if event.key == pygame.K_d:
                    player.changespeed(-5, 0)
                if event.key == pygame.K_w:
                    player.changespeed(0, 5)
                if event.key == pygame.K_s:
                    player.changespeed(0, -5)
                if event.key == pygame.K_LEFT:
                    player.changeangle(-5)
                if event.key == pygame.K_RIGHT:
                    player.changeangle(5)
        
        # --- Game logic
        random_x = random.randint(-100,800)
        random_y = random.randint(-100,600)

        player.move(enemy_list,team_list)
   
        for Enemy in enemy_list:
            Enemy.update()

        for Team in team_list:
            Team.update()     

        for bullet in bullet_list:
            bullet.update()

            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemy_list, True)
            team_hit_list = pygame.sprite.spritecollide(bullet, team_list, True)

            for Enemy in enemy_hit_list:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
                explosioneffect.play()
                score += 1
            if len(team_hit_list) > 0:
                pygame.mixer.music.load('gameoverbgm.wav')
                pygame.mixer.music.play(0)
                gameoverscreen()
            if bullet.rect.y < -10:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.y > 510:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.x < -10:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)
            if bullet.rect.x > 710:
                bullet_list.remove(bullet)
                movingsprites.remove(bullet)

        # --- Draw a frame

        screen.fill(black)

        movingsprites.draw(screen)

        font = pygame.font.SysFont(None, 25)
        text = font.render("Score "+str(score),True, white)
        screen.blit(text, (0,0))

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

storyscreen()
