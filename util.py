import numpy as np

def rescale(arr: np.ndarray):
    return arr * .5 + .5

def normalize(arr: np.ndarray):
    return arr / np.linalg.norm(arr)

def reflect(normal, ray_direction):
    vpn = 2 * np.dot(ray_direction, normal) * normal
    return ray_direction - vpn 
