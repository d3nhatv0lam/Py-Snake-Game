#developer : D3n
#----
#libary set
import pygame, sys , time
import random
from pygame.locals import *

#screen set
pygame.init()
pygame.display.set_caption('Snake Game Dev by D3n!')
window = 800
title_size = 40
range = (title_size // 2 , window, title_size)
Game_Screen = pygame.display.set_mode([window ,window])

#color set
Gray = (28, 28, 28)
Red = (255,0,0)
Blue = (0,0,255)
Lime = (0,255,0)
Orange = (255, 165, 0)

#variable set
get_random_position = lambda:[random.randrange(*range) , random.randrange(*range)]
length = 2
Stop_screen = False
#allow snake change dir = False
move = False

    #font
#lose
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Game Over', True, Lime, Gray)
textRect = text.get_rect()
textRect.center = (window // 2, window // 6)
#reset
mess = font.render('Press "Space" to restart!', True, Blue, Gray)
messRect = mess.get_rect()
messRect.center =(window // 2 , window // 4)
#win
win_mess = font.render("You Won!", True, Blue, Gray)
win_messRect = win_mess.get_rect()
win_messRect.center =(window // 2 , window // 3)

#snake define
snake = pygame.rect.Rect([0,0,title_size -2 , title_size -2])
snake.center = get_random_position()
snake_bodys = [snake.copy()]
snake_dir = (0,0)

#food define
food = snake.copy()
food.center = get_random_position()


#FPS set
FPS_SET = pygame.time.Clock()
time , time_step = 0 , 70

#backgound set
Game_Screen.fill(Gray)

def Lose():
    Game_Screen.blit(text, textRect)
    Game_Screen.blit(mess,messRect)
    


def Eat_myself() -> bool:
    if (snake_dir != (0,0)):
        for snake_body in snake_bodys:
            if (snake_body == snake):
                pygame.draw.rect(Game_Screen,Orange,snake_body)
                return True
    return False


def Snake(snake_bodys,Stop_screen):
    #draw snake
    for snakebody in snake_bodys:
        pygame.draw.rect(Game_Screen,Lime,snakebody)
    #move & fill
    snake.move_ip(snake_dir)
    
    if Eat_myself() == True:
        Lose()
        Stop_screen = True
    
    if Stop_screen == False:
        snake_bodys.append(snake.copy())
        snake_bodys = snake_bodys[-length:]
    return snake_bodys , Stop_screen


def Food_eatfood(length):
    #draw food
    pygame.draw.rect(Game_Screen,Red,food)
    #if snake eat food
    if (food == snake):
        length += 1
        food.center = get_random_position()
        #food can't spawn on snake
        for snakebody in snake_bodys:
            if food == snakebody:
                food.center = get_random_position()
            
    return length


def Get_move(event,dir_now)-> tuple:
    # 4 direction of snake
    up_dir = (0, -title_size)
    down_dir = (0,title_size)
    left_dir = (-title_size,0)
    right_dir = (title_size,0)
    #set direction move
    snake_direction = dir_now
    if (event.key == pygame.K_w or event.key == pygame.K_UP) and (dir_now != down_dir):
        snake_direction = up_dir
    if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (dir_now != up_dir):
        snake_direction = down_dir
    if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (dir_now != right_dir):
        snake_direction = left_dir
    if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (dir_now != left_dir):
        snake_direction = right_dir
    return snake_direction


def Border():
    coordinates = title_size//2
    #coordinates (0,0) = (coordinates,coordinates)
    #coordinates (window,0) = (coordinates,window-coordinates)
    #coordinates (0,window) = (window-coordinates,coordinates)
    #coordinates (window , window) = (window-coordinates,window-coordinates)

    #is food spawn in window?
    if (food.left < 0 or food.right > window or food.top < 0 or food.bottom > window):
        food.center = get_random_position()
    
    #snake go out left border
    if (snake.center[0] < coordinates):
        snake.center = (window-coordinates, snake.center[1])
    #snake go out right border
    if (snake.center[0] > window-coordinates ):
        snake.center = (coordinates, snake.center[1])
    #snake go out above border
    if (snake.center[1] < coordinates):
        snake.center = (snake.center[0], window-coordinates)
    #snake go down border
    if (snake.center[1] > window-coordinates):
        snake.center = (snake.center[0], coordinates)
    
#controler
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        #check move
        if event.type == pygame.KEYDOWN:
            if not move:
                snake_dir = Get_move(event,snake_dir)
                move = True
            #reset snake
            if event.key == pygame.K_SPACE:
                if Stop_screen:
                    length = 2
                    snake.center = get_random_position()
                    snake_bodys = [snake.copy()]
                    food.center = get_random_position()
                    snake_dir = (0,0)
                    Stop_screen = False

    if (Stop_screen == False):
        time_now = pygame.time.get_ticks()
        if time_now - time > time_step:
            time = time_now
            Game_Screen.fill(Gray)
            Border()
            snake_bodys , Stop_screen = Snake(snake_bodys,Stop_screen)
            length = Food_eatfood(length)
            move = False
    if length == (window // title_size)**2:
        Game_Screen.blit(win_mess,win_messRect)
        Stop_Screen = True


    #game fps

    pygame.display.flip()
    FPS_SET.tick(60)

