import numpy as np
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

