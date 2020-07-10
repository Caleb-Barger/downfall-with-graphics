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
        SURFACE_MAIN.blit(
            self.sprite, (self.x*constants.CELL_WIDTH, self.y*constants.CELL_HEIGHT))


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

        tile_is_wall = (GAME_MAP[self.owner.x + dx]
                        [self.owner.y + dy].block_path == True)

        target = map_check_for_creatures(
            self.owner.x + dx, self.owner.y + dy, self.owner)

        if target:
            self.attack(target, 5)

        if not tile_is_wall and target is None:
            self.owner.x += dx
            self.owner.y += dy

    def attack(self, target, damage):
        print(
            f"{self.name_instance} attacks {target.creature.name_instance} for {damage} damage!")
        target.creature.take_damage(damage)

    def take_damage(self, damage):
        self.hp -= damage
        print(f"{self.name_instance}'s health is {self.hp}/{self.max_hp}")

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
    print(f"{monstor.creature.name_instance} is dead")
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

    return new_map


def map_check_for_creatures(x, y, exclude_object=None):

    target = None

    if exclude_object:
        # check objlist to find creature at that location that is not excluded
        for obj in GAME_OBJECTS:
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                    obj.creature):

                target = obj

            if target:
                return target

    else:
        # check objlist to find any creature at that location
        for obj in GAME_OBJECTS:
            if (obj is not exclude_object and
                obj.x == x and
                obj.y == y and
                    obj.creature):

                target = obj

            if target:
                return target


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
    draw_map(GAME_MAP)

    # draw obj's
    for obj in GAME_OBJECTS:
        obj.draw()

    # update the display
    pygame.display.flip()


def draw_map(map):
    for x in range(0, constants.MAP_WIDTH):
        for y in range(0, constants.MAP_HEIGHT):
            if map[x][y].block_path:
                # Draw a wall
                SURFACE_MAIN.blit(
                    constants.S_WALL, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))
            else:
                # Draw the floor
                SURFACE_MAIN.blit(
                    constants.S_FLOOR, (constants.CELL_WIDTH*x, constants.CELL_HEIGHT*y))


#                                    __
#  /'\_/`\            __            /\ \
# /\      \     __   /\_\    ___    \ \ \        ___     ___   _____
# \ \ \__\ \  /'__`\ \/\ \ /' _ `\   \ \ \  __  / __`\  / __`\/\ '__`\
#  \ \ \_/\ \/\ \L\.\_\ \ \/\ \/\ \   \ \ \L\ \/\ \L\ \/\ \L\ \ \ \L\ \
#   \ \_\\ \_\ \__/.\_\\ \_\ \_\ \_\   \ \____/\ \____/\ \____/\ \ ,__/
#    \/_/ \/_/\/__/\/_/ \/_/\/_/\/_/    \/___/  \/___/  \/___/  \ \ \/
#                                                                \ \_\
#                                                                 \/_/


def main_game_loop():
    '''In this function loop the main game'''
    game_quit = False
    player_action = "no-action"

    while not game_quit:

        player_action = game_handle_keys()

        if player_action == "QUIT":
            game_quit = True

        if player_action != "no-action":
            for obj in GAME_OBJECTS:
                if obj.ai:
                    obj.ai.take_turn()

        draw_game()

    pygame.quit()
    exit()


#  ______              __             ___
# /\__  _\          __/\ \__         /\_ \    __
# \/_/\ \/     ___ /\_\ \ ,_\    __  \//\ \  /\_\  ____      __
#    \ \ \   /' _ `\/\ \ \ \/  /'__`\  \ \ \ \/\ \/\_ ,`\  /'__`\
#     \_\ \__/\ \/\ \ \ \ \ \_/\ \L\.\_ \_\ \_\ \ \/_/  /_/\  __/
#     /\_____\ \_\ \_\ \_\ \__\ \__/.\_\/\____\\ \_\/\____\ \____\
#     \/_____/\/_/\/_/\/_/\/__/\/__/\/_/\/____/ \/_/\/____/\/____/


def game_initalize():
    '''This function initalizes the main window in pygame'''

    global SURFACE_MAIN, GAME_MAP, PLAYER, ENEMY, GAME_OBJECTS

    pygame.init()

    SURFACE_MAIN = pygame.display.set_mode(
        (constants.MAP_WIDTH*constants.CELL_WIDTH, constants.MAP_HEIGHT*constants.CELL_HEIGHT))

    GAME_MAP = map_create()

    creature_com1 = com_Creature("greg")
    PLAYER = obj_Actor(3, 3, "Python", constants.S_PLAYER,
                       creature=creature_com1)

    creature_com2 = com_Creature("Jackie", death_function=death_monstor)
    ai_com = ai_Test()
    ENEMY = obj_Actor(10, 5, "Crab", constants.S_ENEMY,
                      creature=creature_com2, ai=ai_com)

    GAME_OBJECTS = [PLAYER, ENEMY]


#  __  __
# /\ \/\ \
# \ \ \/'/'     __   __  __
#  \ \ , <    /'__`\/\ \/\ \
#   \ \ \\`\ /\  __/\ \ \_\ \
#    \ \_\ \_\ \____\\/`____ \
#     \/_/\/_/\/____/ `/___/> \
#                        /\___/
#                        \/__/
#  __  __                       __   ___
# /\ \/\ \                     /\ \ /\_ \
# \ \ \_\ \     __      ___    \_\ \\//\ \      __   _ __
#  \ \  _  \  /'__`\  /' _ `\  /'_` \ \ \ \   /'__`\/\`'__\
#   \ \ \ \ \/\ \L\.\_/\ \/\ \/\ \L\ \ \_\ \_/\  __/\ \ \/
#    \ \_\ \_\ \__/.\_\ \_\ \_\ \___,_\/\____\ \____\\ \_\
#     \/_/\/_/\/__/\/_/\/_/\/_/\/__,_ /\/____/\/____/ \/_/


def game_handle_keys():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return "QUIT"
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                PLAYER.creature.move(0, -1)
                return "player-moved"

            if event.key == pygame.K_s:
                PLAYER.creature.move(0, 1)
                return "player-moved"

            if event.key == pygame.K_a:
                PLAYER.creature.move(-1, 0)
                return "player-moved"

            if event.key == pygame.K_d:
                PLAYER.creature.move(1, 0)
                return "player-moved"

    return "no-action"


if __name__ == '__main__':
    game_initalize()
    main_game_loop()
