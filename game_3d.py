import pygame
import math

""" game setting """
WIDTH = 1200
HEIGHT = 800
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
TILE = 100
FPS = 60
FPS_POS = (WIDTH - 65, 5)


""" colors """
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 0, 0)
GREEN = (0, 220, 0)
BLUE = (0, 0, 220)
DARKGREY = (110, 110, 100)
PURPLE = (120, 0, 120)
SKYBLUEE = (0, 186, 255)
YELLOW = (220, 220, 0)
DARKBROWN = (97, 61, 25)
DARKRANGE = (255, 40, 25)


""" texture setting """
TEXTURE_WIDTH = 1200
TEXTURE_HEIGHT = 1200
TEXTURE_SCALE = TEXTURE_WIDTH // TILE

""" player setting """
player_pos = (HALF_WIDTH // 4, HALF_HEIGHT - 50)
player_angle = 0
player_speed = 2

""" область бачення ray casting setting """

FOV = math.pi / 3
HALF_FOV = FOV / 2
NUM_RAYS = 300
MAX_DEPTH = 800
DELTA_ANGLE = FOV / NUM_RAYS
DIST = NUM_RAYS / (2 * math.tan(HALF_FOV))
PROJ_COEFF = 3 * DIST * TILE
SCALE = WIDTH // NUM_RAYS

""" sprites setting """
DOUBLE_PI = 2 * math.pi
CENTER_RAY = NUM_RAYS // 2 - 1


""" mini map setting """
MAP_SCALE = 5
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MAP_SCALE)

text_map = [
    '111111111111',
    '1.....2....1',
    '1.22.....2.1',
    '1..........1',
    '1.22....1..1',
    '1.2......2.1',
    '1....2.....1',
    '111111111111'
]

word_map = dict()
mini_map = set()
for j, row in enumerate(text_map):
    for i, char in enumerate(row):
        if char != '.':
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
        if char == '1':
            word_map[(i * TILE, j * TILE)] = '1'
        elif char == '2':
            word_map[(i * TILE, j * TILE)] = '2'


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

        self.angle %= DOUBLE_PI


class Drawing:
    def __init__(self, sc, map_sc):
        self.screen = sc
        self.sc_map = map_sc
        self.font = pygame.font.SysFont('Arial', 38, bold=True)
        self.textures = {'1': pygame.image.load('images/wall1.png').convert(),
                         '2': pygame.image.load('images/wall2.png').convert(),
                         's': pygame.image.load('images/sky3.png').convert()
                         }

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.screen.blit(self.textures['s'], (sky_offset, 0))
        self.screen.blit(self.textures['s'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['s'], (sky_offset - WIDTH, 0))
        pygame.draw.rect(self.screen, DARKGREY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def word(self, player_pos, player_angle):
        ray_casting(self.screen, player_pos, player_angle, self.textures)

    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, 0, DARKRANGE)
        self.screen.blit(render, FPS_POS)

    def mini_map(self, player):
        self.sc_map.fill(BLACK)
        map_x, map_y = player.x // MAP_SCALE, player.y // MAP_SCALE

        pygame.draw.line(self.sc_map, YELLOW, (map_x, map_y), ((map_x + 12 * math.cos(player.angle)),
                                                               (map_y + 12 * math.sin(player.angle))), 2)
        pygame.draw.circle(self.sc_map, DARKBROWN, (int(map_x), int(map_y)), 5)
        for x, y in mini_map:
            pygame.draw.rect(self.sc_map, RED, (x, y, MAP_TILE, MAP_TILE))
        self.screen.blit(self.sc_map, MAP_POS)


class Sprite:
    def __init__(self):
        self.type = {
            'barrel': pygame.image.load('images/sprites/barrel.png').convert_alpha()
        }
        self.list_f_object = [
            SpriteObject(self.type['barrel'], True, (7.1, 2.1), 1.8, 0.4),
            SpriteObject(self.type['barrel'], True, (5.9, 2.1), 1.8, 0.4)
        ]


class SpriteObject:
    def __init__(self, object, static, pos, shift, scale):
        self.oobject = object
        self.static = static
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE
        self.shift = shift
        self.scale = scale

    def object_locate(self, player, walls):
        pass



def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(screen, player_pos, player_angle, textures):
    ox, oy = player_pos
    xm, ym = mapping(ox, oy)
    cur_angle = player_angle - HALF_FOV
    texture_v, texture_h = None, None
    for ray in range(NUM_RAYS):
        cos_a = math.cos(cur_angle)
        sin_a = math.sin(cur_angle)
        """ вертикаль """
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in word_map:
                texture_v = word_map[tile_v]
                break
            x += dx * TILE
        """ горизнталь """
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, HEIGHT, TILE):
            depth_h = (y - oy) / sin_a
            xh = ox + depth_h * cos_a
            tile_h = mapping(xh, y + dy)
            if tile_h in word_map:
                texture_h = word_map[tile_h]
                break
            y += dy * TILE

        """ проекція """

        depth, offset, texture = (depth_v, yv, texture_v) if depth_v < depth_h else (depth_h, xh, texture_h)
        offset = int(offset) % TILE
        depth *= math.cos(player_angle - cur_angle)
        proj_height = min(int(PROJ_COEFF / (depth + 0.00001)), 2 * HEIGHT)
        if texture_h != None or texture_v != None:
            wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,  TEXTURE_HEIGHT)
            wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))
            screen.blit(wall_column, (ray * SCALE, HALF_HEIGHT - proj_height // 2))
        cur_angle += DELTA_ANGLE


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
map_screen = pygame.Surface((WIDTH // MAP_SCALE, HEIGHT // MAP_SCALE))
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(screen, map_screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(BLACK)
    drawing.background(player.angle)
    drawing.word(player.pos, player.angle)
    drawing.fps(clock)
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick()
