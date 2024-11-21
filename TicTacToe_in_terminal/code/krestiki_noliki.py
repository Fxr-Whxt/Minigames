

board_size = 3

board = [1,2,3,4,5,6,7,8,9]


        
def draw_board():
    print('____' * board_size)
    for i in range(board_size):
        print((' ' * 3 + '|')*3)
        print('',board[i * 3],  "|",  board[1 + i * 3], '|', board[2 + i * 3], '|')
        print(('_' * 3 + '|')*3)

def game_step(index, char):
    if index > 9 or index < 1 or board[index-1] in ('X', 'O'):
        return False
    
    board[index-1] = char
    return True

def check_win():
    win = False
    current_win = (
    (0,1,2), (3,4,5), (6,7,8), 
    (0,3,6), (1,4,7), (2,5,8),
    (0,4,8), (2,4,6)
    )

    for pos in current_win:
        if board[pos[0]] == board[pos[1]] and board[pos[1]] == board[pos[2]]:
            win = board[pos[0]]

    return win
    

def start_game():
    print('wellcome to tik tak toe!')
    current_player = "X"
    step = 1
    draw_board()

    while step < 10 and check_win() == False:
        index = input('now is: ' + current_player + '. write coordinate ( 0-leave ): ')
        if index == 0:
            break
        if index == str:
            print('niger')
        if game_step(int(index), current_player):
            print('nice balls)')
            
            if (current_player == 'X'):
                current_player = 'O'
            else:
                current_player = "X"


            draw_board()
            step += 1
        else:
            print('Not nice balls)')

    if step == 10:
        print('tie')
    else:
        print('win '+ str(check_win()))
        
    
    


start_game()





















#from tkinter import *
#import random


#tk.mainloop()


#print('hifi')

#import time
#print(time.asctime())

#import turtle
#d = turtle.Pen()
#d.forward(50)
#turtle.done()