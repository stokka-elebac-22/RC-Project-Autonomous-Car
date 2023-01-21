"""defines.py: Class for enums to ensure consistency in values across platforms."""
__copyright__ = "Copyright 2023, DATBAC"
__license__ = "Apache-2.0"
__version__ = "0.1.0"
__status__ = "Testing"

from enum import Enum
class Sensor(Enum):
    HCSR04 = 1   # Ultrasonic distance sensor
    VL53L = 2    # Laser distance sensor

class Position(Enum):
    BACK_RIGHT = 0
    FRONT_RIGHT = 1
    BACK_LEFT = 2
    FRONT_LEFT = 3

class Message_Id(Enum):
    CAN_MOTOR_DATA_ID = 16       # 0x010 //  00010 000
    CAN_STEERING_DATA_ID = 24    # 0x018 //  00011 000

    CAN_SENSOR0_DATA_ID = 32      # 0x020 // 00100 000 (+ position)
    CAN_SENSOR1_DATA_ID = 40      # 0x028 // 00110 000 (+ position)

    CAN_LIGHT_CONTROL_ID = 64    # 0x040
    CAN_RGB_CONTROL_ID = 72      # 0x048

    CAN_BUZZER_CONTROL_ID = 128  # 0x080

    CAN_TEST_MSG_ID = 136        # 0x088
    CAN_DEVICE_SETTINGS_ID = 152 # 0x098

if __name__ == "__main__":
    test = Position(3)
    print("current position is " + test.name)
    test = Position.BACK_LEFT
    print("current position is " + test.name)
    message = Message_Id.CAN_TEST_MSG_ID
    print("CAN message Id: " + message.name + " value: " + hex(message.value))