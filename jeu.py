"""
-------- ESPACE COMMENTAIRE --------











------------------------------------
"""

import pygame
import random
import math

BG_COLOR  = (  21, 21, 21)
MAIN_COLOR       = (153, 164,   242)

X = 0
Y = 1

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PLAYER_SIZE = 50
PLAYER_SIZE_2 = (PLAYER_SIZE, PLAYER_SIZE)

COL_NUMBERS = 7 # Nombre de colonnes
COL_SIZE = WINDOW_WIDTH/COL_NUMBERS # taille d'une colonne

KEY_RIGHT = pygame.K_RIGHT
KEY_LEFT = pygame.K_LEFT

TO_THE_LEFT = -1
TO_THE_RIGHT = 1

SANIC_IMAGE = pygame.image.load("assets/images/sanic.png")
SANIC_IMAGE = pygame.transform.scale(SANIC_IMAGE, (50, 50))

TERMINATOR_IMAGE = pygame.image.load("assets/images/terminator.png")
TERMINATOR_IMAGE = pygame.transform.scale(TERMINATOR_IMAGE, (80, 80))
TERMINATOR_IMAGE = pygame.transform.rotate(TERMINATOR_IMAGE, 180)


pygame.init()

windowDimensions = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(windowDimensions)

window.fill(BG_COLOR)

fini = False
temps = pygame.time.Clock()

def col_to_pos(col):
    return col * COL_SIZE + COL_SIZE / 2

def create_entity(col: int, y: int, velocity: float, acceleration: float, skin, damage: float):
    entity = {
        "col": col,
        "x": col_to_pos(col),
        "y": y,
        "velocity": velocity,
        "acceleration": acceleration,
        "skin": skin,
        "damage": damage
    }

    if(skin):
        entity["x"] += skin.get_size()[0]

    return entity;



def create_player():
    return create_entity(COL_NUMBERS // 2, 500, 0.1, 0, None, 0.0)

player = create_player()

entities = []

def move_player_animation(delta_t, entity):
    goal = col_to_pos(entity["col"])
    
    if(player["x"] == goal):
        return

    delta_x = goal - entity["x"]

    if(delta_x > 0):
        entity["x"] += int(entity["velocity"] * delta_t)
    elif(delta_x < 0):
        entity["x"] -= int(entity["velocity"] * delta_t)
        
    if(player["x"] > goal - COL_SIZE / 2 and player["x"] < goal + COL_SIZE / 2):
        player["x"] = goal


def move(sens):
    global col_x
    
    if((player["col"] <= 1 and sens == TO_THE_LEFT) or (player["col"] >= COL_NUMBERS - 2 and sens == TO_THE_RIGHT)):
        return


    player["col"] += sens

def draw_entities():
    for entity in entities:
        window.blit(entity["skin"], (entity["x"], entity["y"]))

def move_entities(delta):
    for entity in entities:
        entity["velocity"] += entity["acceleration"] * delta
        entity["y"] += entity["velocity"] * delta

        if(entity["y"] > WINDOW_HEIGHT):
            entities.remove(entity)

def spawn_entities():
    if random.random() > 0.99:
        entities.append(
            create_entity(random.randint(0, COL_NUMBERS - 3), -100, 0, 0.0004, TERMINATOR_IMAGE, 0.0)
        )

while not fini:
    #--- Traiter entrées joueur
    for evenement in pygame.event.get():
        if evenement.type == pygame.QUIT:
            fini = True
        elif evenement.type == pygame.KEYDOWN:
            if evenement.key == KEY_RIGHT:
                move(TO_THE_RIGHT)
            elif evenement.key == KEY_LEFT:
                move(TO_THE_LEFT)


    window.fill(BG_COLOR)

    # affichage du joueur
    pygame.draw.rect(window, MAIN_COLOR, (
        (player["x"] - PLAYER_SIZE/2, player["y"]), # pour qu'il soit a l'exact milieu de l'ecran
        PLAYER_SIZE_2), 
        16, 3) #pour les bord arrondis et l'outline


    # pour les bords
    pygame.draw.rect(window, MAIN_COLOR, ((0, 0), (COL_SIZE, WINDOW_HEIGHT)))
    pygame.draw.rect(window, MAIN_COLOR, ((WINDOW_WIDTH - COL_SIZE, 0), (COL_SIZE, WINDOW_HEIGHT)))

    #--- 60 images par seconde
    delta = temps.tick(60)

    move_entities(delta)
    draw_entities()
    spawn_entities()
    move_player_animation(delta, player)

    #--- Afficher (rafraîchir) l'écran
    pygame.display.flip()


pygame.display.quit()
pygame.quit()