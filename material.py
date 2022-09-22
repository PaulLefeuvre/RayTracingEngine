from rtweekend import *
from vec3 import *
from ray import *

class material:
    def __init__(self, albedo):
        self.albedo = albedo

class lambertian(material):
    def __init__(self, albedo):
        super().__init__(albedo)

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
        super().__init__(albedo)
        self.fuzz = fuzz

    def scatter(self, r_in, rec):
        reflected = reflect(unit_vector(r_in.direction()), rec.normal)
        scattered = ray(rec.p, reflected + self.fuzz*random_in_unit_sphere())
        attenuation = self.albedo
        return (dot(scattered.direction(), rec.normal) > 0), scattered, attenuation
