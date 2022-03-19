import tkinter as tk
from tkinter import *
import time
#defender + tir
class Defender:
    def __init__(self):
        self.width = 20 #longeur largeur Defender
        self.height = 20
        self.move_delta = 20  #de combien le defender  avance
        self.id = None   
        self.max_fired_bullets = 8
        self.fired_bullets = []     #liste qui contient les objets bullet
    def install_in(self,canvas):    #permet le dessin du defender
        # creation du Defender
        x = int(canvas['width'])//2 #dessiner le defender au milieu
        y = int(canvas['height']) - self.height #premier point du defender un peu au dessus du y
        self.id = canvas.create_rectangle(x, y, x+self.width, y +self.height , fill='white')
    def move_in(self,canvas ,move_defender):       
        position_x_defender = int(canvas.coords(self.id)[0]) +move_defender     #recupere position x du defender + de combien il avance
        if position_x_defender < 0:
            move_defender=0                     #arret mouvement
        elif position_x_defender > int(canvas['width'])-self.width:
            move_defender=0
        else:
            canvas.move(self.id,move_defender, 0)
    def fire(self,canvas):
        if (len(self.fired_bullets) < self.max_fired_bullets):   
            newBullet = Bullet(self)                #creation objet bullet
            newBullet.install_in(canvas)            #dessin objet bullet
            self.fired_bullets.append(newBullet)    #ajout objet bullet dans liste
            print("balle a etait ajouté")
   
class Bullet():
    def __init__(self,shooter):
        self.radius = 5
        self.color = "red"
        self.speed = 5
        self.id = None
        self.shooter = shooter 
    def install_in(self,canvas):
        position_x_defender = canvas.coords(self.shooter.id)[0] #recuperation x du defender
        position_y_defender = canvas.coords(self.shooter.id)[1] #recuperation y du defender
        x = position_x_defender + self.radius           #dessin de la balle en fonction de la position du defender
        y = position_y_defender - 3*self.radius
        self.id = canvas.create_oval(x, y, x + self.radius, y + self.radius, fill=self.color)
    def move_in(self,canvas):
        canvas.move(self.id, 0,-self.speed)         #animation balle qui monte
        
class Game():
    def __init__(self,frame):
        self.frame = frame
        #self.fleet = Fleet() #j'ai pas encore la class fleet
        self.defender = Defender()
        self.bullet = Bullet(self.defender)
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.frame, width=self.width,height=self.height , bg = "black")
        self.canvas.pack()
        self.defender.install_in(self.canvas)
        #self.pim = tk.PhotoImage(file='background.gif')
        #self.canvas.create_image(0,0,image=self.pim, tags="image")
        #self.fleet.install_in(self.canvas)
        
    def keypress(self,event):
        if event.keysym == 'Left':
            self.defender.move_in(self.canvas,-self.defender.move_delta)
        elif event.keysym == 'Right':
            self.defender.move_in(self.canvas,self.defender.move_delta)   
        elif event.keysym == 'space':
            self.defender.fire(self.canvas)
            
    def animation(self):
            self.move_bullets()
            self.canvas.after(10, self.animation)
            
    def start_animation(self): # lancement install 
        self.canvas.after(10,self.animation)
        
    def move_bullets(self):
        for bullet in self.defender.fired_bullets:
            position_y_balle =self.canvas.coords(bullet.id)[1] #recupere y de la balle 
            bullet.move_in(self.canvas)                        #animation balle qui monte
            if position_y_balle < 0:                           #si balle en dehors de l'ecran supprimer l'objet balle de la liste
                self.canvas.delete(bullet.id)
                self.defender.fired_bullets.remove(bullet)
                print("Une balle a etait enlevé")
                
    def move_aliens_fleet(self):
        pass
    
    
class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Space Invaders')
        self.frame = tk.Frame(self.root)
        self.p1 = PhotoImage(file ='images/ufo.png')
        self.root.iconphoto(False, self.p1)
        self.frame.pack(side = "top",fill = "both")
        self.game = Game(self.frame)
    def play(self):
        self.game.start_animation()
        self.root.bind("<Key>", self.game.keypress)
        self.root.mainloop()
        
        
SpaceInvaders().play()