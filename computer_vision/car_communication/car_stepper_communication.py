#!/usr/bin/env python
"""car_stepper_communication.py: Communication module to handle Raspberry pi HW PWM with Pi-HAT."""
from car_communication.abstract_communication import AbstractCommunication
from rpi_hardware_pwm import HardwarePWM # only dependency on Raspberry Pi

# https://pypi.org/project/rpi-hardware-pwm/
# On the Raspberry Pi, add dtoverlay=pwm-2chan to /boot/config.txt. This defaults to GPIO_18 as the pin for PWM0 and GPIO_19 as the pin for PWM1.
# Alternatively, you can change GPIO_18 to GPIO_12 and GPIO_19 to GPIO_13 using dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4.

class CarStepperCommunication(AbstractCommunication):
    '''Class for serial communication with micro controller'''
    def __init__(self, conn_info):
        self.running = False
        self.conn_info = conn_info

    def start(self):
        ''' N/A as this works only locally on Pi'''
        self.running = True

    def stop(self):
        '''Stop connection'''
        self.running = False

    def send_command(self, command):
        '''Send command'''
        pass

    def set_motor_speed(self, m0_dir: int, m0_speed: int, m1_dir: int, m1_speed):
        '''Set the motor speeds directly'''
        # pwm = HardwarePWM(pwm_channel=0, hz=60)
        # pwm.start(100) # full duty cycle
        # pwm.change_duty_cycle(50)
        # pwm.change_frequency(25_000)
        # pwm.stop()

    def drive_direction(self, speed: int, angle: int):
        '''Depending on angle/speed make a calculation on motor speeds
        ### Should this be moved outside of the communication?'''
        self.set_motor_speed( 1, 100, 1, 100)

    def get_next_data(self):
        '''Get next available piece of data'''
        return None

if __name__ == "__main__":
    print("Needs to be imported to be of any use ...")
