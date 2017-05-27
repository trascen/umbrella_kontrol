
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