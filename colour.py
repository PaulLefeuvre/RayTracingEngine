from vec3 import vec3
from rtweekend import clamp
import sys

def write_colour(stream, pixel_colour, samples_per_pixel):
    r = pixel_colour.x()
    g = pixel_colour.y()
    b = pixel_colour.z()

    scale = 1.0 / samples_per_pixel
    r *= scale
    g *= scale
    b *= scale

    print('%s %s %s\n' % (int(256 * clamp(r, 0.0, 0.999)),
                            int(256 * clamp(g, 0.0, 0.999)),
                            int(256 * clamp(b, 0.0, 0.999))), file=stream)
