from rtweekend import *
from vec3 import *
from ray import *

import math

class camera:
    def __init__(self, lookfrom, lookat, vup, vfov, aspect_ratio, aperture, focus_dist): # vfov is vertical field-of-view in degrees
        self.lookfrom = lookfrom    # Point at which the camera is positioned
        self.lookat = lookat        # Point towards which the camera is pointed - indicates direction
        self.vup = vup              # A vector point up for the camera - shows camera orietation
        self.vfov = vfov
        self.aspect_ratio = aspect_ratio
        self.aperture = aperture
        self.focus_dist = focus_dist

        theta = degrees_to_radians(vfov)
        h = math.tan(theta/2)
        VIEWPORT_HEIGHT = 2.0 * h
        VIEWPORT_WIDTH = aspect_ratio * VIEWPORT_HEIGHT

        self.w = unit_vector(lookfrom - lookat)
        self.u = unit_vector(cross(vup, self.w))
        self.v = cross(self.w, self.u)

        self.ORIGIN = lookfrom
        self.horizontal = focus_dist * VIEWPORT_WIDTH * self.u
        self.vertical = focus_dist * VIEWPORT_HEIGHT * self.v
        self.lower_left_corner = self.ORIGIN - self.horizontal/2.0 - self.vertical/2.0 - focus_dist*self.w

        self.lens_radius = aperture/2

    def get_ray(self, s, t):
        rd = self.lens_radius * random_in_unit_disk()
        offset = self.u * rd.x() + self.v * rd.y()
        return ray(
            self.ORIGIN + offset,
            self.lower_left_corner + s*self.horizontal + t*self.vertical - self.ORIGIN - offset
        )
