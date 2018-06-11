import pygame

pygame.init()

display_width = 800
display_height = 600

#background colour
white = (255,255,255)
#buttons colours
black = (0,0,0)
red = (255,0,0)
blue = (0,0,255)
green = (0,255,0)
yellow = (255,255,0)
purple = (255,0,255)
#buttons colours while hovering
bright_black = (128,128,128)
bright_red = (255,102,102)
bright_blue = (102,255,255)
bright_green = (153,255,153)
bright_yellow = (255,255,153)
bright_purple = (255,153,204)


gameDisplay = pygame.display.set_mode((display_width,display_height))

pygame.display.set_caption('MainMenu')

clock = pygame.time.Clock()

GameIsRunning = True

largeText = pygame.font.Font('freesansbold.ttf',115)

def text_objects(text, font):
    textSurface = font.render(text,True,black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((display_width/2), (display_height/2))
    gameDisplay.blit (TextSurf, TextRect)

clicked = False





while GameIsRunning:
    gameDisplay.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GameIsRunning = False
        if event.type == pygame.MOUSEMOTION:
            mouse_position = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            clicked = False
    print(mouse_position)
    
    
    if 100+90>mouse_position[0]>100 and 150+90>mouse_position[1]>150:
        pygame.draw.rect(gameDisplay,bright_black,(100,150,90,90))
        if clicked:
            pygame.draw.rect(gameDisplay,white,(100,150,90,90))
    else:
        pygame.draw.rect(gameDisplay,black,(100,150,90,90))


    if 200+90>mouse_position[0]>200 and 150+90>mouse_position[1]>150:
        pygame.draw.rect(gameDisplay,bright_red,(200,150,90,90))
        if clicked:
            pygame.draw.rect(gameDisplay,white,(200,150,90,90))
    else:
        pygame.draw.rect(gameDisplay,red,(200,150,90,90))

    smallText = pygame.font.Font("freesansbold.ttf",12)
    textSurf, textRect = text_objects("rocket flight", smallText)
    textRect.center = ( (200+(90/2)), (150+(90/2)) )
    gameDisplay.blit(textSurf, textRect)




    if 300+90>mouse_position[0]>300 and 150+90>mouse_position[1]>150:
        pygame.draw.rect(gameDisplay,bright_blue,(300,150,90,90))
        if clicked:
            pygame.draw.rect(gameDisplay,white,(300,150,90,90))
    else:
        pygame.draw.rect(gameDisplay,blue,(300,150,90,90))

    if 400+90>mouse_position[0]>400 and 150+90>mouse_position[1]>150:
       pygame.draw.rect(gameDisplay,bright_green,(400,150,90,90))
       if clicked:
            pygame.draw.rect(gameDisplay,white,(400,150,90,90))
    else:
        pygame.draw.rect(gameDisplay,green,(400,150,90,90))
    
    if 500+90>mouse_position[0]>500 and 150+90>mouse_position[1]>150:
        pygame.draw.rect(gameDisplay,bright_yellow,(500,150,90,90))
        if clicked:
            pygame.draw.rect(gameDisplay,white,(500,150,90,90))
    else:
        pygame.draw.rect(gameDisplay,yellow,(500,150,90,90))

    if 600+90>mouse_position[0]>600 and 150+90>mouse_position[1]>150:
        pygame.draw.rect(gameDisplay,bright_purple,(600,150,90,90))
        if clicked:
            pygame.draw.rect(gameDisplay,white,(600,150,90,90))

    else:
        pygame.draw.rect(gameDisplay,purple,(600,150,90,90))
    
    
    
    
    
    
    pygame.display.update()

    clock.tick(60)

pygame.quit()
quit()