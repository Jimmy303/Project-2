import pygame
import random

pygame.init()

display_width = 800
display_height = 600

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
bright_red = (255,102,102)
lightblue = (51,255,255)
green = (0,200,0)
bright_green = (153,255,153)
purple = (255,0,255)
bright_purple = (255,153,204)


gameDisplay = pygame.display.set_mode((display_width,display_height))

smallText = pygame.font.Font("freesansbold.ttf",12)
largeText = pygame.font.Font("freesansbold.ttf",30)

pygame.display.set_caption('Gervinho rocket flight')

clock = pygame.time.Clock()

rocketImg = pygame.image.load('Gervinho in raket.png')

cloudImg = pygame.image.load('one cloud.png')

def rocket(x,y):
    gameDisplay.blit(rocketImg,(x,y))

def cloud(x,y):
    gameDisplay.blit(cloudImg,(x,y))

def text_objects(text, font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()


def quitgame():
    pygame.quit()
    quit()




def pause():
    pause = True
    clicked = False
    while pause :
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
        TextSurf, TextRect = text_objects("pause", largeText)
        TextRect.center = ((display_width/2), (display_height/3.5))
        gameDisplay.blit(TextSurf, TextRect)
            
        mouse = pygame.mouse.get_pos()
        
        if 150 + 100 > mouse [0] > 150 and 450 + 50 > mouse [1] > 450:
            pygame.draw.rect(gameDisplay, bright_purple, (150,450,100,50))
            if clicked:
                pause = False
        else:
            pygame.draw.rect(gameDisplay, purple, (150,450,100,50))   
        
        textSurf, textRect = text_objects("CONTINUE",smallText)
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
        TextSurf, TextRect = text_objects("Gervinho's rocket flight", largeText)
        TextRect.center = ((display_width/2), (display_height/3.5))
        gameDisplay.blit(TextSurf, TextRect)
            
         

        TextSurf, TextRect = text_objects("TRY TO STAY ALIVE FOR 30 SECONDS BY DODGING THE MOVING CLOUDS YOU HAVE GOT 3 LIVES GOOD LUCK!" , smallText)
        TextRect.center = ((display_width/2), (display_height/2.5))
        gameDisplay.blit(TextSurf, TextRect)
        
        TextSurf, TextRect = text_objects("PRESS P FOR PAUSE", smallText)
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

        textSurf, textRect = text_objects("PLAY", smallText)
        textRect.center = ((150+(100/2)),(450+(50/2)) )
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = text_objects("MENU", smallText)
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
                    
                textsurf, textRect = text_objects("YOU DIED", largeText)
                textRect.center = ( (350+(90/2)), (300+(90/2)) )
                gameDisplay.blit(textsurf, textRect)
            
            if Lives > 0:
                textsurf, textrect = text_objects("YOU WON! CONGRATULATIONS!", largeText)
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

          
            textsurf, textrect = text_objects("MENU", smallText)
            textrect.center = ((550+(100/2)),(450+(50/2)) )
            gameDisplay.blit(textsurf, textrect)
            
            if 150 + 100 > mouse [0] > 150 and 450 + 50 > mouse [1] > 450:
                pygame.draw.rect(gameDisplay, bright_purple, (150, 450, 100, 50))
                if clicked:
                    return False
            else:
                pygame.draw.rect(gameDisplay, purple, (150, 450, 100, 50))

            textsurf, textrect = text_objects("NEXT GAME", smallText)
            textrect.center = ((150+(100/2)),(450+(50/2)) )
            gameDisplay.blit(textsurf, textrect)




            pygame.display.update()
            clock.tick(60)

def game_loop():

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
                    pause_time = pygame.time.get_ticks()-timer_start
                    pause()
                    unpause_time = pygame.time.get_ticks()-timer_start

                    timer_start = timer_start+(unpause_time-pause_time)
        
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

        textSurf, textRect = text_objects("LIVES:"+ str(Lives), largeText)
        textRect.center = ( (520+(90/2)), (50+(80/2)) )
        gameDisplay.blit(textSurf, textRect)

        timer_current = pygame.time.get_ticks()-timer_start
        timer_left = 30000 - timer_current

        textSurf, textRect = text_objects("TIME LEFT:"+ str(timer_left//1000), largeText)
        textRect.center = ( (100+(90/2)), (50+(80/2)) )
        gameDisplay.blit(textSurf, textRect)
        
        if timer_left <= 0:
            return Lives
        pygame.display.update()
        clock.tick(60)
    return Lives
    



status_game = game_intro2()
if status_game:
    gameloop_Lives = game_loop()
    game_outro(gameloop_Lives)

pygame.quit()
quit()



