import pygame
import numpy as np
import random
import time
from classes import Animal, Bullet, Bomb, Button, print_text, Player

pygame.init()
info = pygame.display.Info()
pygame.display.set_caption("Hunter")
screen_width, screen_height = info.current_w, info.current_h
win = pygame.display.set_mode((screen_width, screen_height))
round_end_wind = False
wind_start = time.time()
run = True
shot = True
menu = True
click = False
name_change = False
onbutton = False
can_lvlup = True
message = False
before_lvlstart = True
lvlstart_time = 0
message_start = 0
jump = 0
jump_st = None
sf = 0
shot_time = 0
b_last_time = 0
delay_time = 5
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREEN1 = (0, 170, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
BROWN = (0, 100, 51)
DARKGREEN = (0, 64, 0)
win.fill(GREEN1)
bull_lvl = []
txt = open("money.txt", "r")
money = int(txt.readline())
bull_lvl.append(min(int(txt.readline()), 15))
bull_lvl.append(min(int(txt.readline()), 15))
bull_lvl.append(min(int(txt.readline()), 15))
hp_lvl = int(txt.readline())
speed_lvl = int(txt.readline())
level = int(txt.readline())
txt.close()
start_but = Button(int(screen_width/10), int(screen_width/20), (100, 255, 0), GREEN)
b_s = int(screen_height/200)
bullet = [Bullet(0, b_s, b_s, BROWN, 1, (5 * screen_height) * delay_time / 1000, 0.5, None),
          Bullet(10, 2*b_s, 2*b_s, BLACK, 2, (3 * screen_height) * delay_time / 1000, 1.5, None, 1, True,
                 int(screen_width/12)),
          Bullet(1, b_s, 2*b_s, RED, 0.5, (6 * screen_height) * delay_time / 1000, 0.1, None)]

for i in range(3):
    for _ in range(bull_lvl[i] - 1):
        bullet[i].lvlup()
sel_bull = 0
bullet_reload = [0, 0, 0]
screen_speed = (screen_height / 2) * delay_time / 1000
ms = (screen_height / 2) * delay_time / 1000
gold_speed = (2 * screen_height) * delay_time / 1000
shot_speed = (5 * screen_height) * delay_time / 1000
tree_between = screen_height/10
tree = (-1) * tree_between
road_start = int(screen_width/3 + screen_width/100)
road_end = int(2 * screen_width/3 - screen_width/100)
road_length = road_end - road_start
gold_w = gold_h = int(screen_height/36)
text_h = gold_h
text_w = int(text_h * 2 / 3)
gold_count = 0
bomb_speed = 3000 * delay_time / 1000
tree_pos = []
golds = []
bullets = []
animals = []
bombs = []
bomb_barrels = []
frame = 0
gold_end_pos = None
for i in range(15):
    x = random.randint(int(screen_width/20), int(screen_width/6))
    tree_pos.append([x, tree + i * tree_between])
    x = random.randint(int(21 * screen_width/30), int(33 * screen_width/40))
    tree_pos.append([x, tree + i * tree_between])

tree_pos.reverse()
tree_len = tree_pos.__len__()
t = time.time()
all_animals = [0]
animals_killed = [0]
all_golds = [0]
gold_taked = [0]
money_show = [0]

tree1 = pygame.image.load('tree1.xcf')
tree1 = pygame.transform.scale(tree1, (int(screen_width/8), int(screen_height/8)))
bg = pygame.image.load('grass.png')
bg = pygame.transform.scale(bg, (screen_width, screen_height))
gold_pic = pygame.image.load('gold.png')
gold_pic = pygame.transform.scale(gold_pic, (gold_w, gold_h))
max_hp = 100 + (hp_lvl - 1) * 50
min_speed = 100 * int(screen_height/100) * delay_time / 1000
player_speed = min_speed + (speed_lvl - 1) * min_speed/8
player_pos = [int(screen_width / 2), screen_height - 200]
player_size = [int(screen_height/20), int(2 * screen_height/25)]

player = Player(player_size, player_speed, max_hp, max_hp, None)

soldier_pic = [pygame.image.load('zinvor1.png'), pygame.image.load('zinvor2.png'),
                    pygame.image.load('zinvor3.png'), pygame.image.load('zinvor2.png')]

pics = []
for i in range(4):
    pics.append(pygame.transform.scale(soldier_pic[i], (player_size[0], player_size[1])))

player.pic = pics

cat1 = [pygame.image.load('animals/cat11.png'), pygame.image.load('animals/cat12.png')]
cat2 = [pygame.image.load('animals/cat21.png'), pygame.image.load('animals/cat22.png')]
tiger1 = [pygame.image.load('animals/tiger2.xcf'), pygame.image.load('animals/tiger1.xcf')]
boss1 = [pygame.image.load('animals/bearboss1.xcf'), pygame.image.load('animals/bearboss2.xcf')]
camel1 = [pygame.image.load('animals/camel11.png'), pygame.image.load('animals/camel12.png')]
for i in range(2):
    cat1[i] = pygame.transform.scale(cat1[i], (int(screen_height / 40), int(screen_height / 30)))
    cat2[i] = pygame.transform.scale(cat2[i], (int(screen_height / 40), int(screen_height / 30)))
    tiger1[i] = pygame.transform.scale(tiger1[i], (int(screen_height / 25), int(screen_height / 12)))
    camel1[i] = pygame.transform.scale(camel1[i], (int(screen_height / 25), int(screen_height / 15)))
    boss1[i] = pygame.transform.scale(boss1[i], (int(screen_height / 12.5), int(screen_height / 7.5)))

wave_an = [[cat1, cat2, tiger1, boss1]]

name_rect = pygame.Rect(1.75/3 * screen_width, screen_height/15, screen_width/3, screen_height / 16)
tree_pic = tree1
wave_ind = -1


def forest():
    for i in range(tree_len - 1, -1, -1):
        tree_pos[i][1] += ms
        win.blit(tree_pic, (tree_pos[i][0], tree_pos[i][1]))

    if tree_pos[0][1] >= 9 * screen_height / 8:
        tree_pos.__delitem__(0)
        tree_pos.__delitem__(0)
        x = random.randint(int(screen_width/20), int(screen_width/6))
        tree_pos.append([x, tree_pos[tree_len - 3][1] - tree_between])
        x = random.randint(int(21 * screen_width/30), int(33 * screen_width/40))
        tree_pos.append([x, tree_pos[tree_len - 3][1] - tree_between])


def player_move(pos, fr, cl, fire, shot_frame, st, jump, js, keys, money):
    pos_0 = 0
    pos_1 = 0
    a25 = player_size[0]/2
    a55 = player_size[1] - player_size[0]/2
    ind = int((fr * delay_time) / 100) % 4
    position = [pos[0] - a25, pos[1] - a55]
    rotated_image = player.pic[ind]
    if jump == 0:
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            pos_0 -= 1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            pos_0 += 1
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            pos_1 -= 1
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            pos_1 += 1
    else:
        pos[1] += (jump * 5 * player.speed)
        win.blit(pygame.transform.scale(rotated_image, (int(1.2 * player_size[0]), int(1.2 * player_size[1]))),
                 (position[0], position[1]))
        if abs(pos[1] - js) >= screen_height/7:
            jump = 0

    pos_0 *= player.speed
    pos_1 *= player.speed
    if pos_0 != 0 and pos_1 != 0:
        pos_0 /= np.sqrt(2)
        pos_1 /= np.sqrt(2)

    pos_0 = int(pos_0)
    pos_1 = int(pos_1)

    if jump == 0:
        for an in animals:
            if pos[0] - a25 > an.x + an.pic[0].get_width() or pos[0] + a25 < an.x:
                x = pos[0] + pos_0
                if pos[1] - a25 < an.y + an.pic[0].get_height() and pos[1] + a25 > an.y:
                    if x - a25 <= an.x + an.pic[0].get_width() and x + a25 >= an.x:
                        if x + a25 > an.x + an.pic[0].get_width():
                            pos[0] = an.x + an.pic[0].get_width() - pos_0 + a25 + 1
                        else:
                            pos[0] = an.x - a25 - pos_0 - 1
                        break
            else:
                x = pos[1] + pos_1
                if x - a25 < an.y + an.pic[0].get_height() and x + a25 > an.y:
                    if x - a25 > an.y:
                        if screen_height - player_size[1] >= pos[1] + screen_height / 7:
                            jump = 1
                        else:
                            jump = -1
                        js = pos[1]
                        player.hp -= an.damage
                    else:
                        pos[1] -= pos_1
                    break

    pos[0] += pos_0
    pos[1] += pos_1
    if pos[0] >= road_end - player_size[0]/2:
        pos[0] = road_end - player_size[0]/2
    elif pos[0] <= road_start + player_size[0]/2:
        pos[0] = road_start + player_size[0]/2
    if pos[1] >= screen_height - player_size[0]:
        pos[1] = screen_height - player_size[0] - 1
    elif pos[1] <= a25:
        pos[1] = a25

    if (cl or keys[pygame.K_SPACE]) and time.time() - bullet_reload[sel_bull] >= bullet[sel_bull].reload\
            and bullet[sel_bull].cost <= money:
        money -= bullet[sel_bull].cost
        d = bullet[sel_bull].damage
        r = bullet[sel_bull].reload
        rad = bullet[sel_bull].radius
        l = bullet[sel_bull].lvl
        if sel_bull == 1:
            bull = Bullet(10, 10, 10, BLACK, d, (3 * screen_height) * delay_time / 1000, r, None, l, True, rad)
        elif sel_bull == 2:
            bull = Bullet(1, 5, 10, RED, d, (6 * screen_height) * delay_time / 1000, r, None, l)
        else:
            bull = Bullet(0, 5, 5, BROWN, d, (5 * screen_height) * delay_time / 1000, r, None, l)
        bull.x = pos[0] + int(0.28 * a25)
        bull.y = pos[1] - a55
        bullets.append(bull)
        bullet_reload[sel_bull] = time.time()

    if cl or keys[pygame.K_SPACE]:
        fire = True
    else:
        fire = False

    if not fire:
        if pos_0 > 0:
            if pos_1 > 0:
                rotated_image = pygame.transform.rotate(player.pic[ind], -135)
                position = [pos[0] - a25, pos[1] - a25]
            elif pos_1 < 0:
                rotated_image = pygame.transform.rotate(player.pic[ind], -45)
                position = [pos[0] - a25, pos[1] - a55]
            else:
                rotated_image = pygame.transform.rotate(player.pic[ind], -90)
                position = [pos[0] - a25, pos[1] - a25]
        elif pos_0 < 0:
            if pos_1 > 0:
                rotated_image = pygame.transform.rotate(player.pic[ind], 135)
                position = [pos[0] - a55, pos[1] - a25]
            elif pos_1 < 0:
                rotated_image = pygame.transform.rotate(player.pic[ind], 45)
                position = [pos[0] - a55, pos[1] - a55]
            else:
                rotated_image = pygame.transform.rotate(player.pic[ind], 90)
                position = [pos[0] - a55, pos[1] - a25]
        else:
            if pos_1 > 0:
                rotated_image = pygame.transform.rotate(player.pic[ind], 180)
                position = [pos[0] - a25, pos[1] - a25]

    if not jump:
        win.blit(rotated_image, (position[0], position[1]))
    return pos, fire, shot_frame, st, jump, js, money


def new_golds(count):
        dirq = random.randint(1, 30 - count * 3)
        golds.append([road_start + dirq * (road_end - road_start) / 30, -100])

        if 8 > count > 1:
            golds.append([int(road_start + dirq * (road_end - road_start) / 30 + text_w), -100])
            if count == 4:
                golds.append([int(road_start + dirq * (road_end - road_start) / 30), -150])
                golds.append([int(road_start + dirq * (road_end - road_start) / 30 + text_w), -150])

        if count == 8:
            golds.append([int(road_start + dirq * (road_end - road_start) / 30), -150])
            for i in range(1, 4):
                golds.append([int(road_start + dirq * (road_end - road_start) / 30 + text_w * i), -100])
                golds.append([int(road_start + dirq * (road_end - road_start) / 30 + text_w * i), -150])

        all_golds[0] += count


def gold_spawn(ti, gold_c, pos, money):
    if time.time() - ti >= 2:
        ti = time.time()
        x = random.randint(0, 10)
        if x < 4:
            new_golds(1)
            gold_c += 1
        elif x < 7:
            new_golds(2)
            gold_c += 2
        elif x < 9:
            new_golds(4)
            gold_c += 4
        else:
            new_golds(8)
            gold_c += 8

    w1 = pos[0] - 25
    w2 = pos[0] + 25
    h1 = pos[1] - 25
    h2 = pos[1] + 25
    for i in range(gold_c - 1, -1, -1):
        if golds[i][1] >= screen_height + 1:
            golds.__delitem__(i)
            continue
        gold_taked[0] += 1
        if w2 >= golds[i][0] >= w1 and h2 >= golds[i][1] >= h1:
            golds.__delitem__(i)
            money += 1
        elif w2 >= golds[i][0] + gold_w >= w1 and h2 >= golds[i][1] >= h1:
            golds.__delitem__(i)
            money += 1
        elif w2 >= golds[i][0] + gold_w >= w1 and h2 >= golds[i][1] + gold_h >= h1:
            golds.__delitem__(i)
            money += 1
        elif w2 >= golds[i][0] >= w1 and h2 >= golds[i][1] + gold_h >= h1:
            golds.__delitem__(i)
            money += 1
        else:
            gold_taked[0] -= 1

    gold_c = golds.__len__()
    for i in range(gold_c):
        win.blit(gold_pic, (golds[i][0], golds[i][1]))
        golds[i][1] += ms

    return ti, gold_c, money


def print_money(mon):
    x = mon
    degree = 1
    while x > 9:
        degree += 1
        x /= 10

    text_width = gold_w + (degree + 1) * text_w
    text_height = int(1.2 * gold_h)
    text_start_x = int(19 * screen_width / 20) - text_width - gold_w
    text_start_y = gold_h
    pygame.draw.rect(win, WHITE, (text_start_x, text_start_y, text_width, text_height), 0, int(gold_h/2))
    win.blit(gold_pic, (text_start_x, int(1.1 * text_start_y)))
    print_text(win, str(mon), text_start_x + int((gold_w + text_width)/2), int(1.6 * text_start_y), BLACK, gold_w)


def bullet_shot(sel_bull):
    for b in range(bullet.__len__()):
        bullet[b].left_draw_rel(win, b, screen_width, screen_height, bullet_reload[b], sel_bull == b)
        if sel_bull == b and bullet[b].cost > money:
            sel_bull = 0
    for bul in bullets:
        rem = bul.draw(win)
        if rem:
            bullets.remove(bul)

    return sel_bull


def bomb_explosion():
    for bomb in bombs:
        if bomb[2] == 0:
            x = player_pos[0] - bomb[0]
            y = player_pos[1] - bomb[1]
            if x ** 2 + y ** 2 <= (bomb[3] + player_size[0]) ** 2:
                player.hp -= bomb[4]
        bomb[2] += bomb_speed
        if 20 * (1 - bomb[2]/bomb[3]) < 1:
            bombs.remove(bomb)
        else:
            pygame.draw.circle(win, YELLOW, (bomb[0], bomb[1]), bomb[2], int(20 * (1 - bomb[2]/bomb[3])))


def progress():
    prog = (time.time() - lvlstart_time - 3)/(27 + level)
    if prog >= 1:
        prog = 1
    sx = screen_width/4
    ey1 = ey = sy = screen_height/15
    ex = screen_width * 0.75
    ex1 = (ex - sx) * prog + sx
    pygame.draw.line(win, DARKGREEN, (sx, sy), (ex1, ey1), 10)
    if prog < 1:
        pygame.draw.line(win, RED, (ex1, ey1), (ex, ey), 10)


def animal_spawn(fr):
    if animals.__len__() == 0 and not round_end_wind:
        x = level % 15
        v = random.randint(0, x)
        if v <= x/2 + 1:
            pic_l = wave_an[wave_ind][0][0].get_width()
            if v == 0:
                pic = wave_an[wave_ind][0]
            else:
                pic = wave_an[wave_ind][1]
            an_hp = 1.44 ** int(level/10)
            an_ms = 900
            an_d = 2
        else:
            pic_l = wave_an[wave_ind][2][0].get_width()
            pic = wave_an[wave_ind][2]
            an_hp = 3 + 1.3**int(level/10)
            an_ms = 700
            an_d = 5

        d = random.randint(road_start, road_end)
        l = min(int((road_end - d)/(1.5 * pic_l)), level + 1)
        if l > 0:
            count = random.randint(1, l)
        else:
            count = 0

        all_animals[0] += count
        for i in range(count):
            animals.append(Animal(an_hp, pic, an_ms * delay_time / 1000, d + 1.5 * i * pic_l, -100, an_d))

    for a in animals:
        if a.y > screen_height + 1:
            animals.remove(a)
        for bul in bullets:
            if a.y + a.pic[0].get_height() >= bul.y and player_pos[1] > a.y \
                    and a.x + a.pic[0].get_width() >= bul.x >= a.x - bul.w:
                if bul.radius > 0:
                    bombs.append([bul.x + bul.w/2, bul.y, 0, bul.radius, bul.damage])
                    for an in animals:
                        mx = an.x + an.pic[0].get_width()/2
                        my = an.y + an.pic[0].get_height()/2
                        if (mx - bul.x)**2 + (my - bul.y)**2 <= bul.radius**2 and a != an:
                            an.hp -= bul.damage

                a.hp -= bul.damage
                bullets.remove(bul)
                break


def died_animals(fr, money):
    for a in animals:
        if a.hp <= 0:
            animals.remove(a)
            animals_killed[0] += 1
            money += a.cost
            continue

        a.draw(win, fr, delay_time)

    return money


def bomb_spawn(last_time):
    if time.time() - last_time >= 1:
        if random.randint(0, 6) == 0:
            bomb_barrels.append(Bomb(20, random.randint(road_start + 50, road_end - 50), -100, 5, 150))
        last_time = time.time()

    for barrel in bomb_barrels:
        if barrel.y > screen_height + 100:
            bomb_barrels.remove(barrel)
        else:
            exploted = barrel.bomb_explode(animals, bullets, player_pos, player_size, bombs)
            if not exploted:
                barrel.draw(win, ms)
            else:
                bomb_barrels.remove(barrel)

    return last_time


def draw_background():
    pygame.draw.rect(win, GREEN, (0, 0, screen_width, screen_height))
    pygame.draw.rect(win, BLACK, (0, 0, int(screen_width/20), screen_height))
    pygame.draw.rect(win, BLACK, (int(19 * screen_width/20), 0, int(screen_width / 20), screen_height))
    pygame.draw.line(win, SILVER, (screen_width/3, 0), (screen_width/3, screen_height), int(screen_width/100))
    pygame.draw.line(win, SILVER, (screen_width / 1.5, 0), (screen_width / 1.5, screen_height), int(screen_width/100))
    pygame.draw.rect(win, GRAY, (road_start, 0, road_length, screen_height))
    forest()


def draw_updates(can_lvlup, onbutton, money):
    need_message = False
    for n in range(bullet.__len__()):
        can_lvlup, ob, money, m = bullet[n].draw_strength(win, int(screen_width/12), int((5*n + 1) * screen_height/17),
                                                       screen_width, screen_height, click, m_pos, can_lvlup, money)
        if m:
            need_message = m

        if ob:
            onbutton = ob
        bull_lvl[n] = bullet[n].lvl

    ob, m, can_lvlup, money = player.updates(win, screen_width, screen_height, frame, delay_time, money, click, m_pos, can_lvlup)
    if ob:
        onbutton = ob

    if m:
        need_message = m
    return can_lvlup, onbutton, money, need_message


def player_info():
    x = 0.9 * screen_width
    y1 = screen_height/10
    y2 = screen_height * 0.9
    y3 = y2 - (y2 - y1) * player.hp/player.max_hp
    if player.max_hp > player.hp:
        pygame.draw.line(win, RED, (x, y1), (x, y3), 10)

    if player.hp != 0:
        pygame.draw.line(win, GREEN1, (x, y3), (x, y2), 10)


def before_level(bls):
    t = time.time() - lvlstart_time
    if t < 1:
        txt = "3"
    elif t < 2:
        txt = "2"
    elif t < 3:
        txt = "1"
    else:
        bls = False
        return bls

    ind = int(frame * delay_time / 100) % 4
    win.blit(player.pic[ind], (player_pos[0] - player_size[0]/2, player_pos[1] - player_size[1]/2))

    print_text(win, "ROUND " + str(level), screen_width/2, screen_height/2, BLACK, int(screen_height/10))
    print_text(win, txt, screen_width/2, screen_height * 0.6, BLACK, int(screen_height/10))
    forest()
    return bls


def clear_all():
    player.hp = player.max_hp
    bombs.clear()
    golds.clear()
    animals.clear()
    bomb_barrels.clear()
    animals.clear()
    animals_killed[0] = 0
    all_animals[0] = 0
    all_golds[0] = 0
    gold_taked[0] = 0
    money_show[0] = 0


next_button = Button(screen_width/20, screen_height/20, WHITE, WHITE)
menu_button = Button(screen_width/18, screen_height/20, SILVER, WHITE)


def round_end(ws, money):
    deltat = time.time() - ws
    act = 0
    rx = int(screen_width * 0.3)
    ry = int(screen_height * 0.4)
    rw = int(screen_width / 2.5)
    rh = int(screen_height / 3)
    if 1 >= deltat >= 0.5:
        tx = int(screen_width/2 - (deltat - 0.5)/0.5 * 0.2 * screen_width)
        ty = int(screen_height/2 - (deltat - 0.5)/0.5 * 0.1 * screen_height)
        tw = int((deltat - 0.5)/0.5 * rw)
        th = int((deltat - 0.5) / 0.5 * rh)
        pygame.draw.rect(win, RED, (tx, ty, tw, th), 0, int(tw/2))
    elif deltat >= 1:
        pygame.draw.rect(win, RED, (rx, ry, rw, rh), 0, int(rw / 2))
        if all_animals[0] == 0:
            an_gold_bonus = int(48 + level)
        else:
            an_gold_bonus = int(animals_killed[0]/all_animals[0] * (48 + level))

        if deltat <= 1.5:
            an_gold_bonus = int((deltat - 1) / 0.5 * an_gold_bonus)
        else:
            if all_golds[0] == 0:
                gold_bonus = int(78 + level)
            else:
                gold_bonus = int(gold_taked[0]/all_golds[0] * (78 + level))

            if deltat <= 2:
                gold_bonus = int((deltat - 1.5) / 0.5 * gold_bonus)

            else:
                bonus = int(10 * level)
                if deltat <= 2.5:
                    bonus = int((deltat - 2) / 0.5 * bonus)

                else:
                    coins = int(bonus + gold_bonus + an_gold_bonus)

                    if deltat <= 3:
                        coins = int((deltat - 2.5)/0.5 * coins)

                    else:
                        bh = next_button.height
                        if deltat <= 3.5:
                            bw = (deltat - 3)/0.5 * (screen_width + next_button.width) - screen_width
                            next_button.draw(win, rx + rw/2 - bw/2, ry + rh * 0.9 - bh/2, "Next", click, m_pos,
                                             int(screen_height/40), BLACK, BLACK)
                        else:
                            next_button.active_color = SILVER
                            bw = next_button.width
                            act = next_button.draw(win, rx + rw/2 - bw/2, ry + rh * 0.9 - bh/2, "Next", click, m_pos,
                                             int(screen_height/40), BLACK, BLACK)

                    money += (coins - money_show[0])
                    money_show[0] = coins

                    print_text(win, "You receive: " + str(coins), rx + rw / 2, ry + rh * 0.7, WHITE,
                               int(screen_height / 20))

                print_text(win, "Bonus: " + str(bonus), rx + rw/2, ry + rh * 0.55, WHITE,
                           int(screen_height / 30))

            print_text(win, "Bonus for coins: " + str(gold_bonus), rx + rw/2, ry + rh/2.5, WHITE, int(screen_height/30))

        print_text(win, "Bonus for animals: " + str(an_gold_bonus), rx + rw/2, ry + rh/4, WHITE, int(screen_height/30))

    if deltat < 0.5:
        print_text(win, "WIN", screen_width/2, screen_height * 0.4, BLACK, int(screen_height/5 * deltat))
    else:
        print_text(win, "WIN", screen_width / 2, screen_height * 0.4, BLACK, int(screen_height / 10))

    return money, act


def die_end(ws, money):
    t = time.time() - ws
    act = 0
    rx = int(screen_width * 0.3)
    ry = int(screen_height * 0.4)
    rw = int(screen_width / 2.5)
    rh = int(screen_height / 3)
    if t <= 0.5:
        tx = int(screen_width / 2 - t / 0.5 * 0.2 * screen_width)
        ty = int(screen_height / 2 - t / 0.5 * 0.1 * screen_height)
        tw = int(t / 0.5 * rw)
        th = int(t / 0.5 * rh)
        pygame.draw.rect(win, RED, (tx, ty, tw, th), 0, int(tw / 2))
    elif t > 0.5:
        pygame.draw.rect(win, RED, (rx, ry, rw, rh), 0, int(rw / 2))
        bonus = 10 * level
        if t <= 1:
            bonus = int((t - 0.5)/0.5 * bonus)

        else:
            bh = next_button.height
            rec_g = bonus
            if t <= 1.5:
                rec_g = int(rec_g * (t - 1)/0.5)
            else:
                if t <= 2:
                    bw = (t - 1.5) / 0.5 * (screen_width + next_button.width) - screen_width
                    next_button.draw(win, rx + rw / 2 - bw / 2, ry + rh * 0.9 - bh / 2, "Restart", click, m_pos,
                                     int(screen_height / 40), BLACK, BLACK)
                else:
                    next_button.active_color = SILVER
                    bw = next_button.width
                    act = next_button.draw(win, rx + rw / 2 - bw / 2, ry + rh * 0.9 - bh / 2, "Restart", click, m_pos,
                                           int(screen_height / 40), BLACK, BLACK)

            money += (rec_g - money_show[0])
            money_show[0] = rec_g
            print_text(win, "You receive: " + str(rec_g), rx + rw/2, ry + 2 * rh/3, WHITE, int(screen_height/15))
        print_text(win, "Bonus: " + str(bonus), rx + rw/2, ry + rh/3, WHITE, int(screen_height/20))

    return money, act


while run:
    frame += 1
    pygame.time.delay(delay_time)
    m_pos = pygame.mouse.get_pos()
    events = pygame.event.get()
    keys = pygame.key.get_pressed()
    if level % 15 == 1:
        wave_ind += 1
        wave_ind %= 1

    for ev in events:
        if ev.type == pygame.QUIT:
            run = False
        if ev.type == pygame.MOUSEBUTTONDOWN:
            click = True
        else:
            click = False
            can_lvlup = True
        if menu:
            if click and name_rect.collidepoint(m_pos):
                name_change = True
            if ev.type == pygame.KEYDOWN:
                if name_change:
                    if ev.key == pygame.K_RETURN:
                        name_change = False
                    elif ev.key == pygame.K_BACKSPACE:
                        player.name = player.name[:-1]
                    elif player.name.__len__() < 10:
                        player.name += ev.unicode
        else:
            name_change = False

    if menu:
        pygame.draw.rect(win, GREEN1, (0, 0, screen_width, screen_height))
        act = start_but.draw(win, screen_width/2 - start_but.width/2, 0, "Start",
                             click, m_pos, int(screen_width/50), BLACK, BLACK)
        if act == 1:
            menu = False
            lvlstart_time = time.time()
            before_lvlstart = True
        if act == 1 or act == -1:
            onbutton = True
        else:
            onbutton = False

        can_lvlup, onbutton, money, m = draw_updates(can_lvlup, onbutton, money)
        if name_change:
            pygame.draw.rect(win, SILVER, (name_rect.x, name_rect.y, name_rect.w, name_rect.h), 5)
        print_text(win, player.name, int(2.25 / 3 * screen_width), int(screen_height * (1 / 15 + 1 / 32)), BLACK,
                   int(screen_height / 32))
        if m and not message:
            message = True
            message_start = time.time()

    else:
        draw_background()
        if round_end_wind:
            ms = 0
            act = 0
            if not player.died:
                win.blit(player.pic[1], (player_pos[0] - player_size[0]/2, player_pos[1] - player_size[1]/2))
                money, act = round_end(wind_start, money)
            else:
                money, act = die_end(wind_start, money)
                if act == 1:
                    player.died = False

            if act == 1 or act == -1:
                onbutton = True
            else:
                onbutton = False

            if act == 1:
                round_end_wind = False
                before_lvlstart = True
                lvlstart_time = time.time()
        if not round_end_wind:

            if before_lvlstart:
                ms = screen_speed
                before_lvlstart = before_level(before_lvlstart)
            if not before_lvlstart:
                if keys[pygame.K_1] or keys[pygame.K_KP1]:
                    sel_bull = 0
                elif keys[pygame.K_2] or keys[pygame.K_KP2]:
                    sel_bull = 1
                elif keys[pygame.K_3] or keys[pygame.K_KP3]:
                    sel_bull = 2
                if time.time() - lvlstart_time >= 30 + level and animals.__len__() == 0:
                    round_end_wind = True
                    wind_start = time.time()
                    clear_all()
                    gold_count = 0
                    level += 1

                if player.died:
                    if time.time() - player.dietime >= 2:
                        round_end_wind = True
                        wind_start = time.time()
                        clear_all()
                        gold_count = 0
                    font_size = int((time.time() - player.dietime)/2 * screen_height/10)
                    print_text(win, "YOU DIED", screen_width/2, screen_height/2, RED, font_size)
                if not player.died:
                    animal_spawn(frame)
                    b_last_time = bomb_spawn(b_last_time)
                    player_pos, shot, sf, shot_time, jump, jump_st, money = \
                        player_move(player_pos, frame, click, shot, sf, shot_time, jump, jump_st, keys, money)
                    t, gold_count, money = gold_spawn(t, gold_count, player_pos, money)
                money = died_animals(frame, money)
                sel_bull = bullet_shot(sel_bull)
                bomb_explosion()
                progress()
                if player.hp <= 0 and not player.died:
                    player.hp = 0
                    player.died = True
                    player.dietime = time.time()

        sel_bull = bullet_shot(sel_bull)
        player_info()
        to_menu = menu_button.draw(win, screen_width/16, screen_height * 0.87, "Menu", click, m_pos,
                                   int(screen_height/30), BLACK, BLACK)
        if to_menu == 1:
            menu = True
            clear_all()
            gold_count = 0
        if to_menu == 1 or to_menu == -1:
            onbutton = True
    if message:
        if time.time() - message_start <= 3:
            font_size = int(screen_width * 0.01)
            print_text(win, "You don't have enough money", m_pos[0], m_pos[1], BLACK, font_size)
        else:
            message = False
    if onbutton:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_HAND)
    else:
        pygame.mouse.set_system_cursor(pygame.SYSTEM_CURSOR_ARROW)

    print_money(money)

    pygame.display.update()


money_txt = open('money.txt', 'w+')
money_txt.write(str(money) + "\n")
money_txt.writelines(str(bullet[0].lvl) + "\n")
money_txt.writelines(str(bullet[1].lvl)+"\n")
money_txt.writelines(str(bullet[2].lvl)+"\n")
money_txt.writelines(str(int((player.max_hp - 50)/50)) + "\n")
money_txt.writelines(str(int((player.speed - min_speed)/(min_speed/8) + 1)) + " \n")
money_txt.writelines(str(level) + " \n")
money_txt.close()
pygame.quit()
