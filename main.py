import tkinter as tk
from tkinter import *
import time


        
class Bullet():
    def __init__(self,shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 8
        self.id = None
        self.shooter = shooter 
        

    def install_in(self,canvas,position_defender):
        w = self.radius
        self.canvas_width = int(canvas.cget("width"))
        self.canvas_height = int(canvas.cget("height")) 
        x, y=position_defender,self.canvas_height - 25 #position de la balle  il faut recuperer la position x du defender
        self.oval_id =canvas.create_oval(x,y,x+w,y+w,outline = 'black',fill = self.color)  #dessiner bullet
        self.canvas = canvas
    def move_in(self):
            self.canvas.move(self.oval_id,0,-self.radius)
            self.canvas.after(self.speed,self.move_in)
        
        
    
class Defender:
    def __init__(self):
        self.width = 20 #longeur largeur Defender
        self.height = 20
        self.move_delta = 20 #de combien il avance
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = 1
        
    def install_in(self,canvas):
        # creation du Defender
        self.canvas_width = int(canvas.cget("width")) #recupere longeur largeur du canvas
        self.canvas_height = int(canvas.cget("height"))
        x, y= self.canvas_width//2,self.canvas_height-self.width 
        self.id =canvas.create_rectangle(x,y,x+self.width ,y+self.width ,outline = 'black',fill = 'white') #dessin Defender
    def move_in(self,canvas ,dx):
        canvas.move(self.id,dx,0)
    def fire(self,canvas):
        self.defender_pos = canvas.coords(self.id)[0] + 10 
        self.fired_bullets = self.fired_bullets + 1
        #if position_bullet<= 0:
               # self.fired_bullets = self.fired_bullets -1
        #else:
         #self.fired_bullets = self.fired_bullets + 1

        
        
       
       

class Game(object):
    def __init__(self,frame):
        self.frame = frame
        #self.fleet = Fleet() #j'ai pas encore la class fleet
        self.defender = Defender()
        self.bullet = Bullet(self.defender)
        self.height = 800
        #self.width = self.fleet.get_width()
        self.canvas = tk.Canvas(self.frame, width=800, height=600, bg="black")
        self.defender.install_in(self.canvas)
        self.canvas.pack()
        #self.fleet.install_in(self.canvas)
    def animation(self,event):
        if event.keysym == 'Left' and self.canvas.coords(self.defender.id)[0] > 0 :  #block left
            self.defender.move_in(self.canvas,-self.defender.move_delta)
        elif event.keysym == 'Right' and  self.canvas.coords(self.defender.id)[2] < self.height : #block Right
             self.defender.move_in(self.canvas,self.defender.move_delta)
        if event.keysym == 'space' and self.defender.fired_bullets <= self.defender.max_fired_bullets: #fais l'animation bullet si appuie sur espace + assez de balle restante
            self.defender.fire(self.canvas)
            self.move_bullets()
            
    def start_animation(self): # lancement install 
        self.animation
    def move_bullets(self):
        self.bullet.install_in(self.canvas,self.defender.defender_pos)
        self.bullet.move_in()
        self.bullet_pos = self.canvas.coords(self.bullet.oval_id)
        
        
    def move_aliens_fleet(self):
        pass
    
    
class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Space Invaders')
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.game = Game(self.frame)
    def play(self):
        self.game.start_animation()
        self.root.bind("<Key>", self.game.animation)
        self.root.mainloop()
        
        
SpaceInvaders().play()