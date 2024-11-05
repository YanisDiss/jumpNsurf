"""
-------- ESPACE COMMENTAIRE --------











------------------------------------
"""

import pygame

GRISCLAIR  = (  214, 214, 214)
BLEU       = (153, 164,   242)

X = 0
Y = 1

FENETRE_LARGEUR = 800
FENETRE_HAUTEUR = 600

BORD_LARGEUR = 100

PLAYER_TAILLE = 50
PLAYER_TAILLE_2 = (PLAYER_TAILLE, PLAYER_TAILLE)

NOMBRE_COLONNES = 5
TOUCHE_DROITE = pygame.K_RIGHT
TOUCHE_GAUCHE = pygame.K_LEFT

AGAUCHE = -1
ADROITE = 1

def move(sens):
    player_position[X] += FENETRE_LARGEUR / NOMBRE_COLONNES * sens
    if (player_position[X] < 0): player_position[X]
    elif (player_position[X] + PLAYER_TAILLE >= FENETRE_LARGEUR):
        player_position[X] = FENETRE_LARGEUR - PLAYER_TAILLE

pygame.init()

fenetre_taille = (FENETRE_LARGEUR, FENETRE_HAUTEUR)
fenetre = pygame.display.set_mode(fenetre_taille)

fenetre.fill(GRISCLAIR)

player_position = [400, 500]

fini = False
temps = pygame.time.Clock()

while not fini:
    #--- Traiter entrées joueur
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == TOUCHE_DROITE:
                move(ADROITE)
            elif evenement.key == TOUCHE_GAUCHE:
                move(AGAUCHE)


    fenetre.fill(GRISCLAIR)

    # affichage du joueur
    pygame.draw.rect(fenetre, BLEU, (
        (player_position[0] - PLAYER_TAILLE/2, player_position[1]), # pour qu'il soit a l'exact milieu de l'ecran
        PLAYER_TAILLE_2), 
        16, 3) #pour les bord arrondis et l'outline


    # pour les bords
    pygame.draw.rect(fenetre, BLEU, ((0, 0), (BORD_LARGEUR, FENETRE_HAUTEUR)))
    pygame.draw.rect(fenetre, BLEU, ((FENETRE_LARGEUR - BORD_LARGEUR, 0), (BORD_LARGEUR, FENETRE_HAUTEUR)))


    #--- Afficher (rafraîchir) l'écran
    pygame.display.flip()

    #--- 60 images par seconde
    temps.tick(60)


pygame.display.quit()
pygame.quit()