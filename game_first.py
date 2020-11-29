import os
import turtle
import random

base_path = os.path.dirname(__file__)

window = turtle.Screen()
window.bgpic(os.path.join(base_path, 'images', 'background.png'))
window.tracer(n=2)

BASE_X, BASE_Y = 0, -300
ENEMY_COUNT = 5


def create_rocket(color, from_x, from_y, where_x, where_y):
    rocket = turtle.Turtle(visible=False)

    rocket.speed(0)
    rocket.penup()
    rocket.color(color)
    rocket.setpos(x=from_x, y=from_y)
    heading = rocket.towards(where_x, where_y)
    rocket.setheading(heading)
    rocket.showturtle()
    info_rocket = {'rockets': rocket, 'status': 'fly', 'target': [where_x, where_y], 'bomb_radius': 0}
    return info_rocket


def rocket_fire(x, y):
    my_rockets.append(create_rocket('yellow', from_x=BASE_X, from_y=BASE_Y, where_x=x, where_y=y))


def rocket_enemy_fire():
    x = random.randint(-600, 600)
    y = 400
    enemy_rockets.append(create_rocket('red', from_x=x, from_y=y, where_x=BASE_X, where_y=BASE_Y))


def rockets_forward(rocket: list):
    rockets = rocket
    for roc in rockets:
        if roc['status'] == 'fly':
            roc['rockets'].forward(4)
            target = roc['target']
            if roc['rockets'].distance(x=target[0], y=target[1]) < 20:
                roc['rockets'].shape('circle')
                roc['status'] = 'bomb'
        elif roc['status'] == 'bomb':
            roc['bomb_radius'] += 1
            if roc['bomb_radius'] > 5:
                roc['status'] = 'end'
                roc['rockets'].clear()
                roc['rockets'].hideturtle()
            else:
                roc['rockets'].shapesize(roc['bomb_radius'])
        elif roc['status'] == 'end':
            roc['rockets'].clear()
            roc['rockets'].hideturtle()
    del_list = [i for i in rockets if i['status'] == 'end']
    for i in del_list:
        rockets.remove(i)


def check_enemy_rocket_count():
    if len(enemy_rockets) < 5:
        rocket_enemy_fire()


def check_enemy_intersection():
    for my_rocket in my_rockets:
        if my_rocket['status'] == 'bomb':
            my_roc = my_rocket['rockets']
            for enemy_rocket in enemy_rockets:
                if enemy_rocket['rockets'].distance(my_roc.xcor(), my_roc.ycor()) < my_rocket['bomb_radius'] * 10:
                    enemy_rocket['status'] = 'end'


window.onclick(rocket_fire)
my_rockets = []
enemy_rockets = []
base_rocket = turtle.Turtle(visible=False)
base_rocket.speed(0)
base_rocket.penup()
base_rocket.setpos(x=BASE_X, y=BASE_Y)
base_pic = os.path.join(base_path, 'images', 'base.gif')
window.register_shape(base_pic)
base_rocket.shape(base_pic)
base_rocket.showturtle()

base_health = 2000


def game_over():
    return base_health < 0


def check_impact():
    global base_health
    for enemy_rocket in enemy_rockets:
        if enemy_rocket['status'] == 'bomb':
            if enemy_rocket['rockets'].distance(BASE_X, BASE_Y) < enemy_rocket['bomb_radius'] * 10:
                base_health -= 100
                enemy_rocket['bomb_radius'] += 5
                print(base_health)

while True:
    window.update()
    if game_over():
        continue
    check_impact()
    check_enemy_intersection()
    check_enemy_rocket_count()
    rockets_forward(rocket=my_rockets)
    rockets_forward(rocket=enemy_rockets)
