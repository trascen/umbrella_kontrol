from framebuffer import UmbrellaFB
from colorsys import hsv_to_rgb
import random
import time

class HsvFillEffect:
    def __init__(self):
        self.h = 0
        self.s = 1
        self.v = 255
        self.fb = UmbrellaFB()

    def update_and_get_fb(self, ts):
        c = hsv_to_rgb(self.h,self.s,self.v)
        self.fb.clear(int(c[0]), int(c[1]), int(c[2]), 0, 0)
        return self.fb

    def set_h(self, val):
        self.h = val

    def set_s(self, val):
        self.s = 1 - val

    def set_v(self, val):
        self.v = int(255 - val*255)

class LineScrollEffect:
    def __init__(self):
        self.y = 0
        self.last_t = 0
        self.speed = 0.5
        self.fb = UmbrellaFB()

    def update_and_get_fb(self, ts):
        dt = ts - self.last_t
        self.y = (self.y + dt*self.speed ) % 4
        self.fb.clear(0,0,0,0,0)
        for x in range(0,3):
            self.fb.draw(x, int(self.y), 255,255,255,0,0)
        self.last_t = ts
        return self.fb

    def set_speed(self, v):
        self.speed = 0.5 + v * 40

class RunningPointEffect:
    def __init__(self):

        self.y = 0
        self.x = 0
        self.last_t = 0
        self.speed = 0.5
        self.fb = UmbrellaFB()

    def update_and_get_fb(self, ts):
        dt = ts - self.last_t
        if dt < 1:
            return self.fb

        while dt >= 1:
            dt -= 1
            self.x += 1
            if self.x > 2:
                self.x = 0
                self.y += 1
            if self.y > 3:
                self.y = 0

        self.fb.clear(0,0,0,0,0)
        self.fb.draw(self.x, self.y, 255,255,255,0,0)
        self.last_t = ts
        return self.fb

    def set_speed(self, v):
        self.speed = 0.5 + v * 40

class RainbowEffect:
    def __init__(self):
        self.speed = 1
        self.offs = 1
        self.fb = UmbrellaFB()

    def update_and_get_fb(self, ts):
        s = ts * self.speed

        self.fb.clear(0,0,0,0,0)
        for x in range(0,3):
            for y in range(0,4):
               pos = (s + self.offs * y) % 1
               c = hsv_to_rgb(pos, 1, 255)
               self.fb.draw(x, y, int(c[0]), int(c[1]), int(c[2]),0,0)

        return self.fb

    def set_speed(self, v):
       self.speed = v % 1
    
    def set_offset(self, v):
       self.offs = v % 0.3


class FireEffect:
    def __init__(self):
        self.fb = UmbrellaFB()
        self.last_ts = 0
        self.cells = [
            ( (0,0,0), (0,0,0), 0, 0, 0)
        ] * 12
    
    def update_and_get_fb(self, ts):
        self.generate_new_target_colors(ts)
        self.fill_fb(ts)
        return self.fb

    def generate_new_target_colors(self, ts):
        for i in range(0,12):
            if self.cells[i][4] <= ts:
                self.cells[i] = self.generate_new_target(ts, self.cells[i][1])

    def generate_new_target(self, ts, start_color):
        fade_duration = random.uniform(0.2,1)
        stop_duration = random.uniform(0,2) 
        return (
            start_color,
            self.random_color(),
            ts,
            ts + fade_duration,
            ts + fade_duration + stop_duration
        )

    def random_color(self):
        return random.choice([(255,40,0),(150, 30, 0),(30,30,0),(170,100, 0), (20,0,0), (10, 0, 0), (100,0,100)])


    def fill_fb(self, ts):
        for x in range(0,3):
            for y in range(0,4):
                self.fb.draw(x,y,*self.blend(self.cells[x+y*3], ts), 0, 0)

    def shuffle(self, doit):
        if not doit:
            return
        for i in range(0, 12):
            self.cells[i] = (self.cells[i][0], self.cells[i][1], self.cells[i][2], self.cells[i][2], self.cells[i][2])
    
    def blend(self, cell, ts):
        if ts >= cell[3]:
            return cell[1]
        else:
            s = cell[0]
            t = cell[1]
            bf = 1 - ( (ts - cell[2]) / (cell[3] - cell[2]) )
            #print(str(ts) + " " + str(cell) + " " + str(bf))
            return ( s[0] * bf + t[0] * (1-bf), s[1] * bf + t[1] * (1-bf), s[2] * bf + t[2] * (1-bf) )

