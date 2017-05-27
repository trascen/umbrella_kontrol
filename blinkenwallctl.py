import socket
import threading
import sys

class BlinkenwallCtl:
    def __init__(self):
        self.working = self.opensock()
        if not self.working:
            print('Blinkenwall control could not open connection')

    def opensock(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP
            self.sock.connect(("10.20.30.26", 1234))
            return True
        except:
            return False

    def send(self, cmd):
        if not self.working:
            return

        retries = 2

        while retries > 0:
            try:
                buffer=bytearray()
                buffer.append(cmd)
                if self.sock.send(buffer) == 0:
                    raise Exception('Blinkenwall connection closed')
                #print('sent BlinkenwallCmd ' + str(cmd))
                return
            except:
                e = sys.exc_info()[0]
                print('Error sending blinkenwall command: ' + str(e))
                self.opensock()
                retries -= 1


    def send_next(self, doit):
        if doit:
            self.send(43)

    def send_prev(self, doit):
        if doit:
            self.send(45)

    def send_blank(self, doit):
        if doit:
            self.send(32)