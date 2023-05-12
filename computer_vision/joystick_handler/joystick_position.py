import dataclasses
import struct

@dataclasses.dataclass
class CurrentHeading:
    '''Object to keep track of current heading'''
    def __init__(self):
        self.x_velocity = 0
        self.y_velocity = 0
        self.button = [0, 0]

    def update_direction(self, direction: int, value: float):
        '''update direction'''
        if direction == 0:  # left -1, right + 1
            self.x_velocity = int(value * 100)
        elif direction == 1: # forward -1, backwards + 1
            self.y_velocity = int(value * 100)

    def update_button(self, btn_number: int, value: int):
        '''update button'''
        if btn_number >= 0 and btn_number < 2:
            self.button[btn_number] = bool(value)

    def set_heading_from_bytes(self, bytes):
        '''Set heading from sent socket bytes'''
        self.x_velocity = bytes[1] - 128
        self.y_velocity = bytes[2] - 128
        self.button[0] = bool(bytes[3] & 1)
        self.button[1] = bool(bytes[3] & 2)

    def get_byte_for_heading(self, prefix_number: int) -> bytes:
        '''Get bytes to send (socket)'''
        return struct.pack("i", prefix_number +
            ((self.x_velocity + 128) << 8) +
            ((self.y_velocity + 128) << 16) +
            (self.button[0] << 24) +
            (self.button[1] << 25))