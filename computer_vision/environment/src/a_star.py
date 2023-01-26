'''
A star algorithm
'''
from .lib import Node, BinarySearchList, Objects

class AStar:
    '''A* Algorithm'''
    def __init__(self):
        self.valid = ['None'] # a list of object names that are valid

    def find_path(self, mat, start_pos, end_pos) -> Node:
        '''Returns the start node'''
        # The f_value will be the total distance and calculated with pythagoras
        # without the square root
        if mat is None:
            return None
        size = (len(mat[0]), len(mat))
        h_value = (start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2
        start_node = Node(position=start_pos, h_value=h_value)
        open_list = BinarySearchList() # a list of possible candidates to be the next current node
        open_list.insert(start_node)

        while True:
            if len(open_list) == 0:
                break
            # find the node in the open list with lowest f value
            cur = open_list.pop(0)
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
                # checks if position is out of bounds
                if pos[0] > size[0] - 1 or \
                    pos[0] < 0 or \
                    pos[1] > size[1] - 1 or \
                    pos[1] < 0:
                    continue
                # if finish node
                if pos == end_pos:
                    finish_node = Node(pos, 0, parent=cur)
                    return finish_node
                # checks if tile is valid
                object_id = mat[pos[0]][pos[1]]
                object_data = Objects().get_data(object_id)
                # if the object is a hindrance(not valid)
                if object_data.name not in self.valid:
                    continue
                # check if node already in the list
                if open_list.contains(pos):
                    continue
                # if not in the list, create a node with cur note as parent
                h_value = (pos[0]-end_pos[0])**2 + (pos[1]-end_pos[1])**2
                new_node = Node(pos, h_value, parent=cur)
                # add the new node to the open list
                open_list.insert(new_node)
            # sets the value to 1 (hindrance) so it can not be used again
            mat[cur.position[0]][cur.position[1]] = 1

        return cur

    def get_data(self, mat, start_pos, end_pos):
        '''Returns the data'''
        node = self.find_path(mat, start_pos, end_pos)
