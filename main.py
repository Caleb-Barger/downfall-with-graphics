import libtcodpy as libtcod
import pygame

import constants

#  ____    __                           __
# /\  _`\ /\ \__                       /\ \__
# \ \,\L\_\ \ ,_\  _ __   __  __    ___\ \ ,_\   ____
#  \/_\__ \\ \ \/ /\`'__\/\ \/\ \  /'___\ \ \/  /',__\
#    /\ \L\ \ \ \_\ \ \/ \ \ \_\ \/\ \__/\ \ \_/\__, `\
#    \ `\____\ \__\\ \_\  \ \____/\ \____\\ \__\/\____/
#     \/_____/\/__/ \/_/   \/___/  \/____/ \/__/\/___/


class str_Tile:
    def __init__(self, block_path):
        self.block_path = block_path
        self.explored = False


#  _____   __                          __
# /\  __`\/\ \       __               /\ \__
# \ \ \/\ \ \ \____ /\_\     __    ___\ \ ,_\   ____
#  \ \ \ \ \ \ '__`\\/\ \  /'__`\ /'___\ \ \/  /',__\
#   \ \ \_\ \ \ \L\ \\ \ \/\  __//\ \__/\ \ \_/\__, `\
#    \ \_____\ \_,__/_\ \ \ \____\ \____\\ \__\/\____/
#     \/_____/\/___//\ \_\ \/____/\/____/ \/__/\/___/
#                   \ \____/
#                    \/___/


class obj_Actor:
    def __init__(self, x, y, name_object, sprite, creature=None, ai=None):
        self.x, self.y = x, y  # Map address
        self.name_object = name_object
        self.sprite = sprite

        self.creature = creature
        if creature:
            creature.owner = self

        self.ai = ai
        if ai:
            ai.owner = self

    def draw(self):
        is_visable = libtcod.map_is_in_fov(FOV_MAP, self.x, self.y)

        if is_visable:
            SURFACE_MAIN.blit(
                self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))


class obj_Game:
    def __init__(self):

        self.current_map = map_create()
        self.current_objects = []

        self.message_history = []



#  ____                                                           __
# /\  _`\                                                        /\ \__
# \ \ \/\_\    ___     ___   _____     ___     ___      __    ___\ \ ,_\   ____
#  \ \ \/_/_  / __`\ /' _ `\/\ '__`\  / __`\ /' _ `\  /'__`\/' _ `\ \ \/  /',__\
#   \ \ \L\ \/\ \L\ \/\ \/\ \ \ \L\ \/\ \L\ \/\ \/\ \/\  __//\ \/\ \ \ \_/\__, `\
#    \ \____/\ \____/\ \_\ \_\ \ ,__/\ \____/\ \_\ \_\ \____\ \_\ \_\ \__\/\____/
#     \/___/  \/___/  \/_/\/_/\ \ \/  \/___/  \/_/\/_/\/____/\/_/\/_/\/__/\/___/
#                              \ \_\
#                               \/_/


class com_Creature:
    '''
    Creatures have health and can damage other objects by attacking them... they can also die
    '''

    def __init__(self, name_instance, hp=10, death_function=None):
        self.name_instance = name_instance
        self.max_hp = hp
        self.hp = hp
        self.death_function = death_function

    def move(self, dx, dy):

        tile_is_wall = (GAME.current_map[self.owner.x + dx]
                        [self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(
            self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target, 5)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        game_message(f"{self.name_instance} attacks {target.creature.name_instance} for {damage} damage!", constants.COLOR_WHITE)
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        game_message(f"{self.name_instance}'s health is {self.hp}/{self.max_hp}", constants.COLOR_RED)

        if self.hp <= 0:
            if self.death_function is not None:
                self.death_function(self.owner)

# class com_Item:

# class com_Container:


#  ______  ______
# /\  _  \/\__  _\
# \ \ \L\ \/_/\ \/
#  \ \  __ \ \ \ \
#   \ \ \/\ \ \_\ \__
#    \ \_\ \_\/\_____\
#     \/_/\/_/\/_____/


class ai_Test:
    '''
    Once per turn, execute
    '''

    def take_turn(self):
        self.owner.creature.move(libtcod.random_get_int(0, -1, 1),
                                 libtcod.random_get_int(0, -1, 1))


def death_monstor(monstor):
    ''' On death, most monstors stop moving'''
    # print(f"{monstor.creature.name_instance} is dead")
    game_message(f"{monstor.creature.name_instance} is dead", constants.COLOR_GREY)
    monstor.creature = None
    monstor.ai = None


#  /'\_/`\
# /\      \     __     _____
# \ \ \__\ \  /'__`\  /\ '__`\
#  \ \ \_/\ \/\ \L\.\_\ \ \L\ \
#   \ \_\\ \_\ \__/.\_\\ \ ,__/
#    \/_/ \/_/\/__/\/_/ \ \ \/
#                        \ \_\
#                         \/_/


def map_create():

    new_map = [[str_Tile(False) for y in range(0, constants.MAP_HEIGHT)]
               for x in range(0, constants.MAP_WIDTH)]

    for x in range(constants.MAP_WIDTH):
        new_map[x][0].block_path = True
        new_map[x][constants.MAP_HEIGHT-1].block_path = True

    for y in range(constants.MAP_HEIGHT):
        new_map[0][y].block_path = True
        new_map[constants.MAP_WIDTH-1][y].block_path = True

    new_map[10][10].block_path = True
    new_map[12][8].block_path = True
    new_map[5][5].block_path = True

    map_make_fov(new_map)

    return new_map


def map_check_for_creatures(x, y, exclude_object=None):

    target = None

    if exclude_object:
        # check objlist to find creature at that location that is not excluded
        for obj in GAME.current_objects:
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                    obj.creature):

                target = obj

            if target:
                return target

    else:
        # check objlist to find any creature at that location
        for obj in GAME.current_objects:
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                    obj.creature):

                target = obj

            if target:
                return target


def map_make_fov(incoming_map):
    global FOV_MAP

    FOV_MAP = libtcod.map_new(constants.MAP_WIDTH, constants.MAP_HEIGHT)

    for y in range(constants.MAP_HEIGHT):
        for x in range(constants.MAP_WIDTH):
            libtcod.map_set_properties(FOV_MAP, x, y,
                                       not incoming_map[x][y].block_path, not incoming_map[x][y].block_path)


def map_calculate_fov():
    global FOV_CALCULATE

    if FOV_CALCULATE:
        FOV_CALCULATE = False
        libtcod.map_compute_fov(FOV_MAP, PLAYER.x, PLAYER.y, constants.TORCH_RADIUS, constants.FOV_LIGHT_WALLS,
                                constants.FOV_ALGO)


#  ____
# /\  _`\
# \ \ \/\ \  _ __    __     __  __  __
#  \ \ \ \ \/\`'__\/'__`\  /\ \/\ \/\ \
#   \ \ \_\ \ \ \//\ \L\.\_\ \ \_/ \_/ \
#    \ \____/\ \_\\ \__/.\_\\ \___x___/'
#     \/___/  \/_/ \/__/\/_/ \/__//__/


def draw_game():

    global SURFACE_MAIN

    # clear surface
    SURFACE_MAIN.fill(constants.COLOR_DEFAULT_BG)

    # draw the map
    draw_map(GAME.current_map)

    # draw obj's
    for obj in GAME.current_objects:
        obj.draw()

    draw_debug()
    draw_messages()

    # update the display
    pygame.display.flip()


def draw_map(map):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):

            is_visable = libtcod.map_is_in_fov(FOV_MAP, x, y)

            if is_visable:

                map[x][y].explored = True

                if map[x][y].block_path:
                    # Draw a wall
                    SURFACE_MAIN.blit(
                        constants.S_WALL, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))
                else:
                    # Draw the floor
                    SURFACE_MAIN.blit(
                        constants.S_FLOOR, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))

            elif map[x][y].explored:
                if map[x][y].block_path:
                    # Draw a wall
                    SURFACE_MAIN.blit(
                        constants.S_WALLEXPLORED, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))
                else:
                    # Draw the floor
                    SURFACE_MAIN.blit(
                        constants.S_FLOOREXPLORED, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))


def draw_debug():
    
    draw_text(SURFACE_MAIN, f"FPS: {str(int(CLOCK.get_fps()))}", (0, 0), constants.COLOR_WHITE, constants.COLOR_BLACK)

def draw_messages():
    
    if len(GAME.message_history) <= constants.NUM_MESSAGES:
        to_draw = GAME.message_history # <--- MAGIC NUMBER FIX THIS LATER!!!
    else:
        to_draw = GAME.message_history[-constants.NUM_MESSAGES:]

    text_height = helper_text_height(constants.FONT_MESSAGE_TEXT)

    start_y = (constants.MAP_HEIGHT*constants.CELL_HEIGHT - (constants.NUM_MESSAGES * text_height)) - 10

    i = 0
    
    for message, color in to_draw:

        draw_text(SURFACE_MAIN, message, (0, start_y + (i * text_height)), color, constants.COLOR_BLACK)

        i += 1
        

def draw_text(display_surface, text_to_display, T_coords, text_color, back_color=None):
    
    ''' this function takes in some text and displays it on surface arg'''

    text_surface, text_rect = helper_text_objects(text_to_display, text_color, back_color)

    text_rect.topleft = T_coords

    display_surface.blit(text_surface, text_rect)


#  __  __          ___
# /\ \/\ \        /\_ \
# \ \ \_\ \     __\//\ \    _____      __   _ __   ____
#  \ \  _  \  /'__`\\ \ \  /\ '__`\  /'__`\/\`'__\/',__\
#   \ \ \ \ \/\  __/ \_\ \_\ \ \L\ \/\  __/\ \ \//\__, `\
#    \ \_\ \_\ \____\/\____\\ \ ,__/\ \____\\ \_\\/\____/
#     \/_/\/_/\/____/\/____/ \ \ \/  \/____/ \/_/ \/___/
#                             \ \_\
#                              \/_/


def helper_text_objects(incoming_text, incoming_color, incoming_bg):
    ''' renders out the text and gives a surf and rect'''

    if incoming_bg:
        Text_surface = constants.FONT_DEBUG_MESSAGE.render(
            incoming_text, False, incoming_color, incoming_bg)
        
    else:
        Text_surface = constants.FONT_DEBUG_MESSAGE.render(
            incoming_text, False, incoming_color)

    return Text_surface, Text_surface.get_rect()

def helper_text_height(font):
    
    font_object = font.render('g', False, (0, 0, 0))
    font_rect = font_object.get_rect()
    
    return font_rect.height


#  ____
# /\  _`\
# \ \ \L\_\     __      ___ ___      __
#  \ \ \L_L   /'__`\  /' __` __`\  /'__`\
#   \ \ \/, \/\ \L\.\_/\ \/\ \/\ \/\  __/
#    \ \____/\ \__/.\_\ \_\ \_\ \_\ \____\
#     \/___/  \/__/\/_/\/_/\/_/\/_/\/____/


def main_game_loop():
    '''In this function loop the main game'''
    game_quit = False
    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys()

        map_calculate_fov()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME.current_objects:
                if obj.ai:
                    obj.ai.take_turn()

        draw_game()

        CLOCK.tick(constants.GAME_FPS)

    pygame.quit()
    exit()

def game_initalize():
    '''This function initalizes the main window in pygame'''

    global SURFACE_MAIN, GAME, CLOCK, FOV_CALCULATE, PLAYER, ENEMY

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(
        (constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    GAME = obj_Game()

    CLOCK = pygame.time.Clock()


    FOV_CALCULATE = True

    creature_com1 = com_Creature("Caleb")
    PLAYER = obj_Actor(3, 3, "Python", constants.S_PLAYER,
                       creature=creature_com1)

    creature_com2 = com_Creature("Kevin", death_function=death_monstor)
    ai_com = ai_Test()
    ENEMY = obj_Actor(10, 5, "Crab", constants.S_ENEMY,
                      creature=creature_com2, ai=ai_com)

    GAME.current_objects = [PLAYER, ENEMY]


def game_handle_keys():
    global FOV_CALCULATE
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                PLAYER.creature.move(0, -1)
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_s:
                PLAYER.creature.move(0, 1)
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_a:
                PLAYER.creature.move(-1, 0)
                FOV_CALCULATE = True
                return "player-moved"

            if event.key == pygame.K_d:
                PLAYER.creature.move(1, 0)
                FOV_CALCULATE = True
                return "player-moved"

    return "no-action"


def game_message(game_msg, msg_color):
    
    GAME.message_history.append((game_msg, msg_color))


if __name__ == '__main__':
    game_initalize()
    main_game_loop()
