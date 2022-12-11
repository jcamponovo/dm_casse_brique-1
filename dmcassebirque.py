import pyxel, random

# pip install -U pyxel

# taille de la fenetre 128x128 pixels
# ne pas modifier
pyxel.init(128, 128, title="Nuit du c0de")

# position initiale du plateforme
plateforme_x = 50
plateforme_y = 100

# position de depart de la balle
balle_x = 60
balle_y = 70

# liste position des briques
briques = []

# vecteur force
forceVertical = 1
forceHorizontal = 0

vie_joueur

def plateforme_deplacement(x):
    """déplacement avec les touches de directions"""
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x < 120:
            x = x + 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x = x - 1
    return x

def balle_deplacement(x, y, forceVertical, forceHorizontal, vie_joueur):
    """ fonction qui s'occupe des deplacements
    de la balle qui va vers le bas et les collision avec la plateforme"""
    y = y + forceVertical *1.07
    x = x + forceHorizontal
    if y >= 127:
        y = 70
        x = 60
        forceHorizontal = 0
        vie_joueur -= 1
    return x,y,forceHorizontal,vie_joueur

def creation_brique(briques):
    """
    affichage successif des briques les unes à la suite des autres avec comme paramètres de position i et k.
    """
    for y in range(5, 50, 5):
        for x in range(10, 120, 10):
            v = random.randint(1, 3)
            briques.append((x,y,v))
    return briques

def collision(balle_x, balle_y, forceVertical, forceHorizontal, briques):
    """
	fonction qui gère les collisions entre la balle et les briques
    """
    for b in briques:
    	vie = b[2]
    	# si la balle tape en dessous de la brique
    	if balle_x <= b[0] + 8 and balle_y <= b[1] + 2 and balle_x + 2 >= b[0] and balle_y + 2 >= b[1] + 4:
        	forceVertical = 1
        	forceHorizontal = 0
        	vie -= 1
        	break
        # si la balle arrive sur le coté gauche
		elif balle_x + 2 <= b[0] + 3 and balle_y <= b[1] + 2 and balle_x + 2 >= b[0] and balle_y + 2 >= b[1]:
        	forceVertical = 1
        	forceHorizontal = -1
        	vie -= 1
        	break
        # si la balle arrive à droite
        elif balle_x + 2 <= b[0] + 8 and balle_y <= b[1] + 2 and balle_x + 2 >= b[0] and balle_y + 2 >= b[1]:
        	forceVertical = 1
        	forceHorizontal = 1
        	vie -= 1
        	break
        # si la balle arrive au dessus
        elif balle_x + 2 <= b[0] + 8 and balle_y + 2 <= b[1] and balle_x + 2 >= b[0] and balle_y + 2 >= b[1]:
            forceVertical = 1
            forceHorizontal = 0
            vie -= 1
            break   
	if vie == 0:
		briques.remove(b)     

    return forceVertical, forceHorizontal, briques


# =========================================================
# == UPDATE
# =========================================================
def update():
    """mise à jour des variables (30 fois par seconde)"""

    global plateforme_x, plateforme_y, balle_x, balle_y, forceVertical, forceHorizontal, briques

    # mise à jour de la position du plateforme
    plateforme_x = plateforme_deplacement(plateforme_x)
    
    # deplacemebt de la balle
    balle_x, balle_y, forceHorizontal, vie_joueur = balle_deplacement(balle_x, balle_y, forceVertical, forceHorizontal,vie_joueur)

    #collision entre la balle et les briques
    forceVertical, forceHorizontal, briques = collision(balle_x, balle_y, forceVertical, forceHorizontal, briques)

    #condition lorsque la balle touche la plateforme
    if plateforme_x + 20 >= balle_x + 2 >= plateforme_x and balle_y + 2 <= plateforme_y + 5 and balle_y + 2 >= plateforme_y :
        forceVertical = -1
        forceHorizontal = 0
    elif balle_x + 2 <= plateforme_x + 31 and balle_y + 2 <= plateforme_y + 5 and balle_x + 2 >= plateforme_x + 21 and balle_y + 2 >= plateforme_y :
        forceVertical = -1
        forceHorizontal = -1
    elif balle_x <= plateforme_x -1 and balle_y <= plateforme_y + 5 and balle_x >= plateforme_x - 10 and balle_y >= plateforme_y:
        forceVertical = -1
        forceHorizontal = 1

    elif balle_y < 1:
        forceVertical = 1
    elif balle_x < 1:
        forceHorizontal = 1
    elif balle_x > 127:
        forceHorizontal = -1


# =========================================================
# == DRAW
# =========================================================
def draw():
    """création des objets (30 fois par seconde)"""

    # vide la fenetre
    pyxel.cls(6)
	if vie_joueur != 0:
    	# forme de la platform
    	pyxel.rect(plateforme_x, plateforme_y, 20, 2, 3)
    	pyxel.tri(plateforme_x, plateforme_y+4, plateforme_x-10, plateforme_y+4, plateforme_x, plateforme_y, 2)
    	pyxel.tri(plateforme_x+20, plateforme_y+4, plateforme_x+30, plateforme_y+4, plateforme_x+20, plateforme_y, 2)

    	# dessin de la balle
    	pyxel.circb(balle_x, balle_y, 2, 5)

    	# dessin des briques
    	for i in briques:
    	    pyxel.rect(i[0], i[1], 8, 2, i[2])
	else:
		pyxel.text("game over")

# creation des briques
briques = creation_brique(briques)
pyxel.run(update, draw)
