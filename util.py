import numpy as np
from math import sqrt

def rescale(arr: np.ndarray):
    return arr * .5 + .5

def normalize(arr: np.ndarray):
    return arr / sqrt(sum([i*i for i in arr]))

def reflect(normal, ray_direction):
    vpn = 2 * np.dot(ray_direction, normal) * normal
    return normalize(ray_direction - vpn) 

def clamp_color(rgb_arr):
    for idx, channel_value in enumerate(rgb_arr):
        if channel_value < 0:
            rgb_arr[idx] = 0
        elif channel_value > 1:
            rgb_arr[idx] = 1
        else:
            continue
    return rgb_arr