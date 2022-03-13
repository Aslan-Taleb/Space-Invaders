import tkinter as tk
from tkinter import *
import time



class Bullet():
    def __init__(self):
        self.radius = 5
        self.color = "red"
        self.speed = 80
        self.id = None

    def install_in(self,canvas):
        w = self.radius
        self.canvas_width = int(canvas.cget("width"))
        self.canvas_height = int(canvas.cget("height")) 
        self.canvas = canvas
        x, y= self.canvas_width//2,self.canvas_height - 25 #position de la balle  il faut recuperer la position x du defender
        self.oval_id =self.canvas.create_oval(x,y,x+w,y+w,outline = 'black',fill = self.color)  #dessiner bullet

    def move_in(self):
        self.canvas.move(self.oval_id,0,-20)
        self.canvas.after(self.speed, self.move_in)
        
        
        
class Defender:
    def __init__(self):
        self.width = 20 #longeur largeur Defender
        self.height = 20
        self.move_delta = 20 #de combien il avance
        self.id = None
        self.bullet = Bullet()
        self.max_fired_bullets = 8
        self.fired_bullets = 0  #c'est censé etre une liste 
        
    def install_in(self, canvas):
        # creation du Defender
        w = self.width 
        self.canvas_width = int(canvas.cget("width")) #recupere longeur largeur du canvas
        self.canvas_height = int(canvas.cget("height"))
        x, y= self.canvas_width//2,self.canvas_height-w
        self.canvas = canvas
        self.id =self.canvas.create_rectangle(x,y,x+w,y+w,outline = 'black',fill = 'white') #dessin Defender
        print()
    def move_in(self,event):
        max = self.canvas_width 
        min = 0
        if event.keysym == 'Left' and self.canvas.coords(self.id)[0] > min :  #block left
            self.canvas.move(self.id,-10,0)
        elif event.keysym == 'Right' and  self.canvas.coords(self.id)[2] < max : #block Right
            self.canvas.move(self.id,10,0)
        if event.keysym == 'space' and self.fired_bullets <= self.max_fired_bullets: #fais l'animation bullet si appuie sur espace + assez de balle restante
            self.bullet.install_in(self.canvas)
            self.bullet.move_in()
            self.fired_bullets = self.fired_bullets + 1
            

        
                

class fenetre:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Space Invaders')
        self.root.geometry("800x600")
        self.root.config(background= 'black')
        self.canvas_width = 800
        self.canvas_height = 600
        self.defender = Defender()  #ajout de la class defender
        self.bullet = Bullet()
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        self.canvas = tk.Canvas(self.frame, width=self.canvas_width, height=self.canvas_height, bg="black")
        self.canvas.pack(side="top", fill="both", expand=True)
    
    def install(self):
        self.defender.install_in(self.canvas)  #dessin de defender dans le canvas
        
    def start(self): # lancement install 
        self.install()
        self.root.bind("<Key>",self.defender.move_in)
        self.root.mainloop()
        
jeu = fenetre()
jeu.start()