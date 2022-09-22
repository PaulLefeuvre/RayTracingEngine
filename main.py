from vec3 import *
from colour import *
from ray import ray
from hittable_list import *
from rtweekend import *
from sphere import *
from camera import *
from material import *

import math
import sys
import multiprocessing
from itertools import repeat


def ray_colour(r, world, depth):
    rec = hit_record()

    if(depth <= 0):
        return colour(0, 0, 0)

    rec = world.hit(r, 0.001, infinity, rec)
    if(rec != None):
        scatter_check, scattered, attenuation = rec.mat_ptr.scatter(r, rec)
        if(scatter_check == True): # The calculation works out
            return attenuation * ray_colour(scattered, world, depth-1)
        return colour(0, 0, 0)

    unit_direction = unit_vector(r.direction())
    t = 0.5*(unit_direction.y() + 1.0)
    return (1.0-t)*colour(1.0, 1.0, 1.0) + t*colour(0.5, 0.7, 1.0)

def render_pixel(i, j):
    pixel_colour = colour(0, 0, 0)
    for s in range(samples_per_pixel):
        u = (i + random_float()) / (IMAGE_WIDTH-1.0)
        v = (j + random_float()) / (IMAGE_HEIGHT-1.0)
        r = cam.get_ray(u, v)
        pixel_colour += ray_colour(r, world, MAX_DEPTH)
    return pixel_colour

## Image
ASPECT_RATIO = 16.0/9.0
IMAGE_WIDTH = 400
IMAGE_HEIGHT = int(IMAGE_WIDTH/ASPECT_RATIO)
samples_per_pixel = 100
MAX_DEPTH = 30

## World
world = hittable_list()

material_ground = lambertian(colour(0.8, 0.8, 0.0))
material_center = lambertian(colour(0.1, 0.2, 0.5))
material_left = dielectric(1.5)
material_right = metal(colour(0.8, 0.6, 0.2), 0.0)

world.add(sphere(point3( 0.0, -100.5, -1.0),  100, material_ground))
world.add(sphere(point3( 0.0,    0.0, -1.0),  0.5, material_center))
world.add(sphere(point3(-1.0,    0.0, -1.0),  0.5, material_left))
world.add(sphere(point3(-1.0,    0.0, -1.0), -0.4, material_left))
world.add(sphere(point3( 1.0,    0.0, -1.0),  0.5, material_right))

## Camera
cam = camera()
if __name__ == "__main__":
    ## Render
    import pygame

    pygame.init()
    window = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
    window.fill((0, 0, 0))
    pygame.display.update()

    pixel_range = range(1, IMAGE_WIDTH+1)
    for j in range(IMAGE_HEIGHT-1, 0, -1):
        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as pool:
            result = pool.starmap(render_pixel, [(i, j) for i in pixel_range])
            pool.close()
            pool.join()
            for i in pixel_range:
                write_colour(window, (i-1, IMAGE_HEIGHT-j-1), result[i-1], samples_per_pixel)
                pygame.display.update()
                pygame.event.get()

    pygame.image.save(window, "HollowGlassSphere.jpg")

    running = True
    while running:
         for event in pygame.event.get():
             if event.type == pygame.QUIT:
                 running = False

# -------- OLD OUTPUT METHOD - CREATING .PPM FILE ----------------------
#
# print("P3\n" + str(IMAGE_WIDTH) + " " + str(IMAGE_HEIGHT) + "\n255")
#
# for j in range(IMAGE_HEIGHT-2, 0, -1):
#     print("\rScanlines remaining: %s " % (j), file=sys.stderr, end="")
#     sys.stderr.flush()
#     for i in range(1, IMAGE_WIDTH+1):
#         pixel_colour = colour(0, 0, 0)
#         for s in range(samples_per_pixel):
#             u = (i + random_float()) / (IMAGE_WIDTH-1.0)
#             v = (j + random_float()) / (IMAGE_HEIGHT-1.0)
#             r = cam.get_ray(u, v)
#             pixel_colour += ray_colour(r, world, MAX_DEPTH)
#         write_colour(sys.stdout, pixel_colour, samples_per_pixel)
#
# print("\nDone.", file=sys.stderr)
