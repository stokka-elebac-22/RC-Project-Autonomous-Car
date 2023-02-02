'''
A star algorithm
'''
import math
import numpy as np
try:
    from lib import Node, BinarySearchList, Objects
except ImportError:
    from .lib import Node, BinarySearchList, Objects

class AStar:
    '''A* Algorithm'''
    def __init__(self, weight: int=0, penalty: int=1):
        self.valid = ['None'] # a list of object names that are valid
        self.weight = weight
        self.penalty = penalty

    def find_path(self, mat: np.ndarray, start_pos: tuple[int, int],
        end_pos: tuple[int, int]) -> list[Node]:
        '''Returns the start node'''
        # The f_value will be the total distance and calculated with pythagoras
        # without the square root
        if mat is None:
            return None

        # if weight is not 0, create a weight matrix
        weighted_mat = None
        if self.weight != 0:
            weighted_mat = self.create_weight_matrix(mat)

        size = (len(mat[0]), len(mat))
        h_value = math.sqrt((start_pos[0]-end_pos[0])**2 + (start_pos[1]-end_pos[1])**2)
        start_node = Node(position=start_pos, h_value=h_value)
        open_list = BinarySearchList() # a list of possible candidates to be the next current node
        open_list.insert(start_node)

        objects = Objects()

        while True:
            if len(open_list) == 0:
                break
            # find the node in the open list with lowest f value
            cur = open_list.pop(0)
            # check all the surounding tiles
            pos = cur.position
            positions = [
                (pos[0]-1, pos[1]),
                (pos[0]+1, pos[1]),
                (pos[0], pos[1]-1),
                (pos[0], pos[1]+1),
                (pos[0]-1, pos[1]-1),
                (pos[0]+1, pos[1]-1),
                (pos[0]-1, pos[1]+1),
                (pos[0]+1, pos[1]+1),
            ]
            constraints = [
                [],
                [],
                [],
                [],
                [0, 2],
                [2, 1],
                [0, 3],
                [1, 3]
            ]
            for i, pos in enumerate(positions):
                # checks if position is out of bounds
                if pos[0] > size[1] - 1 or \
                    pos[0] < 0 or \
                    pos[1] > size[0] - 1 or \
                    pos[1] < 0:
                    continue
                # if finish node
                if pos == end_pos:
                    finish_node = Node(pos, 0, parent=cur)
                    return finish_node
                # checks if tile is valid

                obstacles_detected = []
                for con in constraints[i]:
                    pos_x = positions[con][0]
                    pos_y = positions[con][1]
                    if pos_x > size[1] - 1 or \
                        pos_x < 0 or \
                        pos_y > size[0] - 1 or \
                        pos_y < 0:
                        obstacles_detected.append(True)
                        continue
                    con_object_id = mat[pos_x][pos_y]
                    if con_object_id == 1:
                        obstacles_detected.append(True)

                if len(obstacles_detected) > 0 and all(obstacles_detected):
                    continue

                object_id = mat[pos[0]][pos[1]]
                object_data = objects.get_data(object_id)
                # if the object is a hindrance(not valid)
                if object_data.name not in self.valid:
                    continue
                # check if node already in the list
                ret, node = open_list.get(pos)
                if ret:
                    old_f_value = node.f_value
                    new_h_value = math.sqrt((pos[0]-end_pos[0])**2 + (pos[1]-end_pos[1])**2)
                    new_g_value = cur.g_value + math.sqrt(
                        abs(cur.position[0]-node.position[0])**2 +
                        abs(cur.position[1]-node.position[1]))
                    new_f_value = new_h_value + new_g_value
                    if weighted_mat is not None:
                        # adding a weight
                        new_f_value += weighted_mat[pos[0]][pos[1]]
                    if new_f_value > old_f_value:
                        continue
                    open_list.delete(node.position)
                # if not in the list, create a node with cur note as parent
                h_value = math.sqrt((pos[0]-end_pos[0])**2 + (pos[1]-end_pos[1])**2)
                new_node = Node(pos, h_value, parent=cur)
                if weighted_mat is not None:
                    new_node.f_value += weighted_mat[pos[0]][pos[1]]
                # add the new node to the open list
                open_list.insert(new_node)
            # sets the value to 1 (hindrance) so it can not be used again
            mat[cur.position[0]][cur.position[1]] = 1

        return cur

    def create_weight_matrix(self, mat: np.ndarray) -> np.ndarray:
        '''Creating a weighted matrix'''
        # checks if the matrix is valid
        if mat is None or len(mat) == 0 or len(mat[0]) == 0:
            return
        size = (len(mat), len(mat[0]))
        # weighted_mat = np.full((size[0], size[1]), (0,0), dtype=(int,int))
        weighted_mat = np.zeros((size[0], size[1]), dtype=int)

        diff_pos = [(1,-1),(1,0),(1,1),(0,-1),(0,0),(0,1),(-1,-1),(-1,0),(-1,1)]
        positions = set()
        for i in range(self.weight+1):
            for j in range(self.weight+1):
                for pos in diff_pos:
                    positions.add((pos[0]*i, pos[1]*j))

        # NEED TO IMPROVE THIS!
        for row in range(size[0]):
            for col in range(size[1]):
                # checks if it is a hindrance and then applies a weight to the tiles around
                if mat[row][col] == 1:
                    # checks all surronding positions
                    for pos in positions:
                        idx_x = col + pos[0]
                        idx_y = row + pos[1]
                        # checks if position is out of bounds
                        if idx_x > size[1] - 1 or \
                            idx_x < 0 or \
                            idx_y > size[0] - 1 or \
                            idx_y < 0:
                            continue
                        weight = self.weight - max(abs(pos[0]), abs(pos[1])) + 1
                        weighted_mat[idx_y][idx_x] += weight * self.penalty
        return weighted_mat


    def get_data(self, mat: np.ndarray, start_pos: tuple[int, int], end_pos: tuple[int, int]):
        '''Returns a path list'''
        if start_pos is None or end_pos is None:
            return False, None
        node = self.find_path(mat, start_pos, end_pos)
        path_list = []
        while node is not None:
            path_list.append(node.position)
            node = node.parent
        return True, path_list
        