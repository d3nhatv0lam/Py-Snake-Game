# V.2 -- By D3n
# in version 2, I wanna use class instead of var
#---------------------
#libary
import pygame, sys , time
import random
from pygame.locals import *

#screen set
pygame.init()
pygame.font.init()
font = pygame.font.Font('freesansbold.ttf', 32)
#FPS set
FPS_SET = pygame.time.Clock()

#Global var
title_size = 50
time = 0
get_random_position = lambda:[random.randrange(title_size // 2 , Game_screen.width , title_size) 
                              ,random.randrange(title_size // 2 , Game_screen.width , title_size)]


#color
Gray = (28, 28, 28)
Red = (255,0,0)
Blue = (0,0,255)
Lime = (0,255,0)
Orange = (255, 165, 0)

class Screen():
    def __init__(self, title , width = 800 , height = 800 , fill = Gray):
        self.width = width
        self.height = height
        self.title = title
        self.fill = fill
        self.CurrentState = False
    
    def makeCurrentScreen(self):
        pygame.display.set_caption(self.title)
        self.CurrentState = True
        self.screen = pygame.display.set_mode((self.width,self.height))

    def endCurrentScreen(self):
        self.CurrentState = False

    def CheckUpdate(self,fill):
        self.fill = fill
        return self.CurrentState
    
    def screenUpdate(self):
        if self.CurrentState:
            #vẽ lại nền
            self.screen.fill(self.fill)
    
    def returnTitle(self):
        return self.screen
    
class Snake():
    def __init__(self, head= [0,0,title_size-2 , title_size -2], length = 2 ,dir = (0,0) , moved = False , speed = 120):
        self.head = create_Rect(head)
        self.head.center = get_random_position()
        self.eyes = []
        self.bodys = [self.head.copy()]
        self.length = length
        self.dir = dir
        self.speed = speed
        self.moved = moved
        self.score = self.length
        self.max_score = 0
        self.alive = True
        #decor of snake
        self.up_eyes_dir = []
        self.down_eyes_dir = []
        self.left_eyes_dir = []
        self.right_eyes_dir = []

    def restart(self):
        self.head.center = get_random_position()
        self.eyes = []
        self.bodys = [self.head.copy()]
        self.length = 2
        self.dir = (0,0)
        self.moved = False
        self.score = 0
        self.alive = True

        Game_screen.makeCurrentScreen()

    
    def draw(self):
        for body_part in self.bodys:
            pygame.draw.rect(Game_screen.screen,Lime,body_part)
        for eyes in self.eyes:
            pygame.draw.rect(Game_screen.screen,Red,eyes)
        
    def is_alive(self):
        if self.dir != (0,0):
            #collidelist : Kiểm tra va chạm
            if self.head.collidelist(self.bodys) != -1:
                self.alive = False
        return self.alive

    def move(self,Obj_screen):
        self.head.move_ip(self.dir)
        for eyes in self.eyes:
            eyes.move_ip(self.dir)

        Check_border(Obj_screen,self)

        self.is_alive()
        self.bodys.append(self.head.copy())
        self.bodys = self.bodys[-self.length:]
        self.draw()

        if not self.alive:
            pygame.draw.rect(Game_screen.screen,Orange,self.head)
            for eyes in self.eyes:
                pygame.draw.rect(Game_screen.screen,Red,eyes)
            Game_Over(Obj_screen)
            pygame.display.update()

    def eyes_pos_update(self):
        self.up_eyes_dir = [create_Rect([self.head.left+10,self.head.top+2 ,8,8]),create_Rect([self.head.left+30,self.head.top+2 ,8,8])]
        self.down_eyes_dir = [create_Rect([self.head.left+10,self.head.bottom-10,8,8]),create_Rect([self.head.left+30,self.head.bottom-10,8,8])]
        self.left_eyes_dir = [create_Rect([self.head.left +1,self.head.top+10 ,8,8]) , create_Rect([self.head.left+1,self.head.top+30 ,8,8])]
        self.right_eyes_dir = [create_Rect([self.head.right-10,self.head.top+10 ,8,8]) , create_Rect([self.head.right-10,self.head.top+30,8,8])]

    def change_direction(self,event):
        up_dir = (0, -title_size)
        down_dir = (0,title_size)
        left_dir = (-title_size,0)
        right_dir = (title_size,0)
        self.eyes_pos_update()
        #set direction move & eye direction
        if (event.key == pygame.K_w or event.key == pygame.K_UP) and (self.dir != down_dir):
            self.dir    = up_dir
            self.eyes   = self.up_eyes_dir
        if (event.key == pygame.K_s or event.key == pygame.K_DOWN) and (self.dir != up_dir):
            self.dir    = down_dir
            self.eyes   = self.down_eyes_dir
        if (event.key == pygame.K_a or event.key == pygame.K_LEFT) and (self.dir != right_dir):
            self.dir    = left_dir
            self.eyes   = self.left_eyes_dir
        if (event.key == pygame.K_d or event.key == pygame.K_RIGHT) and (self.dir != left_dir):
            self.dir    = right_dir
            self.eyes   = self.right_eyes_dir


class Food():
    def __init__(self, pos = [0,0,title_size-2 , title_size -2]):
        self.pos = create_Rect(pos)
        self.pos.center = get_random_position()

    def check_draw(self,Obj_snake):
        while self.pos.collidelist(Obj_snake.bodys) != -1 and Obj_snake.score < Cute_snake.max_score:
            self.pos.center = get_random_position()
        pygame.draw.rect(Game_screen.screen,Red, self.pos)

    def eat_food(self,Obj_snake):
        if (Obj_snake.head == self.pos):
            self.pos.center = get_random_position()
            Obj_snake.score += 1
            Obj_snake.length += 1


def create_Rect(Obj_pos):
    return pygame.rect.Rect(Obj_pos[0],Obj_pos[1],Obj_pos[2],Obj_pos[3])

def Check_border(Obj_screen,Obj_snake):
    coordinates = title_size//2
    #out of width window
    if Obj_snake.head.center[0] < 0:
        Obj_snake.head.center = (Obj_screen.width - coordinates ,Obj_snake.head.center[1])
        for eyes in Obj_snake.eyes:
            eyes.center = (eyes.center[0]+Obj_screen.width,eyes.center[1])

    if Obj_snake.head.center[0] > Obj_screen.width:
        Obj_snake.head.center = (coordinates , Obj_snake.head.center[1])
        for eyes in Obj_snake.eyes:
            eyes.center = (eyes.center[0]-Obj_screen.width,eyes.center[1])
    #out of height window
    if Obj_snake.head.center[1] < 0:
        Obj_snake.head.center = (Obj_snake.head.center[0] , Obj_screen.height-coordinates)
        for eyes in Obj_snake.eyes:
            eyes.center = (eyes.center[0],eyes.center[1]+Obj_screen.height)

    if Obj_snake.head.center[1] > Obj_screen.height:
        Obj_snake.head.center = (Obj_snake.head.center[0] , coordinates)
        for eyes in Obj_snake.eyes:
            eyes.center = (eyes.center[0],eyes.center[1]-Obj_screen.height)


def Game_Over(Obj_screen):
    lose = font.render('Game Over', True, Lime, Gray)
    loseRect = lose.get_rect()
    loseRect.center = (Obj_screen.width // 2, Obj_screen.height // 6)
    Obj_screen.screen.blit(lose,loseRect)

    mess = font.render('Press "Space" to restart!', True, Blue, Gray)
    messRect = mess.get_rect()
    messRect.center =(Obj_screen.width // 2, Obj_screen.height // 4)
    Obj_screen.screen.blit(mess,messRect)


    

#game console
Game_screen = Screen("Snake Game Dev by D3n!",600,600)
Game_screen.makeCurrentScreen()
Cute_snake = Snake()
Cute_snake.max_score = ((Game_screen.width*Game_screen.height)//(title_size*title_size))
food = Food()

Running = True
#controler
while Running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False
        if event.type == pygame.KEYDOWN:
            if not Cute_snake.moved:
                Cute_snake.change_direction(event)
                Cute_snake.moved = True
            if not Cute_snake.alive:
                if event.key == pygame.K_SPACE:
                    Cute_snake.restart()
                    
    if Cute_snake.alive:
        time_now = pygame.time.get_ticks()
        if time_now - time > Cute_snake.speed:
            time = time_now
            pygame.display.update()

            Game_screen.screenUpdate()
            food.check_draw(Cute_snake)

            Cute_snake.move(Game_screen)
            food.eat_food(Cute_snake)

            if Cute_snake.score == Cute_snake.max_score:
                win_mess = font.render("You Won!", True, Blue, Gray)
                win_messRect = win_mess.get_rect()
                win_messRect.center =(Game_screen.width // 2, Game_screen.height // 4)
                Game_screen.screen.blit(win_mess,win_messRect)

                show_score = font.render(f"Max Score:{Cute_snake.max_score}",True,Red, Gray)
                show_scoreRect = show_score.get_rect()
                show_scoreRect.center = (Game_screen.width // 2, Game_screen.height // 3)
                Game_screen.screen.blit(show_score,show_scoreRect)

                Cute_snake.alive = False
                pygame.display.update()

            Cute_snake.moved = False
    else:
        Game_screen.endCurrentScreen()

    FPS_SET.tick(60)

pygame.quit()