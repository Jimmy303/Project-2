import pygame
import time
import random
import sys
from pygame.locals import *
import math

pygame.init()
pygame.mixer.init()

entering = pygame.mixer.Sound("entering.wav")
jump = pygame.mixer.Sound("j1.wav")
puazu = pygame.mixer.Sound("puazu.wav")
doodzijn = pygame.mixer.Sound("doodzijn.wav")
overwin = pygame.mixer.Sound("overwin.wav")
fire_sound = pygame.mixer.Sound("Arcade Explo A.wav")
explosion_sound = pygame.mixer.Sound("Arcade Explo A.wav")
menuClick = pygame.mixer.Sound("buttonclick.wav")
pygame.mixer.music.load("menumusic1.wav")
music_playing = True
pygame.mixer.music.play(-1)
mRollover = True
menuRollover = pygame.mixer.Sound("buttonrollover.wav")

size = [700, 500]
screen = pygame.display.set_mode(size)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
display_width = 800
display_height = 600

blauw = (110,255,255)
WHITE = (255,255,255)
zwart = (0,0,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
aqua = (0,255,255)
light_red = (255,0,0)
light_green = (0,255,0)
grey = (160,160,160)
red = (200,0,0)
green = (0,200,0)
blue = (0,0,200)
bright_red = (255,0,0)
bright_green = (0,255,0)    
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
yellow = (200,200,0)
light_yellow = (255,255,0)
aqua = (0,255,255)
light_red = (255,0,0)
light_green = (0,255,0)
black = (0,0,0)
grey = (160,160,160)
white = (255,255,255)
red = (200,0,0)
lightblue = (51,255,255)
purple = (255,0,255)
bright_purple = (255,153,204)
green = (0,200,0)
blue = (0,0,200)
bright_red = (255,0,0)
bright_green = (0,255,0)
yellow = (200,200,0)
light_yellow = (255,255,0)
green = (34,177,76)
light_green = (0,255,0)

largeText = pygame.font.Font('freesansbold.ttf',115)
smallText = pygame.font.Font("freesansbold.ttf",12)
largeText = pygame.font.Font("freesansbold.ttf",30)
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Coma')
clock = pygame.time.Clock()

charImg = pygame.image.load('ger_up1.png')
charImg2 = pygame.image.load('ger_down1.png')
charMini = pygame.transform.scale(charImg2, (25, 25))
img = pygame.image.load('ger_up1.png')
achtergrond = pygame.image.load("paddle.png")
background = pygame.image.load('coma2.png').convert()
background2 = pygame.image.load('backg.png').convert()
background2_rect = background.get_rect()
mobImg = pygame.image.load('gerdark.png')
bulletImg = pygame.image.load('bullet.png')
rocketImg = pygame.image.load('Gervinho in raket.png')
cloudImg = pygame.image.load('one cloud.png')

score = 0
pause = False

explosion_anim = {}
explosion_anim['enemy'] = []

done = False

# Start positie van Rechthoek
rect_x = 50
rect_y = 50
 
# Snelheid en richting van Rechthoek
rect_change_x = 5
rect_change_y = 5
 
# Font van de tekst van het scherm (Grootte 36)
font = pygame.font.Font(None, 36)
font1 = pygame.font.Font(None, 50)
font2 = pygame.font.Font(None, 40)

display_instructions = True
instruction_page = 1

def text_objects2(text, font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = charImg
        self.image.set_colorkey(white)
        self.rect = self.image.get_rect()
        self.rect.centerx = display_width/2
        self.rect.bottom = display_height - 10
        self.speedx = 0
        self.speedy = 0
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        


    def update(self):
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 100:
            self.hidden = False
            self.rect.centerx = display_width/2
            self.rect.bottom = display_height -10
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -5
        if keystate[pygame.K_RIGHT]:
            self.speedx = +5
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = +5
        if keystate[pygame.K_SPACE]:
            self.shoot()
        if self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > display_height:
            self.rect.bottom = display_height
        if self.rect.top < 0:
            self.rect.top = 0

        
        self.rect.x += self.speedx
        self.rect.y += self.speedy


    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)

    def hide(self):
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (display_width/2, display_height + 200)

class Mob (pygame.sprite.Sprite):
    global gameover
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = mobImg
        self.image.set_colorkey(black)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(display_width - self.rect.width)
        self.rect.y = random.randrange(-100,-40)
        self.speedy = random.randrange(5,8)
        self.speedx = random.randrange(-3,3)

        
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > display_height + 10 or self.rect.left < -25 or self.rect.right > display_width + 20:
            self.rect.x = random.randrange(display_width - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(5,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(bulletImg, (20,20))
        self.rect = self.image.get_rect() 
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

for i in range(9):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(filename)
    img_enemy = pygame.transform.scale(img, (75,75))
    explosion_anim['enemy'].append(img_enemy)

def unpaused():
    global pause
    pause = False

def paused():

    
    
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects1("Paused", largeText, black)
        TextRect.center = ((display_width/2),(display_height/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("Continue",150,450,100,50,green,bright_green,unpaused)
        button("Quit",550,450,100,50,red,bright_red,game_intro)

        pygame.display.update()
        clock.tick(15)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)



def mute():
    global music_playing
    if music_playing == True:
        pygame.mixer.music.stop()
        music_playing = False
    else:
        pygame.mixer.music.play(-1)
        music_playing = True

def quitgame():
    pygame.quit()
    quit()

def button(msg,x,y,w,h,ic,ac,action=None):
    global mRollover
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        gameDisplay.blit(text, (x,y))
        
        if mRollover == True:
            pygame.mixer.Sound.play(menuRollover)
            mRollover = False
        


        if click[0] == 1 and action !=None:
            pygame.mixer.Sound.play(menuClick)
            action()
    
    
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        gameDisplay.blit(text, (x,y))

def game_intro():
    
    global music_playing
        
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.blit(background, (-10, 0))

        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("Coma", largeText, red)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        button("Start",50,300,100,25,white,red,minigame)
        button("Highscore",50,350,100,25,white,red,highscore)
        button("Help",50,400,100,25,white,red,help)
        button("Quit",50,500,100,25,white,red,quitgame)
        button("Credits",50,450,100,25,white,red,crdts)
        if music_playing == True:
            button("Mute",700,550,100,25,white,red,mute)
        else:
            button("Unmute",700,550,100,25,white,red,mute)
  
        pygame.display.update()
        clock.tick(15)

def highscore():
    
    highscore = True
    while crdts:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("Highscore", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def Win1():
    global mgame1
    global score
    mgame1 = True
    Win1 = True
    while Win1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        button("Try again",350,500,100,25,white,red,game_loop)
        button("Continue",100,500,100,25,white,red,minigame)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("YOU WON", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        draw_text(gameDisplay, "your score was:", 18, display_width/2, display_height/2)
        draw_text(gameDisplay, str(score), 40, display_width/2, 350)
        pygame.display.update()
        clock.tick(15)

def dead():
    
    dead = True
    while dead:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        button("Try again",100,500,100,25,white,red,game_loop)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("YOU DIED", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        draw_text(gameDisplay, "your score was:", 18, display_width/2, display_height/2)
        draw_text(gameDisplay, str(score), 40, display_width/2, 350)
        pygame.display.update()
        clock.tick(15)

def crdts():
    crdts = True
    while crdts:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("Credits", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def helpgame1():
    helpgame1 = True
    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        button("Start",100,500,100,25,white,red,game_loop)
        Text = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects1("Press space to shoot", Text, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        Text = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects1("Use arows to move", Text, black)
        TextRect.center = ((display_width/2), (display_height/3))
        gameDisplay.blit(TextSurf, TextRect)
        Text = pygame.font.Font('freesansbold.ttf',20)
        TextSurf, TextRect = text_objects1("Press p to pause", Text, black)
        TextRect.center = ((display_width/2), 250)
        gameDisplay.blit(TextSurf, TextRect)
        draw_text(gameDisplay, "Get at least 100", 20, display_width/2, 300)
        pygame.display.update()
        clock.tick(15)

def help():
    help = True
    while help:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        gameDisplay.fill(blue)
        button("Go back",600,500,100,25,white,red,game_intro)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("Help", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        pygame.display.update()
        clock.tick(15)

def minigame():
    minigame = True
    while minigame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(blue)
        largeText = pygame.font.Font('freesansbold.ttf',115)
        TextSurf, TextRect = text_objects1("Minigames", largeText, black)
        TextRect.center = ((display_width/2), (display_height/4))
        gameDisplay.blit(TextSurf, TextRect)
        button("Minigame 1",250,300,100,25,white,red,helpgame1)
        button("Minigame 2",250,350,100,25,white,red,joyce)
        button("Minigame 3",250,400,100,25,white,red,main)     
        button("Minigame 4",425,300,100,25,white,red,mo_h)
        button("Minigame 5",425,350,100,25,white,red,game_meryem)
        button("Minigame 6",425,400,100,25,white,red,mo_k)   
        button("Go back",600,500,100,25,white,red,game_intro)
        pygame.display.update()
        clock.tick(15)

def text_objects1(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_display(text):
    
    TextSurf, TextRect = text_objects(text, largeText, black)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)


    pygame.display.update()
    game_loop()

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font('freesansbold.ttf', size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def game_loop():
    global score
    global pause
    global all_sprites
    global mobs
    global bullets
    global player
    pygame.mixer.music.stop()
    
    
    
    running = True
    
    gameExit = False
    
    game_over = True
    while running:
        if game_over:
           
            game_over = False
            score = 0
            all_sprites = pygame.sprite.Group()
            mobs = pygame.sprite.Group()
            bullets = pygame.sprite.Group()
            player = Player()
            all_sprites.add(player)
            for i in range(15):
                m = Mob()
                all_sprites.add(m)
                mobs.add(m) 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused()
                
        clock.tick(60)
        
        
        all_sprites.update()
        
        hits = pygame.sprite.groupcollide(mobs, bullets, True, True)
        for hit in hits:
            score += 1
            expl = Explosion(hit.rect.center, 'enemy')
            all_sprites.add(expl)
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)

        hits = pygame.sprite.spritecollide(player, mobs, True)
        for hit in hits:
            explo = Explosion(player.rect.center, 'enemy')
            all_sprites.add(explo)
            m = Mob()
            all_sprites.add(m)
            mobs.add(m)
            player.hide()
            player.lives -= 1
            
            if player.lives == 0:
                game_over = True
                if score > 100:
                    Win1()
                else:
                    dead()


        gameDisplay.fill(black)
        gameDisplay.blit(background2, background2_rect)
        all_sprites.draw(gameDisplay)
        draw_text(gameDisplay, str(score), 18, display_width/2, 10)
        draw_lives(gameDisplay, display_width-100, 5, player.lives, charMini)


        pygame.display.update()
        

#####Joyce#####
def rocket(x,y):
    gameDisplay.blit(rocketImg,(x,y))

def cloud(x,y):
    gameDisplay.blit(cloudImg,(x,y))

def paused2():
    paused2 = True
    clicked = False
    while paused2 :
        for event in pygame.event.get():
            print (event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            
        gameDisplay.fill(lightblue)
        TextSurf, TextRect = text_objects2("pause", largeText)
        TextRect.center = ((display_width/2), (display_height/3.5))
        gameDisplay.blit(TextSurf, TextRect)
            
        mouse = pygame.mouse.get_pos()
        
        if 150 + 100 > mouse [0] > 150 and 450 + 50 > mouse [1] > 450:
            pygame.draw.rect(gameDisplay, bright_purple, (150,450,100,50))
            if clicked:
                paused2 = False
        else:
            pygame.draw.rect(gameDisplay, purple, (150,450,100,50))   
        
        textSurf, textRect = text_objects2("CONTINUE",smallText)
        textRect.center = ((150+(100/2)),(450+(50/2)) )
        gameDisplay.blit(textSurf, textRect)
              
        pygame.display.update()
        clock.tick(60)


def game_intro2():
    intro = True
    clicked = False
    while intro:
        for event in pygame.event.get():
            print (event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
            
        gameDisplay.fill(lightblue)
        TextSurf, TextRect = text_objects2("Gervinho's rocket flight", largeText)
        TextRect.center = ((display_width/2), (display_height/3.5))
        gameDisplay.blit(TextSurf, TextRect)
            
         

        TextSurf, TextRect = text_objects2("TRY TO STAY ALIVE FOR 30 SECONDS BY DODGING THE MOVING CLOUDS YOU HAVE GOT 3 LIVES GOOD LUCK!" , smallText)
        TextRect.center = ((display_width/2), (display_height/2.5))
        gameDisplay.blit(TextSurf, TextRect)
        
        TextSurf, TextRect = text_objects2("PRESS P FOR PAUSE", smallText)
        TextRect.center = ((display_width/2), (display_height/2))
        gameDisplay.blit(TextSurf, TextRect)


        mouse = pygame.mouse.get_pos()

        #print (mouse)

        if 150 + 100 > mouse [0] > 150 and 450 + 50 > mouse [1] > 450:
            pygame.draw.rect(gameDisplay, bright_green, (150,450,100,50))
            if clicked:
                return True
        else:
            pygame.draw.rect(gameDisplay, green, (150,450,100,50))
                
        if 550 + 100 > mouse [0] > 550 and 450 + 50 > mouse [1] > 450:
            pygame.draw.rect(gameDisplay, bright_red, (550,450,100,50))
            if clicked:
                return False
        else:
            pygame.draw.rect(gameDisplay, red, (550,450,100,50))

        textSurf, textRect = text_objects2("PLAY", smallText)
        textRect.center = ((150+(100/2)),(450+(50/2)) )
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = text_objects2("MENU", smallText)
        textRect.center = ((550+(100/2)),(450+(50/2)) )
        gameDisplay.blit(textSurf, textRect)

        pygame.display.update()
        clock.tick(60)
                    
def game_outro(Lives):
         outro = True
         clicked = False
         while outro:
            for event in pygame.event.get():
                print (event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clicked = True
                if event.type == pygame.MOUSEBUTTONUP:
                    clicked = False

            gameDisplay.fill(lightblue)
            if Lives <= 0:
                    
                textsurf, textRect = text_objects2("YOU DIED", largeText)
                textRect.center = ( (350+(90/2)), (300+(90/2)) )
                gameDisplay.blit(textsurf, textRect)
            
            if Lives > 0:
                textsurf, textrect = text_objects2("YOU WON! CONGRATULATIONS!", largeText)
                textrect.center = ((display_width/2), (display_height/1.5))
                gameDisplay.blit(textsurf, textrect)

            mouse = pygame.mouse.get_pos()

            #print (mouse)

    
                
            if 550 + 100 > mouse [0] > 550 and 450 + 50 > mouse [1] > 450:
                pygame.draw.rect(gameDisplay, bright_red, (550,450,100,50))
                if clicked:
                    return False
            else:
                pygame.draw.rect(gameDisplay, red, (550,450,100,50))

          
            textsurf, textrect = text_objects2("MENU", smallText)
            textrect.center = ((550+(100/2)),(450+(50/2)) )
            gameDisplay.blit(textsurf, textrect)
            
            if 150 + 100 > mouse [0] > 150 and 450 + 50 > mouse [1] > 450:
                pygame.draw.rect(gameDisplay, bright_purple, (150, 450, 100, 50))
                if clicked:
                    return False
            else:
                pygame.draw.rect(gameDisplay, purple, (150, 450, 100, 50))

            textsurf, textrect = text_objects2("NEXT GAME", smallText)
            textrect.center = ((150+(100/2)),(450+(50/2)) )
            gameDisplay.blit(textsurf, textrect)




            pygame.display.update()
            clock.tick(60)

def joyce ():
    status_game = game_intro2()
    if status_game:
        gameloop_Lives = game_loop2()
        game_outro(gameloop_Lives)

def game_loop2():   

    rocket_startx =(display_width * 0.88)
    rocket_starty =(display_height * 0.02) 
    rocket_x = rocket_startx
    rocket_y = rocket_starty

    cloud_x = 50
    cloud_y = 100

    cloud2_x = 500
    cloud2_y = 200

    cloud3_x = 300
    cloud3_y = 350

    cloud4_x = 30
    cloud4_y = 550

    cloud5_x = 500
    cloud5_y = 450

    rocket_width = 118
    rocket_height = 68

    cloud_width = 100
    cloud_height = 48

    x_change = 0
    y_change = 0

    Lives = 3

    hit = False

    counter = 0 

    gameExit = False
    timer_start = pygame.time.get_ticks()
    while not gameExit and Lives > 0:
        cloud_x += 2
        cloud2_x += 2
        cloud3_x += 6
        cloud4_x += 2
        cloud5_x += 5

        if cloud_x > display_width:
           cloud_x = 0
           cloud_y = random.randint(0,display_height)
        if cloud2_x > display_width:
           cloud2_x = 0
           cloud2_y = random.randint(0,display_height)
        if cloud3_x > display_width:
           cloud3_x = 0
           cloud3_y = random.randint(0,display_height)
        if cloud4_x > display_width:
           cloud4_x = 0
           cloud4_y = random.randint(0,display_height)
        if cloud5_x > display_width:
           cloud5_x = 0
           cloud5_y = random.randint(0,display_height)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y_change = -5
                elif event.key == pygame.K_DOWN:
                    y_change = 5

                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

                if event.key == pygame.K_p:
                    paused2_time = pygame.time.get_ticks()-timer_start
                    paused2()
                    unpaused2_time = pygame.time.get_ticks()-timer_start

                    timer_start = timer_start+(unpaused2_time-paused2_time)
        
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                           x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                           y_change = 0

        rocket_x += x_change
        rocket_y += y_change


        gameDisplay.fill(lightblue)

        cloud(cloud_x,cloud_y)
        cloud(cloud2_x,cloud2_y)
        cloud(cloud3_x,cloud3_y)
        cloud(cloud4_x,cloud4_y)
        cloud(cloud5_x,cloud5_y)

        rocket(rocket_x,rocket_y)
    
        if rocket_x + rocket_width > display_width:
           x_change = 0
           rocket_x = display_width-rocket_width
        if rocket_x < 0:
            x_change = 0
            rocket_x = 0

        if rocket_y + rocket_height > display_height:
           y_change = 0
           rocket_y = display_height-rocket_height
        if rocket_y < 0:
           y_change = 0
           rocket_y = 0     
       
        if not hit:
            if rocket_x < cloud_x + cloud_width and rocket_x +rocket_width > cloud_x and rocket_y < cloud_y + cloud_height and rocket_y + rocket_height > cloud_y:
                Lives=Lives-1
                counter= 0
                hit=True
            if rocket_x < cloud2_x + cloud_width and rocket_x +rocket_width > cloud2_x and rocket_y < cloud2_y + cloud_height and rocket_y + rocket_height > cloud2_y:
                Lives=Lives-1
                counter= 0
                hit=True

            if rocket_x < cloud3_x + cloud_width and rocket_x +rocket_width > cloud3_x and rocket_y < cloud3_y + cloud_height and rocket_y + rocket_height > cloud3_y:
               Lives=Lives-1
               counter= 0
               hit=True
            if rocket_x < cloud4_x + cloud_width and rocket_x + rocket_width > cloud4_x and rocket_y < cloud4_y + cloud_height and rocket_y + rocket_height > cloud4_y:
               Lives=Lives-1
               counter= 0
               hit=True
            if rocket_x < cloud5_x + cloud_width and rocket_x + rocket_width > cloud5_x and rocket_y < cloud5_y + cloud_height and rocket_y + rocket_height > cloud5_y:
                Lives=Lives-1
                counter= 0
                hit=True
        if hit:
           counter = counter+1
           print(counter)
           if counter > 30:
               hit = False

        textSurf, textRect = text_objects2("LIVES:"+ str(Lives), largeText)
        textRect.center = ( (520+(90/2)), (50+(80/2)) )
        gameDisplay.blit(textSurf, textRect)

        timer_current = pygame.time.get_ticks()-timer_start
        timer_left = 30000 - timer_current

        textSurf, textRect = text_objects2("TIME LEFT:"+ str(timer_left//1000), largeText)
        textRect.center = ( (100+(90/2)), (50+(80/2)) )
        gameDisplay.blit(textSurf, textRect)
        
        if timer_left <= 0:
            return Lives
        pygame.display.update()
        clock.tick(60)
    return Lives

####RAYEN####
class Player2(pygame.sprite.Sprite):
    """
    This class represents the bar at the bottom that the player controls.
    """
 
    # -- Methoden
    def __init__(self):
        """ Constructor function """
 
        # De constructor oproepen
        super().__init__()
 
        # De afbeelding van de speler maken.
        # Dit kan ook een afbeelding zijn.
        width = 40
        height = 60
        self.image = pygame.image.load("ger_down3.png")
 
        # De Afbeelding aan het blok koppelen.
        self.rect = self.image.get_rect()
 
        # De snelheid van de speler bepalen
        self.change_x = 0
        self.change_y = 0
 
        # Lijst van sprites waar we tegen aan kunnen botsen
        self.level = None
 
    def update(self):
        """ Move the player. """
        # Zwaartekracht
        self.calc_grav()
 
        # Rechts en Links bewegen
        self.rect.x += self.change_x
 
        # Kijken of we tegen iets aan botsen
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # Als je naar rechts beweegt,
            # Onze rechterkant tegen de linkerkant van het object zetten al we er tegen aan komen
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # En andersom
                self.rect.left = block.rect.right
 
        # Hoog/Laag
        self.rect.y += self.change_y
 
        # Kijken of we tegen iets aan botsen
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Onze Positie reseten op basis van de objecten
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Onze verticale beweging stoppen
            self.change_y = 0
 
            if isinstance(block, MovingPlatform):
                self.rect.x += block.change_x
 
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # Checken of we op de grond zijn
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
        pygame.mixer.Sound.play(jump)
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
 
class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """
 
    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this code.
            """
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
 
 
class MovingPlatform(Platform):
    """ This is a fancier platform that can actually move. """
    change_x = 0
    change_y = 0
 
    boundary_top = 0
    boundary_bottom = 0
    boundary_left = 0
    boundary_right = 0
 
    player = None
 
    level = None
 
    def update(self):
        """ Move the platform.
            If the player is in the way, it will shove the player
            out of the way. This does NOT handle what happens if a
            platform shoves a player into another object. Make sure
            moving platforms have clearance to push the player around
            or add code to handle what happens if they don't. """
 
        # Move left/right
        self.rect.x += self.change_x
 
        # See if we hit the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # If we are moving right, set our right side
            # to the left side of the item we hit
            if self.change_x < 0:
                self.player.rect.right = self.rect.left
            else:
                # Otherwise if we are moving left, do the opposite.
                self.player.rect.left = self.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
 
        # Check and see if we the player
        hit = pygame.sprite.collide_rect(self, self.player)
        if hit:
            # We did hit the player. Shove the player around and
            # assume he/she won't hit anything else.
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y < 0:
                self.player.rect.bottom = self.rect.top
            else:
                self.player.rect.top = self.rect.bottom
 
        # Check the boundaries and see if we need to reverse
        # direction.
        if self.rect.bottom > self.boundary_bottom or self.rect.top < self.boundary_top:
            self.change_y *= -1
 
        cur_pos = self.rect.x - self.level.world_shift
        if cur_pos < self.boundary_left or cur_pos > self.boundary_right:
            self.change_x *= -1
 
 
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving
            platforms collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        #self.background = None
     
        # How far this world has been scrolled left/right
        self.world_shift = 0
        self.level_limit = -1000
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self, screen):
        """ Draw everything on this level. """
 
        # Draw the background
        screen.fill(WHITE)
        screen.blit(self.background,(self.world_shift // 3,0))
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
    def shift_world(self, shift_x):
        """ When the user moves left/right and we need to scroll everything:
        """
 
        # Keep track of the shift amount
        self.world_shift += shift_x
 
        # Go through all the sprite lists and shift
        for platform in self.platform_list:
            platform.rect.x += shift_x
 
        for enemy in self.enemy_list:
            enemy.rect.x += shift_x
 
 
class Level_01(Level):
    """ Definition for level 1. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        
        
        self.background = pygame.image.load("bg.jpg").convert()
        self.background.set_colorkey(WHITE)
        self.level_limit = -1500
 
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 [70, 600, 1800, 200],
                 [70, 600, 2000, 100],
                 [70, 600, 2300, 75],]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
        # Add a custom moving platform
        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1600
        block.change_x = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)
 
 
class Level_02(Level):
    """ Definition for level 2. """
 
    def __init__(self, player):
        """ Create level 1. """
 
        # Call the parent constructor
        Level.__init__(self, player)
           
        self.background = pygame.image.load("wallpaper1.png").convert()
        self.background.set_colorkey(BLACK)
        self.level_limit = -2000
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 70, 500, 550],
                 [210, 70, 800, 400],
                 [210, 70, 1000, 500],
                 [210, 70, 1120, 280],
                 [70, 600, 1800, 200],
                 [70, 600, 2000, 100],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 1500
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70, 70)
        block.rect.x = 1700
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = 10
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70, 70)
        block.rect.x = 1600
        block.rect.y = 300
        block.boundary_top = 100
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70, 40)
        block.rect.x = 1350
        block.rect.y = 280
        block.boundary_left = 1350
        block.boundary_right = 1800
        block.change_x = 10
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

 
class Level_03(Level):
    """ Definition for level 3. """
 
    def __init__(self, player):
        """ Create level 3. """
 
        # Call the parent constructor
        Level.__init__(self, player)
        
        
        self.background = pygame.image.load("bg2.jpg").convert()
        self.background.set_colorkey(BLACK)
        self.level_limit = -1500
 
        # Array with type of platform, and x, y location of the platform.
        level = [[210, 70, 100, 400],
                 [210, 70, 400, 550],
                 [210, 70, 400, 300],
                 [210, 70, 200, 150],
                 [70, 600, 600, 100],
                 [70, 600, 800, 50],
                 [210, 100, 1000, 150],
                 [70, 600, 1500, 50],
                 [10, 250, 1800, 50],
                 [210, 70, 1700, 400],
                 [70, 600, 2000, 10],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
 
        # Add a custom moving platform
        block = MovingPlatform(70, 70)
        block.rect.x = 700
        block.rect.y = 0
        block.boundary_top = 0
        block.boundary_bottom = 550
        block.change_y = -20
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70, 40)
        block.rect.x = 1100
        block.rect.y = 100
        block.boundary_left = 1100
        block.boundary_right = 1400
        block.change_x = 2
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

        block = MovingPlatform(70, 70)
        block.rect.x = 1900
        block.rect.y = 150
        block.boundary_top = 150
        block.boundary_bottom = 550
        block.change_y = -5
        block.player = self.player
        block.level = self
        self.platform_list.add(block)

def button123(msg,x,y,w,h,ic,ac,action=None):
    global mRollover
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        screen.blit(text, (x,y))
        
        if mRollover == True:
            pygame.mixer.Sound.play(menuRollover)
            mRollover = False
        
        if click[0] == 1 and action !=None:
            pygame.mixer.Sound.play(menuClick)
            action()
    
    
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        screen.blit(text, (x,y))

def text_objects123(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def message_to_screen123(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects123(msg,color,size)
    textRect.center = (int(SCREEN_WIDTH / 2), int(SCREEN_HEIGHT / 2)+y_displace)
    screen.blit(textSurf, textRect)

def victory123():
    message_to_screen123('You escaped!!!',GREEN) 
    pygame.mixer.Sound.play(overwin)
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
        button123("Play Again",150,450,100,50,GREEN,RED,main)
        button123("Menu",350,450,100,50,BLUE,WHITE,minigame)
        button123("Next Game",550,450,100,50,RED,GREEN,mo_h)
        pygame.display.update()
        clock.tick(60) 
        
def crashed123():
    message_to_screen123('You Lose!',RED)
    pygame.mixer.Sound.play(doodzijn)
    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        
        button123("Play Again",150,450,100,50,BLUE,RED,main)
        button123("Quit",550,450,100,50,RED,RED,minigame)
        pygame.display.update()
        clock.tick(60) 

def unpaused3():
    global pause
    pause = False

def paused3():

    
    
    pygame.mixer.Sound.play(puazu)
    while pause:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = text_objects3("Paused", largeText, BLACK)
        TextRect.center = ((SCREEN_WIDTH/2),(SCREEN_HEIGHT/2))
        screen.blit(TextSurf, TextRect)

        button123("Continue",150,450,100,50,GREEN,WHITE,unpaused3)
        button123("Play Again",350,450,100,50,BLUE,RED,crashed123)
        button123("Quit",550,450,100,50,RED,WHITE,minigame)
        
        pygame.display.update()
        clock.tick(15)
 
def text_objects3(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def button2(msg,x,y,w,h,ic,ac,action=None):
    global mRollover
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        screen.blit(text, (x,y))
        

        if click[0] == 1 and action !=None:
            action()
    
    
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        screen.blit(text, (x,y))

def main():
    """ Main Program """
    pygame.init()
    global pause
    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)
 
    pygame.display.set_caption("Prison Break")
 
    # Create the player
    player = Player2()
 
    # Create all the levels
    level_list = []
    level_list.append(Level_01(player))
    level_list.append(Level_02(player))
    level_list.append(Level_03(player))
    pygame.mixer.Sound.play(entering)
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    active_sprite_list = pygame.sprite.Group()
    player.level = current_level
 
    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)
 
    # Loop until the user clicks the close button.
    done = False
 
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
 
    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = True
                    paused3()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()
 
        # Update the player.
        active_sprite_list.update()
 
        # Update items in the level
        current_level.update()
 
        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right >= 500:
            diff = player.rect.right - 500
            player.rect.right = 500
            current_level.shift_world(-diff)
 
        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left <= 120:
            diff = 120 - player.rect.left
            player.rect.left = 120
            current_level.shift_world(diff)
 
        # If the player gets to the end of the level, go to the next level
        current_position = player.rect.x + current_level.world_shift
        if current_position < current_level.level_limit:
            if current_level_no < len(level_list)-1:
                player.rect.x = 120
                current_level_no += 1
                current_level = level_list[current_level_no]
                player.level = current_level
            else:
                # Out of levels. This just exits the program.
                # You'll want to do something better.
                victory123()
 
        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
       
        

        
         # --- Timer going up ---
        font = pygame.font.Font(None, 25)
 
        frame_count = 0
        frame_rate = 60
        start_time = 90
    # Calculate total seconds
        total_seconds = frame_count // frame_rate
 
    # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
 
    # Use python string formatting to format in leading zeros
        output_string = "Time: {0:02}:{1:02}".format(minutes, seconds)
 
    # Blit to the screen
        text = font.render(output_string, True, BLACK)
        screen.blit(text, [1, 1])
 
    # --- Timer going down ---
    # --- Timer going up ---
    # Calculate total seconds
        total_seconds = start_time - (frame_count // frame_rate)
        if total_seconds < 0:
            total_seconds = 0
 
    # Divide by 60 to get total minutes
        minutes = total_seconds // 60
 
    # Use modulus (remainder) to get seconds
        seconds = total_seconds % 60
 
    # Use python string formatting to format in leading zeros
        output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)
 
    # Blit to the screen
        text = font.render(output_string, True, BLACK)
 
        screen.blit(text, [1, 20])   

        current_level.draw(screen)
        active_sprite_list.draw(screen)
        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
        frame_count += 1



        # Limit to 60 frames per second
        
        clock.tick(frame_rate)
 
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
 
    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.  





###mo.h###
def unpaused4():
    global pause
    pause = False

def text_objects4(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def paused4():
    while pause:
            for event in pygame.event.get():

                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                
            #gameDisplay.fill(white)
            largeText = pygame.font.SysFont("comicsansms",115)
            TextSurf, TextRect = text_objects4("Paused", largeText)
            TextRect.center = ((display_width/2),(display_height/2))
            gameDisplay.blit(TextSurf, TextRect)

            button4("Continue",150,450,100,50,green,bright_green,unpaused4)
            button4("Quit",550,450,100,50,red,bright_red,quit)

            pygame.display.update()
            clock.tick(15)

def button4(msg,x,y,w,h,ic,ac,action=None):
    
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        gameDisplay.blit(text, (x,y))
    
    


        if click[0] == 1 and action !=None:

            action()
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        gameDisplay.blit(text, (x,y))

def victory4():
    message_display4('You lose!')

def win4():
    message_display4('You win!')

def quitgame():
    pygame.quit()
    quit()

def message_display4(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects4(text, largeText)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

def text_objects4(text, font):
    textSurface = font.render(text, True, blauw)
    return textSurface, textSurface.get_rect()

def text_objects4(text, font):
    textSurface = font.render(text, True, red)
    return textSurface, textSurface.get_rect()

class Pong:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.font = pygame.font.Font("freesansbold.ttf", 50)
        self.ball = pygame.Rect(400, 300, 10, 10)
        self.ballAngle = math.radians(0)
        self.ballSpeed = 13
        self.playerScore = 0
        self.opponentScore = 0
        self.direction = -1
        self.playerRects = {
            -60:pygame.Rect(50, 380, 10, 20), # Bottom of paddle
            -45:pygame.Rect(50, 360, 10, 20),
            -30:pygame.Rect(50, 340, 10, 20),
            -0:pygame.Rect(50, 320, 10, 20),
            30:pygame.Rect(50, 300, 10, 20),
            45:pygame.Rect(50, 280, 10, 20),
            60:pygame.Rect(50, 260, 10, 20), # Top of paddle
        }

        self.opponentRects = {
            -60:pygame.Rect(750, 380, 10, 20), # Bottom of paddle
            -45:pygame.Rect(750, 360, 10, 20),
            -30:pygame.Rect(750, 340, 10, 20),
            -0:pygame.Rect(750, 320, 10, 20),
            30:pygame.Rect(750, 300, 10, 20),
            45:pygame.Rect(750, 280, 10, 20),
            60:pygame.Rect(750, 260, 10, 20), # Top of paddle
        }

        self.pause = 10
    
    def drawPlayers(self):
        for pRect in self.playerRects:
            pygame.draw.rect(self.screen, (0,0,0), self.playerRects[pRect])
            pygame.draw.rect(self.screen, (255,0,0), self.playerRects[pRect], 2)

        for oRect in self.opponentRects:
            pygame.draw.rect(self.screen, (0,0,0), self.opponentRects[oRect])
            pygame.draw.rect(self.screen, (0,0,255), self.opponentRects[oRect], 2)

    def updatePlayer(self):
        key = pygame.key.get_pressed()
        if self.ball.y <= 0 or self.ball.y > 595:
            self.ballAngle *= -1

        if key[K_UP]:
            if self.playerRects[60].y > 0:
                for pRect in self.playerRects:
                    self.playerRects[pRect].y -= 25
                
        elif key[K_DOWN]:
            if self.playerRects[-60].y < 590:
                for pRect in self.playerRects:
                    self.playerRects[pRect].y += 25

    def updateBall(self):
        self.ball.x += self.direction * self.ballSpeed * math.cos(self.ballAngle)
        self.ball.y += self.direction * self.ballSpeed * -math.sin(self.ballAngle)
        if self.ball.x > 800 or self.ball.x < 0:
            if self.ball.x > 800:
                self.playerScore += 1
        
            elif self.ball.x < 0:
                self.opponentScore += 1
            self.ball.x = 400
            self.ball.y = 300
            self.ballAngle = math.radians(0)
            self.pause = 10
            if self.opponentScore == 3:
                victory4()
            if self.playerScore == 3:
                win4()
            if self.playerScore == 3 or self.opponentScore == 3:
                quitgame()
    
        if self.direction < 0:
            for pRect in self.playerRects:
                if self.playerRects[pRect].colliderect(self.ball):
                    self.ballAngle = math.radians(pRect)
                    self.direction = 1
                    break

        else:
            for oRect in self.opponentRects:
                if self.opponentRects[oRect].colliderect(self.ball):
                    self.ballAngle = math.radians(oRect)
                    self.direction = -1

    def updateOpponent(self):
        if self.ball.y > self.opponentRects[0].y:
            if self.opponentRects[-60].y > 580:
                return
            for oRect in self.opponentRects:
                self.opponentRects[oRect].y += 6

        elif self.ball.y < self.opponentRects[0].y:
            if self.opponentRects[60].y <= 0:
                return
            for oRect in self.opponentRects:
                self.opponentRects[oRect].y -= 6
                 
    def run(self):
        global pause
        clock = pygame.time.Clock()
        while True:
            achtergrond = pygame.image.load("paddle.png") 
            gameDisplay.blit(achtergrond,(0,0))
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        pause = True
                        paused4()
            pygame.draw.rect(self.screen, (110,255,255), self.ball)
            pygame.draw.rect(self.screen, (0,0,0), self.ball, 1)
            self.screen.blit(self.font.render(str(self.playerScore), -1, (0,0,0)), (200, 25))
            self.screen.blit(self.font.render(str(self.opponentScore), -1, (0,0,0)), (600, 25))
            self.drawPlayers()
            self.updatePlayer()
            self.updateOpponent() 
            if self.pause:
                self.pause -= 1
            else:
                self.updateBall()

            pygame.display.flip()
def mo_h():
    Pong().run()





###Meryam###

tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth = 5
ground_height = 35

background3 = pygame.image.load("ger_left1.png")


def score5(score):
    text = smallfont.render("Score: "+str(score), True, black)
    gameDisplay.blit(text, [0,0])
    
def text_objects5(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def text_to_button(msg, color, buttonx, buttony, buttonwidth, buttonheight, size = "small"):
    textSurf, textRect = text_objects(msg,color,size)
    textRect.center = ((buttonx+(buttonwidth/2)), buttony+(buttonheight/2))
    gameDisplay.blit(textSurf, textRect)
   
def message_to_screen(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects5(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def tank(x,y,turPos):
    x = int(x)
    y = int(y)
    possibleTurrets = [(x-27, y-2),
                       (x-26, y-5),
                       (x-25, y-8),
                       (x-23, y-12),
                       (x-20, y-14),
                       (x-18, y-15),
                       (x-15, y-17),
                       (x-13, y-19),
                       (x-11, y-21)
                       ]
  
    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
       
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)
    return possibleTurrets[turPos]

def enemy_tank(x,y,turPos):
    x = int(x)
    y = int(y)
    possibleTurrets = [(x+27, y-2),
                       (x+26, y-5),
                       (x+25, y-8),
                       (x+23, y-12),
                       (x+20, y-14),
                       (x+18, y-15),
                       (x+15, y-17),
                       (x+13, y-19),
                       (x+11, y-21)
                       ]
  
    pygame.draw.circle(gameDisplay, black, (x,y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x-tankHeight, y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x,y), possibleTurrets[turPos], turretWidth)
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
       
    pygame.draw.circle(gameDisplay, black, (x-15, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x-5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+5, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+10, y+20), wheelWidth)
    pygame.draw.circle(gameDisplay, black, (x+15, y+20), wheelWidth)
    return possibleTurrets[turPos]

def pause5():
    paused = True
    message_to_screen("Paused",black,-100,size="large")
    message_to_screen("Press C to continue playing or Q to quit",red,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        
        clock.tick(5)

def barrier(xlocation,randomHeight, barrier_width):
    
    pygame.draw.rect(gameDisplay, black, [xlocation, display_height-randomHeight, barrier_width,randomHeight])
    
def explosion5(x, y, size=50):
    pygame.mixer.Sound.play(explosion_sound)
    explode = True
    while explode:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        startPoint = x,y
        colorChoices = [red, light_red, yellow, light_yellow]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x +random.randrange(-1*magnitude,magnitude)
            exploding_bit_y = y +random.randrange(-1*magnitude,magnitude)
            pygame.draw.circle(gameDisplay, colorChoices[random.randrange(0,4)], (exploding_bit_x,exploding_bit_y),random.randrange(1,5))
            magnitude += 1
            pygame.display.update()
            clock.tick(100)
        explode = False
        
def fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,enemyTankX, enemyTankY):
    pygame.mixer.Sound.play(fire_sound)
    fire = True
    damage = 0
    startingShell = list(xy)
    print("FIRE!",xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #print(startingShell[0],startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)
        startingShell[0] -= (12 - turPos)*2
        # y = x**2
        startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(gun_power/50))**2) - (turPos+turPos/(12-turPos)))
        if startingShell[1] > display_height-ground_height:
            print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:", hit_x,hit_y)
            
            if enemyTankX + 10 > hit_x > enemyTankX - 10:
                print("Critical Hit!")
                damage = 25
            elif enemyTankX + 15 > hit_x > enemyTankX - 15:
                print("Hard Hit!")
                damage = 18
            elif enemyTankX + 25 > hit_x > enemyTankX - 25:
                print("Medium Hit")
                damage = 10
            elif enemyTankX + 35 > hit_x > enemyTankX - 35:
                print("Light Hit")
                damage = 5
            
            
            explosion5(hit_x,hit_y)
            fire = False
        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight
        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            print("Impact:", hit_x,hit_y)
            explosion5(hit_x,hit_y)
            fire = False
            
        pygame.display.update()
        clock.tick(60)
    return damage
        
def e_fireShell(xy,tankx,tanky,turPos,gun_power,xlocation,barrier_width,randomHeight,ptankx,ptanky):
    pygame.mixer.Sound.play(fire_sound)
    damage = 0
    currentPower = 1
    power_found = False
    while not power_found:
        currentPower += 1
        if currentPower > 100:
            power_found = True
        #print(currentPower)
        fire = True
        startingShell = list(xy)
        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            #pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)
            startingShell[0] += (12 - turPos)*2
            startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(currentPower/50))**2) - (turPos+turPos/(12-turPos)))
            if startingShell[1] > display_height-ground_height:
                hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
                hit_y = int(display_height-ground_height)
                #explosion(hit_x,hit_y)
                if ptankx+15 > hit_x > ptankx - 15:
                    print("target acquired!")
                    power_found = True
                fire = False
            check_x_1 = startingShell[0] <= xlocation + barrier_width
            check_x_2 = startingShell[0] >= xlocation
            check_y_1 = startingShell[1] <= display_height
            check_y_2 = startingShell[1] >= display_height - randomHeight
            if check_x_1 and check_x_2 and check_y_1 and check_y_2:
                hit_x = int((startingShell[0]))
                hit_y = int(startingShell[1])
                #explosion(hit_x,hit_y)
                fire = False
    
    
    fire = True
    startingShell = list(xy)
    print("FIRE!",xy)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        #print(startingShell[0],startingShell[1])
        pygame.draw.circle(gameDisplay, red, (startingShell[0],startingShell[1]),5)
        startingShell[0] += (12 - turPos)*2
        # y = x**2
        gun_power = random.randrange(int(currentPower*0.90), int(currentPower*1.10))
        
        startingShell[1] += int((((startingShell[0]-xy[0])*0.015/(gun_power/50))**2) - (turPos+turPos/(12-turPos)))
        if startingShell[1] > display_height-ground_height:
            print("last shell:",startingShell[0],startingShell[1])
            hit_x = int((startingShell[0]*display_height-ground_height)/startingShell[1])
            hit_y = int(display_height-ground_height)
            print("Impact:",hit_x,hit_y)
            if ptankx + 10 > hit_x > ptankx - 10:
                print("Critical Hit!")
                damage = 25
            elif ptankx + 15 > hit_x > ptankx - 15:
                print("Hard Hit!")
                damage = 18
            elif ptankx + 25 > hit_x > ptankx - 25:
                print("Medium Hit")
                damage = 10
            elif ptankx + 35 > hit_x > ptankx - 35:
                print("Light Hit")
                damage = 5
            
            explosion5(hit_x,hit_y)
            fire = False
        check_x_1 = startingShell[0] <= xlocation + barrier_width
        check_x_2 = startingShell[0] >= xlocation
        check_y_1 = startingShell[1] <= display_height
        check_y_2 = startingShell[1] >= display_height - randomHeight
        if check_x_1 and check_x_2 and check_y_1 and check_y_2:
            print("Last shell:",startingShell[0], startingShell[1])
            hit_x = int((startingShell[0]))
            hit_y = int(startingShell[1])
            print("Impact:", hit_x,hit_y)
            explosion(hit_x,hit_y)
            fire = False
        
        
        pygame.display.update()
        clock.tick(60)
    return damage

def power(level):
    text = smallfont.render("Power: "+str(level)+"%",True, black)
    gameDisplay.blit(text, [display_width/2,0])

def game_over5():
    game_over = True
    while game_over:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("Game Over",green,-100,size="large")
        message_to_screen("You died.",black,-30)
        button("Go back",600,500,100,25,green,red,minigame)
        
        pygame.display.update()
        clock.tick(15)
def you_win5():
    win = True
    while win:
        for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
        gameDisplay.fill(white)
        message_to_screen("You won!",green,-100,size="large")
        message_to_screen("Congratulations!",black,-30)
        button("Go back",600,500,100,25,green,red,minigame)
        pygame.display.update()
        clock.tick(15)

def health_bars(player_health, enemy_health):
    if player_health > 75:
        player_health_color = green
    elif player_health > 50:
        player_health_color = yellow
    else:
        player_health_color = red
    if enemy_health > 75:
        enemy_health_color = green
    elif enemy_health > 50:
        enemy_health_color = yellow
    else:
        enemy_health_color = red
    pygame.draw.rect(gameDisplay, player_health_color, (680, 25, player_health, 25))
    pygame.draw.rect(gameDisplay, enemy_health_color, (20, 25, enemy_health, 25))

def game_meryem():
    pygame.mixer.music.stop()

    gameExit = False
    gameOver = False
    FPS = 15
    player_health = 100
    enemy_health = 100
    barrier_width = 50
    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    tankMove = 0
    currentTurPos = 0
    changeTur = 0
    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9
    
    fire_power = 80
    power_change = 0
    xlocation = (display_width/2) + random.randint(-0.1*display_width, 0.1*display_width) 
    randomHeight = random.randrange(display_height*0.1,display_height*0.5)
    
    while not gameExit:
        
        
        if gameOver == True:
            #gameDisplay.fill(white)
            message_to_screen("Game Over",red,-50,size="large")
            message_to_screen("Press C to play again or Q to exit",red,50)
            pygame.display.update()
            while gameOver == True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameExit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_c:
                            gameLoop()
                        elif event.key == pygame.K_q:
                            
                            gameExit = True
                            gameOver = False
         
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tankMove = -5
                    
                elif event.key == pygame.K_RIGHT:
                    tankMove = 5
                    
                elif event.key == pygame.K_UP:
                    changeTur = 1
                    
                elif event.key == pygame.K_DOWN:
                    changeTur = -1
                elif event.key == pygame.K_p:
                    pause5()
                elif event.key == pygame.K_SPACE:
                    
                    damage = fireShell(gun,mainTankX,mainTankY,currentTurPos,fire_power,xlocation,barrier_width,randomHeight,enemyTankX,enemyTankY)
                    enemy_health -= damage
                    possibleMovement = ['f','r']
                    moveIndex = random.randrange(0,2)
                    for x in range(random.randrange(0,10)):
                        if display_width * 0.3 > enemyTankX > display_width * 0.03:
                            if possibleMovement[moveIndex] == "f":
                                enemyTankX += 5
                            elif possibleMovement[moveIndex] == "r":
                                enemyTankX -= 5
                            gameDisplay.fill(white)
                            health_bars(player_health,enemy_health)
                            gun = tank(mainTankX,mainTankY,currentTurPos)
                            enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                            fire_power += power_change
                            power(fire_power)
                            barrier(xlocation,randomHeight,barrier_width)
                            gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])
                            pygame.display.update()
                            clock.tick(FPS)
                            
                            
                        
                    
                    
                    damage = e_fireShell(enemy_gun,enemyTankX,enemyTankY,8,50,xlocation,barrier_width,randomHeight,mainTankX,mainTankY)
                    player_health -= damage
                    
                elif event.key == pygame.K_a:
                    power_change = -1
                elif event.key == pygame.K_d:
                    power_change = 1
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    tankMove = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    changeTur = 0
                    
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    power_change = 0
                
                    
        
        mainTankX += tankMove
        currentTurPos += changeTur
        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0
        if mainTankX - (tankWidth/2) < xlocation+barrier_width:
            mainTankX += 5
            
        gameDisplay.fill(white)
        health_bars(player_health,enemy_health)
        gun = tank(mainTankX,mainTankY,currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
        
        fire_power += power_change
        if fire_power > 100:
            fire_power = 100
        elif fire_power < 1:
            fire_power = 1
        
        
        power(fire_power)
        barrier(xlocation,randomHeight,barrier_width)
        gameDisplay.fill(green, rect=[0, display_height-ground_height, display_width, ground_height])

        gameDisplay.blit(background3, (700,565))

        pygame.display.update()
        if player_health < 1:
            game_over5()
        elif enemy_health < 1:
            you_win5()
        clock.tick(FPS)
    pygame.quit()
    quit()


#####Toevoeging mo.k
block_color = aqua
car_width = 60
carImg = pygame.image.load('ger_up10.png')
Backgrond2 = pygame.image.load('jwz.png')
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)


def button6(msg,x,y,w,h,ic,ac,action=None):
    global mRollover
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        gameDisplay.blit(text, (x,y))
        
        if mRollover == True:
            pygame.mixer.Sound.play(menuRollover)
            mRollover = False
        


        if click[0] == 1 and action !=None:
            pygame.mixer.Sound.play(menuClick)
            action()
    
    
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        gameDisplay.blit(text, (x,y))

def text_objects6(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("dodged: "+str(count), True, white)
    gameDisplay.blit(text,(0,0))

def message_to_screen6(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects6(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def pause6():
    paused = True
    message_to_screen6("Paused",black,-100,size="large")
    message_to_screen6("Press C to continue playing or Q to quit",red,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        
        clock.tick(5)

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))



def message_display6(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects6(text, largeText,aqua)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop2()

def victory6():
    message_to_screen6('You escaped!!',green)    

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        #####Toevoeging mo.k
block_color = aqua
car_width = 60
carImg = pygame.image.load('ger_up10.png')
Backgrond2 = pygame.image.load('jwz.png')
smallfont = pygame.font.SysFont("comicsansms", 25)
medfont = pygame.font.SysFont("comicsansms", 50)
largefont = pygame.font.SysFont("comicsansms", 85)


def button6(msg,x,y,w,h,ic,ac,action=None):
    global mRollover
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
   

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ac))
        gameDisplay.blit(text, (x,y))
        
        if mRollover == True:
            pygame.mixer.Sound.play(menuRollover)
            mRollover = False
        


        if click[0] == 1 and action !=None:
            pygame.mixer.Sound.play(menuClick)
            action()
    
    
    else:
        smallText = pygame.font.Font("freesansbold.ttf",20)
        text = smallText.render(msg, 1, (ic))
        gameDisplay.blit(text, (x,y))

def text_objects6(text, color,size = "small"):
    if size == "small":
        textSurface = smallfont.render(text, True, color)
    if size == "medium":
        textSurface = medfont.render(text, True, color)
    if size == "large":
        textSurface = largefont.render(text, True, color)
    return textSurface, textSurface.get_rect()

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("dodged: "+str(count), True, white)
    gameDisplay.blit(text,(0,0))

def message_to_screen6(msg,color, y_displace = 0, size = "small"):
    textSurf, textRect = text_objects6(msg,color,size)
    textRect.center = (int(display_width / 2), int(display_height / 2)+y_displace)
    gameDisplay.blit(textSurf, textRect)

def pause6():
    paused = True
    message_to_screen6("Paused",black,-100,size="large")
    message_to_screen6("Press C to continue playing or Q to quit",red,25)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False
                    elif event.key == pygame.K_q:
                        pygame.quit()
                        quit()
        
        clock.tick(5)

def things(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])

def car(x,y):
    gameDisplay.blit(carImg,(x,y))



def message_display6(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects6(text, largeText,aqua)
    TextRect.center = ((display_width/2),(display_height/2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)

    game_loop2()

def victory6():
    message_to_screen6('You escaped!!',green)    

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button6("Play Again",150,450,100,50,green,bright_green,mo_k)
        button6("Menu",550,450,100,50,red,green)

        pygame.display.update()
        clock.tick(15)  

def crash():
    message_to_screen6('You Crashed',red)

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button6("Play Again",150,450,100,50,green,bright_green,mo_k)
        button6("Quit",550,450,100,50,red,bright_red,quit)

        pygame.display.update()
        clock.tick(15) 

def mo_k():
        
    pygame.mixer.music.stop()
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0
    gameOver = False
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause6()
                    #paused = True
                    #paused()                     
                    
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        x += x_change
        gameDisplay.blit(Backgrond2,(0,0))

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1        

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()

        if dodged > 1:
            victory6()
            
                         
        pygame.display.update()
        clock.tick(60)
        pygame.quit()
        quit()

        button6("Play Again",150,450,100,50,green,bright_green,mo_k)
        button6("Menu",550,450,100,50,red,green,game_intro)

        pygame.display.update()
        clock.tick(15)  

def crash():
    message_to_screen6('You Crashed',red)

    while True:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        #gameDisplay.fill(white)
        

        button6("Play Again",150,450,100,50,green,bright_green,mo_k)
        button6("Quit",550,450,100,50,red,bright_red,quit)

        pygame.display.update()
        clock.tick(15) 

def mo_k():
        
    pygame.mixer.music.stop()
    
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0

    thing_startx = random.randrange(0, display_width)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    thingCount = 1

    dodged = 0
    gameOver = False
    gameExit = False

    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                if event.key == pygame.K_RIGHT:
                    x_change = 5
                if event.key == pygame.K_p:
                    pause6()
                    #paused = True
                    #paused()                     
                    
                    

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0
        
        x += x_change
        gameDisplay.blit(Backgrond2,(0,0))

        # things(thingx, thingy, thingw, thingh, color)
        things(thing_startx, thing_starty, thing_width, thing_height, block_color)
        
        thing_starty += thing_speed
        car(x,y)
        things_dodged(dodged)

        if x > display_width - car_width or x < 0:
            crash()

        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0,display_width)
            dodged += 1
            thing_speed += 1        

        if y < thing_starty+thing_height:
            print('y crossover')

            if x > thing_startx and x < thing_startx + thing_width or x+car_width > thing_startx and x + car_width < thing_startx+thing_width:
                print('x crossover')
                crash()

        if dodged > 10:
            victory6()
            
                         
        pygame.display.update()
        clock.tick(60)

    pygame.quit()
    quit()



game_intro()
pygame.quit()
quit()
