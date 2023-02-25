'''Lib'''
import dataclasses


@dataclasses.dataclass
class Status:
    '''Status'''
    def __init__(self) -> None:
        self.active = None

@dataclasses.dataclass
class Action:
    '''Action (temporary)'''
    def move(self, direction: bool, left_motor: int, right_motor: int):
        '''move'''
