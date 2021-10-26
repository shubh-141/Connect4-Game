# SAPX14's coonect4 is game in which player whose 4 boxes are filled first wins

import numpy as np
import pygame 
import math


ROW_COUNT = 6                               # create variable for number of rows
COL_COUNT = 7                               # create variable for number of columns

# function for making our 6x7 matrix
def create_board():                         
    board = np.zeros((ROW_COUNT,COL_COUNT)) # initialize every element of matrix with value=0
    return board                            # return board i.e our matrix

# function for changing value of element in row or column 
def drop_piece(board ,row ,col ,piece):
    board[row][col] = piece                 # piece here means the striker of player 1 or player 2

# this function ensures that the piece is placed on correct location i.e (mn)th position 
def is_valid_location(board ,col):
    return board[ROW_COUNT-1][col] == 0     # here row-1 is done because index counting starts from 0 so it ends on 5

# this functions verifies whether the element in next row can be used or is occupied
def next_open_row(board ,col):
    for r in range(ROW_COUNT):              # for loop loops over all elements in row
        if board[r][col] == 0:              # if the element is zero i.e unoccupied then return that index
            return r

# prints the board i,e the 6x7 matrix when this function is called
def print_board(board):
    print(np.flip(board , 0))               # flip function is used to add elements from bottom to up because default way is up to down

# function to decide which player wins
def winning(board ,piece):

    # checking rows for win condition  
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT):
            if board[r][c]==piece and board[r][c+1]==piece and board[r][c+2]==piece and board[r][c+3]==piece:
                return True

    # checking columns for win condition              
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c]==piece and board[r+2][c]==piece and board[r+3][c]==piece:
                return True

    # checking for positive diagnol
    for c in range(COL_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c]==piece and board[r+1][c+1]==piece and board[r+2][c+2]==piece and board[r+3][c+3]==piece:
                return True 

    # checking for positive diagnol
    for c in range(COL_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c]==piece and board[r-1][c+1]==piece and board[r-2][c+2]==piece and board[r-3][c+3]==piece:
                return True                

# making actual game board using pygame graphics
def draw_board(board):
    radius = int(pixel_size/2 - 5)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(window ,(0,0,255) ,(c*pixel_size ,r*pixel_size+pixel_size ,pixel_size ,pixel_size))
            pygame.draw.circle(window , (0,0,0) ,(c*pixel_size+50 ,r*pixel_size+pixel_size+50 ) ,radius)
    for c in range(COL_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(window , (255,0,0) ,(c*pixel_size+50 ,height - r*pixel_size-50 ) ,radius)
            elif board[r][c] == 2:
                 pygame.draw.circle(window , (255,255,0) ,(c*pixel_size+50 ,height - r*pixel_size-50 ) ,radius)
    pygame.display.update()

board = create_board()                     # initializes variable for calling create_board function

print_board(board)                         # prints the matrix

game_over = True                           # variable set to true
 
turn = 0                                   # turn variable made to decide which players turn is now , set to 0

# graphic part of code
pygame.init()
pixel_size = 100                           # pixel size variable refers to the length of each block 
width = COL_COUNT*pixel_size               # width of screen here is no.of columns x pixelsize i.e 100x7=700 
height = (ROW_COUNT+1)*pixel_size          # height is (no.of rows+1) x pixelsize i.e 700 extra 100 pixels for gap to be left for loading striker in top of game window 
window = pygame.display.set_mode((width ,height))
draw_board(board)                          # draw board calls the function
pygame.display.update()                    # updates the screen again and again
myfont = pygame.font.SysFont("arial",70)   # declaring a font variable


while game_over:                           # while loop runs until game_over is false 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = False

        # mouse motion is used to track movement of cursor
        if event.type == pygame.MOUSEMOTION:
           
            # draws blank black rectangle after moving cursor to clear previous imgage of red or yellow circle 
            pygame.draw.rect(window ,(0,0,0),(0,0,width ,pixel_size)) 
           
            posx = event.pos[0]           # event.pos is function to obtain cordinate of mouse

            if turn == 0:                 # if turn=0 means player1's turn
                pygame.draw.circle(window , (255,0,0) , (posx , 50) , radius = 45)
            
            else:                         # if turn=1 as incremented in end of code ,then its player2's turn
                pygame.draw.circle(window , (255,255,0) , (posx , 50) , radius = 45)    
       
        pygame.display.update()           # updates the screen 

        if event.type == pygame.MOUSEBUTTONDOWN:    # on mouse click

            # draws blank black rectangle after every click so as to load upcoming striker
            pygame.draw.rect(window ,(0,0,0) , (0,0,width ,pixel_size))

            if turn == 0:  

                # this part is the mechanics of deciding while column to fill by getting position of mouse cursor , col variable is designed such that it rounds of the value to nearest integer after dividing by 100
                # so there are 7 columns 100 pixel wide so 700 pixels , now 1st col is btwn 1-100 ,2nd btwn 100-200 so on , so for example if mouse clicked when x cor =60 so now 60/100 = 0.6 = 1 (roundoff) thus the striker will fall in column 1
                posx = event.pos[0]
                col = int(math.floor(posx/pixel_size)) # floor function is used to roundoff decimals to nearest integers
            
                if is_valid_location(board ,col):  # if the enterd column is correct and empty to be used then ,
                    row = next_open_row(board ,col)# empty row is chosen in that column
                    drop_piece(board ,row ,col ,1) # that empty row gets player1's striker i.e a red coin
                
                    if winning(board ,1):          # if player1 connects4 first then player1 wins 
                        label = myfont.render("Player 1 Wins!",1,(255,0,0)) # as player1 wins a win message is displayed
                        window.blit(label,(150,10)) # this blit function is used to display text when called
                        game_over = False          # as a player wins the var is set to false and loop is ended
        
            else:
                posx = event.pos[0]                # SAME MECHANISM AS PLAYER1
                col = int(math.floor(posx/pixel_size))                
                
                if is_valid_location(board ,col):
                    row = next_open_row(board ,col)
                    drop_piece(board ,row ,col ,2)
                    
                    if winning(board ,2):          # if player2 connect4 first then player2 wins 
                        label = myfont.render("Player 2 Wins!",1,(255,255,0))
                        window.blit(label ,(150,10))
                        game_over = False
                        
        
            print_board(board)   # this function displays the matrix version of our game (see terminal while playing)
            draw_board(board)    # this function enables the main game window of pygame
            turn += 1            # after the above loop is iterated and if it is still true then turn counter is incremented and players get their chance accordingly
            turn = turn%2        # this line of code ensures that when turn is even it is player1's chance and when odd it is player2's chance

            if game_over==False:                  # when game is over var is set to false 
                pygame.time.wait(3000)            # before loop ends there is a delay of 3 seconds and then game window closes automatically