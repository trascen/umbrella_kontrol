import mido

class UmbrellaFB:
    def __init__(self):
        self.fb = [0, 0, 0, 0, 0] * 12

    def get_offset(self, x, y):
        return 5*(x + y*3)

    def draw(self,x,y,r,g,b,w,a):
        offset = self.get_offset(x,y)
        self.fb[offset+0] = r
        self.fb[offset+1] = g
        self.fb[offset+2] = b
        self.fb[offset+3] = w
        self.fb[offset+4] = a

    def clear(self, r, g, b, w, a):
        self.fb = [r, g, b, w, a] * 12

    def blend_all(self, fbs):
        nfbs = len(fbs)
        for i in range(0, len(self.fb)):
            self.fb[i] = 0
            for b in range(0, nfbs):
                self.fb[i] += fbs[b].fb[i]
            self.fb[i] = int(self.fb[i] / nfbs)

    def blend(self, other):
        merged = UmbrellaFB()
        merged.fb = list(map(lambda s: int((s[0] + s[1]) / 2), zip(self.fb, other.fb)))
        return merged
        
    def __str__(self):
        vals = []
        for x in range(0,3):
            for y in range(0,4):
                offset = self.get_offset(x, y)
                vals.append(' '.join([str(v) for v in self.fb[offset:offset+5]]))
        return '\n'.join(vals)

import socket
import time
from struct import pack
import os 
from itertools import chain
import sys

class ArtNet:
    def __init__(self, dst="255.255.255.255", port=0x1936):

        self.seq = 0
        self.dst = dst
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.universe = 3

        #                    Protocol name               DMX         Version   Seq   Phy
        self.hdr = bytearray(b'Art-Net\x00') + bytearray([0, 0x50] + [0, 14])

    def sendrgb(self, r, g, b):
        buf = bytearray([r, g, b, 0, 0] * 12)
        self.sock.sendto(self.hdr + pack(">B", self.seq) + b'\x00' + pack("<H", self.universe) + pack(">H", len(buf)) + buf, (self.dst, self.port))
        self.seq = (self.seq + 1) % 256


    def sendwa(self, w, a):
        buf = bytearray([0, 0, 0, a, w] * 12)
        self.sock.sendto(self.hdr + pack(">B", self.seq) + b'\x00' + pack("<H", self.universe) + pack(">H", len(buf)) + buf, (self.dst, self.port))
        self.seq = (self.seq + 1) % 256

    def sendfb(self, fb):
        buf = bytearray(fb.fb)
        self.sock.sendto(self.hdr + pack(">B", self.seq) + b'\x00' + pack("<H", self.universe) + pack(">H", len(buf)) + buf, (self.dst, self.port))
        self.seq = (self.seq + 1) % 256




def send(fb):
    print('fb sent')
    print(str(fb))

a = UmbrellaFB()
b = UmbrellaFB()

a.draw(0,0,255,255,255,0,0)

b.draw(1,1,0,0,0,255,255)

print(str(a))
print()
print(str(b))
print()
print(str(a.blend(b)))





controls_by_name = { }

class Slider:
    def __init__(self, name, min_value=0, max_value=127):
        self.name = name
        self.min_value = min_value
        self.max_value = max_value
        self.value = 0
        self.callback = None
        controls_by_name[name] = self

    def set_raw_value(self, value):
        self.value = (value - self.min_value) / (self.max_value - self.min_value)
        if self.callback:
            self.callback(self.value)

    def __str__(self):
        return self.name + ': ' + str(self.value)    
    
class Button:
    def __init__(self, name):
        self.name = name
        self.is_pressed = False
        self.callback = None
        controls_by_name[name] = self

    def set_raw_value(self, value):
        self.is_pressed = value == 127
        if self.callback:
            self.callback(self.is_pressed)
    
    def __str__(self):
        return self.name + ': ' + str(self.is_pressed)

inputs = [ n for n in mido.get_input_names() if not 'Midi Through' in n ]

for n in inputs:
    print(n)

to_open = inputs[0]


korg_nano_control_map = [
 None,
 None,
 Slider('Slider 1'),
 Slider('Slider 2'),
 Slider('Slider 3'),
 Slider('Slider 4'),
 Slider('Slider 5'),
 None,
 Slider('Slider 6'),
 Slider('Slider 7'),
 None,
 None,
 Slider('Slider 8'),
 Slider('Slider 9'),
 Slider('Knob 1'),
 Slider('Knob 2'),
 Slider('Knob 3'),
 Slider('Knob 4'),
 Slider('Knob 5'),
 Slider('Knob 6'),
 Slider('Knob 7'),
 Slider('Knob 8'),
 Slider('Knob 9'),
 Button('Button 1 - Top'),
 Button('Button 2 - Top'),
 Button('Button 3 - Top'),
 Button('Button 4 - Top'),
 Button('Button 5 - Top'),
 Button('Button 6 - Top'),
 Button('Button 7 - Top'),
 Button('Button 8 - Top'),
 Button('Button 9 - Top'),
 None, #32
 Button('Button 1 - Bottom'),
 Button('Button 2 - Bottom'),
 Button('Button 3 - Bottom'),
 Button('Button 4 - Bottom'),
 Button('Button 5 - Bottom'),
 Button('Button 6 - Bottom'),
 Button('Button 7 - Bottom'),
 Button('Button 8 - Bottom'),
 Button('Button 9 - Bottom'),
]

def process_message(msg):
    if len(korg_nano_control_map) <= msg.control or korg_nano_control_map[msg.control] == None:
        print('Unknown control: ' + str(msg.control))
        return
    control = korg_nano_control_map[msg.control]
    control.set_raw_value(msg.value)
    #print(str(control))

def register_control_callback(name, cb):
    if not name in controls_by_name:
        print('control ' + name + ' not found')
        return
    controls_by_name[name].callback = cb


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

    

import threading
class Streamer(threading.Thread):
    def __init__(self, draw):
        super().__init__()
        self.an = ArtNet("10.20.255.255")
        self.draw = draw
        self.ms_wait = 1000/40
        self.effects = []
        self.fb = UmbrellaFB()

    def run(self):
        start_t = time.time()
        while True:
            ts = time.time() - start_t
            self.fb.blend_all(list(map(lambda e: e.update_and_get_fb(ts), self.effects)))
            self.an.sendfb(self.fb)
            time.sleep(self.ms_wait/1000)



def draw():
    global h,s,v
    c = hsv_to_rgb(h,s,v)
    fb.clear(int(c[0]), int(c[1]), int(c[2]), 0, 0)
    for n in range(0,10):
        an.sendfb(fb)
    #print('sent ' + str(h) + ' ' + str(s) + ' ' + str(v) + ' = ' + str(c))

streamer = Streamer(draw)
hsvfill = HsvFillEffect()
linefx = LineScrollEffect()

streamer.effects.append(linefx)
streamer.effects.append(hsvfill)
streamer.start()


def set_ms_wait(val):
    if val == 0:
        print('fps: inf')
    else:
        print('fps: ' + str(1000/val))
    streamer.ms_wait = val

register_control_callback('Knob 1', lambda v: hsvfill.set_h(v))
register_control_callback('Knob 2', lambda v: hsvfill.set_s(v))
register_control_callback('Knob 3', lambda v: hsvfill.set_v(v))
register_control_callback('Knob 4', lambda v: set_ms_wait(int(v * 255)))
register_control_callback('Knob 5', lambda v: linefx.set_speed(v))


print('Opening ' + to_open)
with mido.open_input(inputs[0]) as midi_in:
    for msg in midi_in:
        process_message(msg)



