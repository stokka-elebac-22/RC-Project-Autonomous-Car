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
    CAN_MOTOR_DATA_ID = 16       # 0x010
    CAN_STEERING_DATA_ID = 17    # 0x011

    CAN_SENSOR0_DATA_ID = 32      # 0x020 (+ position)
    CAN_SENSOR1_DATA_ID = 36      # 0x024 (+ position)

    CAN_LIGHT_CONTROL_ID = 64    # 0x040
    CAN_RGB_CONTROL_ID = 65      # 0x041

    CAN_BUZZER_CONTROL_ID = 128  # 0x080
    CAN_TEST_MSG_ID = 129        # 0x081
    CAN_DEVICE_SETTINGS_ID = 130 # 0x082

if __name__ == "__main__":
    test = Position(3)
    print("current position is " + test.name)
    test = Position.BACK_LEFT
    print("current position is " + test.name)
    message = Message_Id.CAN_TEST_MSG_ID
    print("CAN message Id: " + message.name + " value: " + hex(message.value))
