import pygame
import math

from collections import deque
""" game setting """
WIDTH = 1200
HEIGHT = 800
PENTA_HEIGHT = 5 * HEIGHT
HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
DOUBLE_HEIGHT = 2 * HEIGHT
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
FAKE_RAYS = 100
FAKE_RAYS_RANGE = NUM_RAYS - 1 + 2 * FAKE_RAYS


""" mini map setting """
MINIMAP_SCALE = 5
MAP_SCALE = 2 * MINIMAP_SCALE #
MAP_RES = (WIDTH // MINIMAP_SCALE, HEIGHT // MINIMAP_SCALE)
MAP_TILE = TILE // MAP_SCALE
MAP_POS = (0, HEIGHT - HEIGHT // MINIMAP_SCALE)

# text_map = [
#     '111111111111',
#     '1.....2....1',
#     '1.22.....2.1',
#     '1..........1',
#     '1.22....1..1',
#     '1.2......2.1',
#     '1....2.....1',
#     '111111111111'
# ]
map1 = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 4, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 4, 0, 0, 3, 0, 0, 0, 4, 0, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 2, 2, 0, 2, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 1],
    [1, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 0, 0, 0, 0, 3, 3, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 3, 3, 0, 3, 0, 0, 0, 3, 3, 0, 0, 0, 0, 2, 3, 0, 0, 1],
    [1, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 4, 0, 3, 0, 0, 0, 0, 3, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 1],
    [1, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 2, 2, 0, 0, 0, 0, 0, 0, 2, 2, 0, 1],
    [1, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]
WORD_WIDTH = len(map1[0]) * TILE
WORD_HEIGHT = len(map1) * TILE
word_map = dict()
mini_map = set()
for j, row in enumerate(map1):
    for i, char in enumerate(row):
        if char != 0:
            mini_map.add((i * MAP_TILE, j * MAP_TILE))
            if char == 1:
                word_map[(i * TILE, j * TILE)] = 1
            elif char == 2:
                word_map[(i * TILE, j * TILE)] = 2
            elif char == 3:
                word_map[(i * TILE, j * TILE)] = 3
            elif char == 4:
                word_map[(i * TILE, j * TILE)] = 4


class Player:
    def __init__(self):
        self.x, self.y = player_pos
        self.angle = player_angle
        self.sensitivity = 0.004

    @property
    def pos(self):
        return self.x, self.y

    def movement(self):
        self.keys_control()
        self.mouse_control()
        self.angle %= DOUBLE_PI

    def keys_control(self):
        sin_a = math.sin(self.angle)
        cos_a = math.cos(self.angle)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            exit()

        if keys[pygame.K_w]:
            self.x += player_speed * cos_a
            self.y += player_speed * sin_a
            #self.y -= player_speed
        if keys[pygame.K_s]:
            self.x += -player_speed * cos_a
            self.y += -player_speed * sin_a
            #self.y += player_speed
        if keys[pygame.K_a]:
            self.x += player_speed * sin_a
            self.y += -player_speed * cos_a
            #self.x -= player_speed
        if keys[pygame.K_d]:
            self.x += -player_speed * sin_a
            self.y += player_speed * cos_a
            #self.x += player_speed
        if keys[pygame.K_LEFT]:
            self.angle -= 0.02
        if keys[pygame.K_RIGHT]:
            self.angle += 0.02

    def mouse_control(self):
        if pygame.mouse.get_focused():
            difference = pygame.mouse.get_pos()[0] - HALF_WIDTH
            pygame.mouse.set_pos(HALF_WIDTH, HALF_HEIGHT)
            self.angle += difference * self.sensitivity


class Drawing:
    def __init__(self, sc, map_sc):
        self.screen = sc
        self.sc_map = map_sc
        self.font = pygame.font.SysFont('Arial', 38, bold=True)
        self.textures = {1: pygame.image.load('images/wall3.png').convert(),
                         2: pygame.image.load('images/wall4.png').convert(),
                         3: pygame.image.load('images/wall5.png').convert(),
                         4: pygame.image.load('images/wall6.png').convert(),
                         's': pygame.image.load('images/sky3.png').convert()
                         }

    def background(self, angle):
        sky_offset = -10 * math.degrees(angle) % WIDTH
        self.screen.blit(self.textures['s'], (sky_offset, 0))
        self.screen.blit(self.textures['s'], (sky_offset - WIDTH, 0))
        self.screen.blit(self.textures['s'], (sky_offset - WIDTH, 0))
        pygame.draw.rect(self.screen, DARKGREY, (0, HALF_HEIGHT, WIDTH, HALF_HEIGHT))

    def word(self, word_objects):
        for obj in sorted(word_objects, key=lambda n: n[0], reverse=True):
            if obj[0]:
                _, object, object_pos = obj
                self.screen.blit(object, object_pos)


    def fps(self, clock):
        display_fps = str(int(clock.get_fps()))
        render = self.font.render(display_fps, True, DARKRANGE)
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
        self.parameters = {
            'barrel': {
                'sprite': pygame.image.load('images/sprites/barrel/base/0.png').convert_alpha(),
                'angles': None,
                'shift': 1.8,
                'scale': 0.4,
                'animation': deque(
                    [pygame.image.load(f'images/sprites/barrel/anim/{img}.png').convert_alpha() for img in range(12)]),
                'animation_dist': 800,
                'animation_speed': 10,
            },
            'pin': {
                'sprite': pygame.image.load('images/sprites/pin/base/0.png').convert_alpha(),
                'angles': None,
                'shift': 0.6,
                'scale': 0.6,
                'animation': deque(
                    [pygame.image.load(f'images/sprites/pin/anim/{img}.png').convert_alpha() for img in range(8)]),
                'animation_dist': 800,
                'animation_speed': 10,
                'blocked': True,
            },
            'devil': {
                'sprite': pygame.image.load(f'images/sprites/devil/base/0.png').convert_alpha(),
                'angles': None,
                'shift': -0.2,
                'scale': 1.1,
                'animation': deque(
                    [pygame.image.load(f'images/sprites/devil/anim/{img}.png').convert_alpha() for img in range(9)]),
                'animation_dist': 150,
                'animation_speed': 10,
                'blocked': True,
            },
            'flame': {
                'sprite': pygame.image.load('images/sprites/flame/base/0.png').convert_alpha(),
                'angles': None,
                'shift': 0.7,
                'scale': 0.6,
                'animation': deque(
                    [pygame.image.load(f'images/sprites/flame/anim/{img}.png').convert_alpha() for img in range(16)]),
                'animation_dist': 800,
                'animation_speed': 5,
                'blocked': True,
            },
        }
        self.list_of_object = [
            SpriteObject(self.parameters['barrel'], (7.1, 2.1)),
            SpriteObject(self.parameters['barrel'], (5.9, 2.1)),
            SpriteObject(self.parameters['pin'], (8.7, 2.5)),
            SpriteObject(self.parameters['devil'], (8.7, 2.5)),
            SpriteObject(self.parameters['flame'], (8.6, 5.6)),
        ]


class SpriteObject:
    def __init__(self, parameters, pos):
        self.object = parameters['sprite']
        self.angles = parameters['angles']
        self.shift = parameters['shift']
        self.scale = parameters['scale']
        self.animation = parameters['animation']
        self.animation_dist = parameters['animation_dist']
        self.animation_speed = parameters['animation_speed']
        self.animation_count = 0
        self.pos = self.x, self.y = pos[0] * TILE, pos[1] * TILE

        if self.angles:
            self.sprite_angle = [frozenset(range(i, i + 45)) for i in range(0, 360, 45)]
            self.sprite_pos = {angle: pos for angle, pos in zip(self.sprite_angle, self.object)}

    def object_locate(self, player):
        dx, dy = self.x - player.x, self.y - player.y
        distance_to_sprite = math.sqrt(dx ** 2 + dy ** 2)

        theta = math.atan2(dy, dx)
        gamma = theta - player.angle
        if dx > 0 and 180 <= math.degrees(player.angle) <= 360 or dx < 0 and dy < 0:
            gamma += DOUBLE_PI
        delta_rays = int(gamma / DELTA_ANGLE)
        current_ray = CENTER_RAY + delta_rays
        distance_to_sprite *= math.cos(HALF_FOV - current_ray * DELTA_ANGLE)
        fake_ray = current_ray + FAKE_RAYS
        if 0 <= fake_ray <= FAKE_RAYS_RANGE and distance_to_sprite > 30:
            proj_height = min(int(PROJ_COEFF / distance_to_sprite * self.scale), DOUBLE_HEIGHT)
            half_proj_height = proj_height // 2
            shift = half_proj_height * self.shift
            """ вибір спрайта для кута """
            if self.angles:
                if theta < 0:
                    theta += DOUBLE_PI
                theta = 360 - int(math.degrees(theta))
                for angles in self.sprite_angle:
                    if theta in angles:
                        self.object = self.sprite_pos[angles]
                        break
            """ анімація """
            sprite_obj = self.object
            if self.animation and distance_to_sprite < self.animation_dist:
                self.object = self.animation[0]
                if self.animation_count < self.animation_speed:
                    self.animation_count += 1
                else:
                    self.animation.rotate()
                    self.animation_count = 0
            """ маштабуємо обраний мпрайт по висоті і відстані """
            sprite_pos = (current_ray * SCALE - half_proj_height, HALF_HEIGHT - half_proj_height + shift)
            sprite = pygame.transform.scale(sprite_obj, (proj_height, proj_height))
            return (distance_to_sprite, sprite, sprite_pos)
        else:
            return (False, )



def mapping(a, b):
    return (a // TILE) * TILE, (b // TILE) * TILE


def ray_casting(player, textures):
    walls = []

    ox, oy = player.pos
    xm, ym = mapping(ox, oy)
    cur_angle = player.angle - HALF_FOV
    texture_v, texture_h = 1, 1
    for ray in range(NUM_RAYS):
        cos_a = math.cos(cur_angle)
        sin_a = math.sin(cur_angle)
        """ вертикаль """
        x, dx = (xm + TILE, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, WORD_WIDTH, TILE):
            depth_v = (x - ox) / cos_a
            yv = oy + depth_v * sin_a
            tile_v = mapping(x + dx, yv)
            if tile_v in word_map:
                texture_v = word_map[tile_v]
                break
            x += dx * TILE
        """ горизнталь """
        y, dy = (ym + TILE, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, WORD_HEIGHT, TILE):
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
        depth *= math.cos(player.angle - cur_angle)
        proj_height = min(int(PROJ_COEFF / (depth + 0.00001)), PENTA_HEIGHT)

        wall_column = textures[texture].subsurface(offset * TEXTURE_SCALE, 0, TEXTURE_SCALE,  TEXTURE_HEIGHT)
        wall_column = pygame.transform.scale(wall_column, (SCALE, proj_height))

        wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
        walls.append((depth, wall_column, wall_pos))
        cur_angle += DELTA_ANGLE
    return walls


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.mouse.set_visible(False)
map_screen = pygame.Surface(MAP_RES)
clock = pygame.time.Clock()
player = Player()
drawing = Drawing(screen, map_screen)
sprites = Sprite()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.movement()
    screen.fill(BLACK)
    drawing.background(player.angle)
    walls = ray_casting(player, drawing.textures)
    drawing.word(walls + [obj.object_locate(player) for obj in sprites.list_of_object])
    drawing.fps(clock)
    drawing.mini_map(player)

    pygame.display.flip()
    clock.tick()
