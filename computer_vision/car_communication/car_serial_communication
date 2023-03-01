#!/usr/bin/env python
"""car_serial_conn.py: Serial communication module to interface with RC-card."""

from threading import Thread
import queue
import time
import sys
import glob
from abstract_communication import AbstractCommunication
import serial

class CarSerialCommunication(AbstractCommunication):
    '''Class for serial communication with micro controller'''
    def __init__(self, conn_info):
        self.running = False
        self.conn_info = conn_info
        self.incoming_data = queue.Queue()
        self.outgoing_commands = queue.Queue()
        self.connected = False
        self.serial_thread = ""
        self.serial_port = ""

    def start(self):
        ''' Establish serial connection
            :raises No Errors:
                Raises no errors, but closes port if it is open
            :returns:
                Returns True or False (connected)'''
        self.running = True
        try:
            self.serial_port = serial.Serial(self.conn_info["port"],
                                             self.conn_info["baud"], timeout=1)
            if self.serial_port.isOpen():
                self.serial_port.close()
            self.serial_port.open()
            self.connected = True
            self.serial_thread = Thread(target=self.handle_serial,
                            args=(self.serial_port, self.outgoing_commands, self.incoming_data))
            self.serial_thread.start()
            return True
        except IOError:
            self.connected = False
            self.serial_port.close()
            print ("port was already open, closed it!")

        return False

    def stop(self):
        '''Stop serial connection'''
        self.running = False

    def write_serial(self, command):
        '''Write data to serial port'''
        self.serial_port.write(command.encode('utf-8'))

    def hex_ascii_to_int(self, hex_digit):
        ''' Convert hex value to ASCII code
            :raises No Errors:
                Currently no error handling
            :returns:
                Returns ASCII code    '''
        if '0' <= hex_digit <= '9':
            return (int(ord(hex_digit) - 48))  # ASCII-code for '0' is 0x30 = 48
        if 'A' <= hex_digit <= 'F':
            return (int(ord(hex_digit) - 55))  # ASCII-code for 'A' is 0x41 = 65
        return None


    def handle_serial(self, serial_port, command_que, messages):
        ''' Code for reading the serial port while connected.
            Read data will be parsed and added to a list
            Close the serial port in the end '''
        self.running = True
        new_command = ""
        working_string = ""
        char = ""
        while self.running:
            line = []
            c = serial_port.read(1)
            line.append(c)
            working_string += str(c, encoding="utf-8")
            if c == b'\n':
                self.check_message(working_string)
                if line != b'\n':
                    messages.append(working_string)
                working_string = ""
                line = []

            try:
                new_command = command_que.get(block=False)
                self.write_serial(new_command)
                new_command = ""
            except Exception: # pylint: disable=W0718
                pass

            if new_command == 's':
                self.running = False

        while char != '\x03':
            char = str(serial_port.read(1), encoding='utf-8')
            messages.append(char)
        serial_port.close()
        print(serial_port.name, 'is closed')

    def check_message(self, new_line):
        ''' Checks incoming line for data / info and appends
            :raises No Errors:
                Currently no error handling
            :returns:
                Returns nothing, but adds data to lists '''
        pass # pylint: disable=W0107

    def get_serial_ports(self):
        ''' Lists serial port names
            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        '''
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)] # pylint: disable=C0209
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def send_command(self, command):
        '''Send command'''
        self.outgoing_commands.put(command)
        time.sleep(1)

    def set_motor_speed(self, m0_dir: int, m0_speed: int, m1_dir: int, m1_speed):
        '''Set the motor speeds directly'''
        txt = "rc_controller motor-set-speed {m0_d:d} {m0_v:d} {m1_d:d} {m1_v:d}"
        self.send_command(txt.format(
            m0_d = m0_dir, m0_v = m0_speed,
            m1_d = m1_dir, m1_v = m1_speed))

    def drive_direction(self, speed: int, angle: int):
        '''Depending on angle/speed make a calculation on motor speeds
        ### Should this be moved outside of the communication?'''
        self.set_motor_speed( 1, 100, 1, 100)

    def get_next_data(self):
        '''Get next available piece of data'''
        if not self.incoming_data.empty():
            return self.incoming_data.get()
        return None

if __name__ == "__main__":
    print("Needs to be imported to be of any use ...")
