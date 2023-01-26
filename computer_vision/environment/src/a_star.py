'''
A star algorithm
'''
import dataclasses

@dataclasses.dataclass
class Node:
    '''Node'''
    def __init__(self, position, parent=None, f_value=None) -> None:
        self.position = position
        self.parent: Node = parent
        self.f_value = f_value

    def __eq__(self, other):
        return self.position == other.position


class AStar:
    '''A* Algorithm'''
    def find_path(self, mat, start_pos, end_pos) -> Node:
        '''Returns the start node'''
        # The f_value will be the total distance and calculated with pythagoras
        # without the square root
        f_value = abs(start_pos[0]-end_pos[0])**2 + abs(start_pos[1]-end_pos[1])**2
        start_node = Node(position=start_pos, f_value=f_value)
        valid = ['None'] # a list of object names that are valid
        open_list = [] # a list of possible candidates to be the next current node

        while open_list:
            pass

        return start_node


    def get_data(self):
        '''Returns the data'''
