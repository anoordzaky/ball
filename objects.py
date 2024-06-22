import numpy as np
from math import atan2, asin, pi 
from PIL import Image
from util import normalize, rescale

class Ball():
    def __init__(
            self,
            center,
            radius,
            color
    ):
        self.center = center
        self.radius = radius
        self.color = color
    def surface_color(self, ray):
        return self.color

    def intersect(self, ray):
        
        l = self.center - ray.origin #vector that spans from center of the sphere to the camera's position
        ld = np.dot(l, ray.direction) #project l onto the direction of the ray
        d_sqrd  = np.dot(l, l) - ld * ld 
        radius_sqrd = self.radius * self.radius
        if d_sqrd <= radius_sqrd:
            
            half_chord = np.sqrt(radius_sqrd - d_sqrd)

            t0 = ld - half_chord
            t1 = ld + half_chord

            if t0 < 0 and t1 < 0:
                return False
            t = min([t0,t1])
            # print(type(ray.origin + t * ray.direction))
            return ray.origin + t*ray.direction
        return False
    
    def normal(self, ray):
        norm = ray - self.center
        return rescale(normalize(norm))
    
class Floor():
    def __init__(self, y, color1, color2):
        self.color1 = color1
        self.color2 = color2
        self.y = y
    
    def normal(self, ray):
        return np.array([0,-1,0])

    def intersect(self, ray):
        if ray.direction[1] <= 0:
            return False
        distance = self.y - ray.origin[1]
        t = distance / ray.direction[1]

        return ray.origin + t*ray.direction
    
    def surface_color(self, ray):
        x, z = ray[0], ray[1]

        if round(x) % 6 <= 2 and round(z) % 6 <= 2:
            return self.color1
        return self.color2

class Skybox():
    def __init__(self, path):
        self.image = Image.open(path)
        self.size = self.image.size
        self.image_array = np.asarray(self.image)

    def get_color(self,ray):
        u = .5 + atan2(ray[2], ray[0])/(2*pi)
        v = .5 + asin(ray[1])/pi

        intersect_loc = [int(u * self.size[0]), int(v * self.size[1])]
        color = self.image_array[intersect_loc[1], intersect_loc[0]]

        return np.array([color[0], color[1], color[2]]) / 255


