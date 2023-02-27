'''Lib'''
from typing import Tuple, List
import dataclasses


@dataclasses.dataclass
class Status:
    '''Status'''
    def __init__(self) -> None:
        self.active = None

@dataclasses.dataclass
class Action:
    '''Action (temporary)'''
    def __init__(self) -> None:
        # the actions contains a list of list with the actions
        self.actions: List[Tuple[int, int, int]] = []

    def move(self, direction: bool, left_motor: int, right_motor: int):
        '''move'''

    def next(self) -> Tuple[bool, Tuple[bool, int, int]]:
        '''Returns the next action'''
        if len(self.actions) == 0:
            return False, None
        cur = self.actions[0]
        self.actions.remove()
        return True, cur

