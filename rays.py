import numpy as np
from math import tan, radians
from util import normalize

class Ray():
    def __init__(self, origin, direction):
        self.origin = origin
        self.direction = normalize(direction)

    def cast(self, objects):
        for object in objects:
            intersect = object.intersect(self)
            
            if type(intersect) == np.ndarray:
                # print(intersect)
                # end_color = object.surface_color(intersect) * max([np.dot(object.normal(intersect), -light.direction * light.intensity),0])

                return intersect, object
        
        return False, False
    
    # def reflect
            
class Camera():
    def __init__(self, position, fov, resolution):
        self.position = position
        self.fov = fov
        self.resolution = resolution

    def get_z(self, screen_coord):
        pixel_coord = screen_coord - self.resolution / 2
        z = self.resolution[1] / tan(radians(self.fov/2))

        ray_direction = normalize(np.array([pixel_coord[0], pixel_coord[1], -z]))

        return Ray(self.position, ray_direction)

class Light():
    def __init__(self, direction, intensity):
        self.direction = normalize(direction)
        self.intensity = intensity