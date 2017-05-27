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
        reordered = fb.fb[0:5] + fb.fb[5:10] + fb.fb[10:15] + fb.fb[25:30] + fb.fb[20:25] + fb.fb[15:20] + fb.fb[30:35] + fb.fb[35:40] + fb.fb[40:45] + fb.fb[55:60] + fb.fb[50:55] + fb.fb[45:50]

        buf = bytearray(reordered)
        self.sock.sendto(self.hdr + pack(">B", self.seq) + b'\x00' + pack("<H", self.universe) + pack(">H", len(buf)) + buf, (self.dst, self.port))
        self.seq = (self.seq + 1) % 256
