import tkinter as tk
from tkinter import *
import winsound


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
            cls.image_alien = tk.PhotoImage(file='images/alien.png')
            cls.image_width = tk.PhotoImage.width(cls.image_alien)
            cls.image_height = tk.PhotoImage.height(cls.image_alien)
        return cls.image_alien

    def install_in(self, canvas, x, y):  # creation de l'alien
        alien = Alien.get_image()
        self.id = canvas.create_image(x, y, image=alien)

    def touched_by(self, canvas, bullet):
        canvas.delete(self.id)  # suppression de l'alien
        winsound.PlaySound("sounds/explosion.wav", winsound.SND_ASYNC)
        canvas.move(bullet.id, 0, -700)

    def move_in(self, canvas, horizontale, verticale):
        canvas.move(self.id, horizontale, verticale)

    def get_x(self, canvas):
        # recuperation coordonnée en abscisse de l'alien
        return canvas.coords(self.id)[0]

    def get_y(self, canvas):
        # recuperation coordonnée en ordonnée de l'alien
        return canvas.coords(self.id)[1]


class Fleet(object):
    def __init__(self):
        self.aliens_lines = 5  # 5 lignes
        self.aliens_columns = 10  # de 10 aliens
        self.aliens_inner_gap = 50
        self.alien_x_delta = 5
        self.alien_y_delta = 15
        self.alien_width = None
        self.alien_id = []  # liste vide d'alien
        self.explo = 0
        self.location_explo = None
        self.victory = False
        self.score = 0
        self.affichage_score = None

    def install_in(self, canvas):
        alien = Alien()
        Alien.get_image()
        y = 0
        # deplace y de la hauteur d'un alien pour changer de ligne
        for line in range(self.aliens_lines):
            y = y + Alien.image_height
            x = 0
            # creation de chaques aliens d'une column a l'autre sur une ligne
            for column in range(self.aliens_columns):
                x = x + Alien.image_width
                alien = Alien()  # creation objet alien
                self.alien_width = alien.image_width
                alien.install_in(canvas, x, y)
                self.alien_id.append(alien)  # ajout dans liste d'un alien

    def manage_touched_aliens_by(self, canvas, bullet):
        image_width = 64
        image_height = 64

        pos_x1_balle, pos_y1_balle, pos_x2_balle, pos_y2_balle = canvas.coords(
            bullet.id)  # recup coords de la balle
        target = canvas.find_overlapping(
            pos_x1_balle, pos_y1_balle, pos_x2_balle, pos_y2_balle)
        if (len(target) == 2):
            for alien in self.alien_id:
                pos_x_alien, pos_y_alien = canvas.coords(alien.id)
                # si la balle atteint les coords de l'image de l'alien
                if (pos_x_alien <= pos_x1_balle <= pos_x_alien+image_width and pos_y_alien <= pos_y1_balle <= pos_y_alien+image_height):
                    # suppression du canvas de l'alien + move de la balle
                    alien.touched_by(canvas, bullet)
                    self.alien_id.remove(alien)  # suppr de l'alien de la liste
                    canvas.delete(self.affichage_score)  # mis a jour du score
                    self.score = self.score + 10  # ajout du score
                    self.affichage_score = canvas.create_text(100, 20, font=(
                        "Rockwell", 20), text="SCORE : "+str(self.score), fill='white')
                # si liste d'alien vide creation de l'ecran de Victoire + Son
                if len(self.alien_id) == 0:
                    canvas.create_text(640, 480, font=(
                        "fonts/space_invaders.ttf", 50), text='VICTORY !', fill='green')
                    canvas.create_text(640, 600, font=(
                        "fonts/space_invaders.ttf", 30), text=" Votre Score est de : "+str(self.score), fill='white')
                    canvas.delete(self.affichage_score)  # mis a jour du score
                    winsound.PlaySound("sounds/victory.wav",
                                       winsound.SND_ASYNC)
                    self.victory = True


class Defender:
    def __init__(self):
        self.width = 20  # longeur largeur Defender
        self.height = 60
        self.move_delta = 20  # de combien le defender  avance
        self.id = None
        self.max_fired_bullets = 8
        self.fired_bullets = []  # liste qui contient les objets bullet

    def install_in(self, canvas):  # permet le dessin du defender
        # creation du Defender
        x = int(canvas['width'])//2  # dessiner le defender au milieu
        # premier point du defender un peu au dessus du y
        y = int(canvas['height']) - self.height
        img = PhotoImage(file='images/ship.png')
        canvas.image1 = img
        self.id = canvas.create_image(x, y, image=img, anchor='nw')

    def move_in(self, canvas, move_defender):
        # recupere position x du defender + de combien il avance
        position_x_defender = int(canvas.coords(self.id)[0]) + move_defender
        if position_x_defender < 0:
            move_defender = 0  # arret mouvement
        elif position_x_defender > int(canvas['width'])-self.width:
            move_defender = 0
        else:
            canvas.move(self.id, move_defender, 0)

    def fire(self, canvas):
        if (len(self.fired_bullets) < self.max_fired_bullets):
            newBullet = Bullet(self)  # creation objet bullet
            newBullet.install_in(canvas)  # dessin objet bullet
            # ajout objet bullet dans liste
            self.fired_bullets.append(newBullet)
            winsound.PlaySound("sounds/shoot.wav", winsound.SND_ASYNC)


class Bullet():
    def __init__(self, shooter):
        self.radius = 8
        self.color = "blue"
        self.speed = 10  # vitesse de la balle
        self.id = None
        self.shooter = shooter

    def install_in(self, canvas):
        position_x_defender = canvas.coords(self.shooter.id)[
            0]  # recuperation x du defender
        position_y_defender = canvas.coords(self.shooter.id)[
            1]  # recuperation y du defender
        # dessin de la balle en fonction de la position du defender
        x = position_x_defender + self.radius + 12
        y = position_y_defender - 3*self.radius
        self.id = canvas.create_oval(
            x, y, x + self.radius, y + self.radius, fill=self.color)

    def move_in(self, canvas):
        canvas.move(self.id, 0, -self.speed)  # animation balle qui monte


class Game():
    def __init__(self, frame):
        self.frame = frame
        self.fleet = Fleet()
        self.defender = Defender()
        self.bullet = Bullet(self.defender)
        self.width = 1280
        self.height = 960
        self.canvas = tk.Canvas(
            self.frame, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        self.defender.install_in(self.canvas)
        self.fleet.install_in(self.canvas)
        self.horizontale = 2  # de combien bouge droite gauche  fleet
        self.verticale = 0  # de combien bouge bas fleet
        self.game_over = False

    def keypress(self, event):  # evenement à la pression des touches gauche droite ou q d et espace
        if (self.game_over == False and self.fleet.victory == False):
            if event.keysym == 'q' or event.keysym == 'Left':
                self.defender.move_in(self.canvas, -self.defender.move_delta)
            elif event.keysym == 'd' or event.keysym == 'Right':
                self.defender.move_in(self.canvas, self.defender.move_delta)
            elif event.keysym == 'space':
                self.defender.fire(self.canvas)

    def animation(self):

        if (self.game_over == False):
            self.move_bullets()
            self.move_aliens_fleet()
            self.canvas.after(16, self.animation)

    def start_animation(self):  # lancement install
        self.canvas.after(16, self.animation)

    def move_bullets(self):
        for bullet in self.defender.fired_bullets:
            position_y_balle = self.canvas.coords(
                bullet.id)[1]  # recupere y de la balle
            self.fleet.manage_touched_aliens_by(self.canvas, bullet)
            bullet.move_in(self.canvas)  # animation balle qui monte
            if position_y_balle < 0:  # si balle en dehors de l'ecran supprimer l'objet balle de la liste
                self.canvas.delete(bullet.id)
                self.defender.fired_bullets.remove(bullet)

    def move_aliens_fleet(self):
        for fleet in self.fleet.alien_id:  # boucle dans une liste avec des objets alien
            fleet.move_in(self.canvas, self.horizontale, self.verticale)

        alien_plus_a_droite = max([a.get_x(self.canvas)
                                  for a in self.fleet.alien_id])
        alien_plus_a_gauche = min([a.get_x(self.canvas)
                                  for a in self.fleet.alien_id])

        if alien_plus_a_droite + 50 > self.width or alien_plus_a_gauche - 50 < 0:   # test fleet a la limite de l'ecran
            self.horizontale = -self.horizontale  # on part dans l'autre sens
            self.verticale += 0.1  # fleet descend

        alien_plus_bas = max([a.get_y(self.canvas)
                             for a in self.fleet.alien_id])

        if alien_plus_bas > self.height - self.defender.height - 30:
            self.canvas.create_text(640, 480, font=(
                "Rockwell", 50), text='GAME OVER ! ', fill='red')
            self.game_over = True
            winsound.PlaySound("sounds/game_over.wav", winsound.SND_ASYNC)


class SpaceInvaders(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.geometry = ("800x600")
        self.root.title('Space Invaders')
        self.icone = PhotoImage(file='images/ufo.png')
        self.root.iconphoto(False, self.icone)
        self.root.resizable(width=False, height=False)
        self.frame = tk.Frame(self.root)
        self.frame.pack(side="top", fill="both")
        self.game = Game(self.frame)

    def play(self):
        self.game.start_animation()
        self.root.bind("<Key>", self.game.keypress)
        self.root.mainloop()


SpaceInvaders().play()
