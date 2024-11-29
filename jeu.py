"""
-------- ESPACE COMMENTAIRE --------






test




------------------------------------
"""

import pygame
import random

####################################################### Initialization #######################################################
BG_COLOR  = (  21, 21, 21)
SCORE_COLOR = (255, 255, 255)
MENU_COLOR = (56, 82, 128)
MPOLICE_COLOR = (0, 0, 0)
M2POLICE_COLOR = (36, 37, 38)

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
KEY_QUIT = pygame.K_q
KEY_ENTER = pygame.K_e
KEY_RETRY = pygame.K_r

TO_THE_LEFT = -1
TO_THE_RIGHT = 1

SANIC_IMAGE = pygame.image.load("assets/images/sanic.png")
SANIC_IMAGE = pygame.transform.scale(SANIC_IMAGE, (50, 50))

TERMINATOR_IMAGE = pygame.image.load("assets/images/terminator.png")
TERMINATOR_IMAGE = pygame.transform.scale(TERMINATOR_IMAGE, (80, 80))
TERMINATOR_IMAGE = pygame.transform.rotate(TERMINATOR_IMAGE, 180)

SPIKE_BALL_IMAGE = pygame.image.load("assets/images/spikeball.png")
SPIKE_BALL_IMAGE = pygame.transform.scale(SPIKE_BALL_IMAGE, (80, 80))
SPIKE_BALL_IMAGE = pygame.transform.rotate(SPIKE_BALL_IMAGE, 180)

CYPHER_IMAGE = pygame.image.load("assets/images/cypher.png")
CYPHER_IMAGE = pygame.transform.scale(CYPHER_IMAGE, (120, 100))

JAKE_IMAGE = pygame.image.load("assets/images/jake.png")
JAKE_IMAGE = pygame.transform.scale(JAKE_IMAGE, (100, 120))

POTION_IMAGE = pygame.image.load("assets/images/potion.png")
POTION_IMAGE = pygame.transform.scale(POTION_IMAGE, (80, 80))

HP_BAR_SIZE = 7
playerMaxHealth = 100
playerHealth = playerMaxHealth

main_color = (0,255,255)

# fonctionpour creer des images
def image(name: str, length: float, width: float, angle: float):
    img = pygame.image.load("assets/images/" + name + ".png")
    img = pygame.transform.scale(img, (length, width))
    img = pygame.transform.rotate(img, angle)
    return img

pygame.init()

pygame.mixer.init()
damageSound = pygame.mixer.Sound("assets/audio/hurt.mp3")

pygame_icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(pygame_icon)

windowDimensions = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(windowDimensions)

window.fill(BG_COLOR)
fini = False
temps = pygame.time.Clock()
time_elapsed = 0

def col_to_pos(col):
    return int(col * COL_SIZE + COL_SIZE / 2)

####################################################### Entities #######################################################

def create_entity(col: int, y: int, velocity: float, acceleration: float, skin, damage: int, sike_probability = 0, sike_speed = 1):
    entity = {
        "col": col,
        "x": col_to_pos(col),
        "y": y,
        "velocity": velocity,
        "acceleration": acceleration,
        "skin": skin,
        "damage": damage,
        "sike_probability": sike_probability,
        "sike_speed": sike_speed
    }

    if(skin):
        entity["x"] -= skin.get_size()[0]/2

    return entity

def create_player():
    return create_entity(COL_NUMBERS // 2, 500, 1, 0, None, 0.0, 0)

def spawn_entity(entity_type):
    if entity_type == "terminator":
        return create_entity(random.randint(1,COL_NUMBERS -2), -100, 0.5, 0, TERMINATOR_IMAGE, 5, 0, .5)
    if entity_type == "spike_ball":
        return create_entity(random.randint(1,COL_NUMBERS -2), -100, 0.2, 0.002, SPIKE_BALL_IMAGE, 10, 0.005, .5)
    if entity_type == "cypher":
        return create_entity(random.randint(1,COL_NUMBERS -2), -100, 0.2, 0, CYPHER_IMAGE, 50, 0.002)
    if entity_type == "jake":
        return create_entity(random.randint(1,COL_NUMBERS -2), -100, 0.05, 0, JAKE_IMAGE, 99999, 0)
    if entity_type == 'potion':
        return create_entity(random.randint(1,COL_NUMBERS -2), -100, 0.2, 0, POTION_IMAGE, -50, 0)

player = create_player()

entities = []

def damage_player():
    global player, playerHealth
    for entity in entities:
        th = 80
        if (entity["damage"] != 0 and (player["y"] <= entity["y"] + 30 and entity["y"] + th <= WINDOW_HEIGHT) and player["col"] == entity["col"]):
            entities.remove(entity)
            damageSound.play()
            if playerHealth > 0 and playerHealth - entity["damage"] < playerMaxHealth: playerHealth -= entity["damage"]

            
def move_player(sens):
    global col_x, score
    
    if((player["col"] <= 1 and sens == TO_THE_LEFT) or (player["col"] >= COL_NUMBERS - 2 and sens == TO_THE_RIGHT)):
        return

    player["col"] += sens

    add_score(1)

def draw_entities():
    for entity in entities:
        window.blit(entity["skin"], (entity["x"], entity["y"]))

def move_entity_animation(delta_t, entity):
    goal = col_to_pos(entity["col"])

    skin = entity["skin"]

    if(skin):
        goal -= skin.get_size()[0]/2
    threshold = 10 * entity["sike_speed"]

    if(entity["x"] == goal):
        return

    delta_x = goal - entity["x"]

    """
    j'ai reussi a fix le stroke mais il faut
    encore que j'arrive a faire en sorte que sa position
    X ne soit pas offset quand j'arrive au goal
    (mets la vitesse plus forte = ce que je veux dire sera plus visible)
    
    """

    if(delta_x > threshold): # si il se deplace a droite
        if(entity["x"] > goal):
            entity["x"] = goal
        else:
            entity["x"] += entity["sike_speed"] * delta_t

    elif(delta_x < -threshold):# a gauche
        if(entity["x"] < goal):
            entity["x"] = goal
        else:
            entity["x"] -= entity["sike_speed"] * delta_t

def move_entities(delta):
    for entity in entities:
        entity["velocity"] += entity["acceleration"] * delta
        entity["y"] += entity["velocity"] * delta

        if entity["sike_probability"] and (random.random() > 1 - entity["sike_probability"]):
            if(entity["col"] == 1):
                entity["col"] += 1
            elif(entity["col"] == COL_NUMBERS - 2):
                entity["col"] -= 1
            else:
                entity["col"] += random.randrange(-1, 2, 2)
        
        move_entity_animation(delta, entity)
        

        if(entity["y"] > WINDOW_HEIGHT):
            entities.remove(entity)

def spawn_entities():
    for entity_type in levels[current_level]["entities"]:
        if time_elapsed % entity_type["spawn_rate"] == 0:
            entities.append(spawn_entity(entity_type["type"]))

####################################################### Level #######################################################


def create_level(col_amount: int, required_score: int, rgb_speed, entities: list):
    return {
        "required_score": required_score,
        "col_amount": col_amount,
        "rgb_speed": rgb_speed,
        "entities": entities
    }


levels = [
    # Level 1
    create_level(
        7,
        0,
        0,
        [
            {
                "type": "terminator",
                "spawn_rate": 50
            },
              
        ]
    ),
    create_level(
        7,
        50,
        1,
        [
            {
                "type": "terminator",
                "spawn_rate": 50
            },
            {
                "type": "spike_ball",
                "spawn_rate": 100
            },
            {
                "type": "potion",
                "spawn_rate": 400
            }   
        ]
    ),
    create_level(
        7,
        100,
        10,
        [
            {
                "type": "terminator",
                "spawn_rate": 40
            },
            {
                "type": "spike_ball",
                "spawn_rate": 100
            },
                        {
                "type": "cypher",
                "spawn_rate": 200
            },
            {
                "type": "potion",
                "spawn_rate": 400
            }
        ]
    ),
    create_level(
        7,
        150,
        30,
        [
            {
                "type": "terminator",
                "spawn_rate": 30
            },
            {
                "type": "spike_ball",
                "spawn_rate": 80
            },
            
            {
                "type": "cypher",
                "spawn_rate": 100
            },
            {
                "type": "potion",
                "spawn_rate": 400
            }
        ]
    ),
    create_level(
        7,
        200,
        50,
        [
            {
                "type": "terminator",
                "spawn_rate": 100
            },
            {
                "type": "spike_ball",
                "spawn_rate": 50
            },
            {
                "type": "cypher",
                "spawn_rate": 50
            },
            {   
                "type": "jake",
                "spawn_rate": 200
            }
        ]
    ),
]

def add_score(amount: int):
    global score, current_level
    score += amount

    for i in range(len(levels)):
        if levels[i]["required_score"] <= score:
            if i >= len(levels) - 1:
                current_level = len(levels) - 1
                break

            if levels[i + 1]["required_score"] > score:
                current_level = i

    
current_level = 0

####################################################### Render #######################################################

def draw_borders():
    """
    Dessine les bords
    """
    pygame.draw.rect(window, main_color, ((0, 0), (COL_SIZE, WINDOW_HEIGHT)))
    pygame.draw.rect(window, main_color, ((WINDOW_WIDTH - COL_SIZE, 0), (COL_SIZE, WINDOW_HEIGHT)))

def draw_player():
    pygame.draw.rect(window, main_color, (
    (player["x"] - PLAYER_SIZE/2, player["y"]), # pour qu'il soit a l'exact milieu de l'ecran
    PLAYER_SIZE_2), 
    16, 3) #pour les bord arrondis et l'outlineµ
    
def draw_hp():
    pygame.draw.rect(window, (255,0,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE, HP_BAR_SIZE)), 0, 3)
    pygame.draw.rect(window, (0,255,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE / playerMaxHealth * playerHealth, HP_BAR_SIZE)),0,3)

def draw_score():
    marquoir = police.render(str(score), True, SCORE_COLOR)
    window.blit(marquoir, marquoir.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT // 10)))


def draw_game():
    window.fill(BG_COLOR)

    draw_borders()

    draw_player()

    draw_hp()

    draw_entities()

    draw_score()

score = 0
police = pygame.font.SysFont('monospace', WINDOW_HEIGHT//12, True ) 

def render_home_screen():
    global police

    window.fill(main_color)

    police_title = pygame.font.SysFont('Monospace', 60, True)
    title = police_title.render("Jump'N'Surf", True, MPOLICE_COLOR)
    title_width, title_height = police_title.size("Jump'N'Surf")
    window.blit(title, ((WINDOW_WIDTH - title_width) // 2, (WINDOW_HEIGHT - title_height) // 4))

    message1 = police.render("[E]nter", True, M2POLICE_COLOR)
    message1_width, message1_height = police.size("[E]nter")
    window.blit(message1, ((WINDOW_WIDTH - message1_width) // 2, 3 * WINDOW_HEIGHT // 5))

    message2 = police.render("[Q]uit", True, M2POLICE_COLOR)
    message2_width, message2_height = police.size("[Q]uit")
    window.blit(message2, ((WINDOW_WIDTH - message2_width) // 2, 3 * WINDOW_HEIGHT // 5 + 1.2 * message2_height))

def render_death_screen():
   global playerHealth, isDead, police, score

   if playerHealth <= 0:
       isDead = True
       window.fill(main_color)

       police_character = pygame.font.SysFont('monospace', 24, True)
       message = police_character.render("GAME OVER", True, MPOLICE_COLOR)
       messageWidth, messageHeight = police_character.size("GAME OVER!")
       window.blit(message, ((WINDOW_WIDTH - messageWidth) // 2, (WINDOW_HEIGHT - messageHeight) // 2))

       # Afficher le score final
       score_message = police_character.render(f"Score : {score} ", True, SCORE_COLOR)
       score_width, score_height = score_message.get_size()
       window.blit(score_message, ((WINDOW_WIDTH - score_width) // 2, (WINDOW_HEIGHT - score_height) // 2 + 50))
    
       retry_message = police_character.render("[R]etry", True, MPOLICE_COLOR)
       retry_width, retry_height = retry_message.get_size()
       window.blit(retry_message, ((WINDOW_WIDTH - retry_width) // 2, (WINDOW_HEIGHT - retry_height) // 2 + 100))       

def reset():
    global playerHealth, score, isDead, isInStartMenu, entities, current_level, time_elapsed
    entities = []
    score = 0
    playerHealth = playerMaxHealth
    isDead = False
    isInStartMenu = False
    time_elapsed = 0
    current_level = 0
    


####################################################### Color animation #######################################################

red=main_color[0]
green=main_color[1]
blue=main_color[2]

ry = False #red to yellow
yg = False # yellow to green
gc = False # green to cyan
cb = False # cyan to blue
bp = False # blue to purple
pr = False # purple to red

def animate_color(speed):
    global main_color, red, green, blue, ry,yg,gc,cb,bp,pr
    if(speed == 0):
        return
    
    # red to green
    if (red == 255 and green < 255 and blue ==0): ry = True
    elif (red == 255 and green == 255 and blue ==0): yg = True

    if (red == 255 and green == 255 and blue ==0): ry = False
    if (red == 0 and green == 255 and blue ==0): yg = False

    # green to blue
    if (green == 255 and blue < 255 and red == 0): gc = True
    elif (green == 255 and blue == 255 and red == 0): cb = True

    if (green == 255 and blue == 255 and red == 0): gc = False
    if (green == 0 and blue == 255 and red == 0): cb = False

    # blue to red
    if (blue == 255 and red < 255 and green == 0): bp = True
    elif (blue == 255 and red == 255 and green == 0): pr = True

    if (blue == 255 and red == 255 and green == 0): bp = False
    if (blue == 0 and blue == red and green == 0): pr = False
    

    if (0<=red<256 and 0<=green<256 and 0<=blue<256):
                if yg:
                    red = max(red - speed, 0)
                    cb = False
                    bp = False
                    pr = False
                if ry:
                    green = min(green + speed, 255)
                    bp = False
                    pr = False
                    ry = False
              
                if cb:
                    green = max(green - speed, 0)
                    pr = False
                    ry = False
                    yg = False
                if gc:
                    blue = min(blue + speed, 255)
                    ry = False
                    yg = False
                    gc = False

                if pr:
                    blue = max(blue - speed, 0)
                    yg = False
                    gc = False
                    cb = False
                if bp:
                    red = min(red + speed, 255)
                    gc = False
                    cb = False
                    bp = False

    main_color = (red,green,blue)

####################################################### Main loop #######################################################

isInStartMenu = True
isDead = False

while not fini:
        #--- Traiter entrées joueur
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                exit()
                fini = True
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == KEY_RIGHT:
                    move_player(TO_THE_RIGHT)
                elif evenement.key == KEY_LEFT:
                    move_player(TO_THE_LEFT)
                elif evenement.key == KEY_ENTER:
                    isInStartMenu = False
                elif evenement.key == KEY_QUIT:
                    exit()
                    fini = True
                elif evenement.key == KEY_RETRY:
                    if isDead == True:
                        reset()

        if isInStartMenu:
            render_home_screen()
        else:
            #--- 60 images par seconde
            delta = temps.tick(60)
            draw_game()
            move_entities(delta)
            spawn_entities()
            move_entity_animation(delta, player)
            damage_player()
            render_death_screen()
            animate_color(levels[current_level]["rgb_speed"] * 2)

            time_elapsed += delta

        #--- Afficher (rafraîchir) l'écran
        pygame.display.flip()

pygame.time.wait(5000)
pygame.display.quit()
pygame.quit()
exit()