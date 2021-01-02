import pygame
import math

WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
DARKGREY = (110, 110, 100)
PURPLE = (120, 0, 120)

player_pos = (HALF_WIDTH, HALF_HEIGHT)
player_angle = 0
player_speed = 2

""" область бачення """
TILE = 100
FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 120
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS


text_map = [
    'WWWWWWWWWWWW',
    'W......W...W',
    'W..WWW...W.W',
    'W....W..WW.W',
    'W..W....W..W',
    'W..W...WWW.W',
    'W....W.....W',
    'WWWWWWWWWWWW'
]

word_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char == 'W':
            word_map.add((i * TILE, j * TILE))

class Player:

    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle


    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
            #self.y -= player_speed
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
            #self.y += player_speed
        if keys[pygame.K_a]:
            self.x += player_speed * cos_a
            self.y += -player_speed * sin_a
            #self.x -= player_speed
        if keys[pygame.K_d]:
            self.x += -player_speed * cos_a
            self.y += player_speed * sin_a
            #self.x += player_speed
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02


def ray_casting(screen, player_pos, player_angle):
    cur_angle = player_angle - HALF_FOV
    xo, yo = player_pos
    for ray in range(NUM_RAYS):
        cos_a = math.cos(cur_angle)
        sin_a = math.sin(cur_angle)
        for depth in range(MAX_DEPTH):
            x = xo + depth * cos_a
            y = yo + depth * sin_a
            if (x // TILE * TILE, y // TILE * TILE) in word_map:
                depth *= math.cos(player_angle - cur_angle)
                c = 255 / (1 + depth * depth * 0.0001)
                color = (int(c), int(c), int(c))
                proj_height = PROJ_COEFF / depth
                pygame.draw.rect(screen, color, (ray * SCALE, HALF_HEIGHT - proj_height // 2, SCALE, proj_height))
                break
        #pygame.draw.line(screen, DARKGREY, player_pos, (x, y), 2)
        cur_angle += DELTA_ANGLE

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
player = Player()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(BLACK)
    pygame.draw.rect(screen, BLUE, (0,0,WIDTH, HALF_HEIGHT))
    pygame.draw.rect(screen, DARKGREY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))
    ray_casting(screen, player.pos, player.angle)
    # pygame.draw.circle(screen, GREEN, (int(player.x), int(player.y)), 12)
    # pygame.draw.line(screen, GREEN, player.pos, ((player.x + WIDTH * math.cos(player.angle)),
    #                                              (player.y + WIDTH * math.sin(player.angle))))
    # for x,y in word_map:
    #     pygame.draw.rect(screen, DARKGREY, (x, y, TILE, TILE), 2)
    pygame.display.flip()
    clock.tick(60)
