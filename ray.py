from vec3 import vec3

class ray:
    def __init__(self, origin, direction):
        self.orig = origin
        self.dir = direction

    def origin(self):
        return self.orig

    def direction(self):
        return self.dir

    def at(self, t):
        return self.orig + t*self.dir
