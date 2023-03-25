#!/usr/bin/env python
"""can_handler.py: Class for handling CAN communication."""

from _thread import start_new_thread
import queue
import can
# from can.bus import BusState

class CanBusCommunication():
    '''CAN Bus communication with Car'''
    def __init__(self, conn_info): # pylint: disable=W0613
        """Receives all messages and prints them to the console until Ctrl+C is pressed."""
        self.bus = ""
        self.running = False
        self.incoming_data  = queue.Queue()

    def start(self):
        ''' Start running CanBUS
            :raises No Errors:
                Raises no errors, but closes port if it is open
            :returns:
                Returns True or False (connected)'''
        self.running = True
        start_new_thread(self.run_server, ())

    def run_server(self):
        '''Method started by start, running as a thread'''
        self.bus = can.Bus(interface='socketcan', channel='can0', receive_own_messages=True)
        try:
            while self.running:
                print("CAN bus connected ...")
                msg = self.bus.recv(2)
                if msg is not None:
                    print("Received data ...")
                    print(msg.data)
                    print(msg.arbitration_id)
                    a_id = bytearray(0)
                    a_id.append(msg.arbitration_id)
                    my_bytes = bytearray(a_id + msg.data)
                    print(my_bytes)
                    self.incoming_data.put(my_bytes)

        except KeyboardInterrupt:
            pass  # exit

    def send_command(self, command):
        '''Send custom command on CAN interface'''
        msg = can.Message(arbitration_id=command[0], is_extended_id=False,
                          data=[command[1], command[2], command[3]])
        self.bus.send(msg, timeout=0.2)

    def stop(self):
        '''Stop CAN'''
        self.running = False

    def get_next_data(self):
        '''Get next available piece of data'''
        if not self.incoming_data.empty():
            return self.incoming_data.get()
        return None

    def set_motor_speed(self, m0_dir: int, m0_speed: int, m1_dir: int, m1_speed):
        '''Needs implementation'''
        pass # pylint: disable=W0107

    def drive_direction(self, speed: int, angle: int):
        '''Needs implementation'''
        pass # pylint: disable=W0107


if __name__ == '__main__':
    pass
