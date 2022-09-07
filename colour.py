from vec3 import vec3
from rtweekend import clamp
import math
import sys
import pygame

def write_colour(surface, pos, pixel_colour, samples_per_pixel):
    r = pixel_colour.x()
    g = pixel_colour.y()
    b = pixel_colour.z()

    scale = 1.0 / samples_per_pixel
    r = math.sqrt(scale * r)
    g = math.sqrt(scale * g)
    b = math.sqrt(scale * b)

    surface.fill((int(256 * clamp(r, 0.0, 0.999)),
                                int(256 * clamp(g, 0.0, 0.999)),
                                int(256 * clamp(b, 0.0, 0.999))), (pos, (1, 1)))

    # ---------- OLD OUTPUT METHOD -------------------------
    # print('%s %s %s\n' % (int(256 * clamp(r, 0.0, 0.999)),
    #                         int(256 * clamp(g, 0.0, 0.999)),
    #                         int(256 * clamp(b, 0.0, 0.999))), file=stream)
