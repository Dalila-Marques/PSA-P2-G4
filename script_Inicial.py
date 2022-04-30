from ast import Lambda
import glob
import os
import sys

try:
    sys.path.append(glob.glob('../carla/dist/carla-*%d.%d-%s.egg' % (
        sys.version_info.major,
        sys.version_info.minor,
        'win-amd64' if os.name == 'nt' else 'linux-x86_64'))[0])
except IndexError:
    pass

import carla
#import random
import time

def main():
    actorList =[]
    try:

        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.load_world('Town02')
        #print(client.get_available_maps())

        blueprintLibrary = world.get_blueprint_library()
        #print(blueprintLibrary)
        vehicle_bp = blueprintLibrary.filter('mustang')[0]
        transform = carla.Transform(carla.Location(x=180, y=237, z=20),carla.Rotation(yaw=180))
        vehicle = world.spawn_actor(vehicle_bp,transform)
        actorList.append(vehicle)
    
        camera_bp=blueprintLibrary.find('sensor.camera.rgb')
        camera_bp.set_attribute('image_size_x','800')
        camera_bp.set_attribute('image_size_y','600') 
        camera_transform = carla.Transform(carla.Location(x=1.5, z=2))
        camera = world.spawn_actor(camera_bp,camera_transform, attach_to=vehicle)

        #TODO: Camera.listen function
        #camera.listen( Lambda image:save_to_disk('output/%d064.png'%image.frame))
        time.sleep(20)
    
    finally:
        print('Delete actorList')
        #client.apply_batch([carla.command.DestroyActor(x) for x in actorList])    
    
    finally:
        print('Delete actorList')
        #client.apply_batch([carla.command.DestroyActor(x) for x in actorList])    
           
if __name__=='__main__':
    main()
