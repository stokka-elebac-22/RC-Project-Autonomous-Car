'''
A star algorithm
'''
from .lib import Node
class AStar:
    '''A* Algorithm'''
    def find_path(self, mat, start_pos, end_pos) -> Node:
        '''Returns the start node'''
        # The f_value will be the total distance and calculated with pythagoras
        # without the square root
        f_value = abs(start_pos[0]-end_pos[0])**2 + abs(start_pos[1]-end_pos[1])**2
        start_node = Node(position=start_pos, f_value=f_value)
        valid = ['None'] # a list of object names that are valid
        open_list = [start_node] # a list of possible candidates to be the next current node

        while open_list:
            # find the node in the open list with lowest f value
            # For now this is done with a linear search method O(N) but can be
            # optimized by always have the list sorted log(N)
            current_node =



        return start_node


    def get_data(self):
        '''Returns the data'''
