"""
Projet module 7
Timothy Battaille et David de Meester
Novembre 2022

Ce projet consiste dans la création d'un mini-jeu, un escape game où le joueur doit parcourir un chateau avec des indices
à trouver et des portes à ouvrir.
"""

#IMPORTS
from CONFIGS import *
import turtle as t
#CONSTANTES GLOBALES

#ZONE_PLAN_MINI = (-240, -240)  # Coin inférieur gauche de la zone d'affichage du plan
#ZONE_PLAN_MAXI = (50, 200)  # Coin supérieur droit de la zone d'affichage du plan

#FONCTIONS

def lire_matrice(fichier: str):
    """lecture du fichier contenant le plan et revoie de la matrice du jeu"""
    with open(fichier,'r') as f:
        l = []
        for line in f.readlines():
            l.append([int(x) for x in line.split()])
        return l

def calculer_pas(matrice: list):
    """Reçoit la matrice du jeu en argument et retourne la longueur du coté des cases du jeu (pas) en pixels turtle"""
    longueur = ZONE_PLAN_MAXI[0]-ZONE_PLAN_MINI[0]
    hauteur = ZONE_PLAN_MAXI[1]-ZONE_PLAN_MINI[1]
    pas = min(longueur//len(matrice[0]), hauteur//len(matrice))
    return pas

def coordonnees(case:tuple, pas: int):
    """Reçoit le tuple des coordonnées de la case dans le jeu (case) et la dimension de la case (pas)
     et retourne le tuple des coordonnées du coin inférieur gauche de la case"""
    x, y = case[1]*pas + ZONE_PLAN_MINI[0], ZONE_PLAN_MAXI[1] - (case[0] + 1) * pas
    return (x, y)
    
def coordonnees_milieu(case:tuple, pas:int):
    """Fonction similaire à coordonnes() mais qui retourne le milieu de la case"""
    co1 = case[1]*pas + ZONE_PLAN_MINI[0],ZONE_PLAN_MAXI[1] - (case[0] + 1) * pas
    co2 = ZONE_PLAN_MINI[0] + (case[1] + 1) * pas, ZONE_PLAN_MAXI[1] - case[0] *pas
    x,y = ((co1[0]+co2[0])//2),((co1[1]+co2[1])//2)
    return (x, y)

def init_turtle():
    """Initialise les paramètres Turtle"""
    t.tracer(0)
    t.update()
    t.color(COULEUR_CASES)
    t.hideturtle()

def tracer_carre(dimension: int):
    """Reçoit la longueur du carré en argument et trace un carré de cette dimension"""
    t.pendown()
    for i in range(4):
        t.fd(dimension)
        t.left(90)
    t.penup()
    
def tracer_case(case: tuple, couleur: str, pas: int):
    """Reçoit l'emplacement de la case, la couleur, et la dimension et trace la case voulue"""
    coord = coordonnees(case, pas)
    t.goto(coord)
    t.fillcolor(couleur)
    t.begin_fill()
    tracer_carre(pas)
    t.end_fill()

def afficher_plan(matrice: list):
    """Reçoit la matrice du jeu et la dessine"""
    pas = calculer_pas(matrice)
    init_turtle()
    for i_ligne in range(len(matrice)):
        for i_colonne in range(len(matrice[0])):
            case = (i_ligne, i_colonne)
            couleur = COULEURS[matrice[i_ligne][i_colonne]] #la couleur est assignée à la couleur définie dans CONFIGS.py
            tracer_case(case, couleur, pas) 

def deplacer(matrice:list, position:tuple, mouvement:tuple):
    """Fonction de déplacement du personnage et gestion des effets de celui-ci"""
    tracer_case(ma_pos, COULEUR_CASES, mon_pas)
    ma_pos[0] += mouvement[0]  
    ma_pos[1] += mouvement[1]
    t.goto(coordonnees_milieu(ma_pos, mon_pas))  
    t.dot(taille_dot, COULEUR_PERSONNAGE)

    

def deplacer_gauche():
    """Fonction qui appelle la fonction déplacer pour aller à gauche"""
    global matrice, position
    t.onkeypress(None, "Left")   # Désactive la touche Left
    deplacer(matrice_jeu,ma_pos,(0, -1)) # traitement associé à la flèche gauche appuyée par le joueur
    t.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche

def deplacer_droite():
    """Fonction qui appelle la fonction déplacer pour aller à droite"""
    global matrice, position
    t.onkeypress(None, "Right")   # Désactive la touche Right
    deplacer(matrice_jeu,ma_pos,(0, 1)) # traitement associé à la flèche droite appuyée par le joueur
    t.onkeypress(deplacer_droite, "Right") 

def deplacer_haut():
    """Fonction qui appelle la fonction déplacer pour aller au haut"""
    global matrice, position
    t.onkeypress(None, "Up")   # Désactive la touche Up
    deplacer(matrice_jeu,ma_pos,(-1, 0)) # traitement associé à la flèche haut appuyée par le joueur
    t.onkeypress(deplacer_haut, "Up") 

def deplacer_bas():
    """Fonction qui appelle la fonction déplacer pour aller au bas"""
    global matrice, position
    t.onkeypress(None, "Down")   # Désactive la touche Down
    deplacer(matrice_jeu,ma_pos,(1, 0)) # traitement associé à la flèche bas appuyée par le joueur
    t.onkeypress(deplacer_bas, "Down") 



#LES VARIABLES GENERALES
matrice_jeu = lire_matrice(fichier_plan) 
mon_pas = calculer_pas(matrice_jeu) #Taille des côtés des cases du plan
taille_dot = RATIO_PERSONNAGE * mon_pas #Taille du personnage
ma_pos = list(POSITION_DEPART) #Position du personnage 


#AFFICHAGE DU PLAN ET DU PERSONNAGE

afficher_plan(matrice_jeu)
t.goto(coordonnees_milieu((0,1),mon_pas)) #Place le personnage à la case départ
t.dot(taille_dot,COULEUR_PERSONNAGE)


#ECOUTE DE LA TORTUE POUR LES DEPLACEMENTS

t.listen()    # Déclenche l’écoute du clavier
t.onkeypress(deplacer_gauche, "Left")   # Associe à la touche Left du clavier une fonction appelée deplacer_gauche
t.onkeypress(deplacer_droite, "Right")  # Idem pour la touche Right
t.onkeypress(deplacer_haut, "Up")       # Idem pour la touche Up
t.onkeypress(deplacer_bas, "Down")      # Idem pour la touche Down
t.mainloop()    # Place le programme en position d’attente d’une action du joueur



