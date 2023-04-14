'''main_headless.py: DATBAC23 Car system main.'''
from driving.driving import Driving


class Headless():  # pylint: disable=R0903
    '''Class handling headless running'''
    # pylint: disable=R0902
    def __init__(self, conf: dict): # pylint: disable=R0912
        driving = Driving(conf)
        driving.run()
