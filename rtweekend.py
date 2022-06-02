import math
import random

infinity = float('inf') # Change to '9e999' if issues arise
pi = math.pi

def degrees_to_radians(degrees):
    return degrees * pi / 180.0

def random_float(min=0.0, max=1.0):
    if(max<=min):
        raise Exception("the values for min and max do not produce a real range")
    return random.uniform(min, max)

def clamp(x, min, max):
    if (x < min):
        return min
    if (x > max):
        return max
    return x
