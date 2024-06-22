import cv2
import numpy as np
from tqdm import tqdm
from PIL import Image
from rays import Ray, Camera, Light
from objects import Ball, Floor
from util import normalize

def main():
    shadow_bias = 10e-1
    camera = Camera(
        position=np.array([0,0,0]),
        resolution=np.array([1280,720]),
        fov=90
    )

    objects = [
        # Ball(np.array([-5,0,-8]),1, np.array([1,0,0])),
        Ball(np.array([0,0,-10]),2, np.array([0,1,0])),
        Ball(np.array([-5,0,-10]),2, np.array([.6,.2,.8])),
        Floor(2, np.array([0,0,0]), np.array([1,1,1]))
    ]
    
    light = Light(direction=np.array([8,10,-15]), intensity=1.0)

    frame = np.empty(shape=[camera.resolution[1], camera.resolution[0], 3], dtype=np.uint8)
    # pixels = camera.resolution[0]*camera.resolution[1]

    for y in tqdm(range(camera.resolution[1])):
        for x in range(camera.resolution[0]):
            camera_ray = camera.get_z(np.array([x,y]))

            intersect, object = camera_ray.cast(objects=objects)
            if type(intersect) == np.ndarray:
                normal = object.normal(intersect)
                color = object.surface_color(intersect)

                light_ray = Ray(intersect + normal*shadow_bias, -light.direction)
                light_intersect, _ = light_ray.cast(objects=objects)
                if type(light_intersect) == np.ndarray:
                    color = color * .1 / light.intensity
                color =  color * max(np.dot(normal, -light.direction * light.intensity),0)
            else:
                color = np.array([0,0,0])

            frame[y,x] = color * 255



    # Image.fromarray(frame).show()
    cv2.imshow("test frame",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

