import cv2
import numpy as np
from tqdm import tqdm
from rays import Ray, Camera, Light
from objects import Ball, Floor, Skybox
from util import normalize

def main():
    shadow_bias = 10e-1
    camera = Camera(
        position=np.array([0,0,0]),
        resolution=np.array([1280,720]),
        fov=90
    )

    skybox = Skybox("skybox_3.jpg")

    objects = [
        Ball(np.array([5,1,-15]),2, np.array([0,1,0])),
        Ball(np.array([-6,0,-15]),2, np.array([0,0,1])),
        Floor(2, np.array([0,0,0]), np.array([1,1,1]))
    ]
    
    light = Light(direction=np.array([-1,1,-1]), intensity=1.0)

    frame = np.empty(shape=[camera.resolution[1], camera.resolution[0], 3], dtype=np.uint8)

    for y in tqdm(range(camera.resolution[1])):
        for x in range(camera.resolution[0]):
            camera_ray = camera.get_z(np.array([x,y]))

            intersect, object = camera_ray.cast(objects=objects)
            if type(intersect) == np.ndarray:
                normal = object.normal(intersect)
                color = object.surface_color(intersect)

                light_ray = Ray(intersect + normal, -light.direction)
                light_intersect, _ = light_ray.cast(objects=objects)
                if type(light_intersect) == np.ndarray:
                    color = color * .1 / light.intensity          
                color =  color * max([np.dot(normal,-light.direction * light.intensity),0])
            else:
                color = skybox.get_color(camera_ray.direction)

            frame[y,x] = color * 255

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.imshow("test frame",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

