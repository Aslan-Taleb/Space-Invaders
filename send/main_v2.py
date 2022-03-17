import tkinter as tk
from tkinter import *
import time

class Alien(object):
    image_alien = None
    image_width = None
    image_height = None
    
    def __init__(self):
        self.id = None
        self.alive = True
    
    @classmethod
    def get_image(cls):
        if cls.image_alien == None:
            cls.image_alien = tk.PhotoImage(file='alien.gif')
            cls.image_width = tk.PhotoImage.width(cls.image_alien)
            cls.image_height = tk.PhotoImage.height(cls.image_alien)
        return cls.image_alien
    
    def install_in(self, canvas, x, y):
        alien = Alien.get_image()
        self.id = canvas.create_image(x, y, image=alien)
        
    def touched_by(self, canvas, bullet):
        pass
    
    def move_in(self, canvas, dx, dy):
        canvas.move(self.id, dx, dy)
        
class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5
        self.aliens_columns = 10
        self.aliens_inner_gap = 20
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        self.alien_width = None
        self.alien_id = []
        
    def install_in(self, canvas):
        alien = Alien()
        Alien.get_image()
        y= -self.alien_x_delta
        for i in range (0, self.aliens_lines):
            y = y + Alien.image_height + self.alien_y_delta
            x = 0
            for j in range (0, self.aliens_columns):
                x = x + Alien.image_width + self.alien_x_delta
                alien = Alien()
                self.alien_width = alien.image_width
                alien.install_in(canvas, x, y)  
                self.alien_id.append(alien)
                
    def explosionend(self,canvas,explo):
        pass
                
    def explosion(self,canvas,x, y):
      pass
    
    def manage_touched_aliens_by(self,canvas,bullet):
      pass


 
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
        self.fleet = Fleet() 
        self.defender = Defender()
        self.bullet = Bullet(self.defender)
        self.width = 800
        self.height = 600
        self.canvas = tk.Canvas(self.frame, width=self.width,height=self.height , bg = "black")
        self.canvas.pack()
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.fleet_position_x1 = 0
        self.fleet_position_x2 = (self.fleet.alien_width + self.fleet.alien_x_delta) * self.fleet.aliens_columns
        self.dx= 20
        self.dy = 0
        self.fin = 0
        #self.pim = tk.PhotoImage(file='background.gif')
        #self.canvas.create_image(0,0,image=self.pim, tags="image")
        
    def keypress(self,event):
        if event.keysym == 'Left':
            self.defender.move_in(self.canvas,-self.defender.move_delta)
        elif event.keysym == 'Right':
            self.defender.move_in(self.canvas,self.defender.move_delta)   
        elif event.keysym == 'space':
            self.defender.fire(self.canvas)
            
    def animation(self):
            self.move_bullets()
            self.move_aliens_fleet()
            self.canvas.after(300, self.animation)
            
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
        for fleet in self.fleet.alien_id:
            fleet.move_in(self.canvas, self.dx, self.dy)
        self.fleet_position_x1 = self.fleet_position_x1 + self.dx
        self.fleet_position_x2= self.fleet_position_x2 + self.dx
        if(self.fleet_position_x1<=(0 - self.fleet.aliens_columns - (2*self.fleet.alien_x_delta) - 1) or self.fleet_position_x2>= (self.width - self.fleet.aliens_columns*self.fleet.alien_x_delta)):
                self.dx = -self.dx
                self.dy = self.dy+ 0.05
                target = self.canvas.find_overlapping(0, (self.height - self.defender.height - 20), self.width, self.height)
                if (len(target)>=2):
                    self.canvas.create_text(450, 350,font=("Purisa", 18), text='Fin du jeu vous avez perdu !', fill='white')
                    self.fin = 1
    
    
class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Space Invaders')
        self.frame = tk.Frame(self.root)
        self.frame.pack(side = "top",fill = "both")
        self.game = Game(self.frame)
    def play(self):
        self.game.start_animation()
        self.root.bind("<Key>", self.game.keypress)
        self.root.mainloop()
        
        
SpaceInvaders().play()