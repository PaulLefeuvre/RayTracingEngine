from vec3 import *
from colour import write_colour
from ray import ray
from hittable_list import *
from rtweekend import *
from sphere import *
from camera import *

import math
import sys


def ray_colour(r, world):
    rec = hit_record()
    rec = world.hit(r, 0, infinity, rec)
    if(rec != None):
        return 0.5 * (rec.normal + colour(1,1,1))
    unit_direction = unit_vector(r.direction())
    t = 0.5*(unit_direction.y() + 1.0)
    return (1.0-t)*colour(1.0, 1.0, 1.0) + t*colour(0.5, 0.7, 1.0)

## Image
ASPECT_RATIO = 16.0/9.0
IMAGE_WIDTH = 400
IMAGE_HEIGHT = int(IMAGE_WIDTH/ASPECT_RATIO)
samples_per_pixel = 100

## World
world = hittable_list()
world.add(sphere(point3(0,0,-1), 0.5))
world.add(sphere(point3(0,-100.5,-1), 100))

## Camera
cam = camera()

## Render
print("P3\n" + str(IMAGE_WIDTH) + " " + str(IMAGE_HEIGHT) + "\n255")

for j in range(IMAGE_HEIGHT-2, 0, -1):
    print("\rScanlines remaining: %s " % (j), file=sys.stderr, end="")
    sys.stderr.flush()
    for i in range(1, IMAGE_WIDTH+1):
        pixel_colour = colour(0, 0, 0)
        for s in range(samples_per_pixel):
            u = (i + random_float()) / (IMAGE_WIDTH-1.0)
            v = (j + random_float()) / (IMAGE_HEIGHT-1.0)
            r = cam.get_ray(u, v)
            pixel_colour += ray_colour(r, world)
        write_colour(sys.stdout, pixel_colour, samples_per_pixel)

print("\nDone.", file=sys.stderr)
