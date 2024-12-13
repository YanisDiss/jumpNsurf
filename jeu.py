import pygame
import random

pygame.init()

####################################################### Initialization #######################################################

#### CONSTANTES ####
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

DEFAULT_COLOR = (0, 255, 255)

KEY_RIGHT = pygame.K_RIGHT
KEY_LEFT = pygame.K_LEFT
KEY_QUIT = pygame.K_q
KEY_ENTER = pygame.K_e
KEY_RETRY = pygame.K_r
KEY_PAUSE = pygame.K_p
KEY_UNPAUSE = pygame.K_ESCAPE

TO_THE_LEFT = -1
TO_THE_RIGHT = 1

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

# Partie musique du jeu
MENU_MUSIC = pygame.mixer.music.load("assets/audio/menu-music.mp3")

HP_BAR_SIZE = 7


player_max_health = 100
player_health = player_max_health

is_ini_start_menu = True
is_dead = False
in_pause = False
game_over = False 

pygame.mixer.init()
damage_sound = pygame.mixer.Sound("assets/audio/hurt.mp3")
heal_sound = pygame.mixer.Sound("assets/audio/potion1.mp3")

icon = pygame.image.load('assets/images/icon.png')
pygame.display.set_icon(icon)

pygame.display.set_caption("Jump'N'Surf")

windowDimensions = (WINDOW_WIDTH, WINDOW_HEIGHT)
window = pygame.display.set_mode(windowDimensions)

window.fill(BG_COLOR)
window_stopped = False
time = pygame.time.Clock()
time_elapsed = 0

####################################################### Utils #######################################################

def col_to_pos(col):
    return int(col * COL_SIZE + COL_SIZE / 2)


def play_music():
    pygame.mixer.music.play(loops=-1)

play_music()

####################################################### Entities #######################################################

def create_entity(col: int, y: int, velocity: float, acceleration: float, skin, damage: int, sike_probability: float = 0, sike_speed: float = 1):
    """
    Crée un dictionnaire représentant une entitée
    """

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
    """
    Crée l'entitée joueur
    """

    return create_entity(COL_NUMBERS // 2, 500, 1, 0, None, 0.0, 0)

def spawn_entity(entity_type: str):
    """
    Spawn une entitée en fonction de son type
    """
    
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

def collide_player():
    """
    Appelé pour detecter les entitiées qui rentrent en collision avec le joueur

    """
    global player, player_health
    for entity in entities:
        th = 80
        if (entity["damage"] != 0 and (player["y"] <= entity["y"] + 30 and entity["y"] + th <= WINDOW_HEIGHT) and player["col"] == entity["col"]):
            entities.remove(entity)
            if(entity["damage"] > 0):
                damage_sound.play()
            else:
                heal_sound.play()
            player_health = min(player_health - entity["damage"], player_max_health)


def move_player(sens):
    """
    Déplace le joueur d'une colone en fonction du sens.
    """
    
    global col_x
    
    if((player["col"] <= 1 and sens == TO_THE_LEFT) or (player["col"] >= COL_NUMBERS - 2 and sens == TO_THE_RIGHT)):
        return

    player["col"] += sens

def draw_entities():
    """
    Dessine les entitées à l'écran
    """

    for entity in entities:
        window.blit(entity["skin"], (entity["x"], entity["y"]))

def move_entity_animation(delta_t, entity):
    """
    Animation du mouvement des entitiées sur le côté
    """

    goal = col_to_pos(entity["col"])

    skin = entity["skin"]

    if(skin):
        goal -= skin.get_size()[0]/2
    threshold = 10 * entity["sike_speed"]

    if(entity["x"] == goal):
        return

    delta_x = goal - entity["x"]

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
    """
    Déplace toute les entitées en fonction du temps
    """

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
        if entity["y"] > WINDOW_HEIGHT:
            add_score(1)
            entities.remove(entity)

def spawn_entities():
    """
    Génère les entitiées en fonction du niveau et du spawn rate à chaque tick
    """

    for entity_type in levels[current_level]["entities"]:
        if time_elapsed % entity_type["spawn_rate"] == 0:
            entities.append(spawn_entity(entity_type["type"]))

####################################################### Level #######################################################


def create_level(col_amount: int, required_score: int, rgb_speed, message, entities: list):
    """
    Crée un level
    """
    return {
        "required_score": required_score,
        "col_amount": col_amount,
        "rgb_speed": rgb_speed,
        "message": message,
        "entities": entities
    }


levels = [
    # Level 1
    create_level(
        7,
        0,
        0,
        "Doge the enemies !",
        [
            {
                "type": "terminator",
                "spawn_rate": 50
            },
        ]
    ),
    # Level 2
    create_level(
        8,
        20,
        1,
        "Watch out for spike balls!",
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
    # Level 3
    create_level(
        7,
        50,
        5,
        "The cyphers are coming!",
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
    # Level 4
    create_level(
        7,
        100,
        10,
        "Survive the onslaught!",
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
    # Level 5
    create_level(
        7,
        150,
        20,
        "Still alive ? But not for long...",
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
            },
            {
                "type": "potion",
                "spawn_rate": 200
            }
        ]
    ),
    # Level 5
    create_level(
        7,
        250,
        20,
        "Quite impressive... Now, die!",
        [
            {
                "type": "terminator",
                "spawn_rate": 150
            },
            {
                "type": "spike_ball",
                "spawn_rate": 100
            },
            {
                "type": "cypher",
                "spawn_rate": 60
            },
            {   
                "type": "jake",
                "spawn_rate": 200
            },
            {
                "type": "potion",
                "spawn_rate": 220
            }
        ]
    ),
]


def add_score(amount: int):
    """
    Ajoute du score et augmente le niveau si besoin
    """

    global score, current_level
    score += amount
    prev_level = current_level

    for i in range(len(levels)):
        if levels[i]["required_score"] <= score:
            if i >= len(levels) - 1:
                current_level = len(levels) - 1
                break

            if levels[i + 1]["required_score"] > score:
                current_level = i

    if prev_level != current_level:
        display_level_up_text()

    
current_level = 0

####################################################### Render #######################################################

def draw_borders():
    """
    Dessine les bords
    """

    pygame.draw.rect(window, main_color, ((0, 0), (COL_SIZE, WINDOW_HEIGHT)))
    pygame.draw.rect(window, main_color, ((WINDOW_WIDTH - COL_SIZE, 0), (COL_SIZE, WINDOW_HEIGHT)))

def draw_player():
    """
    Dessine le joueur
    """
    
    pygame.draw.rect(window, main_color, (
    (player["x"] - PLAYER_SIZE/2, player["y"]), # pour qu'il soit a l'exact milieu de l'ecran
    PLAYER_SIZE_2), 
    16, 3) #pour les bord arrondis et l'outlineµ
    
def draw_hp():
    """
    Dessine le texte des HP
    """
    
    pygame.draw.rect(window, (255,0,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE, HP_BAR_SIZE)), 0, 3)
    pygame.draw.rect(window, (0,255,0), ((player["x"] - PLAYER_SIZE/2, player["y"] + 55), (PLAYER_SIZE / player_max_health * player_health, HP_BAR_SIZE)),0,3)

def draw_score():
    """
    Dessine le texte du score
    """
    
    marquoir = title_font.render(str(score), True, SCORE_COLOR)
    window.blit(marquoir, marquoir.get_rect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT // 10)))


def draw_game():
    """
    Dessine le jeu
    """

    window.fill(BG_COLOR)

    draw_borders()

    draw_player()

    draw_hp()

    draw_entities()

    draw_score()

    draw_level_up_text()

score = 0
title_font = pygame.font.SysFont('monospace', WINDOW_HEIGHT//12, True )
text_font = pygame.font.SysFont('monospace', WINDOW_HEIGHT//20, True ) 

def draw_home_screen():
    """
    Dessine l'écran d'acceuil du jeu
    """
    
    global title_font

    window.fill(main_color)

    police_title = pygame.font.SysFont('Monospace', 60, True)
    title = police_title.render("Jump'N'Surf", True, MPOLICE_COLOR)
    title_width, title_height = police_title.size("Jump'N'Surf")
    window.blit(title, ((WINDOW_WIDTH - title_width) // 2, (WINDOW_HEIGHT - title_height) // 3))

    message1 = title_font.render("[E]nter", True, M2POLICE_COLOR)
    message1_width, message1_height = title_font.size("[E]nter")
    window.blit(message1, ((WINDOW_WIDTH - message1_width) // 2, 3 * WINDOW_HEIGHT // 5))

    message2 = title_font.render("[Q]uit", True, M2POLICE_COLOR)
    message2_width, message2_height = title_font.size("[Q]uit")
    window.blit(message2, ((WINDOW_WIDTH - message2_width) // 2, 3 * WINDOW_HEIGHT // 5 + 1.2 * message2_height))

def draw_death_screen():
    """
    dessine l'écran de mort
    """

    global player_health, is_dead, title_font, score

    if player_health <= 0:
       is_dead = True
       window.fill(main_color)
       
       police_character = pygame.font.SysFont('monospace', 24, True)
       message = police_character.render("GAME OVER!", True, MPOLICE_COLOR)
       messageWidth, messageHeight = message.get_size()
       window.blit(message, ((WINDOW_WIDTH - messageWidth) // 2, (WINDOW_HEIGHT - messageHeight) // 2 - 25))

       # Afficher le score final
       score_message = police_character.render(f"Score : {score} ", True, SCORE_COLOR)
       score_width, score_height = score_message.get_size()
       window.blit(score_message, ((WINDOW_WIDTH - score_width) // 2, (WINDOW_HEIGHT - score_height) // 2 + 25))
    
       retry_message = police_character.render("[R]etry", True, MPOLICE_COLOR)
       retry_width, retry_height = retry_message.get_size()
       window.blit(retry_message, ((WINDOW_WIDTH - retry_width) // 2, (WINDOW_HEIGHT - retry_height) // 2 + 75))   

def reset():
    """
    Réinitalise l'état
    """

    global player_health, score, is_dead, is_ini_start_menu, entities, current_level, time_elapsed
    entities = []
    score = 0
    player_health = player_max_health
    is_dead = False
    is_ini_start_menu = False
    time_elapsed = 0
    current_level = 0
    reset_colors()
    pygame.mixer.music.stop()
    play_music()


level_up_display_timer = 0

def draw_level_up_text():
    """
    Dessine le texte de changement de niveau
    """

    if level_up_display_timer <= 0:
        return

    global title_font, entities, current_level

    message = title_font.render(f"Phase {current_level + 1}", True, SCORE_COLOR)
    messageWidth, messageHeight = message.get_size()
    window.blit(message, ((WINDOW_WIDTH - messageWidth) // 2, (WINDOW_HEIGHT - messageHeight) // 2 - 30))

    message = text_font.render(f"{levels[current_level]['message']}", True, SCORE_COLOR)
    messageWidth, messageHeight = message.get_size()
    window.blit(message, ((WINDOW_WIDTH - messageWidth) // 2, (WINDOW_HEIGHT - messageHeight) // 2 + 30))
    
def update_level_up_text_counter(delta):
    """
    Met a jour le compteur pour le texte de level up a afficher
    """

    global level_up_display_timer

    if level_up_display_timer > 0:
        level_up_display_timer -= delta

def display_level_up_text():
    """
    Fait apparaitre le texte de level up pendant 3 secondes
    """

    global level_up_display_timer
    level_up_display_timer = 3000

display_level_up_text()

def draw_paused_game():
    """
    Met le jeu en pause
    """

    global title_font, in_pause

    in_pause = True
    window.fill(main_color)

    retry_message = title_font.render("Game in pause !", True, MPOLICE_COLOR)
    retry_width, retry_height = retry_message.get_size()
    window.blit(retry_message, ((WINDOW_WIDTH - retry_width) // 2, (WINDOW_HEIGHT - retry_height) // 2 - 30))

    un_pause_message = text_font.render("Press [Echap] to go back to the game", True, M2POLICE_COLOR)
    un_pause_message_width, un_pause_message_height = un_pause_message.get_size()
    window.blit(un_pause_message, ((WINDOW_WIDTH - un_pause_message_width) // 2, (WINDOW_HEIGHT - un_pause_message_height) // 2 + 30))

####################################################### Color animation #######################################################

def reset_colors():
    global main_color, red, green, blue, ry, yg, gc, cb, bp, pr

    main_color = (DEFAULT_COLOR[0], DEFAULT_COLOR[1], DEFAULT_COLOR[2])
    red=main_color[0]
    green=main_color[1]
    blue=main_color[2]

    ry = False #red to yellow
    yg = False # yellow to green
    gc = False # green to cyan
    cb = False # cyan to blue
    bp = False # blue to purple
    pr = False # purple to red

reset_colors()

def animate_color(speed):
    """
    Anime les couleurs (rgb)
    """
    
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

def pause_game(pause: bool):
    global in_pause
    
    in_pause = pause
    
    if in_pause:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()

def manage_keys():
    global in_pause, is_dead, window_stopped, is_ini_start_menu
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
            window_stopped = True
        elif event.type == pygame.KEYDOWN:
            if event.key == KEY_RIGHT:
                move_player(TO_THE_RIGHT)
            elif event.key == KEY_LEFT:
                move_player(TO_THE_LEFT)
            elif event.key == KEY_ENTER:
                is_ini_start_menu = False
            elif event.key == KEY_QUIT:
                exit()
                window_stopped = True
            elif event.key == KEY_RETRY and is_dead:
                reset()
            elif event.key == KEY_PAUSE:
                    pause_game(True)
            elif event.key == KEY_UNPAUSE:
                    pause_game(False)

####################################################### Main loop #######################################################

while not window_stopped:
    manage_keys()

    delta = time.tick(60)
                        
    if is_ini_start_menu:
        draw_home_screen()
    elif in_pause:
        draw_paused_game()
    elif is_dead:
        draw_death_screen()
    else:
        draw_game()
        move_entities(delta)
        spawn_entities()
        move_entity_animation(delta, player)
        collide_player()
        draw_death_screen()
        animate_color(levels[current_level]["rgb_speed"] * 2)
        update_level_up_text_counter(delta)

        time_elapsed += delta

    pygame.display.flip()

pygame.time.wait(5000)
pygame.display.quit()
pygame.quit()
exit()