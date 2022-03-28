# Space Invaders

[![Language](https://img.shields.io/badge/language-python-blue.svg?style=flat)](https://www.python.org)
[![Module](https://img.shields.io/badge/module-tkinter-brightgreen.svg?style=flat)](http://tkinter.fdex.eu/)
[![Release](https://img.shields.io/badge/release-v1.0-orange.svg?style=flat)](http://www.leejamesrobinson.com/space-invaders.html)

Compte Rendu PCO : Space Invaders

## Présentation générale du programme:

Le programme se lance dans une fenêtre à fond noir ayant pour titre : “Space
Invaders”, une flotte d’aliens composée de 5 lignes de 10 aliens est placé en haut de la
fenêtre et se déplace de droite à gauche et du haut vers le bas.
En bas de la fenêtre est placé un carré blanc représentant le defender, il peut bouger
de droite à gauche dans la limite de la fenêtre grâce au touches directionnelles du clavier ou
à l’aide des touches ‘Q’ pour la gauche et ‘D’ pour la droite, il est possible de tirer en
appuyant sur la touche ‘espace’ du clavier ce qui enverra une balle (et un bruitage de tire) à
partir de la position du defender en direction du haut de la fenêtre. Un alien est ainsi éliminé
lorsque le projectile (ou bullet) est en contact avec lui, ceci entraînera également
l’élimination de la bullet, lors de l’impact, une animation d’explosion apparaît et un bruit
d’explosion se fait entendre. Dès le premier alien éliminé le score apparaît en haut à droite
de l’écran, à chaque alien éliminé le score s’incrémente de 1. Le defender est limité à huit
balles à la fois, une fois cette limite atteinte, il peut de nouveau tirer lorsqu’une balle sort de
la zone de jeu ou qu’elle touche un ennemi. Le jeu se termine si le joueur tue tous les aliens
(victoire du joueur) ou si un alien arrive au même niveau que le defender (défaite du joueur).
Présentation détaillée des différentes classes et de leurs fonctions:

-La classe SpaceInvaders : elle sert à initialiser le canvas et installer la classe Game, elle
permet également de lancer les animations et activer l’utilisation des touches du clavier.
La classe Game : elle initialise les différentes parties du jeu notamment la fenêtre et la flotte.
C’est dans cette classe que les touches du clavier sont associées à des actions et que les
différentes animations ainsi que bruitages sont initialisées et lancées.
La classe Bullet : elle initialise une balle et la place sur le canvas puis la fait se déplacer (elle
est appelée par le defender).

-La classe Defender : elle initialise le defender, le place en bas de la fenêtre au milieu, elle
gère le déplacement du defender et la création de balles dans la limite imposée.
La classe Fleet : elle initialise le nombre de lignes et de colonnes d’aliens puis elle installe le
nombre requis d’aliens sur le canvas (via la classe Alien). Elle gère la collision entre alien et
balle et l’animation d ‘explosion. Elle affiche un message de victoire lorsque tous les aliens
sont éliminés.

-La classe Alien : elle initialise chaque alien et l’installe à l’endroit demandé par la classe
Fleet et le supprime lorsqu’il est touché, elle gère également le mouvement de chaque alien.

## Les difficultées rencontrée :

On a rencontré des difficultés avec les classes manage_touched_aliens_by et
touched_by, on a fonctionné étapes par étapes pour résoudre les problèmes. Il fallait
réussir à trouver les coordonnées des aliens qui bougeaient.
Lors de l’animation de l’explosion, il arrive que l’image de l’explosion ne se supprime
pas notamment lorsqu'il y a beaucoup de choses à gérer, ce qui est assez gênant
mais que nous n’avons malheureusement pas réussi à régler.
De la même manière il arrive que la balle traverse un alien sans le tuer lorsque la
balle ne traverse pas le centre de l’alien, ce qu’on a pas réussi à régler malgré de
nombreux essais.

## ce qu’on aurait pu améliorer :

Nous avions pensé à demander le nom du joueur avant le début du jeu puis à la fin du jeu
faire l’affichage d’un tableau des scores.
## Conclusion :
Nous sommes parvenus à faire un Space Invaders jouable avec la possibilité de
perdre ou de gagner, on a réussi à résoudre les principaux problèmes seuls les
problèmes cités plus haut persistent.
Concernant la perspective d’IA nous avions songé à créer un mode survie,
c'est-à-dire des aliens de chaque côté où le joueur pourrait affronter l’IA en tuant les
aliens ennemis. Le vainqueur serait celui qui a su garder ces aliens en vie
