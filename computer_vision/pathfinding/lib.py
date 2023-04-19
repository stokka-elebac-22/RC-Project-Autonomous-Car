'''Importing libraries'''
import math
try:
    from computer_vision.environment.src.display import DisplayEnvironment
    from computer_vision.environment.src.environment import Environment
except ImportError:
    from environment.src.display import DisplayEnvironment
    from environment.src.environment import Environment

def get_abs_velo(vec: list) -> float:
    '''Calculate the absolute value of a vector'''
    return math.sqrt(vec[0]**2 + vec[1]**2)

def update_display(
          display: DisplayEnvironment,
          environment: Environment,
          path) -> DisplayEnvironment:
    '''Update display if there are new changes'''
    if display is not None:
        cur_mat = environment.get_data()
        display.update(cur_mat)
        for pos in path[1:-1]:
            display.insert(pos, 'Path')
    return display
