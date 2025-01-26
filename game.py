import pyxel, random

life = 4
screen_size = (100, 100)
ship_size = (6, 6)
ship_pos = (45, 45)
shoot_size = (1, 4)
shoot_list = []
ennemies_list = []
boom_list = []

def update():
    global ship_pos, screen_size, shoot_list, ennemies_list, life
    ship_pos = ship_move(ship_pos[0], ship_pos[1])
    shoot_list = new_shoot(ship_pos[0], ship_pos[1], shoot_list)
    shoot_list = shoot_move(shoot_list)
    ennemies_list = new_ennemy(ennemies_list)
    ennemies_list = ennemy_move(ennemies_list)
    life = ship_dead(life)
    ennemy_dead()
    boom_anim()
def draw():
    pyxel.cls(0)
    if life > 0:
        pyxel.text(5, 5, f'Life : {life}', 2)
        pyxel.rect(ship_pos[0], ship_pos[1], ship_size[0], ship_size[1], 1)
        for shoot in shoot_list:
            pyxel.rect(shoot[0], shoot[1], 1, 4, 10)
        for ennemy in ennemies_list:
            pyxel.rect(ennemy[0], ennemy[1], 3, 3, 8)
        for boom in boom_list:
            pyxel.circb(boom[0] + 3, boom[1] + 3, 2 * (boom[2] // 4), 8 + boom[2] % 3)
    else:
        pyxel.text(30, 50, 'GAME OVER', 7)
def ship_move(x, y):
    if pyxel.btn(pyxel.KEY_RIGHT):
        if x < screen_size[0] - ship_size[0]:
            x += 1
    if pyxel.btn(pyxel.KEY_LEFT):
        if x > 0:
            x -= 1
    if pyxel.btn(pyxel.KEY_DOWN):
        if y < screen_size[1] - ship_size[1]:
            y += 1
    if pyxel.btn(pyxel.KEY_UP):
        if y > 0:
            y -= 1
    return (x, y)
def new_shoot(x, y, list):
    if pyxel.btnr(pyxel.KEY_SPACE):
        list.append([x + 3, y - 3])
    return list
def shoot_move(list):
    for shoot in list:
        shoot[1] -= 1
        if shoot[1] < -5:
            list.remove(shoot)
    return list
def new_ennemy(list):
    if pyxel.frame_count % 60 == 0:
        list.append([random.randint(0, 100), 0])
    return list
def ennemy_move(list):
    for ennemy in list:
        ennemy[1] += 1
        if ennemy[1] > 100:
            list.remove(ennemy)
    return list
def ship_dead(life):
    for ennemy in ennemies_list:
        if abs(ennemy[0] - ship_pos[0]) <= 3 and abs(ennemy[1] - ship_pos[1]) <= 3:    
            ennemies_list.remove(ennemy)
            life -= 1
    return life
def ennemy_dead():
    for ennemy in ennemies_list:
        for shoot in shoot_list:
            if abs(ennemy[0] - shoot[0]) <= 2 and abs(ennemy[1] - shoot[1]) <= 2:
                ennemies_list.remove(ennemy)
                shoot_list.remove(shoot)
                new_boom(ennemy[0], ennemy[1])
    return
def new_boom(x, y):
    boom_list.append([x, y, 0])
    return
def boom_anim():
    for boom in boom_list:
        boom[2] += 1
        if boom[2] == 12:
            boom_list.remove(boom)
    return

pyxel.init(screen_size[0], screen_size[1], title='Game play')
pyxel.run(update, draw)