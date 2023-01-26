'''
A star algorithm
'''
from .lib import Node, BinarySearchList

class AStar:
    '''A* Algorithm'''
    def find_path(self, mat, start_pos, end_pos) -> Node:
        '''Returns the start node'''
        # The f_value will be the total distance and calculated with pythagoras
        # without the square root
        if mat is None:
            return
        size = (len(mat[0]), len(mat))
        h_value = abs(start_pos[0]-end_pos[0])**2 + abs(start_pos[1]-end_pos[1])**2
        start_node = Node(position=start_pos, h_value=h_value)
        valid = ['None'] # a list of object names that are valid
        open_list = BinarySearchList() # a list of possible candidates to be the next current node
        open_list.insert(start_node)

        while True:
            if len(open_list) == 0:
                break
            # find the node in the open list with lowest f value
            cur = open_list.get(0)
            # check all the surounding tiles
            pos_x, pos_y = cur.position
            positions = [
                (pos_x-1, pos_y),
                (pos_x+1, pos_y),
                (pos_x, pos_y-1),
                (pos_x-1, pos_y-1),
                (pos_x+1, pos_y-1),
                (pos_x, pos_y+1),
                (pos_x-1, pos_y+1),
                (pos_x+1, pos_y+1),
            ]
            for pos in positions:
                if pos[0] > size[0] - 1 or \
                    pos[0] < 0 or \
                    pos[1] > size[1] or \
                    pos[0] < 0:
                    continue
                # check if node already in the list
            break


        return start_node


    def get_data(self):
        '''Returns the data'''
