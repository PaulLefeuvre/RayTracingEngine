from ray import ray
from vec3 import *

class hit_record:
    def __init__(self):
        pass
    def set_face_normal(self, r, outward_normal):
        front_face = dot(r.direction(), outward_normal) < 0
        self.normal = outward_normal if front_face else -outward_normal


class hittable:
    def __init__(self):
        pass
