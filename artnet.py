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
        reordered = [
            fb.fb[0], fb.fb[1], fb.fb[2],
            fb.fb[5], fb.fb[4], fb.fb[3],
            fb.fb[6], fb.fb[7], fb.fb[8],
            fb.fb[11], fb.fb[10], fb.fb[9],
        ]
        buf = bytearray(fb.fb)
        self.sock.sendto(self.hdr + pack(">B", self.seq) + b'\x00' + pack("<H", self.universe) + pack(">H", len(buf)) + buf, (self.dst, self.port))
        self.seq = (self.seq + 1) % 256
