import pygame
import time


RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GREEN1 = (0, 170, 0)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
SILVER = (192, 192, 192)
YELLOW = (255, 255, 0)
W1 = (205, 205, 205)


class Player:
    def __init__(self, size, speed, hp, max_hp, pics):
        self.size = size
        self.speed = speed
        self.hp = hp
        self.max_hp = max_hp
        self.pic = pics
        self.name = 'Player'
        self.died = False
        self.dietime = None

    def updates(self, win, s_w, s_h, frame, delay_time, money, click, m_pos, can_lvlup):
        onbutton = False
        message = False
        x = s_w - s_w/12 - s_w/3
        y = s_h/15
        w = s_w/3
        h = s_h/4
        font_size = int(h/15)
        pygame.draw.rect(win, WHITE, (x, y, w, h))
        pygame.draw.rect(win, GRAY, (x, y, w, h/4))
        ind = int(frame * delay_time / 50) % 4
        image = pygame.transform.scale(self.pic[ind], (int(1.5 * s_h/20), int(s_h * 0.12)))
        win.blit(image, (x + w - 2.25 * s_h/20, y + h/2 - s_h * 0.06))
        y += h/4
        h -= h/4
        r_x = x + w/12
        r_x1 = x + w/2
        r_y = y + h * 5/12
        t_x = int(x + w/10 + s_h/40)
        t_y = int(r_y - s_h/45)
        print_text(win, "Max HP", t_x, t_y, BLACK, int(s_h/60))
        pygame.draw.line(win, GRAY, (r_x, r_y), (r_x1, r_y), 10)
        cost = int((self.max_hp/50 - 1) * 400)

        text_x = r_x1 + 4 * font_size
        text_y = r_y
        if self.max_hp < 500:
            text = str(self.max_hp) + " -> " + str(self.max_hp + 50)
            x1 = int(r_x + (r_x1 - r_x) * self.max_hp/500)
            pygame.draw.line(win, WHITE, (r_x, r_y), (x1, r_y), 10)
            x2 = int(x1 + (r_x1 - r_x)/10)
            pygame.draw.line(win, SILVER, (x1, r_y), (x2, r_y), 10)

            button = Button((r_x1 - r_x)/2, r_y - t_y + s_h/120 - 7, (255, 190, 0), YELLOW)
            act = button.draw(win, (r_x + r_x1)/2, t_y - s_h/120, "LVL UP(" + str(cost) + ")",
                              click, m_pos, int(s_h/60), BLACK, BLACK)
            if act == 1 and can_lvlup:
                if money < cost:
                    message = True
                else:
                    money -= cost
                    self.max_hp += 50
                    can_lvlup = False
            if act == 1 or act == -1:
                onbutton = True
        else:
            text = "500"
            button = Button((r_x1 - r_x) / 2, r_y - t_y + s_h / 120 - 7, GRAY, GRAY)
            button.draw(win, (r_x + r_x1) / 2, t_y - s_h / 120, "MAX LVL", click, m_pos, int(s_h / 60), BLACK,
                              BLACK)
        print_text(win, text, text_x, text_y, BLACK, font_size)
        pygame.draw.rect(win, RED, (r_x, r_y - 7, r_x1 - r_x, 14), 4)

        r_y += 5/12 * h
        pygame.draw.line(win, GRAY, (r_x, r_y), (r_x1, r_y), 10)
        t_y += int(5 * h/12)
        print_text(win, "Speed ", t_x, t_y, BLACK, int(s_h / 60))
        text_y = r_y
        speed = int(self.speed * 1000/delay_time)
        max_speed = 200 * int(s_h/100)
        delta_s = int(max_speed/16)
        cost = int((speed - max_speed/2)/delta_s + 1) * 200
        if speed < max_speed:
            text = str(speed) + " -> " + str(int(speed + delta_s))
            x1 = int(r_x + (r_x1 - r_x) * speed/max_speed)
            pygame.draw.line(win, WHITE, (r_x, r_y), (x1, r_y), 10)
            x2 = int(x1 + (r_x1 - r_x)/20)
            pygame.draw.line(win, SILVER, (x1, r_y), (x2, r_y), 10)

            button = Button((r_x1 - r_x)/2, r_y - t_y + s_h/120 - 7, (255, 190, 0), YELLOW)
            act = button.draw(win, (r_x + r_x1)/2, t_y - s_h/120, "LVL UP(" + str(cost) + ")",
                              click, m_pos, int(s_h/60), BLACK, BLACK)
            if act == 1 and can_lvlup:
                if money < cost:
                    message = True
                else:
                    money -= cost
                    speed += delta_s
                    self.speed = speed * delay_time/1000
                    can_lvlup = False
            if act == 1 or act == -1:
                onbutton = True
        else:
            text = str(max_speed)
            button = Button((r_x1 - r_x) / 2, r_y - t_y + s_h / 120 - 7, GRAY, GRAY)
            button.draw(win, (r_x + r_x1) / 2, t_y - s_h / 120, "MAX LVL", click, m_pos, int(s_h / 60), BLACK, BLACK)
        print_text(win, text, text_x, text_y, BLACK, font_size)
        pygame.draw.rect(win, RED, (r_x, r_y - 7, r_x1 - r_x, 14), 4)
        self.hp = self.max_hp
        return onbutton, message, can_lvlup, money


def up_task(win, text, st_p, en_p, lvl, value, text_pos, font_size):
    print_text(win, text, text_pos[0], text_pos[1], BLACK, font_size)
    if lvl == 15:
        pygame.draw.line(win, WHITE, st_p, en_p, 10)
    elif lvl == 14:
        x1, y1 = st_p
        x2, y2 = en_p
        en_p2 = (x1 + int((x2 - x1)*14/15), y1)
        pygame.draw.line(win, WHITE, st_p, en_p2, 10)
        pygame.draw.line(win, SILVER, en_p2, en_p, 10)
    else:
        x1, y1 = st_p
        x2, y2 = en_p
        en_p2 = (x1 + int((x2 - x1)*lvl/15), y1)
        en_p3 = (x1 + int((x2 - x1)*(lvl + 1)/15), y1)
        pygame.draw.line(win, WHITE, st_p, en_p2, 10)
        pygame.draw.line(win, SILVER, en_p2, en_p3, 10)
        pygame.draw.line(win, GRAY, en_p3, en_p, 10)

    r_x, r_y = st_p
    r_y -= 7
    r_x2, r_y2 = en_p
    r_w = r_x2 - r_x
    pygame.draw.rect(win, RED, (r_x, r_y, r_w, 14), 4)

    t_x, t_y = en_p
    t_x += 4 * font_size
    if text == "Damage" or text == "Radius":
        if lvl < 15:
            text = str(int(value)) + " -> " + str(int(1.2*value))
        else:
            text = str(int(value))
    elif text == "Reload":
        v1 = int(100 * value)/100
        if lvl < 15:
            v2 = int(100 * value / 1.2) / 100
            text = str(v1) + "s -> " + str(v2) + "s"
        else:
            text = str(v1) + "s"
    print_text(win, text, t_x, t_y, BLACK, int(font_size))


class Animal:
    def __init__(self, hp, pic, ms, pos_x, pos_y, damage):
        self.hp = hp
        self.pic = pic
        self.ms = ms
        self.x = pos_x
        self.y = pos_y
        self.damage = damage
        self.max_hp = hp
        self.cost = int(self.hp)

    def draw(self, win, fr, delay_time):
        win.blit(self.pic[int(fr * delay_time / 100) % 2], (self.x, self.y))
        self.y += self.ms
        if self.hp != self.max_hp:
            s_p1 = (self.x, self.y + self.pic[0].get_height()/2)
            e_p1 = (self.x + self.pic[0].get_width() * self.hp/self.max_hp, self.y + self.pic[0].get_height()/2)
            e_p2 = (self.x + self.pic[0].get_width(), self.y + self.pic[0].get_height()/2)
            pygame.draw.line(win, GREEN, s_p1, e_p1, 3)
            pygame.draw.line(win, RED, e_p1, e_p2, 3)


class Bullet:
    def __init__(self, cost, w, h, color, damage, speed, reload, pic, lvl=1, bomb=False, radius=0):
        self.cost = cost
        self.w = w
        self.h = h
        self.x = None
        self.y = None
        self.color = color
        self.damage = damage
        self.speed = speed
        self.reload = reload
        self.pic = pic
        self.bomb = bomb
        self.radius = radius
        self.lvl = lvl

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.w, self.h))
        self.y -= self.speed
        if self.y <= -100:
            return True
        else:
            return False

    def left_draw_rel(self, win, x, w, h, rel_s, is_selected):
        if h > w:
            h, w = w, h
        rx = int(w/20 + h/20)
        ry = int((2 * x + 1) * h/20)
        rh = rw = int(h/20)
        if is_selected:
            rx, ry, rw, rh = int(rx - rw/6), int(ry - rh/6), int(rw/3 + rw), int(rh/3 + rh)
        bx = int(rx + rw/2 - self.w)
        by = int(ry + rh/2 - self.h)
        pygame.draw.rect(win, self.color, (bx, by, 2 * self.w, 2 * self.h))
        print_text(win, str(self.cost), bx + self.w, ry + int(0.8 * rh), YELLOW, int(rh/4))
        t = time.time() - rel_s
        pygame.draw.rect(win, GREEN1, (rx, ry, rw, rh), 3)
        if t < self.reload:
            '''s_p1 = (rx + 5, by + 3 * self.h)
            e_p1 = (int(rx + 5 + (rw - 10) * (time.time() - rel_s)/self.reload), by + 3 * self.h)
            e_p2 = (rx + rw - 5, by + 3 * self.h)
            pygame.draw.line(win, GREEN1, s_p1, e_p1, 3)
            pygame.draw.line(win, RED, e_p1, e_p2, 3)'''
            p1 = (rx, ry)
            p2 = (rx + rw, ry)
            p3 = (rx + rw, ry + rh)
            p4 = (rx, ry + rh)
            if t < self.reload/4:
                d = (rx + rw * 4 * t/self.reload, ry)
                pygame.draw.lines(win, RED, False, (d, p2, p3, p4, p1), 3)
            elif t < self.reload/2:
                t1 = t - self.reload/4
                d = (rx + rw, ry + rh * 4 * t1/self.reload)
                pygame.draw.lines(win, RED, False, (d, p3, p4, p1), 3)
            elif t < 3 * self.reload/4:
                t1 = t - self.reload/2
                d = (rx + rw - rw * 4 * t1/self.reload, ry + rh)
                pygame.draw.lines(win, RED, False, (d, p4, p1), 3)
            else:
                t1 = t - 3 * self.reload/4
                d = (rx, ry + rh - rh * 4 * t1/self.reload)
                pygame.draw.line(win, RED, d, p1, 3)

    def lvlup(self):
        self.lvl += 1
        self.damage *= 1.2
        self.reload /= 1.05
        if self.bomb:
            self.radius *= 1.05

    def draw_strength(self, win, x, y, s_w, s_h, click, m_pos, can_lvlup, money):
        w = int(s_w/3)
        h = int(s_h/4)
        pygame.draw.rect(win, SILVER, (x, y, w, h))
        pygame.draw.rect(win, WHITE, (x, y, w, h), 5)
        pygame.draw.rect(win, self.color, (int(s_h/40 + x), int(s_h/40 + y), 2 * self.w, 2 * self.h))
        t_x = int(s_h/10 + x) + self.w
        t_y = int(s_h/40 + y) + self.h
        print_text(win, "Bullet", t_x, t_y, BLACK, int(h/10))
        t_x = int(x + s_h/40)
        t_y = int(y + s_h/10)
        text = "Damage"
        up_task(win, text, (t_x, t_y), (x + w/2, t_y), self.lvl, self.damage * 100,
                [t_x + 2 * h/15, t_y - h/10], int(h/15))
        text = "Reload"
        t_y += s_h/15
        up_task(win, text, (t_x, t_y), (x + w / 2, t_y), self.lvl, self.reload,
                [t_x + 2 * h / 15, t_y - h / 10], int(h / 15))
        if self.bomb:
            text = "Radius"
            t_y += s_h/15
            up_task(win, text, (t_x, t_y), (x + w / 2, t_y), self.lvl, self.radius,
                    [t_x + 2 * h / 15, t_y - h / 10], int(h / 15))
        if self.lvl < 15:
            button = Button(w/4, s_h/5, (255, 190, 0), YELLOW)
            b_x = x + w * 0.72
            b_y = y + h/10
            act = button.draw(win, b_x, b_y, 'LVL UP', click, m_pos, int(w/24), BLACK, BLACK)
            if self.bomb:
                lvlup_cost = 800 * self.lvl
            else:
                lvlup_cost = 500 * self.lvl
                if self.cost > 0:
                    lvlup_cost *= 2
            print_text(win, str(lvlup_cost), b_x + button.width/2, b_y + button.height/2 + int(w/12),
                       BLACK, int(w/36))
        else:
            button = Button(w / 4, s_h / 5, GRAY, GRAY)
            button.draw(win, x + w * 0.72, y + h / 10, 'MAX LVL', False, m_pos, int(w / 24), BLACK, BLACK)
            act = 0

        if act == 1 and can_lvlup:
            if self.bomb:
                l_m = 800 * self.lvl
            else:
                l_m = 500 * self.lvl
                if self.cost > 0:
                    l_m *= 2

            if money >= l_m:
                money -= l_m
                self.lvlup()
                message = False
            else:
                message = True
            can_lvlup = False
        else:
            message = False
        if act == 1 or act == -1:
            onbutton = True
        else:
            onbutton = False

        return can_lvlup, onbutton, money, message


class Bomb:
    def __init__(self, size, x, y, d, r):
        self.size = size
        self.x = x
        self.y = y
        self.damage = d
        self.radius = r

    def draw(self, win, ms):
        self.y += ms
        pygame.draw.circle(win, RED, (self.x, self.y), self.size)

    def bomb_explode(self, animals, bullets, player_pos, player_size, bombs):
        explode = False
        for an in animals:
            if an.x + an.pic[0].get_width() >= self.x >= an.x:
                x = 0
            else:
                x = min(an.x + an.pic[0].get_width() - self.x, self.x - an.x)
            y = min(an.y + an.pic[0].get_height() - self.y, self.y - an.y)
            if x**2 + y**2 <= self.size**2:
                explode = True
                break

        if not explode:
            for bullet in bullets:
                if bullet.x + bullet.w >= self.x >= bullet.x:
                    x = 0
                else:
                    x = min(bullet.x + bullet.w - self.x, self.x - bullet.x)
                y = min(bullet.y + bullet.h - self.y, self.y - bullet.y)
                if x**2 + y**2 <= self.size**2:
                    if bullet.radius > 0:
                        bombs.append([bullet.x + bullet.w/2, bullet.y, 0, bullet.radius, bullet.damage])
                    bullets.remove(bullet)
                    explode = True
                    break

        x = player_pos[0] - self.x
        y = player_pos[1] - self.y
        if not explode and x**2 + y**2 <= (self.size + player_size[0]/2)**2:
            explode = True

        if explode:
            for an in animals:
                if an.x + an.pic[0].get_width() >= self.x >= an.x:
                    x = 0
                else:
                    x = min(an.x + an.pic[0].get_width() - self.x, self.x - an.x)
                y = min(an.y + an.pic[0].get_height() - self.y, self.y - an.y)
                if x ** 2 + y ** 2 <= self.radius**2:
                    an.hp -= self.damage

            bombs.append([self.x, self.y, 0, self.radius, self.damage])

        return explode


class Button:
    def __init__(self, width, height, active_color, inactive_color):
        self.width = width
        self.height = height
        self.active_color = active_color
        self.inactive_color = inactive_color

    def draw(self, win, x, y, text, click, m_pos, text_size, text_in_color, text_color):
        act = 0

        if x < m_pos[0] < x + self.width and y < m_pos[1] < y + self.height:
            pygame.draw.rect(win, self.active_color, (x, y, self.width, self.height))
            print_text(win, text, x + self.width/2, y + self.height/2, text_in_color, text_size)
            if click:
                act = 1
            else:
                act = -1
        else:
            pygame.draw.rect(win, self.inactive_color, (x, y, self.width, self.height))
            print_text(win, text, x + self.width/2, y + self.height/2, text_color, text_size)

        return act


def print_text(win, text, x_pos, y_pos, t_color, font_size):
    font = pygame.font.Font('freesansbold.ttf', font_size)
    text_p = font.render(text, True, t_color)
    text_rect = text_p.get_rect()
    text_rect.center = (x_pos, y_pos)
    win.blit(text_p, text_rect)
