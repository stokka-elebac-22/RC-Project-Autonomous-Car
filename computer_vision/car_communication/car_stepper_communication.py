#!/usr/bin/env python
"""car_stepper_communication.py: Communication module to handle Raspberry pi HW PWM with Pi-HAT."""
from car_communication.abstract_communication import AbstractCommunication

try:
    import RPi.GPIO as GPIO
    from rpi_hardware_pwm import HardwarePWM # only dependency on Raspberry Pi
    PWM_POSSIBLE = True
except Exception as e: # pylint: disable=W0702
    print(e)
    print("Not possible to run pi hw-PWM")
    PWM_POSSIBLE = False

MAX_PWM = 8000

# https://pypi.org/project/rpi-hardware-pwm/
# On the Raspberry Pi, add dtoverlay=pwm-2chan to /boot/config.txt. This defaults to GPIO_18 as the pin for PWM0 and GPIO_19 as the pin for PWM1.
# Alternatively, you can change GPIO_18 to GPIO_12 and GPIO_19 to GPIO_13 using dtoverlay=pwm-2chan,pin=12,func=4,pin2=13,func2=4.

class CarStepperCommunication(AbstractCommunication):
    '''Class for serial communication with micro controller'''
    def __init__(self, conn_info):
        self.running = False
        self.conn_info = conn_info
        print("Setting up hardware access GPIO/PWM for Pi")
        self.running = True
        self.EN2 = 24
        self.DIR2 = 23
        self.STEP2 = 18
        self.EN = 6
        self.DIR = 5
        self.STEP = 19
        self.CW0 = 0
        self.CCW0 = 1
        self.CW1 = 1
        self.CCW1 = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.EN, GPIO.OUT)
        GPIO.setup(self.DIR, GPIO.OUT)
        # GPIO.setup(self.STEP, GPIO.OUT)

        GPIO.setup(self.EN2, GPIO.OUT)
        GPIO.setup(self.DIR2, GPIO.OUT)
        # GPIO.setup(self.STEP2, GPIO.OUT)

        GPIO.output(self.DIR, self.CW0)
        GPIO.output(self.DIR2, self.CW1)
        GPIO.output(self.EN, 1)
        GPIO.output(self.EN2, 1)
        self.pwm0 = HardwarePWM(pwm_channel=0, hz=10)
        self.pwm1 = HardwarePWM(pwm_channel=1, hz=10)

    def start(self):
        ''' N/A as this works only locally on Pi'''
        self.pwm0.start(50) # half duty cycle
        self.pwm0.change_frequency(10)

        self.pwm1.start(50) # half duty cycle
        self.pwm1.change_frequency(10)


    def stop(self):
        '''Stop connection'''
        self.pwm0.stop()
        self.pwm1.stop()
        GPIO.output(self.DIR, 0)
        GPIO.output(self.DIR2, 0)
        GPIO.output(self.EN, 1)
        GPIO.output(self.EN2, 1)
        GPIO.cleanup()

        self.running = False

    def send_command(self, command):
        '''Send command'''
        pass

    def set_motor_speed(self, m0_dir: int, m0_speed: int, m1_dir: int, m1_speed):
        '''Set the motor speeds directly'''
        print("Setting new gpio output and pwm values")
        if m0_dir == 0:
            GPIO.output(self.EN, 1)
            GPIO.output(self.EN2, 1)
            GPIO.output(self.DIR, self.CW0)
        else:
            GPIO.output(self.DIR, self.CCW0)
        if m1_dir == 0:
            GPIO.output(self.DIR2, self.CW1)
        else:
            GPIO.output(self.DIR2, self.CCW1)
        if m0_speed > 0:
            GPIO.output(self.EN, 0)
            self.pwm0.change_frequency(m0_speed * 80)
        else:
            GPIO.output(self.EN, 1)
        if m1_speed > 0:
            GPIO.output(self.EN2, 0)
            self.pwm1.change_frequency(m1_speed * 80)
        else:
            GPIO.output(self.EN2, 1)

    def drive_direction(self, speed: int, angle: int):
        '''Depending on angle/speed make a calculation on motor speeds
        ### Should this be moved outside of the communication?'''
        self.set_motor_speed( 1, 100, 1, 100)

    def get_next_data(self):
        '''Get next available piece of data'''
        return None

if __name__ == "__main__":
    print("Needs to be imported to be of any use ...")
