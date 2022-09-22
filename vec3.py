from rtweekend import *

import numpy as np
import math

class vec3:

    def __init__(self, e0, e1, e2):
        self.e = [e0, e1, e2]

    def x(self):
        return self.e[0]

    def y(self):
        return self.e[1]

    def z(self):
        return self.e[2]

    def vals(self):
        return self.e

    def __neg__(self):
        return vec3(-self.e[0], -self.e[1], -self.e[2])

    def __getitem__(self, indicies):
        return self.e[indicies]

    def __iadd__(self, other):
        self.e[0] += other.e[0]
        self.e[1] += other.e[1]
        self.e[2] += other.e[2]
        return self

    def __isub__(self, other):
        self.e[0] -= other.e[0]
        self.e[1] -= other.e[1]
        self.e[2] -= other.e[2]
        return self

    def __imul__(self, t):
        if isinstance(t, int) or isinstance(t, float):
            self.e[0] *= t
            self.e[1] *= t
            self.e[2] *= t
            return self

    def __itruediv__(self, t):
        if isinstance(t, int) or isinstance(t, float):
            self *= (1/t)
            return self

    def __add__(u, v):
        return vec3(u.e[0] + v.e[0], u.e[1] + v.e[1], u.e[2] + v.e[2])

    def __sub__(u, v):
        return vec3(u.e[0] - v.e[0], u.e[1] - v.e[1], u.e[2] - v.e[2])

    def __mul__(u, v):
        if isinstance(v, int) or isinstance(v, float):
            return vec3(v*u.e[0], v*u.e[1], v*u.e[2])
        elif isinstance(v, u.__class__):
            return vec3(u.e[0] * v.e[0], u.e[1] * v.e[1], u.e[2] * v.e[2])

    def __rmul__(u, v):
        return u.__mul__(v)

    def __truediv__(u, v):
        if isinstance(v, int) or isinstance(v, float):
            return (1/v) * u

    def length_squared(self):
        return self.e[0]*self.e[0] + self.e[1]*self.e[1] + self.e[2]*self.e[2]

    def length(self):
        return math.sqrt(self.length_squared())

    def near_zero(self):
        s = 1e-8
        return (abs(self.e[0]) < s) and (abs(self.e[1]) < s) and (abs(self.e[2]) < s)

# define the function aliases for clarity of programming
colour = vec3
point3 = vec3

def dot(u, v):
    return u.e[0] * v.e[0] + u.e[1] * v.e[1] + u.e[2] * v.e[2]

def cross(u, v):
    return vec3(u.e[1] * v.e[2] - u.e[2] * v.e[1],
            u.e[2] * v.e[0] - u.e[0] * v.e[2],
            u.e[0] * v.e[1] - u.e[1] * v.e[0])

def unit_vector(v):
    return v/v.length()

def random(min=0.0, max=1.0):
    return vec3(random_float(min, max), random_float(min, max), random_float(min, max))

def random_in_unit_sphere():
    while True:
        p = random(-1, 1)
        if(p.length_squared() < 1):
            return p

def random_unit_vector():
    return unit_vector(random_in_unit_sphere())

def random_in_hemisphere(normal):
    in_unit_sphere = random_in_unit_sphere()
    if(dot(in_unit_sphere, normal) > 0.0):       # In the same hemisphere as the normal
        return in_unit_sphere
    else:
        return -in_unit_sphere

def reflect(v, n):
    return v - 2*dot(v,n)*n
