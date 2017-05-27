import threading
import time
from artnet import ArtNet
from framebuffer import UmbrellaFB

class Streamer(threading.Thread):
    def __init__(self):
        super().__init__()
        self.an = ArtNet("10.20.255.255")
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