from tkinter import *
import random
import time
# libraries that needed ^

tk = Tk() 

tk.title("Игра") # Here we give name on the title 
tk.resizable(0, 0) 
tk.wm_attributes("-topmost", 1)
canvas = Canvas(tk, width=500, height=400, bd=0, highlightthickness=0) #we transfer the rights to use part of the variable library


canvas.pack()
tk.update()






class Ball:# creatind ball
    def __init__(self, canvas, paddle, color): # very necessary function 
        self.canvas = canvas #using library tkinter  canvas
        self.paddle = paddle # using paddle for ball

        self.id = canvas.create_oval(10, 10, 25, 25, fill=color) # here drawing the ball and requesting the color 
        self.canvas.move(self.id, 245, 100) # moving that ball on the start position

        self.started = False # this function need for lauch the game
        self.canvas.bind_all('<Button-1>', self.start) # start fill happen if you click left button on mouse in the game

        starts = [-3, -2, -1, 1, 2, 3] # random vector shooting that ball 
        random.shuffle(starts)# also that randomising
        self.x = starts[0]# that 0 index will be randomly picked
        self.y = -1# first vector of shoot
        self.canvas_height = self.canvas.winfo_height() # this line must tell another part of code the coordinates of the ball and make borders
        self.canvas_length = self.canvas.winfo_reqwidth() # this also

        self.hit_bottom = False # if that True code dont work ))))

    def start(self, evt): # the start function
        self.started = True 

    def draw(self): # drawing the moveset of the ball and moves that if any touch to the paddle 
        if self.started:
            self.canvas.move(self.id, self.x, self.y)
            pos = self.canvas.coords(self.id)

            if self.hit_paddle(pos) == True: # if hit paddle ball will bounce off 
                            
                self.y = -3
            
            if pos[0] <= 0:
                self.x += 1
            elif pos[2] >= self.canvas_length:
                self.x += -1

            if pos[1] <= 0:
                self.y += 1
            if pos[3] >= self.canvas_height:
                self.y += -1

            if pos[3] >= self.canvas_height:
                self.hit_bottom = True
                self.canvas.create_text(
                                250, 200, text='игра оконченна', font=('Helvetica, 20'), fill='black'
                            )

            if pos[0] <= 0:
                self.x = 3
            if pos[2] >= self.canvas_length:
                self.x = -3
            
    def hit_paddle(self, pos): # that code what will bounce off ball if paddle will be hitten

        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
            
            return False
    
    
class Paddle: # making that paddle 
    def __init__(self,canvas, color):
        
        self.canvas = canvas
        self.id = canvas.create_rectangle(0, 0, 100, 10, fill=color) # making the paddle is that a colored block what we can move left or right
        self.canvas.move(self.id, 200, 300)
        self.x = 0
        
        self.canvas_wigth = self.canvas.winfo_width() # this line must make borders for our paddle

        self.canvas.bind_all('<KeyPress-Left>', self.turn_left) # by this line we can move paddle on left
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right) # by this on right
    def turn_left(self, evt):
            self.x = -2

    def turn_right(self, evt):
        self.x = 2
    
    def draw(self): # drawing that paddle, and set the speed of that paddle
        self.canvas.move(self.id, self.x, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x = 0

        elif pos[2] >= self.canvas_wigth:
            self.x =0
        


paddle = Paddle(canvas, 'black') # give our paddle color, if u want u can change color in 'here' 
ball = Ball(canvas, paddle, 'red') # give our ball settings of paddle and giving that ball a color u can also change the color 'here'



while 1: # loop for playing

    if ball.hit_bottom ==  False:
        ball.draw()
        paddle.draw()
    
    tk.update_idletasks()
    tk.update()
    time.sleep(0.01)

