import pygame
import random
from config import *
pygame.init()

#this is the class for the player, x and y is his position, k is his dimensions,
#which can be changed in the config file
class player():
    #this is to initialise the player
    def __init__(self, x, y, k) :
        self.x=x
        self.y=y
        self.k =k
        self.width = k
        self.height = k
    #this is to display the player
    def display_triangle(self):
        gameDisplay.blit(player_img,(self.x,self.y))

#this is the class for the static object
class static_object :
    #this is to initialise it, rand is a random integer that is used to choose 
    #which image it will be and x and y are its positions
    def __init__(self, x, y,rand) :
        self.x=x
        self.y=y
        self.width= 40
        self.height = int((display_height*0.1))
        self.rand = rand
    #this is to display the object, static_image_surface is a list of images,
    #that was made in config file
    def make_object(self):
        gameDisplay.blit(static_image_surface[self.rand],(self.x,self.y))

#this is a class for the moving obstacles
class moving_object():
    def __init__(self,x,y,width,height,color,vel):
        self.x=-1*(width)
        self.y=y
        self.origin_width = width
        self.width = width
        self.height = height
        self.color = color
        self.vel= vel
    #this is to make and move the object (basically draw the object)
    #player_level is the level of the player currently playing,
    #which is given to make the difficulty appropriate
    def make_object(self, player_level):
        self.x= self.x+self.vel + player_level
        self.width = self.origin_width + (10* player_level)
        pygame.draw.rect(gameDisplay, self.color, (self.x, self.y, self.width, self.height))
        if self.x>display_width:
            self.x= (-1)*self.width
            self.vel = random.randint(1,6)
            self.color = color_list_static[random.randint(0,5)]



#this function draws the background, using variables defined in config
def display_background(display_height,display_width,gameDisplay):
    #fills it with blue
    gameDisplay.fill((0,0,255))
    #sets the distance at which the platforms are made
    x=display_height*0.125
    #thickness of the black platforms
    k=display_height*0.02
    while x<=display_height*0.9:
        pygame.draw.rect(gameDisplay, (0,0,0),
                            (0, x, display_width, k))
        x=x+(display_height*0.125)

#this is a function that updates the score of the player1, relative to a
# certain object, certain parameters of whom are given
def check_player_1(player,a_blue,b_black,c_index,t_no,s_add):
    if player.y<=(blue_space*a_blue+black_space*b_black):
        if score_list[t_no][c_index]==0:
            score[t_no]+=s_add+(level[t_no])
            score_list[t_no][c_index]=1

#this is a function that updates the score of player2, relative to a 
# certain object, certain parameters of whom are given
def check_player_2(player,a_blue,b_black,c_index,t_no,s_add):
    if player.y+player.height>=((blue_space)*a_blue-(black_space*b_black)+black_space):
        if score_list[t_no][c_index]==0:
            score[t_no]+=s_add+(level[t_no])
            score_list[t_no][c_index]=1

#this is the function that calls the above two functions appropriately 
#for every obstacle on the game window
def update_score(player1,player2):
    global player_no
    if player_no==0:
        #in this loop, we check whether we need to add any value to the score 
        #due to its position relative to the objects
        for i in range (13):
            if i%2==0:
                check_player_1(player1, int(i/2)+1, 0, i, 0, 10)
            else:
                check_player_1(player1, int(i/2)+1, 1, i, 0, 5)
    elif player_no==1:
        for i in range (13):
            #in this loop, we check whether we need to add any value to the score 
            #due to its position relative to the objects
            if i%2==0:
                check_player_2(player2, int(i/2)+1, 0, i, 1, 10)
            else:
                check_player_2(player2, int(i/2)+2, 1, i, 1, 5)



#this checks if a player and an object have collided,and return true if they 
#have collided
def did_collide(player, obstacle):
    #This is the distance between the x-coordinate centers of the player and object
    x_dif = abs( (player.x + player.width/2) - (obstacle.x+ obstacle.width/2) )
    #this is the minimum x-distance they can be at
    width_len = (float(player.width + obstacle.width)/2)
    #This is the distance between the y-coordinate centers of the player and object
    y_dif = abs( (player.y + player.height/2) - (obstacle.y + obstacle.height/2) )
    #this is the minimum y-distance they can be at
    height_len = (float(player.height + obstacle.height)/2)
    if x_dif<=width_len and y_dif<=height_len:
        return True
    else:
        return False



#this switches the active player whenever needed
def switch_player(player1, player2):
    #this is to put all the players back at their original positions
    player1.x=display_width*0.5
    player1.y=display_height*0.9
    player2.x=display_width*0.5
    player2.y=display_height*0.05
    global player_no    
    #this is to make it point at the new player
    player_no+=1
    player_no=player_no%2
    #these are to check their lives and see if they can't play or if the game needs
    #to be ended
    if lives[player_no]<=0:
        player_no+=1
        player_no=player_no%2
    if lives[player_no]<=0:
        global initial
        initial=True
    #to initialize the time
    time[player_no]=pygame.time.get_ticks()
    global change_in_x
    change_in_x=0
    global change_in_y
    change_in_y=0
    #to reinitialize the score lists
    for i in range (13):
        score_list[0][i]=0
        score_list[1][i]=0



#this puts random integers in arrays, that will be used to generate objects
for i in range(6):
    rand_pos = random.uniform(0,0.9)
    rand_col = random.randint(0,4)
    list_of_positions.append(rand_pos)
    list_of_color_pos.append(rand_col)
    list_of_indexs.append(random.randint(0,4))

#this is used to generate moving objects and put them into a list
for i in range (7):
    moving_nigga = moving_object(0,(blue_space)+(i)*(blue_space),
                    20,black_space,
                    color_list_static[list_of_color_pos[i%5]],random.randint(1,6))
    list_of_moving_objects.append(moving_nigga)






#this makes the two player objects
player1 = player(display_width*0.5, display_height*0.9, player_dim)
player2 = player(display_width*0.5,display_height*0.9, player_dim)



#This is the main loop
while run:
    #This is the home screen
    while initial:
        
        gameDisplay.fill((0,0,0))
        gameDisplay.blit(first_img,(0,0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                initial = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    time[0]=pygame.time.get_ticks()
                    initial=False
                    initialize_var()

        #This is to show the scores
        player_text1 = font2.render("player1 got "+str(score[0]),1,(255,255,255))
        player_text2 = font2.render("player2 got "+str(score[1]),1,(255,255,255))
        #this is to show who won the last game
        gameDisplay.blit(player_text1,(display_width*0.8,display_height*0.1))
        gameDisplay.blit(player_text2,(display_width*0.8,display_height*0.5))
        #displays player 1 as winner if score[0]>score[1]
        if score[0]>score[1]:
            gameDisplay.blit(result_1,(display_width*0.8,display_height*0.9))
        #displays player 2 as winner if score[1]>score[0]
        elif score[1]>score[0]:
            gameDisplay.blit(result_2,(display_width*0.8,display_height*0.9))
        #displayes that there are no winners
        else:
            gameDisplay.blit(result_equal,(display_width*0.8,display_height*0.9))
        pygame.display.update()
    
    #This is to put the game screen background
    display_background(display_height,display_width,gameDisplay)
    
    #this is for checking if we need to quit, or move the player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if player_no==0:
            #This changes a variable that is added to the position of the
            #respective player later, which creates an illusion of movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_in_x=-step_size
                elif event.key == pygame.K_RIGHT:
                    change_in_x=step_size
                elif event.key == pygame.K_UP:
                    change_in_y = -step_size
                elif event.key == pygame.K_DOWN:
                    change_in_y = step_size
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    change_in_x =0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    change_in_y =0
        #this is if the current player is player2
        else :
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    change_in_x=-step_size
                elif event.key == pygame.K_d:
                    change_in_x=step_size
                elif event.key == pygame.K_w:
                    change_in_y = -step_size
                elif event.key == pygame.K_s:
                    change_in_y = step_size
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a or event.key == pygame.K_d:
                    change_in_x =0
                elif event.key == pygame.K_w or event.key == pygame.K_s:
                    change_in_y =0
    #this is to print out the score, and the number of lives
    player_text1 = font.render("player1 got "+str(score[0]),1,(255,255,255))
    player_text2 = font.render("player2 got "+str(score[1]),1,(255,255,255))
    gameDisplay.blit(player_text1,(display_width*0.8,display_height*0.9))
    gameDisplay.blit(player_text2,(display_width*0.8,display_height*0.1))
    player_live1 = font.render("player1 has "+str(lives[0])+" lives left",1,(255,255,255))
    player_live2 = font.render("player2 has "+str(lives[1])+" lives left",1,(255,255,255))
    gameDisplay.blit(player_live1,(display_width*0.1,display_height*0.9))
    gameDisplay.blit(player_live2,(display_width*0.1,display_height*0.1))

    
    #when we update the position of the players, they are drawn in those new
    #positions, that creates the illusion of movement
    if player_no==0:
        player1.x=player1.x+change_in_x
        player1.y=player1.y+change_in_y
    else :
        player2.x=player2.x+change_in_x
        player2.y=player2.y+change_in_y

    #This is to update the score of the player, depending on position
    update_score(player1,player2)

    #This is to show the static objects, and check if the player has crashed into
    #it
    for i in range(6):
        stat = static_object(list_of_positions[i]*display_width, 
                (blue_space+black_space)+(blue_space)*(i), 
                list_of_indexs[i])
        stat.make_object()
        if not crash:
            if player_no==0:
                crash = did_collide(player1,stat)
            else:
                crash = did_collide(player2,stat)

    #this is to print moving objects, and check for collisions 
    for i in range (7):
        list_of_moving_objects[i].make_object(level[player_no])
        if not crash:
            if player_no==0:
                crash = did_collide(player1,list_of_moving_objects[i])
            else:
                crash = did_collide(player2,list_of_moving_objects[i])

    #this is to print the player
    if player_no==0:
        player1.display_triangle()
    else:
        player2.display_triangle()
    
    #This is to check if the player has crossed the finish line, and to update score,
    #and to switch players
    if player_no==0:
        if player1.y<display_height*0.03:
            #to play music on completion
            good_job_sound = pygame.mixer.Sound('./sound/good.wav')
            good_job_sound.play()
            #add time based score
            t = pygame.time.get_ticks() - time[0]
            score[0]+= int(500000/(1+t))
            #switch player
            switch_player(player1,player2)
            level[0]+= 3
    elif player2.y>(display_height*0.97-player_dim):
        #to play music on completion
        good_job_sound = pygame.mixer.Sound('./sound/good.wav')
        good_job_sound.play()
        #add time based score
        t = pygame.time.get_ticks() - time[1]
        score[1]+= int(500000/(1+t))
        #switch players
        switch_player(player1,player2)
        level[1]+= 3
    
    #this is to decrease lives if player has crashed, and to switch player
    if player_no==0:
        if crash:
            #to play sound on failure
            bitch_sound = pygame.mixer.Sound('./sound/bitch.wav')
            bitch_sound.play()
            #decrease number of lives
            lives[0]-=1
            #switch players
            switch_player(player1,player2)
            #if we dont do this, then crash will always be true, and will result
            #in game crashing
            crash=False
    else:
        if crash:
            #to play sound on failure
            bitch_sound = pygame.mixer.Sound('./sound/bitch.wav')
            bitch_sound.play()
            #decrease number of lives
            lives[1]-=1
            #switch players
            switch_player(player1,player2)
            #if we dont do this, then crash will always be true, and will result
            #in game crashing
            crash = False

    #this is to update the screen
    pygame.display.update()
    clock.tick(60)

pygame.quit()