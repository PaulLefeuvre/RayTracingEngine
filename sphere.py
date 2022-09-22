from hittable import *
from vec3 import *
import math

class sphere:
    def __init__(self, cen, r, mat_ptr):
        self.center = cen
        self.radius = r
        self.mat_ptr = mat_ptr

    def hit(self, r, t_min, t_max, rec):
        oc = r.origin() - self.center
        a = r.direction().length_squared()
        half_b = dot(oc, r.direction())
        c = dot(oc, oc) - self.radius*self.radius

        discriminant = half_b*half_b - a*c
        if (discriminant < 0):
            return None
        sqrtd = math.sqrt(discriminant)

        root = (-half_b - sqrtd) / a
        if root < t_min or t_max < root:
            root = (-half_b + sqrtd) / a
            if root < t_min or t_max < root:
                return None

        rec.t = root
        rec.p = r.at(rec.t)
        outward_normal = (rec.p - self.center) / self.radius
        rec.set_face_normal(r, outward_normal)
        rec.mat_ptr = self.mat_ptr

        return rec
