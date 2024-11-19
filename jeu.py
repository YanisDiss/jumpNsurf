"""
-------- ESPACE COMMENTAIRE --------






test




------------------------------------
"""

import pygame
import random
import math

BG_COLOR  = (  21, 21, 21)
MAIN_COLOR = (153, 164,   242)
SCORE_COLOR = (255, 255, 255)

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


HP_BAR_SIZE = 7
playerHealth = 100
playerMaxHealth = 100

# fonctionpour creer des images
def image(name: str, length: float, width: float, angle: float):
    img = pygame.image.load("assets/images/" + name + ".png")
    img = pygame.transform.scale(img, (length, width))
    img = pygame.transform.rotate(img, angle)
    return img

pygame.init()

windowDimensions = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(windowDimensions)

window.fill(BG_COLOR)

fini = False
temps = pygame.time.Clock()

def col_to_pos(col):
    return int(col * COL_SIZE + COL_SIZE / 2)

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
        entity["x"] -= skin.get_size()[0]/2

    return entity;



def create_player():
    return create_entity(COL_NUMBERS // 2, 500, 1, 0, None, 0.0)

player = create_player()

entities = []

def move_player_animation(delta_t, entity):
    goal = col_to_pos(entity["col"])
    threshold = 10 * entity["velocity"]
    if(player["x"] == goal):
        return

    delta_x = goal - entity["x"]

    """
    j'ai reussi a fix le stroke mais il faut
    encore que j'arrive a faire en sorte que sa position
    X ne soit pas offset quand j'arrive au goal
    (mets la vitesse plus forte = ce que je veux dire sera plus visible)
    
    """

    if(delta_x > threshold): # si il se deplace a droite
        if(player["x"] > goal):
            player["x"] = goal
        else:
            entity["x"] += entity["velocity"] * delta_t

    elif(delta_x < -threshold):# a gauche
        if(player["x"] < goal):
            player["x"] = goal
        else:
            entity["x"] -= entity["velocity"] * delta_t
    
def enemies():
    global player,playerHealth
    for entity in entities:
        if(entity["skin"] == TERMINATOR_IMAGE):
            th = 80
            if ((player["y"] <= entity["y"] + 30 and entity["y"] + th <= WINDOW_HEIGHT) and player["col"] == entity["col"]):
                entities.remove(entity)
                if playerHealth > 0: playerHealth -= entity["damage"]

def move(sens):
    global col_x, score
    
    if((player["col"] <= 1 and sens == TO_THE_LEFT) or (player["col"] >= COL_NUMBERS - 2 and sens == TO_THE_RIGHT)):
        return

    player["col"] += sens

    score += 1 #temporaire?

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
    if random.random() > 0.95:
        entities.append(
            create_entity(random.randint(1,COL_NUMBERS -2), -100, 1, 0, TERMINATOR_IMAGE, 5)
        )

# déclaration du score
score = 0
police = pygame.font.SysFont('monospace', WINDOW_HEIGHT//12, True) 

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


    # pour les bords
    pygame.draw.rect(window, MAIN_COLOR, ((0, 0), (COL_SIZE, WINDOW_HEIGHT)))
    pygame.draw.rect(window, MAIN_COLOR, ((WINDOW_WIDTH - COL_SIZE, 0), (COL_SIZE, WINDOW_HEIGHT)))


    #--- 60 images par seconde
    delta = temps.tick(60)

    move_entities(delta)
    draw_entities()
    spawn_entities()
    move_player_animation(delta, player)
    enemies()

     # affichage du joueur
    pygame.draw.rect(window, MAIN_COLOR, (
        (player["x"] - PLAYER_SIZE/2, player["y"]), # pour qu'il soit a l'exact milieu de l'ecran
        PLAYER_SIZE_2), 
        16, 3) #pour les bord arrondis et l'outline

    # barre de vie
    pygame.draw.rect(window, (255,0,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE, HP_BAR_SIZE)), 0, 3)
    pygame.draw.rect(window, (0,255,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE / playerMaxHealth * playerHealth, HP_BAR_SIZE)),0,3)


    # affichage du score
    marquoir = police.render(str(score), True, SCORE_COLOR)
    window.blit(marquoir, (WINDOW_WIDTH / 2, WINDOW_HEIGHT // 10))

    #--- Afficher (rafraîchir) l'écran
    pygame.display.flip()


pygame.display.quit()
pygame.quit()