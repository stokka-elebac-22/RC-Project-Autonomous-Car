'''
The main file for the driving simulation
'''
import os
import yaml
from driving.driving import Driving

if __name__ == '__main__':
    CONFIG_FILE = 'config'
    print('Reading configuration file...')
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            c = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    # ----- TEST IF PATHS ARE CORRECT ----- #
    if c['simulation']['active']:
        image_paths = c['simulation']['image_paths']
        for image_path in [image_paths['camera_view'], image_paths['arrow']]:
            if not os.path.exists(image_path):
                raise FileNotFoundError

    simulation = Driving(c)
    simulation.run()
