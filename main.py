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
    return (1.0-t)*colour(0, 0, 0) + t*colour(1, 1, 1)

def render_pixel(i, j, world):
    pixel_colour = colour(0, 0, 0)
    for s in range(samples_per_pixel):
        u = (i + random_float()) / (IMAGE_WIDTH-1.0)
        v = (j + random_float()) / (IMAGE_HEIGHT-1.0)
        r = cam.get_ray(u, v)
        pixel_colour += ray_colour(r, world, MAX_DEPTH)
    print("Pixel ({}, {}) done".format(i, j), end='\r')
    return pixel_colour

def random_scene():
    world = hittable_list()

    ground_material = lambertian(colour(0.5, 0.5, 0.5))
    world.add(sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random_float()
            center = point3(a + 0.9*random_float(), 0.2, b + 0.9*random_float())

            if((center - point3(4, 0.2, 0)).length() > 0.9):
                if(choose_mat < 0.8):
                    # Diffuse
                    albedo = random() * random()
                    sphere_material = lambertian(albedo)
                    world.add(sphere(center, 0.2, sphere_material))
                elif(choose_mat < 0.95):
                    # Metal
                    albedo = random(0.5, 1)
                    fuzz = random_float(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(sphere(center, 0.2, sphere_material))
                else:
                    # Glass
                    sphere_material = dielectric(1.5)
                    world.add(sphere(center, 0.2, sphere_material))

    material1 = dielectric(1.5)
    world.add(sphere(point3(0, 1, 0), 1.0, material1))

    material2 = lambertian(colour(0.4, 0.2, 0.1))
    world.add(sphere(point3(-4, 1, 0), 1.0, material2))

    material3 = metal(colour(0.7, 0.6, 0.5), 0.0)
    world.add(sphere(point3(4, 1, 0), 1.0, material3))

    material_ground = lambertian(colour(0.8, 0.8, 0.0))
    material_center = lambertian(colour(0.1, 0.2, 0.5))
    material_left = dielectric(1.5)
    material_right = metal(colour(0.8, 0.6, 0.2), 0.0)

    return world

def space_scene():
    world = hittable_list()

    # ground_material = lambertian(colour(0.5, 0.5, 0.5))
    # world.add(sphere(point3(-1000, 0, 0), 1000, ground_material))
    # world.add(sphere(point3(1000, 0, 0), 1000, ground_material))

    material_center2 = lambertian(colour(0.7, 0.1, 0))
    world.add(sphere(point3(0, 0, 0), 1, material_center2))

    material_spheres1 = metal(colour(1, 0.8, 0), 0.8)
    world.add(sphere(point3(-1, 1, 1), 0.4, material_spheres1))
    world.add(sphere(point3(1, -1, -1), 0.4, material_spheres1))

    material_spheres2 = lambertian(colour(1, 1, 1))
    world.add(sphere(point3(-1.4, 1.4, 1.4), 0.1, material_spheres2))
    world.add(sphere(point3(-1.6, 1.6, 1.6), 0.1, material_spheres2))
    world.add(sphere(point3(1.4, -1.4, -1.4), 0.1, material_spheres2))
    world.add(sphere(point3(1.6, -1.6, -1.6), 0.1, material_spheres2))

    ring_sphere = metal(colour(0.2, 0.2, 0.2), 0.9)
    world.add(sphere(point3(1.2, 0, 0), 0.1, ring_sphere))
    world.add(sphere(point3(-1.2, 0, 0), 0.1, ring_sphere))
    world.add(sphere(point3(0, 0, 1.2), 0.1, ring_sphere))
    world.add(sphere(point3(0, 0, -1.2), 0.1, ring_sphere))
    world.add(sphere(point3(0, 1.2, 0), 0.1, ring_sphere))
    world.add(sphere(point3(0, -1.2, 0), 0.1, ring_sphere))


    return world

## Image
ASPECT_RATIO = 16.0/9.0
IMAGE_WIDTH = 400
IMAGE_HEIGHT = int(IMAGE_WIDTH/ASPECT_RATIO)
samples_per_pixel = 50
MAX_DEPTH = 20

## Camera
lookfrom = point3(13, 2, 3)
lookat = point3(0, 0, 0)
vup = vec3(0, 1, 0)
dist_to_focus = 10.0
aperture = 0.1

cam = camera(lookfrom, lookat, vup, 20, ASPECT_RATIO, aperture, dist_to_focus)

if __name__ == "__main__":
    ## CREATE A MASSIVE WORLD
    world = space_scene()

    ## Render
    import pygame

    pygame.init()
    window = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
    window.fill((0, 0, 0))
    pygame.display.update()

    pixel_range = range(1, IMAGE_WIDTH+1)
    print("Starting render.")
    for j in range(IMAGE_HEIGHT-1, 0, -1):
        with multiprocessing.Pool(multiprocessing.cpu_count()-1) as pool:
            result = pool.starmap(render_pixel, [(i, j, world) for i in pixel_range])
            pool.close()
            pool.join()
            for i in pixel_range:
                write_colour(window, (i-1, IMAGE_HEIGHT-j-1), result[i-1], samples_per_pixel)
                pygame.display.update()
                pygame.event.get()

    pygame.image.save(window, "FinalRender.jpg")

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
