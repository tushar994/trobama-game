import pygame
import random
pygame.init()

#this is for the display and game window
pygame.display.set_caption("to win or to lose... that is the challenge")
display_width = 900
display_height = 700
gameDisplay = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
font= pygame.font.SysFont('freesans',20,True,False)
font2= pygame.font.SysFont('freesans',24,True,False)
run = True
initial = True

#this is for the home window
first_img = './images/gandhi.png'
first_img=pygame.image.load(first_img)
first_img=pygame.transform.scale(first_img,(display_height,display_width))

#variables that control the game screen
blue_space = display_height*0.125
black_space = display_height*0.02

#variables that control the stationary objects
stationary_image_width=40
stationary_image_height= int(display_height*0.1)
list_of_images = ['./images/trump.png','./images/obama.png',
                        './images/pope.png', './images/will.png',
                        './images/queen.png']
static_image_surface = []
for i in range(5):
    static_image_surface.append(pygame.image.load(list_of_images[i]))
    static_image_surface[i] = pygame.transform.scale(static_image_surface[i],
                            (stationary_image_width, stationary_image_height))


#game variables that should not be changed unless told
#the first index is for player one, and the second index is for player2,if 
#is it a list with two variables

#can change score, to give someone a headstart
score= [0,0]
crash = False
#level can be changed to increase the starting difficulty
level = [3,3]
#can be changed to give more lives to each player, can be used to handicap one
#   player too
lives = [3,3]
#this is the list that contains the time at which the player started playing
#his/her turn
time = [0,0]
#This is to initialize a list that is used to see if a player has already crossed
#an object
score_list = [ [],[] ]
for i in range(13):
    score_list[1].append(0)
    score_list[0].append(0)
#this is the variable that tells us which player is playing currently
player_no =0
#These two are used to move the players
change_in_x=0
change_in_y=0
#this is a function that initialises the variables everytime the game restarts
#if any changes are made above, make the same changes in this function
def initialize_var():
    global player_no, change_in_x,change_in_y, crash, run,initial,lives ,score, level
    player_no =0
    change_in_x=0
    change_in_y=0
    lives[0] = 3
    lives[1] = 3
    score= [0,0]
    crash = False
    level = [0,0]
    run = True


#lists that will be used to assign random properties to obstacles
#They are filled with values inside game.py
list_of_positions = []
list_of_indexs = []
color_list_static = [ (19, 108, 84), (93, 19, 108), (252, 4, 120),
                    (133, 150, 21) , (147, 66, 20),(147, 20, 20)]
list_of_color_pos = []
list_of_moving_objects = []




#player properties
#player dim is the dimensions of the player
player_dim = 45
player_img = './images/kid.png'
player_img=pygame.image.load(player_img)
player_img=pygame.transform.scale(player_img,(player_dim,player_dim))
#this is the speed of the players, cannot put two different speeds for two
#players, yet
step_size=10

#some text that is displayed
#when player1 wins
result_1 = font2.render("player1 won ",1,(255,255,255))
#when player2 wins
result_2 = font2.render("player2 won ",1,(255,255,255))
#when the scores are equal, or the game hasn't been played yet
result_equal  = font2.render("YOUR MOM GAY",1,(255,255,255))

#to play background music
pygame.mixer.music.load('./sound/song_dude.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

