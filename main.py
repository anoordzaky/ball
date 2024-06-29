import cv2
import numpy as np
from tqdm import tqdm
from rays import Ray, Camera, Light
from objects import Ball, Floor, Skybox
from util import normalize, reflect, clamp_color

def raytrace(ray, objects, shadow_bias, light, skybox):

    intersect, object = ray.cast(objects=objects)
    normal = None
    if type(intersect) == np.ndarray:

        normal = object.normal(intersect)
        color = object.surface_color(intersect)

        light_ray = Ray(intersect + normal, -light.direction)
        light_intersect, _ = light_ray.cast(objects=objects)

        if type(light_intersect) == np.ndarray:
            
            color = color * .1 / light.intensity

        color =  color * max([np.dot(normal, -light.direction * light.intensity),0])
    else:
        color = skybox.get_color(ray.direction)

    return intersect, normal, color
    


def main():


    shadow_bias = 0.0001
    max_reflect = 3

    reflection_weight = .2
    camera = Camera(
        position=np.array([0,-2,0]),
        resolution=np.array([1280,720]),
        fov=90
    )

    skybox = Skybox("lasilla_inv.jpg")

    objects = [
        Ball(np.array([0,-1,-20]),2, np.array([1,0,0])),
        Ball(np.array([5,-2,-10]),2, np.array([0,1,0])),
        Ball(np.array([-5,-3,-10]),2, np.array([0,0,1])),

        Floor(2, np.array([0,0,0]), np.array([1,1,1]))
    ]
    
    light = Light(direction=np.array([-1,1,-1]), intensity=1.0)

    frame = np.empty(shape=[camera.resolution[1], camera.resolution[0], 3], dtype=np.uint8)

    for y in tqdm(range(camera.resolution[1])):
        for x in range(camera.resolution[0]):

            camera_ray = camera.get_z(np.array([x,y]))

            intersect, normal, color = raytrace(ray=camera_ray, objects=objects, shadow_bias=shadow_bias, light=light, skybox=skybox)
            direction = camera_ray.direction

            if type(intersect) == np.ndarray:
                reflect_direction = direction
                reflect_vec = reflect(normal, reflect_direction)
                reflection_ray = Ray(intersect + reflect_vec , reflect_vec)
                reflection_color = np.array([0,0,0])
                reflection_n = 0

                for ref in range(max_reflect):

                    intersect, normal, curr_color = raytrace(reflection_ray, objects,shadow_bias,light,skybox)
                    reflection_n +=1
                    reflection_color = reflection_color + curr_color
                    if type(intersect) == np.ndarray:
                        reflect_vec = reflect(normal, reflection_ray.direction)
                        reflection_ray = Ray(intersect + reflect_vec, reflect_vec)
                    else:
                        break
                
                reflect_result = reflection_color / reflection_n if reflection_n > 0 else 0

                color = color + (reflect_result * reflection_weight)

            else:
                color = skybox.get_color(camera_ray.direction)

            

            frame[y,x] = clamp_color(color) * 255

    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    cv2.imshow("test frame",frame)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

