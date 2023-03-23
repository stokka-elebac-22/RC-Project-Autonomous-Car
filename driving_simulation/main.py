'''
The main file for the driving simulation
'''
import yaml
from driving import Driving
from driving_loop import DrivingLoop

CONFIG_FILE = 'config'

if __name__ == '__main__':
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            config_file = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    driving = Driving()
    driving_loop = DrivingLoop(driving=driving)
