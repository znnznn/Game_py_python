import os
import turtle
import random

base_path = os.path.dirname(__file__)

window = turtle.Screen()
window.bgpic(os.path.join(base_path, 'images', 'background.png'))
window.tracer(n=2)


base_path = os.path.dirname(__file__)
BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5
BUILDING = {
    'base': {
        'x': BASE_X, 'y': BASE_Y, 'health': 2000,
        'picture': [os.path.join(base_path, 'images', 'base.gif'),
                    os.path.join(base_path, 'images', 'base_opened.gif'),]
    },
    'kremlin': {
        'x': BASE_X-150, 'y': BASE_Y, 'health': 2000,
        'picture': [os.path.join(base_path, 'images', 'kremlin_1.gif'),
                    os.path.join(base_path, 'images', 'kremlin_2.gif'),
                    os.path.join(base_path, 'images', 'kremlin_3.gif')]
    },
    'house': {
        'x': BASE_X+150, 'y': BASE_Y, 'health': 1300,
        'picture': [os.path.join(base_path, 'images', 'house_1.gif'),
                    os.path.join(base_path, 'images', 'house_2.gif'),
                    os.path.join(base_path, 'images', 'house_3.gif')]
    },
    'nuclear': {
        'x': BASE_X+300, 'y': BASE_Y, 'health': 1500,
        'picture': [os.path.join(base_path, 'images', 'nuclear_1.gif'),
                    os.path.join(base_path, 'images', 'nuclear_2.gif'),
                    os.path.join(base_path, 'images', 'nuclear_3.gif')]
    },
    'skyscraper': {
        'x': BASE_X-300, 'y': BASE_Y, 'health': 1500,
        'picture': [os.path.join(base_path, 'images', 'skyscraper_1.gif'),
                    os.path.join(base_path, 'images', 'skyscraper_2.gif'),
                    os.path.join(base_path, 'images', 'skyscraper_3.gif')]
    }
}


class Rocket:
    def __init__(self, from_x, from_y, where_x, where_y, color):
        self.from_x = from_x
        self.from_y = from_y
        self.color = color
        self.where_x = where_x
        self.where_y = where_y

        rocket = turtle.Turtle(visible=False)
        rocket.speed(2)
        rocket.penup()
        rocket.color(color)
        rocket.setpos(x=from_x, y=from_y)
        heading = rocket.towards(where_x, where_y)
        rocket.setheading(heading)
        rocket.showturtle()

        #window.register_shape(os.path.join(base_path, 'images', 'missile.gif'))
        #rocket.shape(os.path.join(base_path, 'images', 'missile.gif'))
        #rocket.showturtle()
        self.rocket = rocket
        self.status = 'fly'
        self.target = where_x, where_y
        self.radius = 0

    def forward(self):
        if self.status == 'fly':
            self.rocket.forward(4)
            if self.rocket.distance(x=self.target[0], y=self.target[1]) < 20:
                self.rocket.shape('circle')
                self.status = 'bomb'
        elif self.status == 'bomb':
            self.radius += 1
            if self.radius > 5:
                self.status = 'end'
                self.rocket.clear()
                self.rocket.hideturtle()
            else:
                self.rocket.shapesize(self.radius)
        elif self.status == 'end':
            self.rocket.clear()
            self.rocket.hideturtle()


class Base:
    def __init__(self, name, building: dict):
        self.name = name
        self.x = building['x']
        self.y = building['y']

        self.pic = building['picture']
        self.health = building['health']
        self.check_health = self.health
        base = turtle.Turtle(visible=False)
        base.speed(0)
        base.penup()
        base.setpos(x=self.x, y=self.y)

        window.register_shape(self.pic[0])
        base.shape(self.pic[0])
        base.showturtle()
        self.base = base

        show_health = turtle.Turtle(visible=False)
        show_health.speed(0)
        show_health.penup()
        show_health.setpos(x=self.x, y=self.y-65)
        show_health.write(str(self.health), align="center", font=("Arial", 20, "bold"))
        self.show_health = show_health
        self.check_show_health = self.show_health

    def show_pic(self):
        if self.name != 'base':
            if self.health <= self.check_health - 1200:
                window.register_shape(self.pic[2])
                self.base.shape(self.pic[2])
            elif self.health <= self.check_health - 700:
                window.register_shape(self.pic[1])
                self.base.shape(self.pic[1])
        if self.health != self.check_show_health:
            self.show_health.clear()
            self.show_health.write(str(self.health), align="center", font=("Arial", 20, "bold"))


def rockets_forward(rockets: list):
    for rocket in rockets:
        rocket.forward()
    del_list = [i for i in rockets if i.status == 'end']
    for i in del_list:
        rockets.remove(i)


def check_enemy_intersection():
    for my_rocket in my_rockets:
        if my_rocket.status == 'bomb':
            for enemy_rocket in enemy_rockets:
                if enemy_rocket.rocket.distance(my_rocket.rocket.xcor(),
                                                my_rocket.rocket.ycor()) < my_rocket.radius * 10:
                    enemy_rocket.status = 'end'


def rocket_fire(x, y):
    my_rockets.append(Rocket(from_x=BASE_X, from_y=BASE_Y, where_x=x, where_y=y, color='yellow'))


def check_enemy_rocket_count():
    if len(enemy_rockets) < 5:
        x = random.randint(-600, 600)
        y = 400
        index_building = random.randint(0, len(base_all)-1)
        if base_all[index_building].health > 0:
            enemy_rockets.append(Rocket(color='red', from_x=x, from_y=y,
                                        where_x=base_all[index_building].x,
                                        where_y=base_all[index_building].y))


def create_building(buildings: dict):
    for building, value in buildings.items():
        set_building = Base(building, value)
        base_all.append(set_building)
        

def game_over():
    for i in base_all:
        if i.name == 'base' and i.health <= 0:
            i.show_health.color('red')
            i.show_health.setpos(x=0, y=0)
            i.show_health.write('G A M E   O V E R', align="center", font=("Arial", 30, "bold"))
            return True
        elif i.health <= 0:
            alive_building.append(i)
        for enemy_rocket in enemy_rockets:
            if enemy_rocket.status == 'bomb' and i not in alive_building:
                if i.health > 0 and enemy_rocket.rocket.distance(i.x, i.y) < enemy_rocket.radius * 10:
                    i.health -= 100
                    enemy_rocket.radius += 5
                    i.show_pic()


my_rockets = []
enemy_rockets = []
base_all = []
alive_building = []
create_building(BUILDING)
window.onclick(rocket_fire)

while True:
    window.update()
    if game_over():
        continue
    check_enemy_intersection()
    check_enemy_rocket_count()
    rockets_forward(rockets=my_rockets)
    rockets_forward(rockets=enemy_rockets)
