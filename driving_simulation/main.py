'''
The main file for the driving simulation
'''
import yaml
from driving import Driving
from driving_setup import DrivingSetup

CONFIG_FILE = 'config'

if __name__ == '__main__':
    # ----- CONFIG ----- #
    with open(CONFIG_FILE + '.yml', 'r', encoding='utf8') as f:
        try:
            config_file = yaml.safe_load(f)
        except yaml.YAMLError as exc:
            print(exc)

    driving = Driving()
    driving_setup = DrivingSetup(conf=config_file, driving=driving)
    driving_setup.run()
