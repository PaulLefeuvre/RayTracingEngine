from rtweekend import *
from vec3 import *
from ray import *

class camera:

    ASPECT_RATIO = 16.0/9.0
    VIEWPORT_HEIGHT = 2.0
    VIEWPORT_WIDTH = ASPECT_RATIO * VIEWPORT_HEIGHT
    FOCAL_LENGTH = 1.0

    ORIGIN = point3(0, 0, 0)
    horizontal = vec3(VIEWPORT_WIDTH, 0.0, 0.0)
    vertical = vec3(0.0, VIEWPORT_HEIGHT, 0.0)
    lower_left_corner = ORIGIN - horizontal/2.0 - vertical/2.0 - vec3(0.0, 0.0, FOCAL_LENGTH)

    def __init__(self):
        pass

    def get_ray(self, u, v):
        return ray(self.ORIGIN, self.lower_left_corner + u*self.horizontal + v*self.vertical - self.ORIGIN)
