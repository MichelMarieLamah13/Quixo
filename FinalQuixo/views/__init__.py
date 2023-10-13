import pygame

WIDTH = 1280
HEIGHT = 650

BOARD_SIZE = 550
SQUARE_SIZE = 100
LINE_WIDTH = 10
CIRCLE_RADIUS = 40
CIRCLE_WIDTH = 10
CROSS_WIDTH = 5
CROSS_PADDING = 15
SPACE = 25

PADDING = 50

# COLOR
LINE_COLOR = (215, 252, 212)  # (0, 1, 18)
CIRCLE_COLOR = (239, 255, 200)
CROSS_COLOR = (0, 255, 0)

TEXT_COLOR_1 = "#d7fcd4"

# SIZE
S_20 = 20
S_30 = 30
S_40 = 40

S_75 = 75
pygame.init()

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

FPS = 60


def get_font(size, msg=False):  # Returns Press-Start-2P in the desired size
    if msg:
        return pygame.font.SysFont("arial", size)
    else:
        return pygame.font.Font("assets/font.ttf", size)
