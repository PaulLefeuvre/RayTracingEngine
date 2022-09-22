from ray import ray
from vec3 import *

class hit_record:
    def __init__(self):
        self.front_face = False

    def set_face_normal(self, r, outward_normal):
        self.front_face = dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if self.front_face else -outward_normal


class hittable:
    def __init__(self):
        pass
