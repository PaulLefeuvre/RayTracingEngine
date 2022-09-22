from rtweekend import *
from vec3 import *
from ray import *

import math

class material:
    def __init__(self):
        pass

class lambertian(material):
    def __init__(self, albedo):
        self.albedo = albedo

    def scatter(self, r_in, rec):
        scatter_direction = rec.normal + random_unit_vector()

        # Catch degenerate scatter direction
        if(scatter_direction.near_zero()):
            scatter_direction = rec.normal

        scattered = ray(rec.p, scatter_direction)
        attenuation = self.albedo

        return True, scattered, attenuation

class metal(material):
    def __init__(self, albedo, fuzz):
        self.albedo = albedo
        self.fuzz = fuzz

    def scatter(self, r_in, rec):
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered = ray(rec.p, reflected + self.fuzz*random_in_unit_sphere())
        attenuation = self.albedo
        return (dot(scattered.direction(), rec.normal) > 0), scattered, attenuation

class dielectric(material):
    def __init__(self, ir):
        self.ir = ir

    def scatter(self, r_in, rec):
        attenuation = colour(1.0, 1.0, 1.0)
        refraction_ratio = (1.0/self.ir) if rec.front_face else self.ir

        unit_direction = unit_vector(r_in.direction())
        cos_theta = min(dot(-unit_direction, rec.normal), 1.0)
        sin_theta = math.sqrt(1.0 - cos_theta*cos_theta)

        cannot_refract = refraction_ratio * sin_theta > 1.0
        if cannot_refract or self.reflectance(cos_theta, refraction_ratio) > random_float():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)

        scattered = ray(rec.p, direction)
        return True, scattered, attenuation

    def reflectance(self, cosine, ref_idx):
        # Use Shlick's approximation for reflectance
        r0 = (1-ref_idx) / (1+ref_idx)
        r0 = r0*r0
        return r0 + (1-r0)*math.pow((1 - cosine), 5)
