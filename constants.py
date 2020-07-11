import pygame
import libtcodpy as libtcod

pygame.init()


# GAME SIZES
GAME_WIDTH = 800
GAME_HEIGHT = 600
CELL_WIDTH = 32
CELL_HEIGHT = 32

# FPS CAP
GAME_FPS = 60

# MAP VARS
MAP_WIDTH = 20
MAP_HEIGHT = 20

# COLOR DEFINITIONS
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREY = (100, 100, 100)
COLOR_RED = (255, 0, 0)

# GAME COLORS
COLOR_DEFAULT_BG = COLOR_GREY

# SPRITES
S_PLAYER = pygame.image.load('./data/player.png')
S_ENEMY = pygame.image.load('./data/crab.png')

S_WALL = pygame.image.load('./data/wall.png')
S_WALLEXPLORED = pygame.image.load('./data/wallunseen.png')

S_FLOOR = pygame.image.load('./data/floor.png')
S_FLOOREXPLORED = pygame.image.load('./data/floorunseen.png')

# FOV SETTINGS
FOV_ALGO = libtcod.FOV_BASIC
FOV_LIGHT_WALLS = True
TORCH_RADIUS = 4

# FONTS
# FONT_DEBUG_MESSAGE = pygame.font.SysFont('joystix', 40)
FONT_DEBUG_MESSAGE = pygame.font.Font('fonts\joystix.ttf', 15)
FONT_MESSAGE_TEXT = pygame.font.Font('fonts\joystix.ttf', 12)

# MSG DEFAULTS
NUM_MESSAGES = 4

