from framebuffer import UmbrellaFB
from colorsys import hsv_to_rgb

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

class RainbowEffect:
    def __init__(self):
        self.speed = 1
        self.offs = 1
        self.fb = UmbrellaFB()

    def update_and_get_fb(self, ts):
        s = ts * self.speed

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